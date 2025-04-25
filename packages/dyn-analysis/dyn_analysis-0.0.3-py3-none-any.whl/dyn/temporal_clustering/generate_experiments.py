#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module is used to generate experiment scripts.

This script generates the bash scripts for the experiments, using a json template file.

.. code:: bash

    python generate_experiments.py TEMPLATE_FILE [-a ASSESSMENT] [OPTIONS]

    TEMPLATE_FILE contains the template for the experiment in json format.
    ASSESSMENT deactivates assessment if it is "n" only.

    Options:
    * -l, --log     activate logger INFO level
    * -d, --debug   activate logger DEBUG level (takes precedence over -l option)

This script generates the following sets of scripts for each algorithm in the template file:

* `step2.1_run_{ALGO}.sh`: perform community detection
* `step2.3_run_matching_metrics_{ALGO}.sh`: run matching metrics
* `step4_community_evolution`: run masks to detect community events (also run for groundtruth)
"""  # noqa: E501
import argparse
import json
import logging
import os
import pathlib

__all__ = []

LOGGER = logging.getLogger(__name__)


def community_detection(config):
    """Generate script to manage community detection (Step 1)

    :param config:
    :type config: dict
    """
    algorithms = config["consensus_clustering"]["algorithm_clustering"]
    metric_options = config["matching_metrics"]["metric"]

    for algorithm in algorithms:
        for metric in metric_options:
            filename = f"{algorithm}_{metric}/step2.1.sh"
            pathlib.Path(f"{algorithm}_{metric}").mkdir(
                parents=True, exist_ok=True
            )
            with open(filename, "w") as f:
                f.write(
                    f"""#!/bin/bash

rm -Rf results

echo "==== Run {algorithm} algorithm ===="
for snapshot in "../../graphs"/*.csv;
do
    python -m dyn.temporal_clustering.community_detection ${{snapshot}} results {algorithm}
done

echo "==== Merge commlist files into one membership.tcommlist file ===="
header='"node_id","static_community_id","evolving_community_id","snapshot"'
echo ${{header}} > results/membership.tcommlist

i=0
INPUT="results/*.commlist"
for file in ${{INPUT}}; do
  # concatenates the file contents into the target file
  cat ${{file}} >> results/membership.tcommlist
  rm ${{file}}
  ((i++))
done

echo "==== Output ===="
echo Concatenation of "${{i}}" commlist files completed.
echo Check the result in "{algorithm}_{metric}/results"
"""  # noqa: E501
                )
            os.chmod(filename, 0o775)  # st.st_mode | stat.S_IEXEC)


def consensus_clustering(config):
    """Generate script to manage consensus clustering (Step 2)

    :param config:
    :type config: dict

    .. todo:: implement
    """
    LOGGER.warning("Consensus clustering is not implemented ... skipped")


def matching_metric(config):
    """Generate script to manage matching metrics (Step 3)

    :param config:
    :type config: dict

    .. todo:: What purpose serves `core_options` variable? (commented out)
    """
    algorithms = config["consensus_clustering"]["algorithm_clustering"]

    # core_options = config["matching_metrics"]["core_based_method"]
    metric_options = config["matching_metrics"]["metric"]

    for algorithm in algorithms:
        for metric in metric_options:
            filename = f"{algorithm}_{metric}/step2.3_run_matching_metrics.sh"
            with open(filename, "w") as f:
                f.write(
                    f"""#!/bin/bash

echo "==== Computing matching metrics===="
python -m dyn.temporal_clustering.build_community_graph results/membership.tcommlist results {metric}

echo "==== Plot sankey ===="
python -m dyn.drawing.main_draw_sankey results --sankey results/communities.gml
\n"""  # noqa: E501
                )
            os.chmod(filename, 0o775)  # st.st_mode | stat.S_IEXEC)


def assess(config):
    """Generate script to compare the results to the ground truth (Step 4)

    :param config:
    :type config: dict
    """
    number_intervals = config["dataset_preparation"]["number_snapshots"] - 1
    dataset = config["dataset_preparation"]["name"]

    algorithms = config["consensus_clustering"]["algorithm_clustering"]
    metric_options = config["matching_metrics"]["metric"]

    for algorithm in algorithms:
        for metric in metric_options:
            filename = f"{algorithm}_{metric}/step3_assess.sh"
            with open(filename, "w") as f:
                f.write(
                    f"""#!/bin/bash

DT_MIN=0
DT_MAX={number_intervals}

echo "==== Comparing tcommlist files===="
echo "= {algorithm}_{metric} ="
python -m dyn.benchmark.assess "../groundtruth/results/membership.tcommlist" results/membership.tcommlist ${{DT_MIN}} ${{DT_MAX}} metrics/
sed -i -e '1s/.*/"dataset","experiment",&/' -e '1!s/.*/"{dataset}","'"{algorithm}_{metric}"'",&/' metrics/transition_metrics.csv
sed -i -e '1s/.*/"dataset","experiment",&/' -e '1!s/.*/"{dataset}","'"{algorithm}_{metric}"'",&/' metrics/partition_metrics.csv

