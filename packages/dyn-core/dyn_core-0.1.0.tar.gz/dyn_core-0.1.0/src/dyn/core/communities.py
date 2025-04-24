"""This module defines structures for handling members, static and evolving
communities.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Set

from pandas import DataFrame

from .community_graphs import EvolvingCommunitiesGraph

__all__ = ["TcommlistRow", "Tcommlist"]


@dataclass
class TcommlistRow:
    """This class defines a single row in Tcommlist format."""

    node_id: Any
    evolving_community_id: Any
    snapshot: int

    def __post_init__(self):
        self.snapshot = int(self.snapshot)

    @property
    def static_community_id(self) -> str:
        return f"{self.evolving_community_id}.{self.snapshot}"


class Tcommlist:
    """This class defines the Tcommlist format.

    :param data:
    """

    def __init__(self, data: List[TcommlistRow] | DataFrame = None):
        self._data: List[TcommlistRow] = (
            []
            if data is None
            else (
                list(TcommlistRow(*row) for row in data.values.tolist())
                if isinstance(data, DataFrame)
                else data
            )
        )

    def append(self, row: TcommlistRow):
        """Append a single row to Tcommlist.

        :param row:
        :raises TypeError: if `row` type is not a :class:`TcommlistRow`
        """
        if isinstance(row, TcommlistRow):
            self._data.append(row)
            return
        raise TypeError(f"unsupported type {type(row)}")

    def __add__(self, other: Tcommlist | TcommlistRow) -> Tcommlist:
        """Add either a single row or a whole Tcommlist object to current one.

        :param other: single row or whole Tcommlist object
        :raises TypeError:
            if `other` type is not :class:`Tcommlist` | :class:`TcommlistRow`
        :return: resulting Tcommlist object
        """
        if isinstance(other, TcommlistRow):
            return Tcommlist(self._data + [other])
        if isinstance(other, Tcommlist):
            return Tcommlist(self._data + other._data)
        raise TypeError(f"unsupported type {type(other)}")

    def __iter__(self) -> Iterator[TcommlistRow]:
        """Iterate over rows.

        :return: rows iterator
        :yield: single Tcommlist row
        """
        return iter(self._data)

    def __eq__(self, other: object) -> bool:
        """Check object is equal to another.

        :param other:
        :raises TypeError: if `other` is not a :class:`Tcommlist`
        :return:
        """
        if not isinstance(other, Tcommlist):
            raise TypeError(f"cannot compare {type(self)} with {type(other)}")
        return self._data == other._data

    def commlist(self, snapshot: int) -> Tcommlist:
        """Return commlist at given snapshot.

        :param snapshot:
        :return: commlist
        """
        return Tcommlist([row for row in self if row.snapshot == snapshot])

    @property
    def commlists(self) -> Dict[int, Tcommlist]:
        """Return commlists as a dictionary.

        :return: commlists

        .. note:: This is as fast as calling :method:`commlist` once.
        """
        res: Dict[int, "Tcommlist"] = {}
        for row in self._data:
            if row.snapshot not in res:
                res[row.snapshot] = Tcommlist()
            res[row.snapshot] += row
        return res

    @property
    def community_flow_graph(self) -> EvolvingCommunitiesGraph:
        """Return community flow graph.

        :return:
        """
        return Membership.from_tcommlist(self).community_graph

    def sort(self) -> Tcommlist:
        """Sort Tcommlist.

        Sorting is done by following rules (in decreasing priority):
            * `snapshot` (ascending order)
            * `evolving_community_id` (ascending order)
            * `node_id`

        :return: sorted Tcommlist

        .. note:: A new Tcommlist object is returned (original is not modified)
        """
        self._data.sort(
            key=lambda row: (
                row.snapshot,
                row.evolving_community_id,
                row.node_id,
            )
        )
        return self

    def drop_duplicates(self) -> Tcommlist:
        """Remove duplicated rows.

        :return: Tcommlist without duplicates

        .. note:: A new Tcommlist object is returned (original is not modified)
        """
        data = self._data
        self._data = []
        for row in data:
            if row not in self:
                self._data.append(row)
        return self

    def __repr__(self) -> str:
        """Return Tcommlist representation

        :return:
        """
        return f"Tcommlist({repr(self._data)})"


class Member:
    """This class defines a member.

    :param id_:
    :param static_communities: static communities which member is part of

    :attr id:

    .. warning::
        This class only structures data, it doesn't contain the logical
        constraints that enables its coherency. Manipulate with caution.
        Please look at :class:`Membership` for a class that enables safe
        manipulation (through its methods only!).
    """

    def __init__(
        self, id_, static_communities: List["StaticCommunity"] = None
    ):
        static_communities = (
            [] if static_communities is None else static_communities
        )
        self.id = id_
        self.static_communities = {
            scomm.snapshot: scomm for scomm in static_communities
        }

    @property
    def snapshots(self) -> List[int]:
        """Return snapshots where member is present.

        :return:
        """
        return sorted(self.static_communities.keys())

    @property
    def evolving_communities(self) -> Dict[int, "EvolvingCommunity"]:
        """Return evolving communities which member is part of.

        :return: evolving communities as a dictionary with snapshots as keys
        """
        return {
            t: scomm.evolving_community
            for t, scomm in self.static_communities.items()
        }


class StaticCommunity:
    """This class represents a static community.

    :param id_:
    :param snapshot:
    :param members:
    :param evolving_community:

    :attr id:

    .. warning::
        This class only structures data, it doesn't contain the logical
        constraints that enables its coherency. Manipulate with caution.
        Please look at :class:`Membership` for a class that enables safe
        manipulation (through its methods only!).
    """

    def __init__(
        self,
        id_,
        snapshot: int,
        members: List[Member] = None,
        evolving_community: "EvolvingCommunity" = None,
    ):
        self.id = id_
        self.snapshot = snapshot
        self.members: Set[Member] = set() if members is None else set(members)
        self.evolving_community = evolving_community


class EvolvingCommunity:
    """This class represents an evolving community.

    :param id_:
    :param static_communities:

    :attr id:

    .. warning::
        This class only structures data, it doesn't contain the logical
        constraints that enables its coherency. Manipulate with caution.
        Please look at :class:`Membership` for a class that enables safe
        manipulation (through its methods only!).
    """

    def __init__(self, id_, static_communities: List[StaticCommunity] = None):
        static_communities = (
            [] if static_communities is None else static_communities
        )
        self.id = id_
        self.static_communities = {
            scomm.snapshot: scomm for scomm in static_communities
        }

    @property
    def members(self) -> List[Member]:
        """Return list of members at all snapshots.

        :return:
        """
        return sorted(
            set.union(
                *(scomm.members for scomm in self.static_communities.values())
            )
        )

    @property
    def snapshots(self) -> List[int]:
        """Return snapshots where evolving community exists.

        :return:
        """
        return sorted(self.static_communities.keys())


class Membership:
    """This class gathers evolving and static communities along their members
    and ensures their coherency.

    :attr evolving_communities: evolving communities with ids as keys
    :attr static_communities: static communities with ids as keys
    :attr members: members with ids as keys

    .. warning::
        This class ensures coherency of data as long as you only modify them
        through its methods!
    """

    def __init__(self):
        self.evolving_communities: Dict[Any, EvolvingCommunity] = {}
        self.static_communities: Dict[Any, StaticCommunity] = {}
        self.members: Dict[Any, Member] = {}
        self._snapshots: Set[int] = set()

    @property
    def snapshots(self) -> List[int]:
        """Return all existing snapshots.

        :return:
        """
        return sorted(self._snapshots)

    def add_member(self, member_id) -> Member:
        """Create and add member by id if not present.

        :param member_id:
        :return: member with given id
        """
        if member_id not in self.members:
            self.members[member_id] = Member(member_id)
        return self.members[member_id]

    def add_evolving_community(
        self, evolving_community_id
    ) -> EvolvingCommunity:
        """Create and add evolving community by id if not present.

        :param evolving_community_id:
        :return: evolving community with given id
        """
        if evolving_community_id not in self.evolving_communities:
            self.evolving_communities[
                evolving_community_id
            ] = EvolvingCommunity(evolving_community_id)
        return self.evolving_communities[evolving_community_id]

    def add_static_community(
        self, static_community_id, snapshot: int
    ) -> StaticCommunity:
        """Create and add static community by id if not present.

        :param static_community_id:
        :return: static community with given id
        """
        if static_community_id not in self.static_communities:
            self.static_communities[static_community_id] = StaticCommunity(
                static_community_id, snapshot
            )
            self._snapshots.add(snapshot)
        return self.static_communities[static_community_id]

    def attach_static_community(
        self, static_community_id, evolving_community_id
    ):
        """Attach static community to evolving community.

        :param static_community_id:
        :param evolving_community_id:
        :raises IndexError:
            * If `static_community_id` static community doesn't exist
            * If `evolving_community_id` static community doesn't exist
        :raises ValueError:
            If evolving community already exists at same snapshot
        """
        if static_community_id not in self.static_communities:
            raise IndexError(f"Unknown StaticCommunity {static_community_id}")
        scomm = self.static_communities[static_community_id]
        if evolving_community_id not in self.evolving_communities:
            raise IndexError(
                f"Unknown EvolvingCommunity {evolving_community_id}"
            )
        dcomm = self.evolving_communities[evolving_community_id]
        if scomm.snapshot not in dcomm.snapshots:
            scomm.evolving_community = dcomm
            dcomm.static_communities[scomm.snapshot] = scomm
        elif scomm != dcomm.static_communities[scomm.snapshot]:
            raise ValueError(
                f"EvolvingCommunity {dcomm.id} duplicated at snapshot "
                f"{scomm.snapshot}"
            )

    def detach_static_community(self, static_community_id):
        """Detach static community from its evolving community (by id).

        :param static_community_id:
        :raises IndexError:
            If `static_community_id` static community doesn't exist
        """
        if static_community_id not in self.static_communities:
            raise IndexError(f"Unknown StaticCommunity {static_community_id}")
        scomm = self.static_communities[static_community_id]

        if (
            scomm.evolving_community is not None
            and scomm.evolving_community.static_communities[scomm.snapshot]
            == scomm
        ):
            scomm.evolving_community.static_communities.pop(scomm.snapshot)
        scomm.evolving_community = None

    def attach_member(self, member_id, static_community_id):
        """Attach static community to evolving community.

        :param member_id:
        :param static_community_id:
        :raises IndexError:
            * If `member_id` member doesn't exist
            * If `static_community_id` static community doesn't exist
        :raises ValueError:
            If member is already in an other community at same snapshot
        """
        if static_community_id not in self.static_communities:
            raise IndexError(f"Unknown StaticCommunity {static_community_id}")
        scomm = self.static_communities[static_community_id]
        if member_id not in self.members:
            raise IndexError(f"Unknown Member {member_id}")
        member = self.members[member_id]
        if scomm.snapshot not in member.snapshots:
            member.static_communities[scomm.snapshot] = scomm
            scomm.members.add(member)
        elif scomm != member.static_communities[scomm.snapshot]:
            raise ValueError(
                f"Member {member.id} duplicated at snapshot {scomm.snapshot}"
            )

    def detach_member(self, member_id, snapshot: int):
        """Detach member from its static community at given snapshot (by id).

        :param member_id:
        :param snapshot:
        :raises IndexError: If `member_id` member doesn't exist
        """
        if member_id not in self.members:
            raise IndexError(f"Unknown Member {member_id}")
        member = self.members[member_id]
        if snapshot in member.snapshots:
            member.static_communities[snapshot].members.discard(member)
            member.static_communities.pop(snapshot)

    def _add_row(self, row: TcommlistRow):
        """Add a tcommlist row to data.

        :param row:

        .. note::
            this method is internal and only used in :meth:`from_tcommlist`
        """
        self.add_member(row.node_id)
        self.add_static_community(row.static_community_id, row.snapshot)
        self.add_evolving_community(row.evolving_community_id)
        self.attach_member(row.node_id, row.static_community_id)
        self.attach_static_community(
            row.static_community_id, row.evolving_community_id
        )

    @classmethod
    def _to_row(
        cls, member: Member, static_community: StaticCommunity
    ) -> TcommlistRow:
        """Create tcommlist row.

        :param member:
        :param static_community:
        :return: tcommlist row
        """
        return TcommlistRow(
            member.id,
            static_community.evolving_community.id,
            static_community.snapshot,
        )

    @property
    def tcommlist(self) -> Tcommlist:
        """Return tcommlist representing current data.

        :return:
        """
        res = []
        static_communities = sorted(
            self.static_communities.values(),
            key=lambda s: (s.snapshot, s.evolving_community.id),
        )
        for scomm in static_communities:
            for member in sorted(scomm.members, key=lambda m: m.id):
                res.append(self._to_row(member, scomm))
        return Tcommlist(res)

    def commlist(self, snapshot: int) -> Tcommlist:
        """Return commlist representing data at given snapshot.

        :param snapshot:
        :return:
        """
        return self.tcommlist.commlist(snapshot)

    @property
    def community_graph(self) -> EvolvingCommunitiesGraph:
        """Return community flow graph representing data.

        :return:
        """
        res = EvolvingCommunitiesGraph()
        static_communities = sorted(
            self.static_communities.values(),
            key=lambda s: (s.snapshot, s.evolving_community.id),
        )
        for scomm in static_communities:
            res.add_node(
                scomm.id,
                scomm.snapshot,
                evolvingCommunity=scomm.evolving_community.id,
                nbMembers=len(scomm.members),
            )
            for prev_sid in res.snapshot_nodes(scomm.snapshot - 1):
                flow = len(
                    self.static_communities[prev_sid].members.intersection(
                        scomm.members
                    )
                )
                if flow > 0:
                    res.add_edge(prev_sid, scomm.id, flow=flow)
        return res

    @classmethod
    def from_community_graph(
        cls, graph: EvolvingCommunitiesGraph
    ) -> "Membership":
        """Create membership object from community flow graph.

        As community flow graph is not as complete, only evolving and static
        communities are added (no members).

        :param graph:
        :return: membership object
        """
        res = cls()
        for sid in graph.nodes:
            did = graph.node_community(sid)
            res.add_evolving_community(did)
            res.add_static_community(sid, graph.node_snapshot(sid))
            res.attach_static_community(sid, did)
        return res

    @classmethod
    def from_tcommlist(cls, tcommlist_: Tcommlist) -> "Membership":
        """Create membership object from tcommlist.

        :param tcommlist_:
        :return: membership object
        """
        res = cls()
        for row in tcommlist_:
            res._add_row(row)
        return res
