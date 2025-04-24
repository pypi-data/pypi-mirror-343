"""This module enables to compare two tcommlist files.
"""
import logging
import os
from collections import Counter, defaultdict
from math import log
from statistics import mean
from typing import Any, Dict, Set

import numpy as np
from dyn.core.communities import Tcommlist
from dyn.core.files_io import save_csv
from scipy import stats
from sklearn import metrics

LOGGER = logging.getLogger(__name__)


class _TemporalCommunity(object):
    """Class representing a Temporal Community Object

    :attribute communities:
        dictionnary of dictionnary associating to each snapshot and each
        community the set of all the corresponding nodes
        {snapshot: {community: set_of_nodes}}
    """

    def __init__(self):
        self.communities = defaultdict(lambda: defaultdict(set))
        self.nodes = defaultdict(lambda: defaultdict(set))
        self.snapshots = set()

        self.community_alias = dict()
        self.community_current_alias = 0
        self.community_transition_alias = dict()
        self.community_transition_current_alias = 0

    @classmethod
    def from_tcommlist(cls, tcommlist: Tcommlist) -> "_TemporalCommunity":
        """Create temporal community object from tcommlist.

        :param tcommlist:
        :return: temporal community object
        """
        tcommunity = _TemporalCommunity()
        for row in tcommlist:
            snapshot = row.snapshot
            node = row.node_id
            community = tcommunity.get_community_alias(row.static_community_id)
            tcommunity.communities[snapshot][community].add(node)
            tcommunity.nodes[snapshot][node] = community
            tcommunity.snapshots.add(snapshot)
        return tcommunity

    def get_community_alias(self, item):
        """Return unique int alias for a given community name

        :param item:
        :return: unique label for `item`
        :rtype: int
        """
        if item not in self.community_alias:
            self.community_alias[item] = self.community_current_alias
            self.community_current_alias += 1
        return self.community_alias[item]

    def get_community_transition_alias(self, item):
        """Return unique int alias for a given community name

        :param item:
        :return: unique label for `item`
        :rtype: int
        """
        if item not in self.community_transition_alias:
            self.community_transition_alias[
                item
            ] = self.community_transition_current_alias
            self.community_transition_current_alias += 1
        return self.community_transition_alias[item]

    def transitions(self, step):
        """
        Returns a generator that lists the transitions taking into account the
        given step

        :param step:
        :type step: int
        """
        tmp = sorted(self.snapshots)
        if step > 0:
            # ex for dt=6 and l=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            # we need all the pairs with dt as interval
            # [(0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11)]
            # return ((x, y) for x,y in zip(l[::step],l[step::step]))
            return ((x, y) for x, y in zip(tmp[:-step], tmp[step:]))
        elif step == 0:
            return ((x, x) for x in tmp)

    def transition_communities(self, snapshot1, snapshot2):
        """
        Groups all nodes that have made the same transition between two
        communities between the two given snapshots into the same set.

        :param snapshot1: label for first snapshot
        :type snapshot1: int
        :param snapshot2: label for second snapshot
        :type snapshot2: int
        :return:
            A dictionary where keys are a given transition
            (community_in_snapshot1, community_in_spashot_2) and values the set
            of node that have made that transition.
            ex: {0: {66, 210, 133, 86, 58, 173}, 1: {3, 20, 5, 12, 13}}
        :rtype: dict

        .. note:: Empty sets are not returned.
        """
        d = dict()
        for key_c1, nodes_c1 in self.communities[snapshot1].items():
            for key_c2, nodes_c2 in self.communities[snapshot2].items():
                nodes = nodes_c1 & nodes_c2
                if nodes:
                    d[
                        self.get_community_transition_alias((key_c1, key_c2))
                    ] = nodes
        return d

    def transition_communities_listofnodes(self, snapshot1, snapshot2):
        """
        Groups all nodes that have made the same transition between two
        communities between the two given snapshots into the same list.

        :param snapshot1: label for first snapshot
        :type snapshot1: int
        :param snapshot2: label for second snapshot
        :type snapshot2: int
        :return:
            A list of list of nodes that have made the same transition
            ex: [[66, 210, 133, 86, 58, 173], [3, 20, 5, 12, 13]]
        :rtype: dict

        .. note:: Empty sets are not returned.
        """
        res = []
        nodes = self.transition_communities(snapshot1, snapshot2).values()
        for nodes_set in nodes:
            res.append(nodes_set)

        return np.array(res, dtype=object)

    def transition_nodes(self, snapshot1, snapshot2):
        """For each node return a label corresponding to a pair of communities

        :param snapshot1: label for first snapshot
        :type snapshot1: int
        :param snapshot2: label for second snapshot
        :type snapshot2: int
        :return:
            A dict with key a node, and value its community
            ex: {66: 0, 210: 0, 133: 0, 86: 0, 58: 0, 173: 0,
            3: 1, 20: 1, 5: 1, 12: 1, 13: 1}
        :rtype: dict
        """
        d = defaultdict(set)

        for key_c1, nodes_c1 in self.communities[snapshot1].items():
            for key_c2, nodes_c2 in self.communities[snapshot2].items():
                nodes = nodes_c1 & nodes_c2
                for node in nodes:
                    d[node] = self.get_community_transition_alias(
                        (key_c1, key_c2)
                    )
        return d


