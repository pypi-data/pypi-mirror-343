#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module is a script which compute events using one mask algorithm or ICEM.

Compute events using either sankey files or membership commlist files based on given mask.
Only `ICEM` uses commlist files, in such case evolving communities can still be retrieved
by providing the communities graph (using `--sankey` argument).

.. code:: bash

    python main_compute_events.py INPUT OUTPUT [--algo ALGO]
        [--community ID1 [--community ID2 [ ... ]]] [OPTIONS]

    INPUT is input tcommlist file. OUTPUT is output .csv file.

    Inputs:
    * --algo ALGO                 ALGO defines the algorithm to use (default: baseline)
    * --community ID              ID of a community to extract (can be set multiple times)

    Options:
    * --alpha ALPHA               set ratio of common members to consider punctual
                                  communities as similar (ICEM only)
    * --beta BETA                 set ratio of common members to consider punctual
                                  communities as very similar (ICEM only)
    * -l, --log                   activate logger INFO level
    * -d, --debug                 activate logger DEBUG level (takes precedence over -l option)
"""  # noqa: E501
import argparse
import logging
from os import makedirs
from os.path import dirname, isdir

from dyn.core.files_io import load_tcommlist, save_csv

from dyn.events.events_calculator import MaskCalculator
from dyn.events.icem_calculator import ICEMCalculator
from dyn.events.masks import all_masks

LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="tcommlist file to analyze")
    parser.add_argument(
        "result_file",
        type=str,
        help="CSV file where the results will be saved",
    )
    parser.add_argument(
        "--algo",
        type=str,
        default="baseline",
        choices=[mask.name for mask in all_masks()] + ["ICEM"],
        help="which algorithm to use (masks or ICEM)",
    )
    parser.add_argument(
        "--community",
        action="append",
        type=str,
        default=[],
        help="In the case where the user wants to analyse sankeys from a "
        "source folder, the list of communities to extract"
        "Each added community must be after a --community flag",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.1,
        help="(for ICEM only) ratio of common members to consider that two "
        "punctual communities are similar",
    )
    parser.add_argument(
        "--beta",
        type=float,
        default=0.9,
        help="(for ICEM only) ratio of common members to consider that two "
        "punctual communities are very similar",
    )
    parser.add_argument(
        "-l", "--log", help="Activate logging INFO level.", action="store_true"
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Activate logging DEBUG level.",
        action="store_true",
    )

    args = parser.parse_args()

    LOG_FORMAT = (
        "[%(asctime)s] [%(levelname)8s] --- %(message)s "
        "(%(filename)s:%(lineno)s)"
    )
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    elif args.log:
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    # Load input tcommlist file
    tcommlist = load_tcommlist(args.input)

    # Preparations
    result_folder = dirname(args.result_file)
    if not (result_folder == "" or isdir(result_folder)):
        makedirs(result_folder)

    # ICEM and GED masks are different from the other
    if args.algo == "ICEM":
        events_detector = ICEMCalculator(
            args.alpha,
            args.beta,
        )
    else:
        events_detector = MaskCalculator(args.algo)

    LOGGER.info("begin events computation")
    events = events_detector.compute(
        tcommlist, args.community if len(args.community) > 0 else None
    )
    LOGGER.info("end events computation")

    LOGGER.info("write events")
    save_csv(
        [events.columns.tolist()] + events.values.tolist(), args.result_file
    )
