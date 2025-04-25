"""This module implements the ICEM algorithm.

.. todo:: review doc-strings to make sure is is detailed enough
"""
import logging
from typing import Any, Dict, List

from dyn.core.communities import Membership, Tcommlist
from pandas import DataFrame

from dyn.events.events_calculator import CommunityEventsDetector

LOGGER = logging.getLogger(__name__)


def membership_to_members_dict(
    membership: Membership,
) -> Dict[int, Dict[Any, List]]:
    """Convert membership to dict.

    Returned membership is a 2-dimensional dictionary with first dimension
    identified by snapshot number, and second dimension identified by a
    punctual community. The latter contains the members as values.

    :param membership:
    :return: membership as a dict
    """
    members = {}
    for scomm in membership.static_communities.values():
        if scomm.snapshot not in members:
            members[scomm.snapshot] = {}
        members[scomm.snapshot][scomm.id] = [m.id for m in scomm.members]

    return members


class ICEMCalculator(CommunityEventsDetector):
    """Class for computing ICEM algorithm on communities.

    :param alpha:
        ratio of common members to consider punctual communities as similar
    :type alpha: float
    :param beta:
        set ratio of common members to consider punctual communities as very
        similar
    :type beta: float

    .. todo:: rework so it uses tcommlist data directly (loading done before)
    """

    def __init__(self, alpha, beta):
        # time steps are int >= 0
        self.members = {}
        self.steps = []

        # values for partial and total similarity
        self.alpha = alpha
        self.beta = beta

        # result dictionnaries to fulfill during the process
        self.event_per_punctual_community = {}
        self.all_similarities = {}
        self.member_sources_per_punctual_community = {}

    def compute(
        self, tcommlist: Tcommlist, evolving_communities: List = None
    ) -> DataFrame:
        """Compute events detection and return events.

        This is done by computing the mask for each static community on the
        community flow graph.

        :param membership:
        :param evolving_communities:
            if set, only return events happening to those evolving communities
        :return: events
        """

        membership = Membership.from_tcommlist(tcommlist)
        evolving_communities = (
            list(membership.evolving_communities.keys())
            if evolving_communities is None
            else evolving_communities
        )
        self.members = membership_to_members_dict(membership)
        self.steps = list(self.members.keys())
        self.steps.sort()

        last_occurrence_of_member = {}
        similarity_list = {}

        def get_similar_communities(similarity_list, punctual_community, step):
            """
            :param similarity_list:
                the list of members of the current punctual community
            :type similarity_list: list
            :param punctual_community:
            :type punctual_community: str
            :param step:
            :type step: int
            :return:
                The partial and very similar communities of the punctual
                community from previous steps as two different entries of a
                dictionary
            :rtype: dict
            """

            def build_empty_values(punctual_community, step):
                """Initialize punctual community members inputs and outputs.

                :param punctual_community:
                :type punctual_community: str
                :param step:
                :type step: int
                """
                self.member_sources_per_punctual_community[
                    (punctual_community, step)
                ] = {
                    "entering": {
                        "partially_similar": 0,
                        "very_similar": 0,
                        "dissimilar": 0,
                    },
                    "leaving": {
                        "partially_similar": 0,
                        "very_similar": 0,
                        "dissimilar": 0,
                    },
                }

            build_empty_values(punctual_community, step)

            source_communities = {}
            nb_members = len(similarity_list)
            for member, (former_step, former_punc_com) in similarity_list:
                if former_step == step:
                    continue

                if not (former_punc_com, former_step) in source_communities:
                    source_communities[(former_punc_com, former_step)] = 0

                source_communities[(former_punc_com, former_step)] += 1

            similar_communities = {"partial": [], "very": []}

            for (
                community,
                former_step,
            ), nb_common_members in source_communities.items():
                # community must be a former step community
                if former_step == step:
                    continue

                if (
                    not (community, former_step)
                    in self.member_sources_per_punctual_community
                ):
                    build_empty_values(community, former_step)

                # nb_common_members / total members of similar former community
                order_similarity = nb_common_members / len(
                    self.members[former_step][community]
                )
                # nb_common_members / total members of current community
                reverse_similarity = nb_common_members / nb_members

                if order_similarity >= self.beta:
                    similar_communities["very"].append(
                        (community, former_step)
                    )
                    self.member_sources_per_punctual_community[
                        (punctual_community, step)
                    ]["entering"]["very_similar"] += reverse_similarity
                    self.member_sources_per_punctual_community[
                        (community, former_step)
                    ]["leaving"]["very_similar"] += order_similarity
                    continue

                elif (
                    order_similarity >= self.alpha
                    and reverse_similarity >= self.alpha
                ):
                    self.member_sources_per_punctual_community[
                        (punctual_community, step)
                    ]["entering"]["partially_similar"] += reverse_similarity
                    self.member_sources_per_punctual_community[
                        (community, former_step)
                    ]["leaving"]["partially_similar"] += order_similarity
                    similar_communities["partial"].append(
                        (community, former_step)
                    )

                else:
                    self.member_sources_per_punctual_community[
                        (punctual_community, step)
                    ]["entering"]["dissimilar"] += reverse_similarity
                    self.member_sources_per_punctual_community[
                        (community, former_step)
                    ]["leaving"]["dissimilar"] += order_similarity

            return similar_communities

        def has_new_member(similarity_list, step):
            """Check if a new member must be added.

            :param similarity_list:
            :type similarity_list: list
            :param step:
            :type step: int
            :return:
                ``True`` if the proportion of new members of punctual_community
                is over self.alpha
            :rtype: bool
            """
            new_members = [
                ((id), (this_step, this_punc_com))
                for ((id), (this_step, this_punc_com)) in similarity_list
                if this_step == step
            ]
            prop_new_members = len(new_members) / len(similarity_list)
            return prop_new_members >= self.alpha

        def new_event(punctual_community, event):
            """Add event associated to punctual community if possible.

            :param punctual_community:
            :type punctual_community: str
            :param event:
            :type event: str

            .. note::
                If punctual community is already associated to an event,
                nothing will be done here.
            """
            if punctual_community in self.event_per_punctual_community:
                LOGGER.debug(
                    f"{event}: Trying to add this event to "
                    f"{punctual_community} which already has "
                    "an event"
                )
                return
            self.event_per_punctual_community[punctual_community] = event

        previous_communities = []

        for step in self.steps:
            these_communities = []
            # will be used to comute Dissolve event
            matched_former_communities = []

            # to construct similarity-lists of communities
            for punc_com in self.members[step].keys():
                these_communities.append((punc_com, step))
                similarity_list[(punc_com, step)] = []

                for member in self.members[step][punc_com]:
                    if member not in last_occurrence_of_member:
                        value = (step, punc_com)
                        last_occurrence_of_member[member] = value
                    # Store in similarity_list the former step membership of
                    # each member or the current membership
                    # for new nodes (or nodes not active in previous step)
                    similarity_list[(punc_com, step)].append(
                        (member, last_occurrence_of_member[member])
                    )

                if not step == self.steps[0]:
                    self.all_similarities[
                        (punc_com, step)
                    ] = get_similar_communities(
                        similarity_list[(punc_com, step)], punc_com, step
                    )
                else:
                    self.all_similarities[(punc_com, step)] = {
                        "partial": [],
                        "very": [],
                    }

            # identification of community evolution
            # Mohammadmosaferi, K. K., & Naderi, H. (2020). Evolution of
            # communities in dynamic social networks: An efficient map-based
            # approach. Expert Systems with Applications, p6, 147, 113221.
            for punc_com in self.members[step]:
                very_similar_communities = self.all_similarities[
                    (punc_com, step)
                ]["very"]
                partial_similar_communities = self.all_similarities[
                    (punc_com, step)
                ]["partial"]

                # matchs = set(very_similar_communities) | set(partial_similar_communities)  # noqa: E501
                matchs = very_similar_communities + partial_similar_communities
                nb_matchs = len(matchs)
                matched_former_communities += matchs

                # update last_occurrence_of_member
                for member in self.members[step][punc_com]:
                    last_occurrence_of_member[member] = (step, punc_com)

                # zero matches
                if nb_matchs == 0:
                    new_event((punc_com, step), "form")
                    continue

                # more than one match
                if nb_matchs > 1:
                    if len(very_similar_communities) >= 2:
                        if has_new_member(
                            similarity_list[(punc_com, step)], step
                        ):
                            new_event((punc_com, step), "merge and grow")
                            continue
                        else:
                            new_event((punc_com, step), "merge")
                            continue

                    elif len(partial_similar_communities) >= 2:
                        if has_new_member(
                            similarity_list[(punc_com, step)], step
                        ):
                            new_event(
                                (punc_com, step), "partial merge and grow"
                            )
                            continue
                        else:
                            new_event((punc_com, step), "partial merge")
                            continue

                # divides (is punc_com the result of divide of one of its
                # 'partial' predecessor?)
                if len(partial_similar_communities) >= 1:
                    for punc_com_2, step2 in self.all_similarities:
                        if punc_com == punc_com_2:
                            continue
                        # We search for (community, former_step) which are
                        # predecessors of 2 or more communities at time "step"
                        partial_similar_communities_2 = self.all_similarities[
                            (punc_com_2, step2)
                        ]["partial"]

                        event_found = False

                        for (
                            community,
                            former_step,
                        ) in partial_similar_communities_2:
                            if (
                                community,
                                former_step,
                            ) in partial_similar_communities:
                                event_found = True

                                if has_new_member(
                                    similarity_list[(punc_com, step)], step
                                ):
                                    new_event(
                                        (punc_com, step), "divide and grow"
                                    )

                                else:
                                    new_event((punc_com, step), "divide")

                                if event_found:
                                    break

                        if event_found:
                            break

                    if event_found:
                        continue

                # one match
                if len(very_similar_communities) == 1:
                    if has_new_member(similarity_list[(punc_com, step)], step):
                        new_event((punc_com, step), "grow")
                        continue
                    else:
                        new_event((punc_com, step), "continue")
                        continue

                elif len(partial_similar_communities) == 1:
                    if has_new_member(similarity_list[(punc_com, step)], step):
                        new_event((punc_com, step), "partial survive and grow")
                        continue
                    else:
                        new_event((punc_com, step), "shrink")
                        continue

            for previous_community, previous_step in previous_communities:
                if (
                    not (previous_community, previous_step)
                    in matched_former_communities
                ):
                    new_event(
                        (previous_community, previous_step + 1), "dissolve"
                    )

            previous_communities = these_communities

        return DataFrame(
            [
                {
                    "snapshot": cluster[1],
                    "static_community_id": cluster[0],
                    "evolving_community_id": (
                        membership.static_communities[
                            cluster[0]
                        ].evolving_community.id
                    ),
                    "label": event,
                }
                for cluster, event in self.event_per_punctual_community.items()
                if membership.static_communities[
                    cluster[0]
                ].evolving_community.id
                in evolving_communities
            ]
        )