class _MembershipMetrics(object):
    """Utility class for several membership similarity metrics"""

    @staticmethod
    def entropy(elements):
        _, counts = np.unique(elements, return_counts=True)
        return stats.entropy(counts)

    @staticmethod
    def joint_entropy(elementsX, elementsY):
        _, countsX = np.unique(elementsX, return_counts=True)
        _, countsY = np.unique(elementsY, return_counts=True)

        # H(X|Y) = H(X, Y) - H(Y)
        # H(X, Y) = H(X|Y) + H(X)
        return stats.entropy(countsX, countsY) + stats.entropy(countsY)

    @staticmethod
    def precision(elementsX, elementsY):
        if len(elementsX) == 0:
            return np.nan
        else:
            return len(elementsX.intersection(elementsY)) / len(elementsX)

    @staticmethod
    def recall(elementsX, elementsY):
        if len(elementsY) == 0:
            return np.nan
        else:
            return len(elementsX.intersection(elementsY)) / len(elementsY)

    @staticmethod
    def f1(elementsX, elementsY):
        precision = _MembershipMetrics.precision(elementsX, elementsY)
        recall = _MembershipMetrics.recall(elementsX, elementsY)

        if precision + recall == 0:
            return np.nan
        else:
            return 2 * (precision * recall) / (precision + recall)

    @staticmethod
    def variation_info_score(elementsX, elementsY):
        """Return variation of information of two sets of elements

        Variation is computed with the following formula:

        .. math::
            entropy(elementsX) + entropy(elementsY) - 2 * mutualinfoscore

        where :math:`entropy` is :func:`entropy` and :math:`mutualinfoscore` is
        :func:`sklearn.metrics.mutual_info_score`

        :param elementsX:
        :param elementsY:
        :rtype: float

        .. todo::
            precise formula with better understanding  of :func:`to_labels`
        """

        # labels1, labels2 = to_labels(elementsX, elementsY)

        mutual_information = (
            metrics.mutual_info_score(elementsX, elementsY)
            if len(elementsX) > 0
            else np.nan
        )
        variation_information = (
            _MembershipMetrics.entropy(elementsX)
            + _MembershipMetrics.entropy(elementsY)
            - 2 * mutual_information
        )

        return variation_information

    @staticmethod
    def normalized_variation_info_score(elementsX, elementsY):
        """Compute normalized variation of information

        Variation of information is computed with this formula:

        .. math:: variationinfoscore(elementsX, elementsY) / log_{base}(N)

        where :math:`N` is the upper bound, and :math:`variationinfoscore` is
        :func:`variation_info_score`

        :param elementsX:
        :param elementsY:
        :param base:
        :type base: int or float
        :rtype: float
        """
        variation_information = _MembershipMetrics.variation_info_score(
            elementsX, elementsY
        )

        size = len(elementsX)

        if size > 1:
            return variation_information / log(size)
        return _MembershipMetrics.entropy(elementsY)


def _to_labels(elementsX, elementsY):
    """Convert two dict of elements in list of labels with the same order

    :param elementsX:
    :param elementsY:
    :rtype: tuple
    """
    keysX = elementsX.keys()
    keysY = elementsX.keys()
    labelsX = []
    labelsY = []
    if keysX != keysY:
        LOGGER.error("Sets of nodes are not the same")

    for key in sorted(keysX):
        labelsX.append(elementsX[key])
        labelsY.append(elementsY[key])

    return labelsX, labelsY


