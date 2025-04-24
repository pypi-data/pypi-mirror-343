"""This module comptute metrics about interaction graphs and community
memberships.

It uses :class:`networkx.Graph` as graph representation.
"""

from collections import defaultdict
from typing import Any, Callable, List

import networkx as nx
import numpy as np
from dyn.core.communities import Membership, Tcommlist
from dyn.core.community_graphs import EvolvingCommunitiesGraph
from dyn.core.files_io import load_csv

from dyn.benchmark.generator.groundtruth_generator import Groundtruth

__all__ = [
    "GroundtruthMetricsComputer",
    "Metric",
    "MetricsHandler",
    "graph_handler",
    "graph_partition_handler",
    "static_community_handler",
    "static_community_graph_handler",
    "evolving_community_handler",
    "snapshot_handler",
    "member_handler",
    "member_snapshot_handler",
    "flow_handler",
    "graph_heavy_metrics",
]


class Metric:
    """This class wraps a metric function to standardize it.

    :param func:
        raw metric function (must return one value or several as a tuple)
    :param fields: fields returned by the `func` metric (in same order)
    """

    def __init__(self, func: Callable, fields: list[str] = None):
        fields = [] if fields is None else fields
        self.func = func
        self.fields = [func.__name__] if len(fields) == 0 else fields

    def __call__(self, *args, **kwargs) -> dict[str, Any]:
        res = self.func(*args, **kwargs)
        _res = res if len(self.fields) > 1 else (res,)
        return {m: v for m, v in zip(self.fields, _res)}

    def __hash__(self) -> int:
        return sum(hash(m) for m in self.fields)

    def __repr__(self) -> str:
        return f"<Metric(func={self.func}, fields={self.fields})>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Metric):
            return False
        return self.func == other.func and self.fields == other.fields

    @classmethod
    def make(cls, *dargs):
        """Decorate a raw metric function.

        This can be used as a parametrized decorator or a simple decorator, by
        providing the decorator (or not) with a list of fields.
        If no fields are provided, the function name is assumed as the only
        field of the metric.

        :param dargs: function or the list of fields as str objects
        :return:
        """
        if len(dargs) > 0 and callable(dargs[0]):
            _func = dargs[0]
            fields = dargs[1:]
        else:
            _func = None
            fields = dargs

        def decorated(func: Callable) -> Metric:
            metric = cls(func, fields)
            return metric

        return decorated if _func is None else decorated(_func)


class MetricsHandler:
    """This class defines a handlers of metrics.

    It calls all stored metrics in :attr:`func` and merge their results in one
    dictionary on :meth:`Metrics.compute` calls.

    Metrics can be added using one of several ways:

    * modify the :attr:`funcs` attribute (to avoid)
    * by adding the raw metric function using `+=` statement
    * by decorating the raw metric function with the wanted handler instance

    :param funcs: metrics

    .. note::
        This uses a listener/callback pattern.
    """

    def __init__(self, *funcs: Metric):
        self.funcs = sorted(set(funcs), key=lambda f: funcs.index(f))

    @property
    def fields(self) -> list[str]:
        """Return merged list of fields.

        :return:
        """
        res = []
        for func in self.funcs:
            res += func.fields
        return res

    def clear(self) -> None:
        """Remove all metrics from handler."""
        self.funcs = []

    def compute(self, *args, **kwargs) -> dict[str, Any]:
        """Compute all metrics and merge their results.

        :return: merged metrics results
        """
        res = {}
        for func in self.funcs:
            res = {**res, **func(*args, **kwargs)}
        return res

    def __call__(self, *dargs):
        """Decorate a raw metric function and add it as a callback.

        This can be used as a parametrized decorator or a simple decorator, by
        providing the decorator (or not) with a list of fields.
        If no fields are provided, the function name is assumed as the only
        field of the metric.

        :param dargs: function or the list of fields as str objects
        :return:
        """
        if len(dargs) > 0 and callable(dargs[0]):
            _func = dargs[0]
            fields = dargs[1:]
        else:
            _func = None
            fields = dargs

        def decorated(func: Callable) -> Metric:
            metric = Metric(func, fields)
            if metric not in self.funcs:
                self.funcs.append(metric)
            return metric

        return decorated if _func is None else decorated(_func)

    def __add__(self, other) -> "MetricsHandler":
        """Add a single metric or the metrics of a whole :class:`Metrics`
        object to the current one.

        :param other: a single metric or a :class:`MetricsHandler` object
        :return: new handler with all metrics
        """
        funcs = other.funcs if isinstance(other, self.__class__) else [other]
        return self.__class__(*self.funcs, *funcs)

    def __sub__(self, other) -> "MetricsHandler":
        """Remove a single metric or the metrics of a whole
        :class:`MetricsHandler` object from the current one.

        :param other: a single metric or a :class:`MetricsHandler` object
        :return: new handler with specified metrics removed
        """
        funcs = (
            set(other.funcs) if isinstance(other, self.__class__) else {other}
        )
        remainings = sorted(
            set(self.funcs) - funcs, key=lambda f: self.funcs.index(f)
        )
        return self.__class__(*remainings)

    def copy(self) -> "MetricsHandler":
        """Return a copy of the handler.

        :return:
        """
        return self.__class__(*self.funcs)


