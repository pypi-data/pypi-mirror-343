"""This module generates a complete benchmark.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from dyn.core.communities import Tcommlist
from networkx import Graph
from numpy.random import SeedSequence

from dyn.benchmark.generator._interfaces import IGenerator
from dyn.benchmark.generator.communities_generator import CommunitiesGenerator
from dyn.benchmark.generator.edges_generator import (
    FastBPAM,
    IStaticGraphGenerator,
)
from dyn.benchmark.generator.events_generator import (
    Event,
    generate_groundtruth_events,
)
from dyn.benchmark.generator.nodes_generator import RandomMemberGenerator

LOGGER = logging.getLogger(__name__)


try:
    from alive_progress import alive_it
except ImportError:

    def alive_it(iterator, *args, **kwargs):
        LOGGER.warning(
            "You need to install the package 'alive-progress'>3 to enjoy full "
            "progress bar features (or install this package with 'pretty' or "
            "'all' optional dependencies)"
        )
        return iterator


@dataclass
class Groundtruth:
    """This class represents a temporal network and its communities.

    :param tcommlist:
    :param graphs: networkx graph for each snapshot
    :param events: community events

    :attr membership:
    """

    tcommlist: Tcommlist
    graphs: Dict[int, Graph]
    events: List[Event]


class GroundtruthGenerator(IGenerator):
    """This class defines a complete benchmark generator.

    :param community_generator:
        community flow graph generator, :class:`CommunitiesGenerator` with
        default arguments if not provided
    :param node_generator:
        membership generator, new :class:`RandomMemberGenerator` instance
        if not provided
    :param edge_generator:
        snapshot network graphs generator, :class:`BPAM` with default
        arguments if not provided
    :param seed:

    .. note::
        `seed` attributes of each step generator will be replaced by a new one
        spwaned from :attr:`seed`.
    """

    def __init__(
        self,
        community_generator: CommunitiesGenerator = None,
        node_generator: RandomMemberGenerator = None,
        edge_generator: IStaticGraphGenerator = None,
        seed: Any = None,
    ):
        self.community_generator = (
            CommunitiesGenerator()
            if community_generator is None
            else community_generator
        )
        self.node_generator = (
            RandomMemberGenerator()
            if node_generator is None
            else node_generator
        )
        self.edge_generator = (
            FastBPAM() if edge_generator is None else edge_generator
        )
        super().__init__(seed=seed)

    def configure_seed(self, seed: Any):
        """Set :attr`seed` and :attr`rng`.

        :param seed:
        :return: instance generator
        """
        super().configure_seed(seed)
        seed_c, seed_n, seed_e = self.seed.spawn(3)
        self.community_generator.seed = seed_c
        self.node_generator.seed = seed_n
        self.edge_generator.seed = seed_e
        return self

    def generate_communities(self):
        """Generate evolving communities.

        :return: evolving communities
        :rtype: dyn.core.community_graphs.EvolvingCommunity
        """
        LOGGER.info("Generating evolving communities")
        return self.community_generator.generate()

    def generate_clusters(self, communities):
        """Generate clusters of members for each time step.

        :return: list of the clusters for each time step as a tcommlist
        :rtype: dyn.core.communities.Tcommlist
        """
        LOGGER.info("Generating members clusters")
        return self.node_generator.generate(communities)

    def generate_graphs(self, tcommlist):
        """Generate graphs for each time step.

        :return: list of timesteps and corresponding graphs
        :rtype: tuple
        """
        LOGGER.info("Generating snapshot graphs")
        return self.edge_generator.create_graphs(tcommlist)

    def generate_events(self, tcommlist):
        """Generate groundtruth events from tcommlist.

        Event types are the following:

        * birth
        * continuation
        * death

        :param tcommlist:
        :return: groundtruth events
        """
        return generate_groundtruth_events(tcommlist)

    def generate(self) -> Groundtruth:
        """Generate complete benchmark.

        :return: groundtruth
        """
        tcommlist = self.generate_clusters(self.generate_communities())
        graphs = self.generate_graphs(tcommlist)
        events = self.generate_events(tcommlist)
        return Groundtruth(tcommlist, graphs, events)

    def _copy_kwargs(self) -> Dict:
        """Return kwargs for constructing a copy.

        :return:
        """
        return {
            "community_generator": self.community_generator.copy(),
            "node_generator": self.node_generator.copy(),
            "edge_generator": self.edge_generator.copy(),
            "seed": SeedSequence(
                entropy=self.seed.entropy,
                spawn_key=self.seed.spawn_key,
                pool_size=self.seed.pool_size,
                n_children_spawned=self.seed.n_children_spawned - 3,
            ),
        }


class ProgressiveGroundtruthGenerator(GroundtruthGenerator):
    """This class defines a complete benchmark generator.

    Its particularity is to integrate a progress bar from package
    `alive-progress` and display the progress of each step.

    :param community_generator:
        community flow graph generator, :class:`CommunitiesGenerator` with
        default arguments if not provided
    :param node_generator:
        membership generator, new :class:`RandomMemberGenerator` instance
        if not provided
    :param edge_generator:
        snapshot network graphs generator, :class:`BPAM` with default
        arguments if not provided
    :param seed:

    .. note::
        * `seed` attributes of each step generator will be replaced by a new
          one spwaned from :attr:`seed`.
        * if the `alive-progress` package is not installed, this generator is
          no different from :class:`GroundtruthGenerator`.
    """

    def generate_communities(self):
        """Generate evolving communities.

        :return: evolving communities
        :rtype: dyn.core.community_graphs.EvolvingCommunity
        """
        gen = self.community_generator

        bar = alive_it(
            gen.create_communities_generator(),
            title="Communities",
            force_tty=True,
        )
        for _ in bar:
            pass

        bar = alive_it(
            gen.create_intra_community_migrations_generator(),
            title="Intra Community Migrations",
            force_tty=True,
        )
        for _ in bar:
            pass

        bar = alive_it(
            gen.create_inter_community_migrations_generator(),
            title="Inter Community Migrations",
            force_tty=True,
        )
        for _ in bar:
            pass
        return gen.graph

    def generate_clusters(self, communities):
        """Generate clusters of members for each time step.

        :return: list of the clusters for each time step as a tcommlist
        :rtype: dyn.core.communities.Tcommlist
        """
        bar = alive_it(
            self.node_generator.create_tcommlist_rows_generator(communities),
            title="Membership",
            force_tty=True,
        )
        return Tcommlist([row for row in bar])

    def generate_graphs(self, tcommlist):
        """Generate graphs for each time step.

        :return: list of timesteps and corresponding graphs
        :rtype: tuple
        """
        return dict(
            iter(
                alive_it(
                    self.edge_generator.create_graphs_generator(tcommlist),
                    title="Static Graphs",
                    force_tty=True,
                )
            )
        )

    def generate_events(self, tcommlist):
        """Generate groundtruth events from tcommlist.

        Event types are the following:

        * birth
        * continuation
        * death

        :param tcommlist:
        :return: groundtruth events
        """
        bar = alive_it(
            generate_groundtruth_events(tcommlist),
            title="Events",
            force_tty=True,
        )
        return sorted(iter(bar), key=lambda e: (e.time, e.evolving_community))