def print_info(tcommunity: Tcommlist, transitions, nodes, elements):
    """Print various information successively

    Information being printed:

    * communities: communities contained in `tcommunity`
    * transitions: `transitions`
    * nodes: `nodes`
    * elements: `elements`
    * entropy: :math:`entropy(elements)`

    :param tcommunity:
    :param transitions:
    :param nodes:
    :param elements:
    """
    tcommunity_ = _TemporalCommunity.from_tcommlist(tcommunity)
    print(f"communities: {tcommunity_.communities}\n")
    print(f"transitions: {transitions}")
    print(f"nodes: {nodes}")
    print(f"elements: {elements}")
    print(f"entropy: {_MembershipMetrics.entropy(elements)}")


def match_communities(
    communitiesX: Dict[Any, Set], communitiesY: Dict[Any, Set], nodesY
):
    """Considering two set of communities X and Y.
    Return for each community of X the matching community in Y.
    For each community of X, each node is labeled with its belonging community
    in Y.
    The matching community in Y is the one with the highest number of labels.

    :param communitiesX:
    :param communitiesY:
    :return: list of pairs
    """

    res = []

    # Subset of community in Y matched by community in X
    communitiesYmatchX = set()

    for comX in communitiesX:
        nodeListX = communitiesX[comX]
        # List of community membership in Y of nodes in
        # the given community comX
        comListY = [nodesY[nodeX] for nodeX in nodeListX]
        # Most represented community in comListY
        comY = Counter(comListY).most_common(1)[0][0]
        res.append([comX, comY])
        communitiesYmatchX.add(comY)

    coverage = (
        len(communitiesYmatchX) / len(communitiesY)
        if len(communitiesY) > 0
        else np.nan
    )
    redundancy = (
        len(communitiesX) / len(communitiesYmatchX)
        if len(communitiesYmatchX) > 0
        else np.nan
    )

    return res, coverage, redundancy


def assess_partition_metrics(
    tcommunityX: Tcommlist, tcommunityY: Tcommlist
) -> dict:
    """Compute partition metrics between two temporal communitiies partitions.

    Partitions are compared between each snapshot.

    :param tcommunityX:
    :param tcommunityY:
    :return: partition metrics
    """
    output = {}

    tcommunityX_ = _TemporalCommunity.from_tcommlist(tcommunityX)
    tcommunityY_ = _TemporalCommunity.from_tcommlist(tcommunityY)

    # Compute metrics for each transition
    for snapshot in tcommunityX_.snapshots:
        assert tcommunityX_.snapshots == tcommunityY_.snapshots

        LOGGER.info(f"Computing metrics for partitions at snapshot {snapshot}")
        # For each community of X we get the nodes belonging to it
        communitiesX = tcommunityX_.communities[snapshot]
        # For each community of Y we get the nodes belonging to it
        communitiesY = tcommunityY_.communities[snapshot]
        # For each node of set of communites X we get the label of the
        # belonging community
        nodesX = tcommunityX_.nodes[snapshot]
        # For each node of set of communites Y we get the label of the
        # belonging community
        nodesY = tcommunityY_.nodes[snapshot]
        # Get community labels of nodes
        labelsX, labelsY = _to_labels(nodesX, nodesY)
        # For each community of X we get the matching community in Y
        matching_list, coverage, redundancy = match_communities(
            communitiesX, communitiesY, nodesY
        )

        output[snapshot] = _assess_metrics(
            matching_list,
            communitiesX,
            communitiesY,
            labelsX,
            labelsY,
            coverage,
            redundancy,
        )
    return output


def assess_transition_metrics(
    tcommunityX: Tcommlist, tcommunityY: Tcommlist, dt_min, dt_max
):
    """Compute transition metrics between two temporal communities partitions.

    Transitions of members between `dt_min` and `dt_max` snapshots are
    compared.
    Metrics are indexed by (`t1`, `t2`) with `t1` the transition source
    snapshot and `t2` the transition destination snapshot.

    :param tcommunityX:
    :param tcommunityY:
    :param dt_min: minimum number of snapshots for the transitions
    :param dt_max: maximum number of snapshots for the transitions
    :return: transition metrics
    """
    output = {}

    tcommunityX_ = _TemporalCommunity.from_tcommlist(tcommunityX)
    tcommunityY_ = _TemporalCommunity.from_tcommlist(tcommunityY)

    # Compute metrics for each transition
    for dt in range(int(dt_min), int(dt_max) + 1):
        assert [(x, y) for x, y in tcommunityX_.transitions(dt)] == [
            (x, y) for x, y in tcommunityY_.transitions(dt)
        ]

        LOGGER.info(f"Computing metrics for {dt}-step transitions")
        for begin, end in tcommunityX_.transitions(dt):
            # For each community of X we get the nodes belonging to it
            communitiesX = tcommunityX_.transition_communities(begin, end)
            # For each community of Y we get the nodes belonging to it
            communitiesY = tcommunityY_.transition_communities(begin, end)

            # For each node of set of communites X we get the label of the
            # belonging community
            nodesX = tcommunityX_.transition_nodes(begin, end)
            # For each node of set of communites Y we get the label of the
            # belonging community
            nodesY = tcommunityY_.transition_nodes(begin, end)

            # Get community labels of nodes
            labelsX, labelsY = _to_labels(nodesX, nodesY)

            # For each community of X we get the matching community in Y
            matching_list, coverage, redundancy = match_communities(
                communitiesX, communitiesY, nodesY
            )

            output[(begin, end)] = _assess_metrics(
                matching_list,
                communitiesX,
                communitiesY,
                labelsX,
                labelsY,
                coverage,
                redundancy,
            )
    return output