class MetricsComputer:
    """This class defines a generic metrics computer which gather multiple
    metrics handlers.
    """

    @property
    def handlers(self) -> dict[str, MetricsHandler]:
        """Return dict of handlers.

        :return:
        """
        res = {}
        for attr in dir(self):
            if attr == "handlers" or attr == "fields":
                continue
            obj = getattr(self, attr)
            if isinstance(obj, MetricsHandler):
                res[attr] = obj
        return res

    @property
    def fields(self) -> dict[str, list[str]]:
        """Return fields grouped by handlers.

        :return:
        """
        return {k: v.fields for k, v in self.handlers.items()}


graph_handler = MetricsHandler()
"""Metric handler containing all graph metrics"""

graph_partition_handler = MetricsHandler()
"""Metric handler containing all graph partition metrics"""

static_community_handler = MetricsHandler()
"""Metric handler containing all static community metrics"""

static_community_graph_handler = MetricsHandler()
"""Metric handler containing all static community graph metrics"""

evolving_community_handler = MetricsHandler()
"""Metric handler containing all evolving community metrics"""

snapshot_handler = MetricsHandler()
"""Metric handler containing all snapshot metrics"""

member_handler = MetricsHandler()
"""Metric handler containing all member metrics"""

member_snapshot_handler = MetricsHandler()
"""Metric handler containing all member snapshot metrics"""

flow_handler = MetricsHandler()
"""Metric handler containing all community flow metrics"""


