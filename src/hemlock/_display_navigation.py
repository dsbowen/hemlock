import matplotlib.pyplot as plt
import networkx as nx

Y_INCREMENT = 0.015

DEFAULT_NODE_COLOR = "#cfe2ff"
CURRENT_NODE_COLOR = "#d1e7dd"
TERMINAL_NODE_COLOR = "#f8d7da"

DEFAULT_EDGE_COLOR = "#b6d4fe"
CURRENT_EDGE_COLOR = "#badbcc"
TERMINAL_EDGE_COLOR = "#f5c2c7"


class Node:
    def __init__(self, page, pos):
        self.page = page
        self.children = []
        self.pos = pos

        self.color = DEFAULT_NODE_COLOR
        if page.terminal:
            self.color = TERMINAL_NODE_COLOR

        self.edgecolor = DEFAULT_EDGE_COLOR
        if page.terminal:
            self.edgecolor = TERMINAL_EDGE_COLOR

        if page.branch:
            self.subgraph = Graph(page.branch, self)
        else:
            self.subgraph = None

    def __len__(self):
        return 1 + (0 if self.subgraph is None else len(self.subgraph))

    def connect(self, prev_node):
        if prev_node.subgraph is None:
            if prev_node.page.forward and prev_node.page.next_page is None:
                prev_node.children.append(self)
            if self.page.back and self.page.prev_page is None:
                self.children.append(prev_node)
        else:
            self.connect(prev_node.subgraph.nodes[-1])

    def get_attributes(self):
        indices = []
        page = self.page
        while page is not None:
            indices.append(str(page.index))
            page = page.root
        indices.reverse()
        label = ".".join(indices)

        attrs = dict(
            pages=[self.page],
            nodes=[self.page.hash],
            labels={self.page.hash: label},
            pos={self.page.hash: self.pos},
            node_color=[self.color],
            edgecolors=[self.edgecolor],
            edges=[(self.page.hash, child.page.hash) for child in self.children],
        )
        if self.subgraph is not None:
            for key, value in self.subgraph.get_attributes().items():
                if key in ("labels", "pos"):
                    attrs[key].update(value)
                else:
                    attrs[key] += value

        return attrs


class Graph:
    def __init__(self, branch, origin_node=None):
        self.branch = branch
        self.nodes = []

        start_x, start_y = 0, 0
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

    def get_attributes(self):
        attrs = dict(
            pages=[],
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
                    attrs[key].update(value)
                else:
                    attrs[key] += value

        return attrs


def display_navigation(tree, node_size=1200, **subplots_kwargs):
    graph = Graph(tree.branch)
    attrs = graph.get_attributes()
    for i, page in enumerate(attrs["pages"]):
        if page is tree.page:
            attrs["node_color"][i] = CURRENT_NODE_COLOR
            if not page.terminal:
                attrs["edgecolors"][i] = CURRENT_EDGE_COLOR

    # TODO: account for next_page going to a page that came before and prev_page going to a page that comes after
    positive_rad_edges, negative_rad_edges = [], []
    for page in attrs["pages"]:
        if page.forward and page.next_page is not None:
            edge = (page.hash, page.next_page.hash)
            if page.branch.id <= page.next_page.branch.id:
                negative_rad_edges.append(edge)
            else:
                positive_rad_edges.append(edge)

        if page.back and page.prev_page is not None:
            edge = (page.hash, page.prev_page.hash)
            if page.branch.id >= page.prev_page.branch.id:
                negative_rad_edges.append(edge)
            else:
                positive_rad_edges.append(edge)

    edgelist_connectionstyle = (
        (attrs["edges"], "arc3"),
        (positive_rad_edges, "arc3,rad=.4"),
        (negative_rad_edges, "arc3,rad=-.4"),
    )

    G = nx.DiGraph()
    G.add_nodes_from(attrs["nodes"])
    G.add_edges_from(attrs["edges"] + positive_rad_edges + negative_rad_edges)

    fig, ax = plt.subplots(**subplots_kwargs)
    nx.draw_networkx_nodes(
        G,
        attrs["pos"],
        ax=ax,
        node_color=attrs["node_color"],
        edgecolors=attrs["edgecolors"],
        linewidths=3,
        node_size=node_size,
    )
    for edgelist, connectionstyle in edgelist_connectionstyle:
        nx.draw_networkx_edges(
            G,
            attrs["pos"],
            edgelist=edgelist,
            connectionstyle=connectionstyle,
            ax=ax,
            arrowsize=20,
            node_size=node_size,
        )
    nx.draw_networkx_labels(G, attrs["pos"], ax=ax, labels=attrs["labels"])
    ax.set_facecolor("whitesmoke")

    return ax