def _assess_save_partition_metrics(
    tcommunityX, tcommunityY, output_dir, output_file
):
    """Compute and save partition metrics between two temporal communitiies
    partitions.

    :param tcommunityX:
    :param tcommunityY:
    :param output_dir:
    :param output_file:
    """

    output = assess_partition_metrics(tcommunityX, tcommunityY)
    headers = output[list(output.keys())[0]].keys()
    res = [["t"] + list(headers)]
    res = [[t] + [m[h] for h in headers] for t, m in output.items()]

    save_csv(
        res,
        os.path.join(output_dir, output_file),
    )


def _assess_save_transition_metrics(
    tcommunityX, tcommunityY, dt_min, dt_max, output_dir, output_file
):
    """Compute and save transition metrics between two temporal communitiies
    partitions.

    :param tcommunityX:
    :param tcommunityY:
    :param output_dir:
    :param output_file:
    """

    output = assess_transition_metrics(
        tcommunityX, tcommunityY, dt_min, dt_max
    )
    headers = output[list(output.keys())[0]].keys()
    res = [["t1", "t2", "dt"] + list(headers)]
    res = [
        [t1, t2, t2 - t1] + [m[h] for h in headers]
        for (t1, t2), m in output.items()
    ]

    save_csv(
        res,
        os.path.join(output_dir, output_file),
    )


def _assess_metrics(
    matching_list,
    communitiesX,
    communitiesY,
    labelsX,
    labelsY,
    coverage,
    redundancy,
) -> dict:
    f1_list = []
    nf1_list = []

    # Compute F1 and NF1 scores
    for comAofX, comBofY in matching_list:
        nodesA = communitiesX[comAofX]
        nodesB = communitiesY[comBofY]
        f1 = _MembershipMetrics.f1(nodesA, nodesB)
        nf1 = f1 * coverage / redundancy
        f1_list.append(f1)
        nf1_list.append(nf1)

    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html
    adjusted_rand = metrics.adjusted_rand_score(labelsX, labelsY)

    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mutual_info_score.html#sklearn.metrics.mutual_info_score
    mutual_information = (
        metrics.mutual_info_score(labelsX, labelsY)
        if len(labelsX) > 0
        else np.nan
    )

    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_mutual_info_score.html#sklearn.metrics.adjusted_mutual_info_score
    adjusted_mutual_information = metrics.adjusted_mutual_info_score(
        labelsX, labelsY
    )

    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.normalized_mutual_info_score.html#sklearn.metrics.normalized_mutual_info_score
    normalized_mutual_information = metrics.normalized_mutual_info_score(
        labelsX, labelsY
    )

    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.fowlkes_mallows_score.html#sklearn.metrics.fowlkes_mallows_score
    fowlkes_mallows = metrics.fowlkes_mallows_score(labelsX, labelsY)

    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html?highlight=jaccard
    jaccard = metrics.jaccard_score(
        labelsX, labelsY, average="micro", zero_division=True
    )

    vi = _MembershipMetrics.variation_info_score(labelsX, labelsY)

    nvi = _MembershipMetrics.normalized_variation_info_score(labelsX, labelsY)

    return {
        "f1": mean(f1_list) if len(f1_list) > 0 else np.nan,
        "nf1": mean(nf1_list) if len(nf1_list) > 0 else np.nan,
        "coverage": coverage,
        "redundancy": redundancy,
        "adjusted_rand": adjusted_rand,
        "mutual_information": mutual_information,
        "adjusted_mutual_information": adjusted_mutual_information,
        "normalized_mutual_information": normalized_mutual_information,
        "fowlkes_mallows": fowlkes_mallows,
        "jaccard": jaccard,
        "vi": vi,
        "nvi": nvi,
    }