class GroundtruthMetricsComputer(MetricsComputer):
    """This class defines the metrics computer for a whole groundtruth.

    For every metrics argument if nothing is provided, the handler defaults
    to using all metrics given to the same name module handler
    (with `_handler` at the end of its variable name).

    :param graph: list of metrics for the :attr:`graph` handler
    :param graph_partition:
        list of metrics for the :attr:`graph_partition` handler
    :param static_community:
        list of metrics for the :attr:`static_community` handler
    :param static_community_graph:
        list of metrics for the :attr:`static_community_graph` handler
    :param evolving_community:
        list of metrics for the :attr:`evolving_community` handler
    :param snapshot:
        list of metrics for the :attr:`snapshot` handler
    :param member:
        list of metrics for the :attr:`member` handler
    :param member_snapshot:
        list of metrics for the :attr:`member_snapshot` handler
    :param flow: list of metrics for the :attr:`flow` handler
    :param components:
        toggle whether :attr:`graph` and :attr:`graph_partition` metrics are
        computed on each graph connected component as well.

    It aggregates the following types of metrics as handlers:

    :attr graph:
    :attr graph_partition:
    :attr static_community:
    :attr static_community_graph:
    :attr evolving_community:
    :attr snapshot:
    :attr member:
    :attr member_snapshot:
    :attr flow:
    """

    def __init__(
        self,
        graph: list[Metric] = None,
        graph_partition: list[Metric] = None,
        static_community: list[Metric] = None,
        static_community_graph: list[Metric] = None,
        evolving_community: list[Metric] = None,
        snapshot: list[Metric] = None,
        member: list[Metric] = None,
        member_snapshot: list[Metric] = None,
        flow: list[Metric] = None,
        components: bool = True,
    ) -> None:
        super().__init__()
        self.graph = (
            MetricsHandler(*graph_handler.funcs)
            if graph is None
            else MetricsHandler(graph)
        )
        self.graph_partition = (
            graph_partition_handler.copy()
            if graph_partition is None
            else MetricsHandler(graph_partition)
        )
        self.static_community = (
            static_community_handler.copy()
            if static_community is None
            else MetricsHandler(static_community)
        )
        self.static_community_graph = (
            static_community_graph_handler.copy()
            if static_community_graph is None
            else MetricsHandler(static_community_graph)
        )
        self.evolving_community = (
            evolving_community_handler.copy()
            if evolving_community is None
            else MetricsHandler(evolving_community)
        )
        self.snapshot = (
            snapshot_handler.copy()
            if snapshot is None
            else MetricsHandler(snapshot)
        )
        self.member = (
            member_handler.copy() if member is None else MetricsHandler(member)
        )
        self.member_snapshot = (
            member_snapshot_handler.copy()
            if member_snapshot is None
            else MetricsHandler(member_snapshot)
        )
        self.flow = (
            flow_handler.copy() if flow is None else MetricsHandler(flow)
        )
        self.components = components

    @property
    def graph_component(self) -> MetricsHandler:
        """Return the metrics handler on graph components.

        It's equal to the :attr:`graph` handler if :attr:`components` is
        ``True``, an empty metrics handler otherwise.

        :return:
        """
        return self.graph if self.components else MetricsHandler()

    @property
    def graph_component_partition(self) -> MetricsHandler:
        """Return the metrics handler on graph components partitions.

        It's equal to the :attr:`graph_partition` handler if :attr:`components`
        is ``True``, an empty metrics handler otherwise.

        :return:
        """
        return self.graph_partition if self.components else MetricsHandler()

    def compute(
        self, groundtruth: Groundtruth
    ) -> dict[str, list[dict[str, Any]]]:
        """Compute all metrics for given groundtruth.

        :param groundtruth:
        :return: results
        """
        graph_metrics = []
        graph_partition_metrics = []
        graph_component_metrics = []
        graph_component_partition_metrics = []
        static_community_metrics = []
        static_community_graph_metrics = []
        snapshot_metrics = []
        evolving_community_metrics = []
        member_metrics = []
        flow_metrics = []
        member_snapshot_metrics = []

        membership = Membership.from_tcommlist(groundtruth.tcommlist)
        community_flow_graph = membership.community_graph
        commlists = groundtruth.tcommlist.commlists
        for t, graph in sorted(
            groundtruth.graphs.items(), key=lambda gg: gg[0]
        ):
            nodes: dict[Any, set] = {}
            for row in commlists[t]:
                if row.static_community_id not in nodes:
                    nodes[row.static_community_id] = set()
                nodes[row.static_community_id].add(row.node_id)
            nodes_partition = list(nodes.values())
            g_metrics = self.graph.compute(graph)
            g_part_metrics = self.graph_partition.compute(
                graph, nodes_partition
            )
            graph_metrics.append({"snapshot": t, **g_metrics})
            graph_partition_metrics.append({"snapshot": t, **g_part_metrics})
            if self.components:
                components = connected_components(graph)
                if len(components) == 1:
                    graph_component_metrics.append(
                        {"snapshot": t, "component": 0, **g_metrics}
                    )
                    graph_component_partition_metrics.append(
                        {"snapshot": t, "component": 0, **g_part_metrics}
                    )
                else:
                    for i, comp in enumerate(components):
                        graph_component_metrics.append(
                            {
                                "snapshot": t,
                                "component": i,
                                **self.graph.compute(comp),
                            }
                        )
                        graph_component_partition_metrics.append(
                            {
                                "snapshot": t,
                                "component": i,
                                **self.graph_partition.compute(
                                    comp, nodes_partition
                                ),
                            }
                        )
            for scomm in community_flow_graph.snapshot_nodes(t):
                static_community_metrics.append(
                    {
                        "static_community": scomm,
                        "snapshot": t,
                        **self.static_community.compute(
                            community_flow_graph, scomm
                        ),
                    }
                )
                static_community_graph_metrics.append(
                    {
                        "static_community": scomm,
                        "snapshot": t,
                        **self.static_community_graph.compute(
                            graph, nodes[scomm]
                        ),
                    }
                )
                successors = [*community_flow_graph.successors(scomm)]
                if len(successors) > 0:
                    # Compute migrants number once and pass it to every flow
                    successor = community_flow_graph.get_node(
                        community_flow_graph.node_community(scomm),
                        t + 1,
                    )
                    migrants = [*community_flow_graph.successors(scomm)]
                    if successor:
                        migrants.remove(successor)

                    migrants_flows = {
                        migrant: community_flow_graph.flow(scomm, migrant)
                        for migrant in migrants
                    }
                    migrants_nb = sum(migrants_flows.values())
                    for tscomm in community_flow_graph.successors(scomm):
                        flow_metrics.append(
                            {
                                "source": scomm,
                                "target": tscomm,
                                **self.flow.compute(
                                    community_flow_graph,
                                    scomm,
                                    tscomm,
                                    migrants_nb=migrants_nb,
                                ),
                            }
                        )
            if len(graph.nodes) > 0:
                for m in graph.nodes:
                    member_snapshot_metrics.append(
                        {
                            "snapshot": t,
                            "node": m,
                            **self.member_snapshot.compute(graph, m),
                        }
                    )
            snapshot_metrics.append(
                {
                    "snapshot": t,
                    **self.snapshot.compute(community_flow_graph, t),
                }
            )
        for ecomm in community_flow_graph.communities:
            evolving_community_metrics.append(
                {
                    "evolving_community": ecomm,
                    **self.evolving_community.compute(
                        community_flow_graph, ecomm
                    ),
                }
            )
        for m, member in membership.members.items():
            member_metrics.append({"node": m, **self.member.compute(member)})

        return {
            "graph": graph_metrics,
            "graph_partition": graph_partition_metrics,
            "graph_component": graph_component_metrics,
            "graph_component_partition": graph_component_partition_metrics,
            "static_community": static_community_metrics,
            "static_community_graph": static_community_graph_metrics,
            "evolving_community": evolving_community_metrics,
            "snapshot": snapshot_metrics,
            "member": member_metrics,
            "flow": flow_metrics,
            "member_snapshot": member_snapshot_metrics,
        }


