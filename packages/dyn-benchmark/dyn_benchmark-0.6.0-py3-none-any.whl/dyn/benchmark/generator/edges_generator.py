"""This module uses stochastic block model to generate graphs from tcommlist

It uses :class:`networkx.Graph` as graph representation.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict
from typing import Generator as Gen

import networkx as nx
from dyn.core.communities import Tcommlist
from dyn.core.files_io import load_tcommlist
from dyn.utils import change_dir
from numpy.random import Generator, default_rng

from dyn.benchmark.generator._interfaces import GeneratorLen, IGenerator

LOGGER = logging.getLogger(__name__)


def create_graph_sbm(
    commlist: Tcommlist, p_in, p_out, rng: Generator | None = None
):
    """Returns graph computed from clusters using Stochastic Block Model (SBM)
    :footcite:p:`holland1983stochastic`.

    :param commlist:
    :param p_in: intra-community edge density
    :type p_in: float
    :param p_out: inter-community edge density
    :type p_out: float
    :param rng: random number generator
    :return:
    :rtype: nx.Graph

    .. footbibliography::
    """
    rng = default_rng() if rng is None else rng

    # Convert commlist to nodes_clusters clusters
    nodes_cluster = {}
    for row in commlist:
        nodes_cluster[row.node_id] = row.static_community_id

    # Set of all nodes
    nodes = list(nodes_cluster.keys())

    # Initialize graph with all nodes but no edge
    graph = nx.Graph()
    graph.add_nodes_from(nodes)

    for i, n1 in enumerate(nodes[:-1]):
        # Iterate over all the nodes in the clusters
        for n2 in nodes[(i + 1) :]:
            # Iterate over all unprocessed other nodes
            prob = p_in if nodes_cluster[n1] == nodes_cluster[n2] else p_out
            if rng.random() < prob:
                graph.add_edge(n1, n2)

    return graph


def create_graph_bpam(
    commlist: Tcommlist,
    gamma_in,
    gamma_out,
    m,
    self_loop: bool = False,
    rng: Generator | None = None,
):
    """Returns graph computed from clusters using Block Preferential
    Attachment Model (BPAM) :footcite:p:`tang2020buckley`.

    A star graph of `m` nodes is used to initialize it.

    :param commlist:
    :param gamma_in:
        intra-community interaction index (often called :math:`\\gamma_{kk}`)
    :type gamma_in: float
    :param gamma_out:
        inter-community interaction index (often called :math:`\\gamma_{lk}`)
    :type gamma_out: float
    :param m: number of new edges created per new node
    :type m: int
    :param self_loop:
        authorize the choice of self loops (as in the reference article)
        **Warning: the returned graph won't necessarily be connected!**
    :param rng: random number generator
    :return: generated graph
    :rtype: nx.Graph

    .. footbibliography::
    """
    rng = default_rng() if rng is None else rng

    # Convert commlist to nodes_clusters clusters
    nodes_cluster = {}
    for row in commlist:
        nodes_cluster[row.node_id] = row.static_community_id

    # Set of all nodes
    nodes = list(nodes_cluster.keys())
    rng.shuffle(nodes)

    # Initialize graph with m nodes
    graph: nx.Graph = nx.star_graph(nodes[: (m + 1)])

    # BPAM
    for node1 in nodes[(m + 1) :]:
        # Compute preferrential attachment probabilities
        prob_dict = {}
        for other in graph.nodes:
            prob_dict[other] = (
                gamma_in
                if nodes_cluster[node1] == nodes_cluster[other]
                else gamma_out
            ) * graph.degree[other]
            if self_loop:
                prob_dict[node1] = gamma_in

        # Create up to m new edges between node and existing nodes
        for _ in range(m):
            sum_p = sum(prob_dict.values())
            node2 = rng.choice(
                [*prob_dict.keys()],
                p=[p / sum_p for p in prob_dict.values()],
                shuffle=False,
            )
            graph.add_edge(node1, node2)
            prob_dict[node2] = (
                gamma_in
                if nodes_cluster[node1] == nodes_cluster[node2]
                else gamma_out
            ) * graph.degree[node2]
    if self_loop:
        graph.remove_edges_from(nx.selfloop_edges(graph))
    return graph


def create_graph_pam(
    commlist: Tcommlist,
    m,
    self_loop: bool = False,
    rng: Generator | None = None,
):
    """Returns graph computed from clusters using Preferential
    Attachment Model (PAM) from :footcite:p:`tonelli2010three`.

    :param commlist:
    :param m: number of new edges created per new node
    :type m: int
    :param self_loop:
        authorize the choice of self loops
        **Warning: the returned graph won't necessarily be connected!**
    :param rng: random number generator
    :return: generated graph
    :rtype: nx.Graph

    .. footbibliography::
    """
    rng = default_rng() if rng is None else rng

    # Convert commlist to nodes_clusters clusters
    nodes_cluster = {}
    for row in commlist:
        nodes_cluster[row.node_id] = row.static_community_id

    # Set of all nodes
    nodes = list(nodes_cluster.keys())
    rng.shuffle(nodes)

    # Initialize graph as an empty graph
    graph = nx.Graph()
    edges = set()
    node_segment = []

    if not self_loop:
        node_segment = [nodes[0]]
        nodes = nodes[1:]

    for node0 in nodes:
        if self_loop:
            node_segment.append(node0)
        edges_added = 0
        for _ in range(m):
            r = rng.integers(0, len(node_segment))
            node1 = node_segment[r]
            if node1 == node0 or (node0, node1) in edges:
                continue
            edges_added += 1
            edges.add((node0, node1))
            graph.add_edge(node0, node1)
            node_segment.append(node1)
            if self_loop:
                node_segment.append(node0)
        if not self_loop:
            node_segment += [node0] * edges_added
    return graph


def create_graph_fast_bpam(
    commlist: Tcommlist,
    gamma_in,
    gamma_out,
    m,
    self_loop: bool = False,
    rng: Generator | None = None,
):
    """Returns graph computed from clusters using Block Preferential
    Attachment Model (BPAM) derived from :footcite:p:`tonelli2010three`.

    :param commlist:
    :param gamma_in:
        intra-community interaction index (often called :math:`\\gamma_{kk}`)
    :type gamma_in: float
    :param gamma_out:
        inter-community interaction index (often called :math:`\\gamma_{lk}`)
    :type gamma_out: float
    :param m: number of new edges created per new node
    :type m: int
    :param self_loop:
        authorize the choice of self loops
        **Warning: the returned graph won't necessarily be connected!**
    :param rng: random number generator
    :return: generated graph
    :rtype: nx.Graph

    .. footbibliography::
    """
    rng = default_rng() if rng is None else rng

    # Convert commlist to nodes_clusters clusters
    nodes_cluster = {}
    communities = set()
    for row in commlist:
        nodes_cluster[row.node_id] = row.static_community_id
        communities.add(row.static_community_id)
    communities = sorted(communities)

    # Set of all nodes
    nodes = list(nodes_cluster.keys())
    rng.shuffle(nodes)

    # Initialize graph as an empty graph
    graph = nx.Graph()
    edges = set()
    community_node_segments = {c: [] for c in communities}

    if not self_loop:
        node0 = nodes[0]
        community_node_segments[nodes_cluster[node0]] = [node0]
        nodes = nodes[1:]

    for node0 in nodes:
        community0 = nodes_cluster[node0]
        if self_loop:
            community_node_segments[community0].append(node0)
        edges_added = 0
        for _ in range(m):
            community_segments_total = {
                c: (gamma_in if c == community0 else gamma_out)
                * len(community_node_segments[c])
                for c in communities
            }
            r = rng.uniform(0, sum(community_segments_total.values()))
            K_curr = 0
            for c, K in community_segments_total.items():
                if r <= K_curr + K:
                    community1 = c
                    r = int((r - K_curr) * len(community_node_segments[c]) / K)
                    break
                K_curr += K

            node1 = community_node_segments[community1][r]
            if node1 == node0 or (node0, node1) in edges:
                continue
            edges_added += 1
            edges.add((node0, node1))
            graph.add_edge(node0, node1)
            community_node_segments[community1].append(node1)
            if self_loop:
                community_node_segments[community0].append(node0)
        if not self_loop:
            community_node_segments[community0] += [node0] * edges_added
    return graph


class IStaticGraphGenerator(IGenerator, ABC):
    """This class defines a common interface for generators of static graphs.

    :param max_iter:
    :type max_iter: int
    :param seed:
    """

    def __init__(self, max_iter=10, seed: Any = None):
        super().__init__(seed=seed)
        self.max_iter = max_iter

    @abstractmethod
    def create_graph(self, commlist: Tcommlist):  # pragma: nocover
        """Create a graph using the provided clusters.

        :param commlist:
        :return: created graph
        :rtype: nx.Graph
        """
        pass

    def _create_graphs_generator(
        self, commlists: Dict[int, Tcommlist]
    ) -> Gen[tuple[int, nx.Graph]]:
        """Create graphs using the provided commlists.

        :param commlists:
        :return: generator of timesteps and corresponding graphs
        """
        timesteps = list(commlists.keys())
        t_iter = iter(timesteps)
        t = next(t_iter)
        n_iter = 0
        while True:
            graph = self.create_graph(commlists[t])
            n_iter += 1

            # Continue with the next time step if the graph is connected
            if not nx.is_connected(graph):
                if self.max_iter < 0 or n_iter < self.max_iter:
                    LOGGER.debug("Graph not connected")
                    LOGGER.debug(
                        f"Starting attempt {n_iter+1} for time step {t}"
                    )
                    continue
                else:
                    LOGGER.error(
                        f"Disconnected graph generated for time step {t}"
                    )
            yield t, graph
            n_iter = 0
            try:
                t = next(t_iter)
            except StopIteration:
                break

    def create_graphs_generator(
        self, tcommlist: Tcommlist
    ) -> GeneratorLen[tuple[int, nx.Graph]]:
        """Create graphs using the provided tcommlist.

        :param tcommlist:
        :return: generator of timesteps and corresponding graphs
        """
        commlists = tcommlist.commlists
        return GeneratorLen(
            self._create_graphs_generator(commlists), len(commlists)
        )

    def create_graphs(self, tcommlist: Tcommlist) -> Dict[int, nx.Graph]:
        """Create graphs using the provided tcommlist.

        :param tcommlist:
        :return: graphs organized by timesteps
        """
        return dict(self.create_graphs_generator(tcommlist))

    def _copy_kwargs(self) -> Dict:
        """Return kwargs for constructing a copy.

        :return:
        """
        kwargs = super()._copy_kwargs()
        kwargs.update(
            {
                "max_iter": self.max_iter,
            }
        )
        return kwargs


class SBM(IStaticGraphGenerator):
    """This class defines a generator of static graphs using Stochastic Block
    Model (SBM) :footcite:p:`holland1983stochastic`.

    :param p_in: intra-community edge probability
    :type p_in: float
    :param p_out: inter-community edge probability
    :type p_out: float
    :param max_iter:
    :type max_iter: int
    :param seed:

    .. footbibliography::
    """

    def __init__(self, p_in=0.8, p_out=0.01, max_iter=10, seed: Any = None):
        self.p_in = p_in
        self.p_out = p_out
        super().__init__(max_iter=max_iter, seed=seed)

    def create_graph(self, commlist: Tcommlist):
        """Create a graph from the provided clusters using Stochastic Block
        Model (SBM).

        :param commlist:
        :return: created graph
        :rtype: nx.Graph
        """
        return create_graph_sbm(commlist, self.p_in, self.p_out, rng=self.rng)

    def _copy_kwargs(self) -> Dict:
        """Return kwargs for constructing a copy.

        :return:
        """
        kwargs = super()._copy_kwargs()
        kwargs.update(
            {
                "p_in": self.p_in,
                "p_out": self.p_out,
            }
        )
        return kwargs


class PAM(IStaticGraphGenerator):
    """This class defines a generator of static graphs using Preferential
    Attachment Model (PAM) :footcite:p:`tonelli2010three`.

    :param m: number of edges created at each step
    :type m: int
    :param self_loop: enable/disable self loops
    :type self_loop: bool
    :param seed:

    .. footbibliography::
    """

    def __init__(
        self,
        m=5,
        self_loop=False,
        seed: Any = None,
        **kwargs,
    ):
        self.m = m
        self.self_loop = self_loop
        super().__init__(max_iter=-1, seed=seed)

    def create_graph(self, commlist: Tcommlist):
        """Create a graph from the provided clusters using Preferential
        Attachment Model (PAM).

        :param commlist:
        :return: created graph
        :rtype: nx.Graph
        """
        return create_graph_pam(
            commlist,
            self.m,
            self.self_loop,
            rng=self.rng,
        )

    def _create_graphs_generator(
        self, commlists: Dict[int, Tcommlist]
    ) -> Gen[tuple[int, nx.Graph]]:
        """Create graphs using the provided tcommlist.

        :param commlists:
        :return: generator of timesteps and corresponding graphs
        """
        for t, commlist in commlists.items():
            yield t, self.create_graph(commlist)

    def _copy_kwargs(self) -> Dict:
        """Return kwargs for constructing a copy.

        :return:
        """
        kwargs = super()._copy_kwargs()
        kwargs.update(
            {
                "m": self.m,
                "self_loop": self.self_loop,
            }
        )
        return kwargs


class BPAM(PAM):
    """This class defines a generator of static graphs using Block Preferential
    Attachment Model (BPAM) :footcite:p:`tang2020buckley`.

    :param gamma_in:
        intra-community interaction index (often called :math:`\\gamma_{kk}`)
    :type gamma_in: float
    :param gamma_out:
        inter-community interaction index (often called :math:`\\gamma_{lk}`)
    :param m: number of edges created at each step
    :type m: int
    :param self_loop: enable/disable self loops
    :type self_loop: bool
    :param seed:

    .. footbibliography::
    """

    def __init__(
        self,
        gamma_in=0.8,
        gamma_out=0.01,
        m=5,
        self_loop=False,
        seed: Any = None,
        **kwargs,
    ):
        self.gamma_in = gamma_in
        self.gamma_out = gamma_out
        self.self_loop = self_loop
        super().__init__(m=m, max_iter=-1, seed=seed)

    def create_graph(self, commlist: Tcommlist):
        """Create a graph from the provided clusters using Block Preferential
        Attachment Model (BPAM).

        :param commlist:
        :return: created graph
        :rtype: nx.Graph
        """
        return create_graph_bpam(
            commlist,
            self.gamma_in,
            self.gamma_out,
            self.m,
            self.self_loop,
            rng=self.rng,
        )

    def _copy_kwargs(self) -> Dict:
        """Return kwargs for constructing a copy.

        :return:
        """
        kwargs = super()._copy_kwargs()
        kwargs.update(
            {
                "gamma_in": self.gamma_in,
                "gamma_out": self.gamma_out,
                "m": self.m,
                "self_loop": self.self_loop,
            }
        )
        return kwargs


class FastBPAM(BPAM):
    """This class defines a generator of static graphs using Block Preferential
    Attachment Model (BPAM) derived from :footcite:p:`tonelli2010three`.

    :param gamma_in:
        intra-community interaction index (often called :math:`\\gamma_{kk}`)
    :type gamma_in: float
    :param gamma_out:
        inter-community interaction index (often called :math:`\\gamma_{lk}`)
    :param m: number of edges created at each step
    :type m: int
    :param self_loop: enable/disable self loops
    :type self_loop: bool
    :param seed:

    .. footbibliography::
    """

    def create_graph(self, commlist: Tcommlist):
        """Create a graph from the provided clusters using Block Preferential
        Attachment Model (BPAM).

        :param commlist:
        :return: created graph
        :rtype: nx.Graph
        """
        return create_graph_fast_bpam(
            commlist,
            self.gamma_in,
            self.gamma_out,
            self.m,
            self.self_loop,
            rng=self.rng,
        )


def main(
    input_file,
    out_dir=None,
    algo=None,
    p_in=0.8,
    p_out=0.01,
    gamma_in=0.8,
    gamma_out=0.01,
    m=5,
    self_loop=False,
    max_iter=10,
):
    """Generate and save graphs as edgelist files from tcommlist file.

    :param input_file: tcommlist file
    :type input_file: str
    :param out_dir: output directory to save graphs
    :type out_dir: str
    :param algo: graph generation algorithm to use
    :type algo: str
    :param p_in: intra-community edge probability (SBM)
    :type p_in: float
    :param p_out: inter-community edge probability (SBM)
    :type p_out: float
    :param gamma_in:
        intra-community interaction index (often called :math:`\\gamma_{kk}`)
        (BPAM)
    :type gamma_in: float
    :param gamma_out:
        inter-community interaction index (often called :math:`\\gamma_{lk}`)
        (BPAM)
    :param m: number of edges created at each step in BPAM
    :type m: int
    :param self_loop: enable/disable self loops in BPAM
    :type self_loop: bool
    :param max_iter:
        max number of attempts at creating a connected graph for each snapshot
        in SBM (note: if negative, can loop infinitely until a valid graph is
        generated)
    """
    tcommlist = load_tcommlist(input_file)

    # Generate graphs
    generator = (
        BPAM(
            gamma_in,
            gamma_out,
            m,
            self_loop,
        )
        if algo == "BPAM"
        else SBM(p_in, p_out, max_iter)
    )

    # Generate graphs
    graphs_list = generator.create_graphs(tcommlist)

    # Write edgelists
    if out_dir is not None:
        with change_dir(out_dir, create=True):
            for t, g in graphs_list:
                nx.write_edgelist(
                    g, "{}.csv".format(t), data=False, delimiter=","
                )
