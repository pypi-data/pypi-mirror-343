"""This module defines all available masks for computing events.

.. todo:: review and complete documentation
"""

__all__ = ["all_masks"]


def all_masks():
    """Return a set of all implemented masks.

    Function called in the argument parsing so that the user can choose any
    Mask that have been implemented here (without us having to add a new
    option).

    :return:
    :rtype: set
    """

    def all_subclasses(mask):
        return set(mask.__subclasses__()).union(
            [s for c in mask.__subclasses__() for s in all_subclasses(c)]
        )

    return all_subclasses(Mask)


class Mask:
    """Base class for mask calculators around one node.

    Each mask is associated with a punctual representative (node) of an
    evolving community.

    :param community_mask: community mask calculator
    :type community_mask: masks_calculator.CommunityCalculator
    :param punctual_community:
    :type punctual_community: str
    """

    def __init__(self, sankey, punctual_community):
        self.mask = {}
        self.punctual_community = punctual_community
        self.sankey = sankey
        self.node = self.sankey.nodes[punctual_community]
        self.step = self.sankey.node_snapshot(punctual_community)
        self.evolving_community = self.node["evolvingCommunity"]
        in_edges = self.sankey.in_edges(punctual_community)
        out_edges = self.sankey.out_edges(punctual_community)
        self.edges = list(in_edges) + list(out_edges)
        self.precomputations = {metric: 0 for metric in self.metrics}
        self.sequence = []
        self.predecessor, self.successor = None, None
        for punctual_community, node in self.sankey.nodes(data=True):
            if (
                self.sankey.node_community(punctual_community)
                == self.evolving_community
            ):
                if (
                    self.sankey.node_snapshot(punctual_community)
                    == self.step - 1
                ):
                    self.predecessor = node
                if (
                    self.sankey.node_snapshot(punctual_community)
                    == self.step + 1
                ):
                    self.successor = node

        self.sequence.sort(key=lambda x: x.split(".")[0])

    def process_internal_edge(self, edge_direction, value):
        """Process internal edge.

        :param edge_direction: ``"leaving"`` or ``"entering"``
        :type edge_direction: str
        :param value:
        """
        pass

    def process_external_edge(self, edge_direction, value):
        """Process external edge.

        :param edge_direction: ``"leaving"`` or ``"entering"``
        :type edge_direction: str
        :param value:
        """
        pass

    def process_edge(self, edge):
        """Check whether the edge is an entering or leaving one.

        :param edge: source, target
        :type edge: tuple
        """
        source, target = edge

        if self.punctual_community == source:
            edge_direction = "leaving"
            value = (
                0
                if self.sankey.node_out_flow(source) == 0
                else self.sankey.edges[edge]["flow"]
                / self.sankey.node_out_flow(source)
            )
        else:
            edge_direction = "entering"
            value = (
                0
                if self.sankey.node_in_flow(target) == 0
                else self.sankey.edges[edge]["flow"]
                / self.sankey.node_in_flow(target)
            )

        if self.sankey.node_community(source) == self.sankey.node_community(
            target
        ):
            self.process_internal_edge(edge_direction, value)
        else:
            self.process_external_edge(edge_direction, value)

    def precompute(self):
        """Precompute mask."""
        for edge in self.edges:
            self.process_edge(edge)

    def compute(self):
        """Compute mask."""
        pass

    def get_mask(self):
        """Return mask as a dictionary.

        :return:
        :rtype: dict
        """
        return self.mask

    def to_tab(self):
        """Return metrics as a list.

        :return:
        :rtype: list
        """
        tab = []
        for metric in self.metrics:
            tab.append(self.mask[metric])
        return tab

    def run(self):
        """Execute mask algorithm."""
        self.precompute()
        self.compute()


class BaselineMask(Mask):
    """Class for baseline mask.

    Override :func:`process_internal_edge` and :func:`process_external_edge`.
    Precompute metrics.

    :param community_mask: community mask calculator
    :type community_mask: masks_calculator.CommunityCalculator
    :param punctual_community:
    :type punctual_community: str
    """

    name = "baseline"
    metrics = [
        "entering_internal",
        "entering_external",
        "leaving_internal",
        "leaving_external",
    ]

    labels = ["external", "internal", "="]

    def process_internal_edge(self, edge_direction, value):
        metric = f"{edge_direction}_internal"
        self.precomputations[metric] += value

    def process_external_edge(self, edge_direction, value):
        metric = f"{edge_direction}_external"
        self.precomputations[metric] += value

    def compute(self):
        self.mask = self.precomputations


class SimpleGrowthMask(BaselineMask):
    """Class for simple growth mask.

    Override :func:`compute` which complete metrics calculations.

    :param community_mask: community mask calculator
    :type community_mask:
        masks_calculator.CommunityCalculator
    :param punctual_community:
    :type punctual_community: str
    """

    name = "simple"
    metrics = (
        BaselineMask.metrics[:2]
        + ["entering_out_of_dataset"]
        + BaselineMask.metrics[2:]
        + ["leaving_out_of_dataset", "internal_growth"]
    )

    def compute(self):
        self.mask = self.precomputations

        for edge_direction in ["entering", "leaving"]:
            internal = self.mask[f"{edge_direction}_internal"]
            external = self.mask[f"{edge_direction}_external"]

            ratio = (
                1 / (internal + external) if internal + external != 0 else 0
            )
            self.mask[f"{edge_direction}_internal"] *= ratio
            self.mask[f"{edge_direction}_external"] *= ratio

            self.mask[f"{edge_direction}_out_of_dataset"] = (
                1 - internal - external
            )

        next_nbMembers = (
            self.successor["nbMembers"] if self.successor is not None else 0
        )
        prev_nbMembers = (
            self.predecessor["nbMembers"]
            if self.predecessor is not None
            else 0
        )
        denominator = max(prev_nbMembers, next_nbMembers)
        self.mask["internal_growth"] = (
            (next_nbMembers - prev_nbMembers) / denominator
            if denominator
            else 0
        )