def division(numerator: float, denominator: float, default=float("nan")):
    """Return division result.

    It returns `default` if `denominator` is 0.

    :param numerator:
    :param denominator:
    :param default: value used if `denominator` is 0
    """
    return default if denominator == 0 else numerator / denominator


def significative_figures(x, n):
    """Return rounded number with significative figures.

    :param x: value
    :type x: int | float
    :param n: number of significative figures (positive)
    :type n: int
    :rtype: int | float
    """
    return x if x == 0 else round(x, -int(np.floor(np.log10(abs(x)))) + n - 1)


def connected_components(graph: nx.Graph) -> List[nx.Graph]:
    """Return connected components as graphs.

    :param graph:
    :return:
    """
    res = []
    for c in nx.connected_components(graph):
        g = nx.Graph()
        sub_graph = graph.subgraph(c)
        g.add_nodes_from((n, graph.nodes[n]) for n in c)
        g.add_edges_from(
            (n1, n2, graph.edges[n1, n2]) for n1, n2 in sub_graph.edges
        )
        res.append(g)
    return res


def biggest_component(graph: nx.Graph) -> nx.Graph:
    """Return connected components with the most nodes.

    :param graph:
    :return:
    """
    subgraphs = connected_components(graph)
    # sort in ascending order on the number of nodes
    sorted_subgraphs = sorted(subgraphs, key=lambda g: len(g.nodes))
    # return last (=biggest)
    return sorted_subgraphs[-1] if len(subgraphs) > 0 else graph


@graph_handler
def diameter(graph):
    """Returns the diameter of the graph

    :param graph:
    :type graph: networkx.Graph
    :rtype: int
    """
    return (
        float("nan")
        if len(graph.edges) == 0 or not nx.is_connected(graph)
        else nx.diameter(graph)
    )


@graph_handler
def number_of_nodes(graph, *args):
    """Returns the count of nodes

    :param graph:
    :type graph: networkx.Graph
    :rtype: int
    """
    return len(graph)


@graph_handler
def number_of_edges(graph, *args):
    """Return the count of edges

    :param graph:
    :type graph: networkx.Graph
    :rtype: int
    """
    return nx.number_of_edges(graph)


@graph_handler
def average_shortest_path_length(graph, *args):
    """Return the average of the shortest path

    :param graph:
    :type graph: networkx.Graph
    :rtype: float

    .. note:: returns ``nan`` if graph has no edges
    """
    return (
        float("nan")
        if len(graph.edges) == 0 or not nx.is_connected(graph)
        else nx.average_shortest_path_length(graph)
    )