"""  # noqa: E501
                )
                os.chmod(filename, 0o775)  # st.st_mode | stat.S_IEXEC)


def community_events(config):
    """Generate script to detect community events (Step 4)

    :param config:
    :type config: dict
    """
    dataset = config["dataset_preparation"]["name"]

    algorithms = config["consensus_clustering"]["algorithm_clustering"]
    metrics = config["matching_metrics"]["metric"]

    for algorithm in algorithms:
        for metric in metrics:
            filename = f"{algorithm}_{metric}/step4_community_evolution.sh"
            with open(filename, "w") as f:
                f.write(
                    f"""#!/bin/bash

echo "= {algorithm}_{metric} ="
python -m dyn.events.main_compute_events results/membership.tcommlist metrics/events-icem.csv --algo ICEM --alpha 0.0 --beta 0.5 $LOG_OPTIONS
sed -i -e '1s/.*/"dataset","experiment",&/' -e '1!s/.*/"{dataset}","'"{algorithm}_{metric}"'",&/' metrics/events-icem.csv
    """  # noqa: E501
                )
                os.chmod(filename, 0o775)  # st.st_mode | stat.S_IEXEC)
    filename = "groundtruth/step4_community_evolution.sh"
    with open(filename, "w") as f:
        f.write(
            f"""#!/bin/bash

echo "= groundtruth ="
python -m dyn.events.main_compute_events results/membership.tcommlist metrics/events-icem.csv --algo ICEM --alpha 0.0 --beta 0.5 $LOG_OPTIONS
sed -i -e '1s/.*/"dataset","experiment",&/' -e '1!s/.*/"{dataset}","'"groundtruth"'",&/' metrics/events-icem.csv
"""  # noqa: E501
        )
        os.chmod(filename, 0o775)  # st.st_mode | stat.S_IEXEC)


def run(config, assessment):
    """Generate experiment scripts.

    :param config:
    :type config: dict
    :param assessment: if ``True``, assessment script is also generated
    :type assessment: bool
    """

    community_detection(config)
    matching_metric(config)
    if assessment:
        assess(config)
    community_events(config)


if __name__ == "__main__":
    example_text = """example:
      python generate_experiments.py template_file -a n

      Template  "consensus_clustering": {
        "window_size": [0,2, '50%'],
        "algorithm_clustering": "infomap"
       },
       Parameter window_size could be an integer or a string with a percentage of number_snapshots

    """  # noqa: E501

    # Configuration of parameters
    parser = argparse.ArgumentParser(
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "template_file", help="Specify a custom template file."
    )
    parser.add_argument(
        "-a",
        "--assessment",
        help="Specify if assessment is needed y/n. Assessment is done by "
        "default (when -a is not provided).",
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

    with open(args.template_file) as json_data_file:
        config = json.load(json_data_file)

    assessment = True
    if args.assessment:
        if args.assessment == "n":
            LOGGER.info("Assessment turned off")
            assessment = False

    try:
        run(config, assessment)
        LOGGER.info("Experiment generated")
    except Exception:
        LOGGER.error("Something went wrong")