class DoubleGrowthMask(BaselineMask):
    """Class for double growth mask.

    Override :func:`compute` which complete metrics calculations.

    :param community_mask: community mask calculator
    :type community_mask:
        masks_calculator.CommunityCalculator
    :param punctual_community:
    :type punctual_community: str
    """

    name = "double"
    metrics = (
        BaselineMask.metrics[:2]
        + ["entering_out_of_dataset", "entering_growth"]
        + BaselineMask.metrics[2:]
        + ["leaving_out_of_dataset", "leaving_growth"]
    )

    def compute(self):
        self.mask = self.precomputations
        n = self.node["nbMembers"]
        nb_members = {
            "entering": self.predecessor["nbMembers"]
            if self.predecessor is not None
            else 0,
            "leaving": self.successor["nbMembers"]
            if self.successor is not None
            else 0,
        }

        for edge_direction in ["entering", "leaving"]:
            internal = self.mask[f"{edge_direction}_internal"]
            external = self.mask[f"{edge_direction}_external"]

            ratio = (
                1 / (internal + external) if internal + external != 0 else 0
            )
            self.mask[f"{edge_direction}_internal"] *= ratio
            self.mask[f"{edge_direction}_external"] *= ratio

            self.mask[f"{edge_direction}_out_of_dataset"] = (
                1 - internal - external
            )

            denominator = max(nb_members[edge_direction], n)
            if edge_direction == "leaving":
                self.mask[f"{edge_direction}_growth"] = (
                    (nb_members[edge_direction] - n) / denominator
                    if denominator
                    else 0
                )
            else:
                self.mask[f"{edge_direction}_growth"] = (
                    (n - nb_members[edge_direction]) / denominator
                    if denominator
                    else 0
                )


class SimpleAllSumsMask(BaselineMask):
    """Class for simple all sums mask.

    Override :func:`compute` which complete metrics calculations.

    :param community_mask: community mask calculator
    :type community_mask:
        masks_calculator.CommunityCalculator
    :param punctual_community:
    :type punctual_community: str
    """

    name = "simple_all_sums"
    metrics = (
        BaselineMask.metrics[:2]
        + ["entering_out_of_dataset"]
        + BaselineMask.metrics[2:]
        + ["leaving_out_of_dataset", "internal_growth"]
    )

    def compute(self):
        self.mask = self.precomputations

        for edge_direction in ["entering", "leaving"]:
            internal = self.mask[f"{edge_direction}_internal"]
            external = self.mask[f"{edge_direction}_external"]

            self.mask[f"{edge_direction}_out_of_dataset"] = (
                1 - internal - external
            )

        next_nbMembers = (
            self.successor["nbMembers"] if self.successor is not None else 0
        )
        prev_nbMembers = (
            self.predecessor["nbMembers"]
            if self.predecessor is not None
            else 0
        )
        denominator = max(prev_nbMembers, next_nbMembers)
        self.mask["internal_growth"] = (
            (next_nbMembers - prev_nbMembers) / denominator
            if denominator
            else 0
        )


class DoubleAllSumsMask(BaselineMask):
    """Class for double all sums mask.

    Override :func:`compute` which complete metrics calculations.

    :param community_mask: community mask calculator
    :type community_mask:
        masks_calculator.CommunityCalculator
    :param punctual_community:
    :type punctual_community: str
    """

    name = "double_all_sums"
    metrics = (
        BaselineMask.metrics[:2]
        + ["entering_out_of_dataset", "entering_growth"]
        + BaselineMask.metrics[2:]
        + ["leaving_out_of_dataset", "leaving_growth"]
    )

    def compute(self):
        self.mask = self.precomputations
        n = self.node["nbMembers"]
        nb_members = {
            "entering": self.predecessor["nbMembers"]
            if self.predecessor is not None
            else 0,
            "leaving": self.successor["nbMembers"]
            if self.successor is not None
            else 0,
        }

        for edge_direction in ["entering", "leaving"]:
            internal = self.mask[f"{edge_direction}_internal"]
            external = self.mask[f"{edge_direction}_external"]

            self.mask[f"{edge_direction}_out_of_dataset"] = (
                1 - internal - external
            )

            denominator = max(nb_members[edge_direction], n)
            if edge_direction == "leaving":
                self.mask[f"{edge_direction}_growth"] = (
                    (nb_members[edge_direction] - n) / denominator
                    if denominator
                    else 0
                )
            else:
                self.mask[f"{edge_direction}_growth"] = (
                    (n - nb_members[edge_direction]) / denominator
                    if denominator
                    else 0
                )
