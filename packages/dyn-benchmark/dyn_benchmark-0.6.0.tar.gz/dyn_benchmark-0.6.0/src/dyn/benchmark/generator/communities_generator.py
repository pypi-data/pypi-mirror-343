"""This module generates communities and their evolution in a graph.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Set, Type

import scipy.stats
from dyn.core.community_graphs import EvolvingCommunitiesGraph
from dyn.core.files_io import save_graph

from dyn.benchmark.generator._interfaces import GeneratorLen, IGenerator

LOGGER = logging.getLogger(__name__)


class MatchingMetric(ABC):
    """This abstract class defines the interface of matching metrics
    in the context of this module.

    :param evolving_communities:
    """

    def __init__(self, evolving_communities: EvolvingCommunitiesGraph):
        self.evolving_communities = evolving_communities

    @abstractmethod
    def compute(self, ct0, ct1) -> float:  # pragma: nocover
        """Compute matching metric.

        :param ct0: source community node
        :param ct1: target community node
        :return: matching metric result
        """
        pass

    @abstractmethod
    def _compute_max_flow(self, ct0, ct1, max_mm) -> float:  # pragma: nocover
        """Compute theoretical flow with given matching metric result.

        :param ct0: source community node
        :param ct1: target community node
        :param max_mm: matching metric result to match
        :return: flow
        """
        pass

    def compute_max_flow(self, ct0, ct1, max_mm) -> int:  # pragma: nocover
        """Compute maximum flow below target matching metric result.

        :param ct0: source community node
        :param ct1: target community node
        :param max_mm: matching metric result strict upper bound
        :return: flow
        """
        flow = self._compute_max_flow(ct0, ct1, max_mm)
        if int(flow) == flow:
            return int(max(flow - 1, 0))
        return int(flow)

    def match(self) -> Dict[Any, Set[Any]]:
        """Compute evolving communities as node clusters using matching metric.

        :return: evolving communities as clusters
        """
        predecessors = {}
        successors = {}
        communities_nodes = {}  # community of each node
        communities = {}  # each evolving communities with its nodes
        # Compute successors and predecessors of each nodes
        for n in self.evolving_communities.nodes:
            communities_nodes[n] = n
            communities[n] = {n}
            successor_mm = -1
            for node_to in self.evolving_communities.successors(n):
                mm = self.compute(n, node_to)
                if (
                    n not in successors
                    or mm > successor_mm
                    or mm == successor_mm
                    and self.evolving_communities.flow(n, node_to)
                    > self.evolving_communities.flow(n, successors[n])
                ):
                    successors[n] = node_to
                    successor_mm = mm
            predecessor_mm = -1
            for node_from in self.evolving_communities.predecessors(n):
                mm = self.compute(node_from, n)
                if (
                    n not in predecessors
                    or mm > predecessor_mm
                    or mm == predecessor_mm
                    and self.evolving_communities.flow(node_from, n)
                    > self.evolving_communities.flow(predecessors[n], n)
                ):
                    predecessors[n] = node_from
                    predecessor_mm = mm
        # Link communities when predecessor and successor matches
        for t in self.evolving_communities.snapshots:
            for n in self.evolving_communities.snapshot_nodes(t):
                if n not in successors:
                    continue
                if predecessors[successors[n]] == n:
                    communities_nodes[successors[n]] = communities_nodes[n]
                    communities[communities_nodes[n]].add(successors[n])
                    communities.pop(successors[n])
        return communities


class Match(MatchingMetric):
    """This class computes the Match Matching metric.

    .. math::

        min(| C_0 \\cap C_1 | / | C_0 |, | C_0 \\cap C_1 | / | C_1 |)

    :param evolving_communities:
    """

    def compute(self, ct0, ct1) -> float:
        """Compute matching metric.

        :param ct0: source community node
        :param ct1: target community node
        :return: matching metric result
        """
        return min(
            self.evolving_communities.flow(ct0, ct1)
            / self.evolving_communities.node_size(ct0),
            self.evolving_communities.flow(ct0, ct1)
            / self.evolving_communities.node_size(ct1),
        )

    def _compute_max_flow(self, ct0, ct1, max_mm) -> float:
        """Compute theoretical flow with given matching metric result.

        :param ct0: source community node
        :param ct1: target community node
        :param max_mm: matching metric result to match
        :return: flow
        """
        return (
            max(
                self.evolving_communities.node_size(ct0),
                self.evolving_communities.node_size(ct1),
            )
            * max_mm
        )


class RelativeOverlap(MatchingMetric):
    """This class computes the Relative Overlap Matching metric.

    .. math::

        | C_0 \\cap C_1 | / | C_0 \\cup C_1 |

    :param evolving_communities:
    """

    def compute(self, ct0, ct1) -> float:
        """Compute matching metric.

        :param ct0: source community node
        :param ct1: target community node
        :return: matching metric result
        """
        flow = self.evolving_communities.flow(ct0, ct1)
        return flow / (
            self.evolving_communities.node_size(ct0)
            + self.evolving_communities.node_size(ct1)
            + flow
        )

    def _compute_max_flow(self, ct0, ct1, max_mm) -> float:
        """Compute theoretical flow with given matching metric result.

        :param ct0: source community node
        :param ct1: target community node
        :param max_mm: matching metric result to match
        :return: flow
        """
        return (
            max_mm
            * (
                self.evolving_communities.node_size(ct0)
                + self.evolving_communities.node_size(ct1)
            )
            / (1 + max_mm)
        )


class Overlap(MatchingMetric):
    """This class computes the Overlap Matching metric.

    .. math::

        | C_0 \\cap C_1 |

    :param evolving_communities:
    """

    def compute(self, ct0, ct1) -> float:
        """Compute matching metric.

        :param ct0: source community node
        :param ct1: target community node
        :return: matching metric result
        """
        return self.evolving_communities.flow(ct0, ct1)

    def _compute_max_flow(self, ct0, ct1, max_mm) -> float:
        """Compute theoretical flow with given matching metric result.

        :param ct0: source community node
        :param ct1: target community node
        :param max_mm: matching metric result to match
        :return: flow
        """
        return max_mm


class CommunitiesGenerator(IGenerator):
    """This class generates a graph for the evolution of communities.

    This generator works by running the following steps:

    * generate communities (nodes only): :meth:`create_communities`
    * generate migrations: :meth:`create_migrations`

    :param community_count: target number of evolving communities
    :param snapshot_count: target number of snapshots
    :param community_size_min: minimum size of a static community
    :param core_nodes_ratio: ratio of members staying in community
    :param matching_metric_type:
    :param seed:

    .. note::
        All methods prefixed with `draw_` are probability distribution that can
        be overriden when subclassing.
    """

    def __init__(
        self,
        community_count: int = 30,
        snapshot_count: int = 12,
        community_size_min: int = 3,
        core_nodes_ratio: float = 0.5,
        matching_metric_type: Type[MatchingMetric] = RelativeOverlap,
        seed: Any = None,
    ):
        super().__init__(seed=seed)
        self.snapshot_count = snapshot_count
        self.community_count = community_count
        self.community_size_min = community_size_min
        self.core_nodes_ratio = core_nodes_ratio
        self.matching_metric_type = matching_metric_type
        self.graph = EvolvingCommunitiesGraph(community="all")

    @property
    def matching_metric(self) -> MatchingMetric:
        """Return matching metric"""
        return self.matching_metric_type(self.graph)

    def draw_community_size(self, *args, **kwargs):
        """Draw size of a community.

        :return: drawn size

        .. warning::
            This should return a value greater or equal to
            :attr:`community_size_min`
        """
        return self.rng.normal(loc=10, scale=3)

    def draw_community_lifetime(self, *args, **kwargs):
        """Draw community lifetime.

        :return: drawn lifetime

        .. warning::
            This should return a value between 1 and :attr:`snapshot_count`
        """
        return scipy.stats.truncnorm.rvs(
            a=-1, b=1, loc=3, scale=2, random_state=self.rng
        )

    def draw_community_start(self, *args, **kwargs):
        """Draw community birth time.

        This value is meant to be linearly transformed towards the interval
        :math:`[0, snapshot\\_count + 1 - lifetime]`. This way a value of 0 is
        be interpreted as a birth at snapshot 0 while a value of 1 is the
        last snapshot possible for the community to be born while living
        its full lifetime without going over :attr:`snapshot_count`.

        :return: drawn community birth time

        .. warning::
            This should return a value between 0 and 1
        """
        return self.rng.random()

    def draw_change_ratio(self, *args, **kwargs):
        """Draw community change ratio.

        This value is used to determine how much a community changes at each
        snapshot according to its current size. A ratio of 0 is interpreted as
        a stable community, -1 corresponds to all member leaving the community
        and 1 corresponds to as many new members as current size.

        :return: drawn community change ratio

        .. warning:: This value should be greater of equal to -1
        """
        return self.rng.normal(scale=0.2)

    def community_size(self):
        value = self.draw_community_size()
        size = int(value)
        if size < self.community_size_min:
            size = self.community_size_min
        return size

    def community_lifetime(self):
        value = self.draw_community_lifetime()
        return int(value)

    def community_start(self, community_length=0):
        maxi = self.snapshot_count - community_length
        ratio = self.draw_community_start()
        if ratio < 0:
            start = 0
        elif ratio >= 1:
            start = maxi - 1
        else:
            start = int(ratio * maxi)
        return start

    def community_change_ratio(self):
        return max(self.draw_change_ratio(), -1)

    def change_size(self, size: int) -> int:
        """Return a new size greater than the minimum size of the communities.

        The new size if chosen using a truncated normal function
        centered on the current size.
        The minimum value is set to the minimum size of the communities.

        .. math::
            max(round(size * community\\_change_{ratio}), community\\_size_{min}

        :param size:
        """  # noqa: E501
        return max(
            round(size * (1 + self.community_change_ratio())),
            self.community_size_min,
        )

    def _add_community_to_graph(
        self, community: Any, snapshot: int, sizes: List[int]
    ):
        """Add a community and its whole lifetime to the flow graph.

        This creates the community nodes starting at `snapshot`.
        Their labels are: `snapshot`.`community`

        :param community: evolving community to create
        :param snapshot: first snapshot of community existence
        :param sizes: community nodes sizes in snapshot order
        """
        for i, size in enumerate(sizes):
            node = f"{snapshot+i}.{community}"
            self.graph.add_node(
                node,
                t=snapshot + i,
                evolvingCommunity=community,
                nbMembers=size,
            )

    def create_community(self, community: Any):
        """Generate one community.

        :param community:
        """
        # Choose the lifetime of the line
        line_length = self.community_lifetime()

        # Choose where the line starts
        start = self.community_start(line_length)

        # Choose the size of the community
        size = self.community_size()

        # Modify the size at each time step
        sizes = [size]
        for _ in range(line_length):
            prev_size = sizes[-1]
            new_size = self.change_size(prev_size)
            if new_size < self.community_size_min:
                new_size = self.community_size_min
            sizes.append(new_size)
        LOGGER.debug(
            f"creating community {community} at t={start} with sizes={sizes}"
        )
        self._add_community_to_graph(community, start, sizes)

    def _create_communities_generator(self):
        """Return the communities basic generator across the time steps.

        The lifetime of the communities is chosen randomly using a probability
        distribution.
        Their starting time step is chosen randomly.
        Their size changes over the time steps as the communities grow and
        shrink.

        After this step, all communities are created as unconnected nodes
        with an evolving community, a size and a snapshot.
        """
        for i in range(self.community_count):
            self.create_community(i)
            yield

        LOGGER.info("{} communities created".format(self.community_count))

    def create_communities_generator(self):
        """Return the communities generator across the time steps.

        The lifetime of the communities is chosen randomly using a probability
        distribution.
        Their starting time step is chosen randomly.
        Their size changes over the time steps as the communities grow and
        shrink.

        After this step, all communities are created as unconnected nodes
        with an evolving community, a size and a snapshot.
        """
        return GeneratorLen(
            self._create_communities_generator(), self.community_count
        )

    def create_communities(self):
        """Create the communities across the time steps.

        The lifetime of the communities is chosen randomly using a probability
        distribution.
        Their starting time step is chosen randomly.
        Their size changes over the time steps as the communities grow and
        shrink.

        After this step, all communities are created as unconnected nodes
        with an evolving community, a size and a snapshot.
        """
        for _ in self.create_communities_generator():
            pass

    def create_intra_community_migration(self, node):
        """Create intra-community output flow for given node.

        If `node` community is continuing, :attr:`core_nodes_ratio`
        ratio of node size is the intra-community flow. This flow is clamped
        to not exceed the size of the successor.

        :param node:
        """
        ecomm = self.graph.node_community(node)
        size = self.graph.node_size(node)
        t = self.graph.node_snapshot(node)
        successor = self.graph.get_node(ecomm, t + 1)
        if successor is None:
            return
        migrants = min(
            round(self.core_nodes_ratio * size),
            self.graph.node_size(successor),
        )
        self.graph.add_edge(node, successor, flow=migrants)

    def _create_intra_community_migrations_generator(self):
        """Create intra-community flows basic generator.

        For each continuing community node, :attr:`core_nodes_ratio`
        ratio of node size is the intra-community flow. This flow is clamped
        to not exceed the size of the successor.
        """
        for n in self.graph.nodes:
            self.create_intra_community_migration(n)
            yield

    def create_intra_community_migrations_generator(self):
        """Create intra-community flows generator.

        For each continuing community node, :attr:`core_nodes_ratio`
        ratio of node size is the intra-community flow. This flow is clamped
        to not exceed the size of the successor.
        """
        return GeneratorLen(
            self._create_intra_community_migrations_generator(),
            len(self.graph.nodes),
        )

    def create_intra_community_migrations(self):
        """Create intra-community flows.

        For each continuing community node, :attr:`core_nodes_ratio`
        ratio of node size is the intra-community flow. This flow is clamped
        to not exceed the size of the successor.
        """
        for _ in self.create_intra_community_migrations_generator():
            pass

    def create_snapshot_inter_community_migrations(self, t: int):
        """Create inter community migrations on given snapshot.

        The remaining output flow of each node is
        distributed towards each successive node (other than the community
        successor) while keeping the same predecessors/successors according to
        the matching metric, and node sizes.

        The distribution route the highest available output flow towards the
        highest available input flow (node with biggest gap between input flow
        and size), iteratively.

        :param t:
        """
        matching_metric = self.matching_metric
        c0_pool = {
            c: self.graph.node_size(c) - self.graph.node_out_flow(c)
            for c in self.graph.snapshot_nodes(t)
        }
        c1_pool = {
            c: self.graph.node_size(c) - self.graph.node_in_flow(c)
            for c in self.graph.snapshot_nodes(t + 1)
        }
        # Compute matching metric of successors
        # Default to 0 when community dies
        # (very strict: prevent any dying community from sending migrants)
        c0_successor_mm = {
            c: matching_metric.compute(c, self.graph.successor(c))
            if self.graph.successor(c)
            else 0
            for c in c0_pool
        }
        # Compute matching metric of predecessors
        # Default to 0 when community is birthed
        # (very strict: prevent any new community from receiving migrants)
        c1_predecessor_mm = {
            c: matching_metric.compute(self.graph.predecessor(c), c)
            if self.graph.predecessor(c)
            else 0
            for c in c1_pool
        }
        # Sort pool of available emigration flow in descending flow order
        c0_pool = dict(
            sorted(c0_pool.items(), key=lambda f: (f[1], f[0]), reverse=True)
        )
        # Create migrations for each source community
        # in descending available pool size order
        for ct0, pool0 in c0_pool.items():
            # Sort pool of available target communities in descending
            # available pool size order
            c1_pool = dict(
                sorted(
                    [(c, f) for (c, f) in c1_pool.items() if f > 0],
                    key=lambda f: (f[1], f[0]),
                    reverse=True,
                )
            )
            ct1_to_remove = []
            for ct1, pool1 in c1_pool.items():
                if ct1 == self.graph.successor(ct0):
                    continue
                if not self.graph.successor(
                    ct0
                ) and not self.graph.predecessor(ct1):
                    # Trying to add a flow between a dying and a new
                    # community => Abort!
                    continue
                if not self.graph.successor(ct0):
                    # Dying community towards continuing one
                    # Just not become new predecessor!
                    c0_successor_mm[ct0] = c1_predecessor_mm[ct1]
                if not self.graph.predecessor(ct1):
                    # Continuing community towards new one
                    # Just not become new successor!
                    c1_predecessor_mm[ct1] = c0_successor_mm[ct0]
                # Try to fit as many ct0 migrants into ct1 as possible
                flow = min(
                    matching_metric.compute_max_flow(
                        ct0,
                        ct1,
                        min(c0_successor_mm[ct0], c1_predecessor_mm[ct1]),
                    ),
                    pool0,
                    pool1,
                )
                if flow == 0:
                    continue
                self.graph.add_edge(ct0, ct1, flow=flow)
                pool0 -= flow
                c1_pool[ct1] -= flow
                if c1_pool[ct1] == 0:
                    ct1_to_remove.append(ct1)
                if pool0 == 0:
                    break
            for ct1 in ct1_to_remove:
                c1_pool.pop(ct1)

    def _create_inter_community_migrations_generator(self):
        """Create inter-community flows basic generator.

        For each snapshot, the remaining output flow of each node is
        distributed towards each successive node (other than the community
        successor) while keeping the same predecessors/successors according to
        the matching metric, and node sizes.

        The distribution route the highest available output flow towards the
        highest available input flow (node with biggest gap between input flow
        and size), iteratively.
        """
        for t in self.graph.snapshots:
            self.create_snapshot_inter_community_migrations(t)
            yield

    def create_inter_community_migrations_generator(self):
        """Create inter-community flows generator.

        For each snapshot, the remaining output flow of each node is
        distributed towards each successive node (other than the community
        successor) while keeping the same predecessors/successors according to
        the matching metric, and node sizes.

        The distribution route the highest available output flow towards the
        highest available input flow (node with biggest gap between input flow
        and size), iteratively.
        """
        return GeneratorLen(
            self._create_inter_community_migrations_generator(),
            len(self.graph.snapshots),
        )

    def create_inter_community_migrations(self):
        """Create inter-community flows.

        For each snapshot, the remaining output flow of each node is
        distributed towards each successive node (other than the community
        successor) while keeping the same predecessors/successors according to
        the matching metric, and node sizes.

        The distribution route the highest available output flow towards the
        highest available input flow (node with biggest gap between input flow
        and size), iteratively.
        """
        for _ in self.create_inter_community_migrations_generator():
            pass

    def create_migrations(self):
        """Create edges between the communities to migrate nodes.

        First intra-community edges are created, then inter-community ones.
        """
        self.create_intra_community_migrations()
        self.create_inter_community_migrations()

    def generate(self) -> EvolvingCommunitiesGraph:
        """Generate evolving community flow graph.

        :return: evolving community flow graph
        """
        self.graph = EvolvingCommunitiesGraph(community="all")
        self.create_communities()
        self.create_migrations()
        return self.graph

    def _copy_kwargs(self) -> Dict:
        """Return kwargs for constructing a copy.

        :return:
        """
        kwargs = super()._copy_kwargs()
        kwargs.update(
            {
                "community_count": self.community_count,
                "snapshot_count": self.snapshot_count,
                "community_size_min": self.community_size_min,
                "core_nodes_ratio": self.core_nodes_ratio,
                "matching_metric_type": self.matching_metric_type,
            }
        )
        return kwargs

    def validate(self):
        """Validate the generated community flow graph.

        :raises ValueError:
            * if any community node has a bigger in flow than its size
            * if any community node has a bigger out flow than its size
            * if communities don't match those built by matching metric
        """
        matching_metric = self.matching_metric
        for n in self.graph.nodes:
            # Check flows are lower or equal to node sizes
            if self.graph.node_in_flow(n) > self.graph.node_size(n):
                raise ValueError(f"in flow greater than size for node '{n}'")
            if self.graph.node_out_flow(n) > self.graph.node_size(n):
                raise ValueError(f"out flow greater than size for node '{n}'")
            # Check communities fit matching metrics
            mm_communities = matching_metric.match()
            communities = self.graph._community_nodes
            if len(mm_communities) != len(communities):
                raise ValueError("communities don't respect matching metrics")
            # Match communities by pairs
            for com1 in communities.values():
                matching = None
                for k2, com2 in mm_communities.items():
                    if com1 == com2:
                        matching = k2
                        break
                if not matching:
                    raise ValueError(
                        "communities don't respect matching metrics"
                    )
                mm_communities.pop(k2)


def main(output):
    """Generate and save communities and their evolution based on
    configuration.

    :param output: output filename
    :type output: str
    """

    # Generate evolving communities
    generator = CommunitiesGenerator()
    generator.create_communities()
    generator.create_migrations()
    save_graph(generator.graph, output)


if __name__ == "__main__":
    gen = CommunitiesGenerator()
    graph = gen.generate()
    print(graph.communities)
    print(graph.snapshots)

    gen.validate()

    from dyn.drawing.sankey_drawing import plot_sankey

    plot_sankey(graph)
