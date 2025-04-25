#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module is used to generate a community graph from commlist files.

This script generates the community graph from commlist files.

.. code:: bash

    python build_community_graph.py INPUT OUTPUT METRIC [OPTIONS]

    INPUT is the input tcommlist file. OUTPUT is the output repository.
    METRIC is the metric chosen.

    Metrics:
    * overlap
    * relative_overlap
    * match

    Options:
    * -s, --start START
                    set start snapshot for analysis
    * -e, --end END set end snapshot for analysis
    * -l, --log     activate logger INFO level
    * -d, --debug   activate logger DEBUG level (takes precedence over -l option)

This script generates the following files inside `OUTPUT` directory:

* `membership.tcommlist`: community-matched tcommlist file
* `communities.gml`: community graph in gml format
* `predecessors.csv`: start_snapshot, end_snapshot, cluster, predecessor_of
* `successors.csv`: start_snapshot, end_snapshot, cluster, successor_of
"""  # noqa: E501
import argparse
import logging
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import List

from dyn.core.communities import Membership, StaticCommunity
from dyn.core.files_io import (
    load_tcommlist,
    save_csv,
    save_graph,
    save_tcommlist,
)

__all__ = []

LOGGER = logging.getLogger(__name__)


@dataclass
class MatchingMetricResult:
    """Dataclass used to compare matching metric results.

    :param metric_result: result of matching metric (first item compared)
    :param intersection_size: size of intersection/flow (second compared)

    .. note::
        This could be directly returned by matching metrics to avoid
        intersection size recomputation.
        We could even use a class to gather both matching metric representation
        and computation.
    """

    metric_result: float
    intersection_size: float

    def __gt__(self, other: "MatchingMetricResult") -> bool:
        if self.metric_result > other.metric_result:
            return True
        if self.metric_result < other.metric_result:
            return False
        return self.intersection_size > other.intersection_size

    def __lt__(self, other: "MatchingMetricResult") -> bool:
        return other < self


def match(ct0, ct1):
    """Return match metric result.

    .. math::

        min(| C_0 \\cap C_1 | / | C_0 |, | C_0 \\cap C_1 | / | C_1 |)

    :param ct0: nodes in first community
    :type ct0: set
    :param ct1: nodes in second community
    :type ct1: set
    :return:
    :rtype: int | float
    """
    intersection_size = len(ct0.intersection(ct1))
    ct0_size = len(ct0)
    ct1_size = len(ct1)
    return min(intersection_size / ct0_size, intersection_size / ct1_size)


def relative_overlap(ct0, ct1):
    """Return relative overlap metric result.

    .. math::

        | C_0 \\cap C_1 | / | C_0 \\cup C_1 |

    :param ct0: nodes in first community
    :type ct0: set
    :param ct1: nodes in second community
    :type ct1: set
    :return:
    :rtype: int | float
    """
    intersection_size = len(ct0.intersection(ct1))
    union_size = len(ct0.union(ct1))
    return intersection_size / union_size


def overlap(ct0, ct1):
    """Return overlap metric result.

    .. math::

        | C_0 \\cap C_1 |

    :param ct0: nodes in first community
    :type ct0: set
    :param ct1: nodes in second community
    :type ct1: set
    :return:
    :rtype: int | float
    """
    intersection_size = len(ct0.intersection(ct1))
    return intersection_size


MATCHING_METRICS = {
    "match": match,
    "relative_overlap": relative_overlap,
    "overlap": overlap,
}


class MatchingCommunities:
    """This class is responsible for computing the community flow graph and
    recognize punctual communities successors and predecessors between two
    snapshots.

    :param communities_t0: communities and their members at `start` snapshot
    :type communities_t0: defaultdict(set)
    :param communities_t1: communities and their members at `end` snapshot
    :type communities_t1: defaultdict(set)
    :param start: first snapshot compared
    :type start: int
    :param end: second snapshot compared
    :type end: int
    :param output_repository:
    :type output_repository: str
    :param community_graph:
    :type community_graph: EvolvingCommunities
    """

    def __init__(
        self,
        communities_t0,
        communities_t1,
        start,
        end,
        output_repository,
        membership: Membership,
    ):
        self.communities_t0 = communities_t0
        self.communities_t1 = communities_t1
        self.start = start
        self.end = end
        self.output_repository = output_repository

        self.communities_size_t0 = dict()
        self.communities_size_t1 = dict()

        self.membership = membership
        self.predecessor = dict()
        self.successor = dict()
        self.predecessor_mmr = dict()
        self.successor_mmr = dict()

    def compute(self, matching_metric):
        """Compute community flow graph and recognize predecessors and
        successors using matching metric.

        :param matching_metric:
        :type matching_metric: Callable
        """

        # For each ct0 cluster in {X1 ... Xn} at t0
        for ct0, ct0_nodes in self.communities_t0.items():
            # For each ct1 cluster in {Y1 ... Yn} at t1
            for ct1, ct1_nodes in self.communities_t1.items():
                # Calculation of the size of the flow between ct0 and ct1
                # i.e. the intersection of the sets of members of each cluster
                intersection = ct0_nodes.intersection(ct1_nodes)
                intersection_size = len(intersection)
                # Successors and predecessors are defined if flow is non-zero.
                if intersection_size > 0:
                    # The relative overlap metric is calculated by taking the
                    # smaller of the two following ratios: flow on the size of
                    # ct0 and flow on the size of ct1.
                    mm = matching_metric(ct0_nodes, ct1_nodes)
                    mm_succ = MatchingMetricResult(mm, intersection_size)
                    mm_pred = MatchingMetricResult(mm, intersection_size)
                    # For a given ct0, if the metric is the highest for
                    # (ct0,ct1) or if it is equal to the highest but with a
                    # larger flow then ct0 is the predecessor of ct1.
                    if (
                        ct0 not in self.predecessor_mmr
                        or mm_pred > self.predecessor_mmr[ct0]
                    ):
                        self.predecessor_mmr[ct0] = mm_pred
                        self.predecessor[ct0] = ct1
                    # For a given ct1, if the metric is the highest for
                    # (ct0,ct1) or if it is equal to the highest but with a
                    # larger flow then ct1 is the successor of ct0.
                    if (
                        ct1 not in self.successor_mmr
                        or mm_succ > self.successor_mmr[ct1]
                    ):
                        self.successor_mmr[ct1] = mm_succ
                        self.successor[ct1] = ct0
        self.build_evolving_communities()

    def build_evolving_communities(self):
        """Link recognized pairs of punctual communities in same evolving
        community"""
        for node, pred in self.predecessor.items():
            if self.successor[pred] == node:
                # pred is next snapshot of node evolving community
                self.membership.detach_static_community(pred)
                self.membership.attach_static_community(
                    pred,
                    self.membership.static_communities[
                        node
                    ].evolving_community.id,
                )

    def export(self):
        """Export links between matching punctual communities.

        Export predecessors / successors status in files.
        """
        save_csv(
            [
                [self.start, self.end, node, pred]
                for node, pred in self.predecessor.items()
            ],
            f"{self.output_repository}/predecessors.csv",
            append=True,
        )
        save_csv(
            [
                [self.start, self.end, node, succ]
                for node, succ in self.successor.items()
            ],
            f"{self.output_repository}/successors.csv",
            append=True,
        )


def static_communities_clusters(
    static_communities: List[StaticCommunity],
) -> defaultdict(set):
    """Convert a list of static communities to clusters.

    :param static_communities:
    :return: punctual communities and their members
    """
    return {s.id: set(m.id for m in s.members) for s in static_communities}


def relabel_communities(
    membership: Membership,
):
    """Recompute labels of static and evolving communities.

    After application, evolving communities will be relabelled as integers
    ``i`` from 0 to the total number of evolving communities detected.
    This is done in snapshots order first.

    Also, all static community will be relabelled:
    ``t``.``i`` where ``t`` is their snapshot, and ``i`` the unique integer
    of their corresponding evolving community.

    :param membership:

    .. note::
        This method is intended to have a more readable and coherent
        membership object after computing matching metrics on all snapshots
    """
    # Sort all non-empty evolving communities by snapshot
    evolving_communities = sorted(
        [
            e
            for e in membership.evolving_communities.values()
            if len(e.snapshots) > 0
        ],
        key=lambda e: min(e.snapshots),
    )

    # Relabel evolving communities
    membership.evolving_communities = {}
    for e in evolving_communities:
        e.id = len(membership.evolving_communities)
        membership.evolving_communities[e.id] = e

    # Relabel static communities
    static_communities = list(membership.static_communities.values())
    membership.static_communities = {}
    for s in static_communities:
        s.id = f"{s.snapshot}.{s.evolving_community.id}"
        membership.static_communities[s.id] = s


if __name__ == "__main__":
    example_text = """example:
      python build_community_graph.py weeks/community_multilevel/commlist/
      weeks/community_multilevel/ 23 315
    """

    # Arguments parsing
    parser = argparse.ArgumentParser(
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Specify an input tcommlist file.")
    parser.add_argument("output", help="Specify an output repository.")
    parser.add_argument(
        "matching_metric",
        choices=[*MATCHING_METRICS.keys()],
        help="Specify a matching metric method among overlap, relative_overlap"
        " and match",
    )
    parser.add_argument("-s", "--start", help="Specify a start snapshot.")
    parser.add_argument("-e", "--end", help="Specify an end snapshot.")
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

    # Arguments validity checks
    if os.path.isfile(args.input):
        input_file = args.input
    else:
        LOGGER.error(f"{args.input} repository does not exist.")
        exit(2)

    # Load memberships from input tcommlist file
    tcommlist = load_tcommlist(input_file).sort()
    membership = Membership.from_tcommlist(tcommlist)

    output_repository = args.output
    os.makedirs(output_repository, exist_ok=True)

    try:
        start = int(args.start) if args.start else min(membership.snapshots)
        end = int(args.end) if args.end else max(membership.snapshots)
    except ValueError:
        LOGGER.error("Start and end snapshot must be integers")
        exit(2)

    if end <= start:
        LOGGER.error("Start snapshot must be strictly before end snapshot")
        exit(2)

    # Output files initialization
    if args.debug:
        save_csv(
            [["start_snapshot", "end_snapshot", "cluster", "predecessor_of"]],
            f"{output_repository}/predecessors.csv",
        )
        save_csv(
            [["start_snapshot", "end_snapshot", "cluster", "successor_of"]],
            f"{output_repository}/successors.csv",
        )

    # Initialize first snapshot
    snapshot_static_communities = defaultdict(list)
    for scomm in membership.static_communities.values():
        snapshot_static_communities[scomm.snapshot].append(scomm)
    dt0 = {}

    # Iterate over snapshots
    for t in range(start, end + 1):
        dt1 = static_communities_clusters(snapshot_static_communities[t])
        mc = MatchingCommunities(
            dt0, dt1, t - 1, t, output_repository, membership
        )
        if args.matching_metric in MATCHING_METRICS:
            mc.compute(MATCHING_METRICS[args.matching_metric])
            if args.debug:
                mc.export()
            dt0 = dt1
        else:
            LOGGER.error("Matching metric '{args.matching_metric}' unknown.")
            exit(1)

    # Relabel communities for easier readability
    relabel_communities(membership)

    # Save built communities in tcommlist file
    save_tcommlist(
        membership.tcommlist, f"{output_repository}/membership.tcommlist"
    )

    # Save built communities in gml for plotting purposes
    save_graph(
        membership.community_graph,
        f"{output_repository}/communities.gml",
    )
