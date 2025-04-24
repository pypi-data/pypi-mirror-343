from dataclasses import dataclass
from typing import List

from dyn.core.communities import Membership, Tcommlist

from dyn.benchmark.generator._interfaces import GeneratorLen


@dataclass
class Event:
    time: int
    static_community: str
    evolving_community: str
    label: str


def create_groundtruth_events_generator(
    tcommlist: Tcommlist,
) -> GeneratorLen[Event]:
    """Return groundtruth events generator from tcommlist.

    Event types are the following:

    * birth
    * continuation
    * death

    :param tcommlist:
    :return: groundtruth events generator
    """
    community_graph = Membership.from_tcommlist(tcommlist).community_graph

    def gen(community_graph):
        for community in community_graph.communities:
            nodes = list(community_graph.community_nodes(community))
            snapshots = [community_graph.node_snapshot(n) for n in nodes]
            ordered = sorted(zip(nodes, snapshots), key=lambda k: k[1])
            yield Event(ordered[0][1], ordered[0][0], community, "birth")
            for node, t in ordered[1:-1]:
                yield Event(t, node, community, "continuation")
            yield Event(ordered[-1][1], ordered[-1][0], community, "death")

    return GeneratorLen(gen(community_graph), len(community_graph.nodes))


def generate_groundtruth_events(
    tcommlist: Tcommlist,
) -> List[Event]:
    """Generate groundtruth events from tcommlist.

    Event types are the following:

    * birth
    * continuation
    * death

    :param tcommlist:
    :return: groundtruth events
    """
    return sorted(
        iter(create_groundtruth_events_generator(tcommlist)),
        key=lambda e: (e.time, e.evolving_community),
    )
