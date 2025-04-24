"""This module implements various types of graphs that can be used to represent
evolving communities.
"""
import sys
from typing import Any, Dict, Tuple

import networkx as nx

if sys.version_info >= (3, 11):  # pragma: nocover
    from typing import Self
else:
    from typing_extensions import Self

__all__ = ["EvolvingCommunitiesGraph"]


class Graph(nx.DiGraph):
    """This class is a wrapper of :class:`nx.DiGraph`.

    It simply adds a class method to create a `Graph` from a
    :class:`nx.DiGraph`, so it is shared among all its derived classes.
    """

    @classmethod
    def from_graph(cls, graph):
        """Create class instance from provided graph.

        :param graph:
        :type graph: nx.DiGraph
        :return: graph with new class
        """
        res = cls()
        res.graph.update(graph.graph)
        for node in graph.nodes:
            res.add_node(node, **graph.nodes[node])
        for n1, n2 in graph.edges:
            res.add_edge(n1, n2, **graph.edges[n1, n2])
        return res

    def __eq__(self, other: object) -> bool:
        """Check object is equal to another.

        :param other:
        :raises TypeError: if `other` is not a :class:`Graph`
        :return:
        """
        if not isinstance(other, Graph):
            raise TypeError(f"cannot compare {type(self)} with {type(other)}")
        if set(self.nodes) != set(other.nodes):
            return False
        if set(self.edges) != set(other.edges):
            return False
        for n in self.nodes:
            if self.nodes[n] != other.nodes[n]:
                return False
        for u, v in self.edges:
            if self.edges[u, v] != other.edges[u, v]:
                return False
        return True

    def copy(self, **kwargs) -> Self:
        """Return deep copy of the graph.

        :return:
        """
        res = self.__class__()
        for node, data in self.nodes(data=True):
            res.add_node(node, **data)
        for u, v, data in self.edges(data=True):
            res.add_edge(u, v, **data)
        return res


class SizeGraph(Graph):
    """This class is a simple graph which nodes have a size.

    This size is represented by a node attribute: `nbMembers`.
    """

    def add_node(self, node, nbMembers=0, **attr):
        """Add node to the graph.

        :param node:
        :param nbMembers: size of the node
        :type nbMembers: int | float
        :param attr: other attributes in a dict-like structure
        """
        super().add_node(node, nbMembers=nbMembers, **attr)

    def node_size(self, node):
        """Return size of node.

        :param node:
        :return:
        :rtype: int | float
        """
        return self.nodes[node]["nbMembers"]


class FlowGraph(Graph):
    """This class implements a flow graph.

    Each edge of the graph have a numeric attribute `flow`.
    """

    def flow(self, n1: Any, n2: Any) -> float:
        """Return flow between source and target node.

        :param n1: source node
        :param n2: target node
        """
        return 0 if (n1, n2) not in self.edges else self.edges[n1, n2]["flow"]

    @property
    def flows(self) -> Dict[Tuple[Any, Any], float]:
        """Return dictionary of all flows indexed by edge."""
        return {(u, v): f for u, v, f in self.edges.data("flow")}

    def node_out_flow(self, node):
        """Return output flow of given node.

        This is the sum of the flows of all output edges of the node.

        :param node:
        :return:
        :rtype: int | float
        """
        return sum(self.edges[e]["flow"] for e in self.out_edges(node))

    def node_in_flow(self, node):
        """Return input flow of given node.

        This is the sum of the flows of all input edges of the node.

        :param node:
        :return:
        :rtype: int | float
        """
        return sum(self.edges[e]["flow"] for e in self.in_edges(node))

    def node_out_flows(self, node):
        """Return the list of output flows for a given node

        :param node:
        :return:
        :rtype: int | float
        """
        return [self.edges[e]["flow"] for e in self.out_edges(node)]

    def node_in_flows(self, node):
        """Return the list of intput flows for a given node

        :param node:
        :return:
        :rtype: int | float
        """
        return [self.edges[e]["flow"] for e in self.in_edges(node)]

    def add_edge(self, n1, n2, flow=0, **attr):
        """Add edge between two nodes.

        :param n1: source node
        :param n2: target node
        :param flow:
        :type flow: int | float
        :param attr: other attributes in dict-like structure

        .. note:: if edge already exists, `flow` is added to its flow
        """
        if (n1, n2) in self.edges:
            self.edges[n1, n2]["flow"] += flow
            return
        super().add_edge(n1, n2, flow=flow, **attr)


