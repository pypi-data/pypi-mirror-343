"""This module generates members and assign them to punctual communities.
"""
from __future__ import annotations

import logging
import pathlib
from typing import Any
from typing import Generator as Gen
from typing import cast

from dyn.core.communities import Member, Membership, Tcommlist, TcommlistRow
from dyn.core.community_graphs import EvolvingCommunitiesGraph
from dyn.core.files_io import save_commlist, save_tcommlist

from dyn.benchmark.generator._interfaces import GeneratorLen, IGenerator

LOGGER = logging.getLogger(__name__)


class CommunityMember(Member):
    """Class representing a community member.

    :param id_:
    :param coreness: tendancy of the member to join already visited communities
    :type coreness: float
    :param intermittence: tendency of the member to stay out of the network
    :type intermittence: float

    :attr id:
    """

    def __init__(self, id_, coreness=0, intermittence=0):
        super().__init__(id_=id_)
        self.coreness = coreness
        self.intermittence = intermittence


class NodeMembership(Membership):
    """This class gathers evolving and static communities along their members
    and ensures their coherency.

    It uses :class:`CommunityMember` as the class for its members.

    :attr evolving_communities: evolving communities with ids as keys
    :attr static_communities: static communities with ids as keys
    :attr members: members with ids as keys

    .. warning::
        This class ensures coherency of data as long as you only modify them
        through its methods!
    """

    def add_member(self, member_id) -> CommunityMember:
        """Create and add member by id if not present.

        :param member_id:
        :return: member with given id
        """
        if member_id not in self.members:
            self.members[member_id] = CommunityMember(member_id)
        return cast(CommunityMember, self.members[member_id])


class RandomMemberGenerator(IGenerator):
    """This class generate random members following a provided community flow
    graph.

    :param seed:

    :attr community_graph: latest community flow graph provided
    :attr membership: latest community membership object built by generator
    """

    def __init__(self, seed: Any = None):
        self.community_graph = EvolvingCommunitiesGraph()
        self.membership = NodeMembership()
        super().__init__(seed=seed)

    def create_member(self) -> CommunityMember:
        """Create one member"""
        return self.membership.add_member(len(self.membership.members))

    def _create_tcommlist_rows_generator(
        self, community_graph: EvolvingCommunitiesGraph = None
    ) -> Gen[TcommlistRow]:
        """Return membership as tcommlist rows basic generator.

        :param community_graph:
        :yield: tcommlist row
        """
        if community_graph is not None:
            self.community_graph = community_graph
        self.membership = NodeMembership.from_community_graph(
            self.community_graph
        )

        for t in self.community_graph.snapshots:
            assigned = set()
            for node in sorted(self.community_graph.snapshot_nodes(t)):
                eid = self.membership.static_communities[
                    node
                ].evolving_community.id
                for node_from, _ in sorted(
                    self.community_graph.in_edges(node), key=lambda k: k[0]
                ):
                    flow = self.community_graph.flow(node_from, node)
                    available = (
                        self.membership.static_communities[node_from].members
                        - assigned
                    )
                    candidates = sorted(available, key=lambda m: m.id)
                    self.rng.shuffle(candidates)
                    members = set(candidates[:flow])
                    for m in candidates[:flow]:
                        self.membership.attach_member(m.id, node)
                        yield TcommlistRow(m.id, eid, t)
                    assigned = assigned.union(members)
                growth = self.community_graph.node_size(node) - len(
                    self.membership.static_communities[node].members
                )
                if growth > 0:
                    members = [self.create_member() for _ in range(growth)]
                    for m in members:
                        self.membership.attach_member(m.id, node)
                        yield TcommlistRow(m.id, eid, t)
                    assigned = assigned.union(set(members))

    def create_tcommlist_rows_generator(
        self, community_graph: EvolvingCommunitiesGraph = None
    ) -> GeneratorLen[TcommlistRow]:
        """Return membership as tcommlist rows generator.

        :param community_graph:
        :return:
        """
        total_size = sum(
            community_graph.node_size(node) for node in community_graph.nodes
        )

        return GeneratorLen(
            self._create_tcommlist_rows_generator(community_graph), total_size
        )

    def generate(
        self, community_graph: EvolvingCommunitiesGraph = None
    ) -> Tcommlist:
        """Generate clusters of members corresponding to `community_graph`
        attribute.

        :param community_graph: if not provided, will use last one provided
        :return: generated tcommlist
        """
        return Tcommlist(
            [
                row
                for row in self.create_tcommlist_rows_generator(
                    community_graph
                )
            ]
        )

    def write_tcommlist(self, filename):
        """Write the benchmark to a tcommlist file.

        :param filename:
        :type filename: str
        """
        save_tcommlist(self.membership.tcommlist, filename)

    def write_commlist(self, directory):
        """Write the benchmark to commlist files, one per snapshot.

        There are one commlist file per timestep, with the following filename
        format: `directory`/`timestep`.commlist

        :param directory:
        :type directory: str
        """
        try:
            # create output dir
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

            # for each snapshot
            for (
                t,
                commlist,
            ) in self.membership.tcommlist.commlists.items():
                filename = directory + "/" + str(t) + ".commlist"
                save_commlist(commlist, filename)
        except Exception:
            LOGGER.error("Invalid output directory " + directory)
