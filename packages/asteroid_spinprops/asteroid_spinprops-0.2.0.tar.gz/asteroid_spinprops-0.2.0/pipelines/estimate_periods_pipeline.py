import random
import pickle
import warnings
import numpy as np
import pandas as pd
import argparse
from functools import partial
import tqdm

from ssolib.pipetools import (
    load_light_curve_data,
    process_single_sso,
    match_true_period,
    fill_missing_periods_and_powers,
    collect_rocks_periods,
)

# from line_profiler import profile
from multiprocessing import Pool

warnings.filterwarnings("ignore")


parser = argparse.ArgumentParser(
    description="Process a number of SSOs in the LS pipeline."
)
parser.add_argument(
    "-n",
    "--num_ssos",
    type=int,
    default=600,
    help="Number of SSOs to process (default: 600)",
)
args = parser.parse_args()

nn = [
    "Agostino",
    "Viktorfischl",
    "Phystech",
    "2001 UG32",
    "1999 CH10",
    "2000 OS38",
    "2002 UJ29",
    "2001 RA7",
]


# @profile
def main():
    ephem_path = "./../data/ephem_cache"
    aggregated_path = "./../data/sso_aggregated_ATLAS_x_ztf_no_radec"

    lcdf = load_light_curve_data("./../data/lc_details.csv")
    with open("./../data/ssoname_keys.pkl", "rb") as f:
        pqload = pickle.load(f)
    path_args = [aggregated_path, pqload, ephem_path]

    names_lcdb = np.unique(lcdf[lcdf["Period"] != -9.99]["Name"])

    selected_indices = random.sample(range(len(names_lcdb)), args.num_ssos)

    results = {
        "names": [],
        "periods": [],
        "powers": [],
        "wperiods": [],
        "wpowers": [],
        "npoints": [],
        "noise": [],
        "Nbs": [],
    }

    names = [names_lcdb[idx] for idx in selected_indices]
    names = nn
    with Pool(4) as p:
        out = list(
            tqdm.tqdm(
                p.imap(
                    partial(process_single_sso, path_args=path_args),
                    names,
                ),
                total=len(names),
            )
        )

    for res in out:
        if res:
            signal, window, noise, name, Nbs, npts = res
            results["periods"].append(signal[2])
            results["powers"].append(signal[3])
            results["wperiods"].append(window[2])
            results["wpowers"].append(window[3])
            results["npoints"].append(npts)
            results["noise"].append(noise)
            results["names"].append(name)
            results["Nbs"].append(Nbs)

    fill_missing_periods_and_powers(results["periods"], results["powers"])
    fill_missing_periods_and_powers(results["wperiods"], results["wpowers"])

    ls_stats = pd.DataFrame(
        {
            "name": results["names"],
            "npoints": results["npoints"],
            "noise": results["noise"],
            "Nbs": results["Nbs"],
        }
    )

    for i in range(5):
        ls_stats[f"P{i}"] = np.stack(results["periods"]).T[i]
        ls_stats[f"A{i}"] = np.stack(results["powers"]).T[i]
        ls_stats[f"WP{i}"] = np.stack(results["wperiods"]).T[i]
        ls_stats[f"WA{i}"] = np.stack(results["wpowers"]).T[i]

    ls_stats["Prock"], ls_stats["Pmethods"] = collect_rocks_periods(ls_stats["name"])

    ls_stats["Prock"] = ls_stats["Prock"].apply(
        lambda x: np.nan if len(x) == 0 or np.isnan(x).all() else x
    )

    # Convert to asteroid period (Hours) from LS frequency space (1/days)
    for i in range(5):
        ls_stats[f"P{i}"] = 48 / ls_stats[f"P{i}"]

    try:
        ls_stats["minP0"] = [
            np.min(
                np.abs(ls_stats["P0"].iloc[i] - ls_stats["Prock"].iloc[i])
                / ls_stats["Prock"].iloc[i]
            )
            if not isinstance(ls_stats["Prock"].iloc[i], float)
            else np.nan
            for i in range(len(ls_stats))
        ]
        ls_stats["minP1"] = [
            np.min(
                np.abs(ls_stats["P1"].iloc[i] - ls_stats["Prock"].iloc[i])
                / ls_stats["Prock"].iloc[i]
            )
            if not isinstance(ls_stats["Prock"].iloc[i], float)
            else np.nan
            for i in range(len(ls_stats))
        ]
    except Exception as e:
        print("P-Prock matching issue:", e)
        ls_stats["minP0"] = np.nan
        ls_stats["minP1"] = np.nan

    ls_stats["Ptrue"], ls_stats["Mtrue"] = match_true_period(
        ls_stats["P0"], ls_stats["Prock"], ls_stats["Pmethods"]
    )
    ls_stats["flag"] = 0

    ls_stats.loc[ls_stats["noise"] > 0.2, "flag"] = 1

    mask_out_of_bounds = [
        isinstance(p, float) or not np.any((p > 0.03 * 24 * 2) & (p < 2 * 24 * 2))
        for p in ls_stats["Prock"]
    ]
    ls_stats.loc[mask_out_of_bounds, "flag"] = 2

    print("Final flagging done, saving file...")
    ls_stats.drop_duplicates("name").to_pickle("./../data/LS_stats_out.pkl")


if __name__ == "__main__":
    main()