@graph_handler("ccf")
def average_clustering(graph, *args):
    """Return the average clustering coefficient

    :param graph:
    :type graph: networkx.Graph
    :rtype: float

    .. note:: returns ``nan`` if graph has no nodes
    """
    return (
        float("nan") if len(graph.nodes) == 0 else nx.average_clustering(graph)
    )


@graph_handler
def nb_connected_components(graph: nx.Graph, *args) -> int:
    """Return number of connected components.

    :param graph:
    :return:
    """
    return len(connected_components(graph))


@static_community_graph_handler
def cut_ratio(graph, community_nodes):
    """Return the fraction of existing edges between a community and
    the rest of the network to which it belongs over the total of all
    possible of such edges.

    :param graph:
    :type graph: networkx.Graph
    :param community_nodes:
    :type community_nodes: list
    :rtype: float
    """

    inter_community_edges = nx.cut_size(graph, community_nodes)
    graph_nodes_count = len(graph)
    community_nodes_count = len(community_nodes)

    denominator = community_nodes_count * (
        graph_nodes_count - community_nodes_count
    )
    if denominator == 0:
        return np.nan
    else:
        return inter_community_edges / denominator


@static_community_graph_handler
def conductance(graph, community_nodes):
    """Return the conductance of a set of nodes"

    :param graph:
    :type graph: networkx.Graph
    :param community_nodes:
    :type community_nodes: list
    :rtype: float

    .. note:: returns ``nan`` if `community_nodes` have no edges
    """

    inter_community_edges, intra_community_edges = community_edges_count(
        graph, community_nodes
    )
    return division(
        inter_community_edges,
        (2 * intra_community_edges + inter_community_edges),
    )


@static_community_graph_handler
def scaled_density(graph, community_nodes):
    """Return the scaled density of a set of nodes

    :param graph:
    :type graph: networkx.Graph
    :param community_nodes:
    :type community_nodes: list
    :rtype: float

    .. note:: returns ``nan`` if `community_nodes` contains only one node
    """

    _, intra_community_edges = community_edges_count(graph, community_nodes)
    community_nodes_count = len(community_nodes)

    return division(2 * intra_community_edges, (community_nodes_count - 1))


@graph_partition_handler("p_in", "p_out")
def edge_probabilities(graph, nodes_partition):
    """Return probabilities of inside and outside edges

    :param graph:
    :type graph: networkx.Graph
    :param nodes_partition:
    :type nodes_partition: list(set)
    :rtype: float, float
    """

    nodes_count = number_of_nodes.func(graph)
    intra_edges = []
    inter_edges = []

    for community_nodes in nodes_partition:
        community_nodes_count = len(community_nodes)
        outside_community_nodes_count = nodes_count - community_nodes_count

        max_intra_community_edges = (
            community_nodes_count * (community_nodes_count - 1)
        ) / 2
        max_inter_community_edges = (
            community_nodes_count * outside_community_nodes_count
        )

        (
            intra_community_edges,
            inter_community_edges,
        ) = community_edges_count(graph, community_nodes)

        if max_intra_community_edges == 0:
            intra_edges_probability = np.nan
        else:
            intra_edges_probability = (
                intra_community_edges / max_intra_community_edges
            )

        if max_inter_community_edges == 0:
            inter_edges_probability = np.nan
        else:
            inter_edges_probability = (
                inter_community_edges / max_inter_community_edges
            )

        intra_edges.append(intra_edges_probability)
        inter_edges.append(inter_edges_probability)

    if len(intra_edges) == 0:
        intra_probability = np.nan
    else:
        intra_probability = sum(intra_edges) / len(intra_edges)

    if len(inter_edges) == 0:
        inter_probability = np.nan
    else:
        inter_probability = sum(inter_edges) / len(inter_edges)

    return intra_probability, inter_probability


@graph_partition_handler
def modularity(graph, nodes_partition):
    """Return the modularity of the community

    :param graph:
    :type graph: networkx.Graph
    :param nodes_partition:
    :type nodes_partition: list(set)
    :rtype: float

    .. note:: returns ``nan`` if graph has no edges
    """

    return (
        float("nan")
        if len(graph.edges) == 0
        else nx.algorithms.community.modularity(graph, nodes_partition)
    )


@graph_partition_handler("coverage", "performance")
def partition_quality(graph: nx.Graph, nodes_partition: list[set]):
    """Return coverage and performance of a graph partition.

    The coverage of a partition is the ratio of the number of intra-community
    edges to the total number of edges in the graph.

    The performance of a partition is the number of intra-community edges plus
    inter-community non-edges divided by the total number of potential edges.

    :param graph:
    :param nodes_partition:
    :return:
    """
    return nx.algorithms.community.partition_quality(graph, nodes_partition)


