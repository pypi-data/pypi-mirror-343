from __future__ import annotations

from typing import Any, Dict

from networkx import Graph


class Member:
    id: Any
    graphs: Dict[Any, SnapshotGraph]


class StaticCommunity:
    id: Any
    snapshot: int
    evolving_community: EvolvingCommunity
    snapshot_graph: SnapshotGraph


class EvolvingCommunity:
    id: Any
    static_communities: Dict[int, StaticCommunity]


class SnapshotGraph:
    t: int
    graph: Graph


class TemporalNetwork:
    members: Dict[Any, Member]
    static_communities: Dict[Any, StaticCommunity]
    evolving_communities: Dict[Any, EvolvingCommunity]
    snapshot_graphs: Dict[int, SnapshotGraph]
