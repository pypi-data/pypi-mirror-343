#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List

from dyn.core.communities import Membership, Tcommlist
from pandas import DataFrame

from dyn.events.masks import all_masks


class CommunityEventsDetector(ABC):
    """This class defines the common interface for all events detector."""

    @abstractmethod
    def compute(
        self, tcommlist: Tcommlist, evolving_communities: List = None
    ) -> DataFrame:
        """Compute events detection and return events.

        This is done by computing the mask for each static community on the
        tcommlist.

        :param membership:
        :param evolving_communities:
            if set, only return events happening to those evolving communities
        :return: events
        """
        pass


class MaskCalculator(CommunityEventsDetector):
    """Class that computes the masks.

    Computes masks for all punctual communities of an evolving
    community.

    :param mask_name:
    :type mask_name: str
    """

    mask_per_name = {mask.name: mask for mask in all_masks()}

    def __init__(self, mask_name):
        self.mask_name = mask_name
        self.mask_per_node = {}

    def compute(
        self, tcommlist: Tcommlist, evolving_communities: List = None
    ) -> DataFrame:
        """Compute events detection and return events.

        This is done by computing the mask for each static community on the
        tcommlist.

        :param membership:
        :param evolving_communities:
            if set, only return events happening to those evolving communities
        :return: events
        """
        membership = Membership.from_tcommlist(tcommlist)
        community_graph = membership.community_graph
        evolving_communities = (
            list(membership.evolving_communities.keys())
            if evolving_communities is None
            else evolving_communities
        )

        self.mask_per_node = {}
        for node in community_graph.nodes:
            if (
                community_graph.node_community(node)
                not in evolving_communities
            ):
                continue

            # The mask is computed for each node
            mask = self.mask_per_name[self.mask_name](community_graph, node)
            self.mask_per_node[
                (node, community_graph.node_snapshot(node))
            ] = mask
            mask.run()
        return DataFrame(
            [
                {
                    "snapshot": cluster[1],
                    "static_community_id": cluster[0],
                    "evolving_community_id": community_graph.node_community(
                        cluster[0]
                    ),
                    **mask.get_mask(),
                }
                for cluster, mask in self.mask_per_node.items()
            ]
        )

    def get_masks(self):
        """Return masks per node.

        :return:
        :rtype: dict
        """
        return self.mask_per_node