class TimeGraph(Graph):
    """This class implements a graph where each node has a snapshot attribute.

    This snapshot attribute is represented by a node attribute `t`.
    """

    def __init__(self, **attr):
        super().__init__(**attr)
        self._snapshot_nodes = {}

    @property
    def snapshots(self):
        return sorted(self._snapshot_nodes.keys())

    @property
    def max_snapshot(self):
        return max(self._snapshot_nodes.keys())

    def node_snapshot(self, node):
        """Return snapshot of the given node.

        :param node:
        :return:
        :rtype: int
        """
        return self.nodes[node]["t"]

    def snapshot_nodes(self, t):
        """Return nodes at given snapshot.

        :param t:
        :return:
        """
        return self._snapshot_nodes.get(t, set())

    def add_node(self, node, t=0, **attr):
        """Add node to the graph.

        :param node:
        :param t: snapshot of the node
        :type t: int
        :param attr: other attributes in a dict-like structure
        :raise IndexError: if `node` already in the graph
        :raise ValueError: if `t` is strictly negative
        """
        if node in self.nodes:
            raise IndexError(f"node is already in the graph: {node}")
        if t < 0:
            raise ValueError(f"snapshot t must be positive, got {t}")
        super().add_node(node, t=t, **attr)
        if t not in self._snapshot_nodes:
            self._snapshot_nodes[t] = set()
        self._snapshot_nodes[t].add(node)

    def add_edge(self, n1, n2, **attr):
        """Add edge between two nodes.

        :param n1: source node
        :param n2: target node
        :param attr: other attributes in dict-like structure
        :raise IndexError: if `n1` is not in the graph
        :raise ValueError: if `n2` is not on the successive snapshot of `n1`

        .. note::
            if `n2` does not exist, it is created on successive snapshot
            beforehand
        """
        if n1 not in self.nodes:
            raise IndexError(f"origin node is not in graph: {n1}")
        if n2 not in self.nodes:
            self.add_node(n2, t=self.node_snapshot(n1) + 1)
        elif self.node_snapshot(n2) != self.node_snapshot(n1) + 1:
            raise ValueError(
                "cannot add edge between non-consecutive snapshots: "
                f"{self.node_snapshot(n1)}, {self.node_snapshot(n2)}"
            )
        super().add_edge(n1, n2, **attr)


class CommunityGraph(Graph):
    """This class implements a graph where each node belongs to a community.

    This community is represented by a node attribute `evolvingCommunity`.
    """

    def __init__(self, **attr):
        super().__init__(**attr)
        self._community_nodes = {}

    @property
    def communities(self):
        return [*self._community_nodes.keys()]

    def node_community(self, node):
        """Return the community of a node.

        :param node:
        :return:
        """
        return self.nodes[node]["evolvingCommunity"]

    def community_nodes(self, evolvingCommunity):
        """Return nodes with given evolving community.

        :param evolvingCommunity:
        :return:
        """
        return self._community_nodes.get(evolvingCommunity, set())

    def add_node(self, node, evolvingCommunity=None, **attr):
        """Add node to the graph.

        :param node:
        :param evolvingCommunity:
        :param attr: other attributes in a dict-like structure
        """
        super().add_node(node, evolvingCommunity=evolvingCommunity, **attr)
        if evolvingCommunity not in self._community_nodes:
            self._community_nodes[evolvingCommunity] = set()
        self._community_nodes[evolvingCommunity].add(node)


class EvolvingCommunitiesGraph(
    SizeGraph, FlowGraph, TimeGraph, CommunityGraph
):
    def add_node(self, node, t=0, evolvingCommunity=None, nbMembers=0, **attr):
        """Add node to the graph.

        :param node:
        :param t: snapshot of the node
        :type t: int
        :param evolvingCommunity:
        :param nbMembers: size of node
        :param attr: other attributes in a dict-like structure
        """
        nodes = (
            []
            if evolvingCommunity not in self.communities
            else self.community_nodes(evolvingCommunity)
        )
        for n in nodes:
            if self.node_snapshot(n) == t:
                raise ValueError(
                    f"an other node={n} of community '{evolvingCommunity}' "
                    f"already exists at snapshot {t}"
                )
        super().add_node(
            node,
            t=t,
            evolvingCommunity=evolvingCommunity,
            nbMembers=nbMembers,
            **attr,
        )

    def add_edge(self, n1, n2, flow: float = 0, **attr):
        """Add edge between two nodes.

        :param n1: source node
        :param n2: target node
        :param flow:
        :param attr: other attributes in dict-like structure
        """
        super().add_edge(n1, n2, flow=flow, **attr)

    def get_node(self, evolvingCommunity=None, t=0):
        """Return node of given evolving community at given snapshot.

        :param evolvingCommunity: community
        :param t: snapshot
        :type t: int
        :return:
        """
        try:
            data = set.intersection(
                self.community_nodes(evolvingCommunity), self.snapshot_nodes(t)
            )
            return data.pop()
        except IndexError:
            return None
        except KeyError:
            return None

    def predecessor(self, n: Any) -> Any:
        """Return community predecessor of node.

        :param n:
        :return: predecessor if existing, else ``None``
        """
        return self.get_node(self.node_community(n), self.node_snapshot(n) - 1)

    def successor(self, n: Any) -> Any:
        """Return community successor of node

        :param n:
        :return: successor if existing, else ``None``
        """
        return self.get_node(self.node_community(n), self.node_snapshot(n) + 1)

    def get_begin_end_snapshot(self, evolvingCommunity):
        """Return start snapshot of given evolving community"""

        time_list = [
            self.nodes[node]["t"]
            for node in self.community_nodes(evolvingCommunity)
        ]

        begin = min(t for t in time_list)
        end = max(t for t in time_list)

        return begin, end
