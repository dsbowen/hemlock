"""Navigation display.

Displays possible user navigation through a tree.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import networkx as nx

Y_INCREMENT = 0.015

DEFAULT_NODE_COLOR = "#cfe2ff"
CURRENT_NODE_COLOR = "#d1e7dd"
TERMINAL_NODE_COLOR = "#f8d7da"

DEFAULT_EDGE_COLOR = "#b6d4fe"
CURRENT_EDGE_COLOR = "#badbcc"
TERMINAL_EDGE_COLOR = "#f5c2c7"

EdgeType = Tuple["hemlock.page.Page", "hemlock.page.Page"]  # type: ignore
# tuple of (list of edges), connection style (str)
EdgelistType = Tuple[List[EdgeType], str]


class Node:
    """Node of the navigation graph.

    Args:
        page (hemlock.page.Page): Page represented by this node.
        pos (Tuple[float, float]): Position of the node in graph.

    Attributes:
        page (hemlock.page.Page): Page represented by this node.
        pos (Tuple[float, float]): Position of the node in graph.
        children (List[Node]): Nodes to which the user can navigate from this node.
        color (str): Color of this node.
        edgecolor (str): Color of the edge of this node.
        subgraph (Graph): Graph representing this page's branch.
    """

    def __init__(
        self, page: "hemlock.page.Page", pos: Tuple[float, float]  # type: ignore
    ):
        self.page = page
        self.children: List[Node] = []
        self.pos = pos

        self.color = DEFAULT_NODE_COLOR
        if page.is_last_page:
            self.color = TERMINAL_NODE_COLOR

        self.edgecolor = DEFAULT_EDGE_COLOR
        if page.is_last_page:
            self.edgecolor = TERMINAL_EDGE_COLOR

        if page.branch:
            self.subgraph = Graph(page.branch, self)
        else:
            self.subgraph = None  # type: ignore

    def __len__(self):
        return 1 + (0 if self.subgraph is None else len(self.subgraph))

    def connect(self, prev_node: Node) -> None:
        """Draw a connection from the prev_node to this node.

        Args:
            prev_node (Node): Node to connect.
        """
        if prev_node.subgraph is None:
            if prev_node.page.forward and prev_node.page.next_page is None:
                prev_node.children.append(self)
            if self.page.back and self.page.prev_page is None:
                self.children.append(prev_node)
        else:
            self.connect(prev_node.subgraph.nodes[-1])

    def get_attributes(self) -> Dict[str, Any]:
        """Get attributes of this node and its subgraph.

        Returns:
            Dict[str, Any]: Attributes.
        """
        attrs = dict(
            nodes=[self.page],
            labels={self.page: self.page.get_position()},
            pos={self.page: self.pos},
            node_color=[self.color],
            edgecolors=[self.edgecolor],
            edges=[(self.page, child.page) for child in self.children],
        )
        if self.subgraph is not None:
            for key, value in self.subgraph.get_attributes().items():
                if key in ("labels", "pos"):
                    attrs[key].update(value)  # type: ignore
                else:
                    attrs[key] += value

        return attrs


class Graph:
    """Graph representing a branch.

    Args:
        branch (hemlock.branch.Branch): Branch represented by this graph.
        origin_node (Node, optional): Root node for this branch. Defaults to None.

    Attributes:
        branch (hemlock.branch.Branch): Branch represented by this graph.
        nodes (List[Node]): Nodes representing the pages of this branch.
    """

    def __init__(
        self, branch: "hemlock.branch.Branch", origin_node: Node = None  # type: ignore
    ):
        self.branch = branch
        self.nodes: List[Node] = []

        start_x, start_y = 0.0, 0.0
        if origin_node is not None:
            start_x = origin_node.pos[0] + 1
            start_y = origin_node.pos[1] + Y_INCREMENT

        i = 0
        for page in branch:
            node = Node(page, (start_x + i, start_y))
            i += len(node)
            if self.nodes:
                node.connect(self.nodes[-1])
            self.nodes.append(node)

        if origin_node is not None:
            if origin_node.page.forward:
                origin_node.children.append(self.nodes[0])
            if branch[0].back:
                self.nodes[0].children.append(origin_node)

    def __len__(self):
        return sum([len(node) for node in self.nodes])

    def get_attributes(self) -> Dict[str, Any]:
        """Get attributes of this graph's nodes and their subgraphs.

        Returns:
            Dict[str, Any]: Attributes.
        """
        attrs: Dict[str, Any] = dict(
            nodes=[],
            labels={},
            pos={},
            node_color=[],
            edgecolors=[],
            edges=[],
        )
        for node in self.nodes:
            for key, value in node.get_attributes().items():
                if key in ("labels", "pos"):
                    attrs[key].update(value)  # type: ignore
                else:
                    attrs[key] += value

        return attrs


def make_digraph(
    tree: "hemlock.tree.Tree",  # type: ignore
) -> Tuple[
    nx.classes.digraph.DiGraph, Dict[str, Any], Tuple[EdgelistType, EdgelistType]
]:
    """Create a networkx digraph based on a tree.

    Args:
        tree (hemlock.tree.Tree): Tree to represent as a graph.

    Returns:
        Tuple[
            nx.classes.digraph.DiGraph,
            Dict[str, Any],
            Tuple[EdgelistType, EdgelistType]
        ]: Digraph, graph attributes, tuple of straight and curved edges.
    """
    graph = Graph(tree.branch)
    attrs = graph.get_attributes()
    for i, page in enumerate(attrs["nodes"]):
        if page is tree.page:
            attrs["node_color"][i] = CURRENT_NODE_COLOR
            if not page.is_last_page:
                attrs["edgecolors"][i] = CURRENT_EDGE_COLOR

    curved_edges = []
    for page in attrs["nodes"]:
        if page.forward and page.next_page is not None:
            curved_edges.append((page, page.next_page))

        if page.back and page.prev_page is not None:
            curved_edges.append((page, page.prev_page))

    edgelist_connectionstyle = (
        (attrs["edges"], "arc3"),
        (curved_edges, "arc3,rad=-.4"),
    )

    nx_graph = nx.DiGraph()
    nx_graph.add_nodes_from(attrs["nodes"])
    nx_graph.add_edges_from(attrs["edges"] + curved_edges)

    return nx_graph, attrs, edgelist_connectionstyle


def display_navigation(
    tree: "hemlock.tree.Tree",  # type: ignore
    ax=None,
    node_size: int = 1200,
    **subplots_kwargs: Any
):
    """Display the navigation graph of a given tree.

    Args:
        tree (hemlock.tree.Tree): Tree to display.
        ax (AxesSubplot): Axis on which to draw the graph.
        node_size (int, optional): Size of the nodes in the graph. Defaults to 1200.

    Returns:
        AxesSubplot: Graph.
    """
    if ax is None:
        _, ax = plt.subplots(**subplots_kwargs)
        ax.set_facecolor("whitesmoke")

    nx_graph, attrs, edgelist_connectionstyle = make_digraph(tree)
    nx.draw_networkx_nodes(
        nx_graph,
        attrs["pos"],
        ax=ax,
        node_color=attrs["node_color"],
        edgecolors=attrs["edgecolors"],
        linewidths=3,
        node_size=node_size,
    )
    for edgelist, connectionstyle in edgelist_connectionstyle:
        nx.draw_networkx_edges(
            nx_graph,
            attrs["pos"],
            edgelist=edgelist,
            connectionstyle=connectionstyle,
            ax=ax,
            arrowsize=20,
            node_size=node_size,
        )
    nx.draw_networkx_labels(nx_graph, attrs["pos"], ax=ax, labels=attrs["labels"])

    return ax