def community_edges_count(graph, community_nodes):
    """Return the number of edges inside the community and the number
    of edges with nodes outside of the community

    :param graph:
    :type graph: networkx.Graph
    :param community_nodes:
    :type community_nodes: list
    :rtype: float
    """

    edges = graph.edges(community_nodes)

    inter_community_edges = 0
    intra_community_edges = 0

    for n1, n2 in edges:
        if (n1 in community_nodes) & (n2 in community_nodes):
            intra_community_edges += 1
        else:
            inter_community_edges += 1

    return intra_community_edges, inter_community_edges


@snapshot_handler("communities_count")
def concurrent_communities(sankey, snapshot):
    """Return number of communities at a given snapshot.

    :param sankey:
    :type sankey: EvolvingCommunities
    :param snapshot:
    :type snapshot: int
    :rtype: int
    """
    return len(sankey.snapshot_nodes(snapshot))


@evolving_community_handler("lifetime")
def community_lifetime(sankey, community):
    """Return lifetime of a community.

    :param sankey:
    :type sankey: EvolvingCommunities
    :param community:
    :rtype: int
    """
    return len(sankey.community_nodes(community))


@evolving_community_handler("begin_snapshot")
def community_begin_snapshot(sankey, community):
    """Return the first snapshot of an evolving community.

    :param sankey:
    :type sankey: EvolvingCommunities
    :param community:
    :rtype: int
    """
    begin, _ = sankey.get_begin_end_snapshot(community)
    return begin


@evolving_community_handler("begin_size")
def community_begin_size(sankey, community):
    """Return the size of an evolving community when it was created

    :param sankey:
    :type sankey: EvolvingCommunities
    :param community:
    :rtype: int
    """
    begin, _ = sankey.get_begin_end_snapshot(community)
    begin_node = sankey.get_node(community, begin)
    return sankey.node_size(begin_node)


@static_community_handler("change_size_ratio")
def static_community_change_size_ratio(
    sankey: EvolvingCommunitiesGraph, static_community: str
) -> float:
    """Return change size ratio relative to predecessor.

    This is the aggregation of the `community.growth_ratio` and
    `community.shrink_ratio` variable as internally aggregated in
    :mod:`dyn.benchmark.generator.communities_generator`.

    :param sankey:
    :param static_community: a static community identifier
    :return:
    """
    predecessor = sankey.get_node(
        sankey.node_community(static_community),
        sankey.node_snapshot(static_community) - 1,
    )
    if not predecessor:
        return float("nan")
    size = sankey.node_size(predecessor)
    return division(sankey.node_size(static_community) - size, size)


@static_community_handler("emigrants_ratio")
def static_community_emigrants_ratio(
    sankey: EvolvingCommunitiesGraph, static_community: str
) -> float:
    """Return emigrants ratio for a given static community

    :param sankey:
    :param static_community: a static community identifier
    :return:
    """
    size = sankey.node_size(static_community)
    successor = sankey.get_node(
        sankey.node_community(static_community),
        sankey.node_snapshot(static_community) + 1,
    )
    community_flow = (
        sankey.edges[static_community, successor]["flow"] if successor else 0
    )
    emigrants = sankey.node_out_flow(static_community) - community_flow

    return division(emigrants, size)


@flow_handler
def relative_emigrants_flow(
    community_flow_graph: EvolvingCommunitiesGraph,
    scomm1: str,
    scomm2: str,
    migrants_nb: int = None,
) -> float:
    """Compute relative migrants flow between communities.

    :param community_flow_graph:
    :param scomm1: source static community
    :param scomm2: target static community
    :param migrants_nb:
        total number of migrants exiting `scomm1` (computed if not provided)
    :return: relative flow
    """
    successor = community_flow_graph.get_node(
        community_flow_graph.node_community(scomm1),
        community_flow_graph.node_snapshot(scomm1) + 1,
    )
    if scomm2 == successor:
        return np.nan
    if migrants_nb is None:
        migrants = [*community_flow_graph.successors(scomm1)]
        if successor:
            migrants.remove(successor)

        migrants_flows = {
            migrant: community_flow_graph.edges[scomm1, migrant]["flow"]
            for migrant in migrants
        }
        migrants_nb = sum(migrants_flows.values())

    return community_flow_graph.flow(scomm1, scomm2) / migrants_nb


