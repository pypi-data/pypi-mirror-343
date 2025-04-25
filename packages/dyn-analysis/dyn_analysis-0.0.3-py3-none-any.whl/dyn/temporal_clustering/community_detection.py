#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module detect communities from members' graphs.

This script generates a commlist files from a member graph edgelists in csv format.

.. code:: bash

    python community_detection.py FILE OUTPUT ALGO [OPTIONS]

    FILE is the graph edgelist file. OUTPUT is the output directory. ALGO the community detection algorithm.

    Algo:
    * community_multilevel
    * community_infomap
    * community_walktrap

    Options:
    * -l, --log     activate logger INFO level
    * -d, --debug   activate logger DEBUG level (takes precedence over -l option)

This script generates the corresponding commlist file in `OUTPUT` directory.
"""  # noqa: E501
import argparse
import logging
import os

import igraph as ig
from dyn.core.communities import Tcommlist, TcommlistRow
from dyn.core.files_io import load_csv, save_commlist, save_csv
from dyn.utils import try_convert

__all__ = []

LOGGER = logging.getLogger(__name__)


class Graph:
    """This class is a wrapper for :class:`igraph.Graph` undirected graph

    :param identifier: identify the graph (e.g snapshot of the graph)
    :type identifier: str
    :param loop: if ``True`` loop edges are authorized
    :type loop: bool

    :attribute obj: :class:`igraph.Graph` internal graph representation
    :attribute nodes: index of each node (accessible per label)
    :attribute nodes_index: label of each node (accessible per index)
    :attribute edges:
    """

    def __init__(self, identifier=None, loop=False):
        self.obj = None
        self.nodes = {}
        self.nodes_index = []
        self.edges = set()
        self.directed = False
        self.weighted = False
        self.loop = loop
        self.identifier = identifier

    def add_node(self, node):
        """Add node to graph.

        :param node: str

        .. warning:: this deletes current igraph graph representation!
        """
        if node not in self.nodes:
            self.nodes[node] = len(self.nodes)
            self.nodes_index.append(node)
        self.obj = None

    def add_edge(self, node1, node2):
        """Add edge to graph.

        :param node1: str
        :param node2: str

        .. warning:: this deletes current igraph graph representation!
        """
        if self.loop or (self.nodes[node1] != self.nodes[node2]):
            self.edges.add(frozenset([self.nodes[node1], self.nodes[node2]]))
        self.obj = None

    def build(self):
        """Build igraph graph representation."""
        self.obj = ig.Graph(
            vertex_attrs={"names": list(self.nodes.keys())},
            edges=[
                [list(edge)[0], list(edge)[1]] for edge in list(self.edges)
            ],
            directed=self.directed,
        )

    def write_edgelist(self, output, filename):
        """Write current edgelist in csv format.

        Output file path is: `output`/undirected_edgelist/`filename`

        :param output: directory prefix
        :type output: str
        :param filename:
        :type filename: str
        """
        repository = "undirected_edgelist/"
        path = f"{output}/{repository}"
        os.makedirs(path, exist_ok=True)
        save_csv(
            [
                [self.nodes_index[a], self.nodes_index[b]]
                for a, b in self.edges
            ],
            f"{path}{os.path.basename(filename)}",
        )


def create_igraph_graph(filename, identifier=None, src=0, dest=1):
    """Load graph and build its :class:`igraph.Graph` representation.

    :param filename: input csv graph filename
    :type filename: str
    :param identifier: graph identifier (e.g snapshot)
    :type identifier: str
    :param src:
    :type src: int
    :param dest:
    :type dest: int
    :return: graph
    :rtype: Graph

    .. note::
        * Currently only undirected, unweighed graph without loops
        * By default src node is in first column (src=0) and target node in the
          second one (dest=1)
    """
    g = Graph(identifier=identifier)

    edges = load_csv(filename)
    for row in edges:
        g.add_node(row[src])
        g.add_node(row[dest])
        g.add_edge(row[src], row[dest])

    g.build()

    return g


def community_detection(graph, algorithm) -> Tcommlist:
    """Perform community detection with given algorithm.

    Choices of algorithm supported:
    * `community_multilevel`
    * `community_infomap`
    * `community_walktrap`

    :param graph:
    :type graph: Graph
    :param algorithm:
    :type algorithm: str
    :return: commlist

    .. seealso::
        `Class documentation igraph.graph <https://igraph.org/python/api/latest/igraph.Graph.html>`_
            Documentation of the :class:`igraph.Graph` class for more information
            on the community detection algorithms.
    """  # noqa: E501

    if algorithm == "community_multilevel":
        comm = graph.obj.community_multilevel()
    elif algorithm == "community_infomap":
        comm = graph.obj.community_infomap()
    elif algorithm == "community_walktrap":
        comm = graph.obj.community_walktrap().as_clustering()
    else:
        LOGGER.error(
            "Community detection algorithm '{args.algorithm}' unknown."
        )
        exit(1)

    commlist = Tcommlist()
    community_name = {}
    for community_index in comm.membership:
        if community_index not in community_name:
            community_name[community_index] = len(community_name)
    for node, community in zip(graph.obj.vs["names"], comm.membership):
        if graph.identifier:
            commlist += TcommlistRow(
                node,
                community_name[community],
                try_convert(graph.identifier),
            )
        else:
            commlist += TcommlistRow(node, community_name[community], -1)
    return commlist


def run(edgelist_file, algorithm, output_repository):
    """Run community detection algorithm.

    Choices of algorithm supported:
    * `community_multilevel`
    * `community_infomap`
    * `community_walktrap`

    :param edgelist_file: graph edgelist filename
    :type edgelist_file: str
    :param algorithm:
    :type algorithm: str
    :param output_repository:
    :type output_repository: str
    """

    filename = os.path.basename(edgelist_file)
    filename_wo_ext = filename.split(".")[0]

    if os.stat(edgelist_file).st_size == 0:
        LOGGER.error(
            f"File {edgelist_file} is empty. Community detection stopped."
        )
        exit(1)
    else:
        LOGGER.info(f"Analyzing {edgelist_file} ...")
        # Create graph and detect community
        g = create_igraph_graph(
            edgelist_file,
            identifier=filename_wo_ext,
        )

        comm = community_detection(g, algorithm)

        # Output communities
        save_commlist(comm, f"{output_repository}/{filename_wo_ext}.commlist")


if __name__ == "__main__":
    example_text = """example:
      python community_detection.py edgelist_timestamp_sorted.csv
      output_folder/ community_multilevel
    """

    parser = argparse.ArgumentParser(
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("file", help="Specify an edgelist file.")
    parser.add_argument("output", help="Specify an output repository.")
    parser.add_argument(
        "algorithm", help="Specify a community detection algorithm."
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

    os.makedirs(args.output, exist_ok=True)

    run(args.file, args.algorithm, args.output)