@static_community_handler("size")
def static_community_size(
    sankey: EvolvingCommunitiesGraph, static_community: str
) -> int:
    """Return static community size.

    :param sankey: community flow graph
    :param static_community:
    :return:
    """
    return sankey.node_size(static_community)


@static_community_handler("turnover_ratio")
def static_community_turnover_ratio(
    sankey: EvolvingCommunitiesGraph, static_community: str
) -> float:
    """Return turnover ratio for a given static community

    This is computed on its input flows w.r.t last community snapshot.

    :param sankey:
    :param static_community: a static community identifier
    :return:
    """
    evolving_comm = sankey.node_community(static_community)
    t = sankey.node_snapshot(static_community)
    predecessor = sankey.get_node(evolving_comm, t - 1)

    if predecessor is None:
        return float("nan")

    pred_size = sankey.node_size(predecessor)
    immigrants = (
        sankey.node_size(static_community)
        - sankey.edges[predecessor, static_community]["flow"]
    )
    emigrants = pred_size - sankey.edges[predecessor, static_community]["flow"]

    return division(emigrants + immigrants, 2 * pred_size)


@snapshot_handler("turnover_ratio")
def snapshot_turnover_ratio(
    sankey: EvolvingCommunitiesGraph, snapshot: int
) -> float:
    """Return network turnover ratio at specific snapshot.

    This is computed on the input flow of connecting/disconnecting members
    w.r.t to the previous network size.

    :param sankey:
    :param snapshot:
    :return:
    """
    if snapshot - 1 not in sankey.snapshots:
        return float("nan")

    size = 0
    pred_size = 0
    flow = 0
    for node in sankey.snapshot_nodes(snapshot):
        flow += sankey.node_in_flow(node)
        size += sankey.node_size(node)
    for node in sankey.snapshot_nodes(snapshot - 1):
        pred_size += sankey.node_size(node)

    immigrants = size - flow
    emigrants = pred_size - flow

    return division(immigrants + emigrants, 2 * pred_size)


@member_snapshot_handler("degree")
def member_snapshot_degree(graph: nx.Graph, member: Any) -> int:
    """Return degree of node.

    :param graph:
    :param member:
    :return: degree
    """
    return graph.degree[member]


@member_handler("snapshots_online")
def members_snapshot_count(member):
    """Count number of snapshots online of a member.

    :param member: member view
    :return: snapshot online count
    """
    return len(member.snapshots)


@member_handler("communities_visited")
def members_visited_communities(member):
    """Count number of visited evolving communities of a member.

    :param member: member view
    :return: visited communities count
    """
    return len(set(member.evolving_communities.values()))


graph_heavy_metrics = [diameter, average_shortest_path_length]
"""This is a list of heavy graph computation metrics.

.. note:: they are a part of the `graph_handler` set of metrics
"""


def dict_to_list(communities_dict):
    """Transform a dict of list of nodes with the following structure :
    {community_key: [list of nodes], ...} to a list of set of nodes :
    [{set of nodes}, ..]

    :param communities_dict:
    :type communities_dict: dict
    :rtype: list

    """
    return [set(value) for key, value in communities_dict.items()]


def load_edgelist(fname):
    """Load edgelist file as undirected unweighted graph.

    :param fname: edgelist filename
    :type fname: str
    :rtype: networkx.Graph
    """
    edgelist = load_csv(fname)
    graph = nx.Graph(edgelist)
    return graph


def tcommlist_to_dict(tcommlist: Tcommlist):
    """Convert tcommlist dataframe into a dict (key snapshot) of dict
    (key community) of list of nodes (community's nodes
    at a given snapshot)
    {snapshot_key : {community_key: [list of nodes]}}

    :param tcommlist:
    :return: tcommlist as a dictionary
    :rtype: defaultdict(lambda: defaultdict(list))
    """
    res = defaultdict(lambda: defaultdict(list))
    for row in tcommlist:
        res[row.snapshot][row.static_community_id].append(row.node_id)
    return res


def nantoempty(value):
    """Transform nan value to empty string

    :param value:
    :type value: int | float
    :rtype: int | float | str
    :raise TypeError: if `value` type unsupported by :func:`numpy.isnan`
    """
    try:
        if np.isnan(value):
            return ""
        else:
            return value
    except TypeError:
        return value
