from hemlock import Tree, Page
from hemlock._display_navigation import (
    Y_INCREMENT,
    DEFAULT_NODE_COLOR,
    CURRENT_NODE_COLOR,
    TERMINAL_NODE_COLOR,
    DEFAULT_EDGE_COLOR,
    CURRENT_EDGE_COLOR,
    TERMINAL_EDGE_COLOR,
    make_digraph,
    display_navigation,
)


class Mixin:
    def assert_correct_digraph(
        self, nodes, positions, node_colors, edge_colors, straight_edges, curved_edges
    ):
        # the arguments for this function are the expected values against which to
        # test the networkx graph, graph attributes, and edge lists
        nx_graph, attrs, edgelist_connectionstyle = make_digraph(self.tree)

        for edge in straight_edges + curved_edges:
            assert edge in nx_graph.edges

        for page in self.tree.branch:
            assert page in nx_graph.nodes

        assert attrs["nodes"] == nodes
        assert attrs["pos"] == positions
        assert attrs["node_color"] == node_colors
        # note that edge colors refers to the color of the edges of the nodes
        # not the color of the edges between nodes
        assert attrs["edgecolors"] == edge_colors

        straight, curved = edgelist_connectionstyle

        assert straight[0] == attrs["edges"]
        for edge in straight_edges:
            assert edge in straight[0]

        for edge in curved_edges:
            assert edge in curved[0]

    def test_display(self):
        # Note: this test simply checks that the display_navigation function can be run
        # without error. It does not verify expected output.
        display_navigation(self.make_tree())


class TestSingletonTree(Mixin):
    @staticmethod
    def make_tree():
        def seed():
            return Page()

        return Tree(seed)

    def test_graph(self):
        self.tree = self.make_tree()
        self.assert_correct_digraph(
            nodes=self.tree.branch,
            positions={self.tree.branch[0]: (0, 0)},
            node_colors=[CURRENT_NODE_COLOR],
            edge_colors=[TERMINAL_EDGE_COLOR],
            straight_edges=[],
            curved_edges=[],
        )


class TestBasicTree(Mixin):
    @staticmethod
    def make_tree():
        def seed():
            return [Page(), Page()]

        return Tree(seed)

    def test_graph(self):
        self.tree = self.make_tree()
        branch = self.tree.branch
        self.assert_correct_digraph(
            nodes=branch,
            positions={branch[0]: (0, 0), branch[1]: (1, 0)},
            node_colors=[CURRENT_NODE_COLOR, TERMINAL_NODE_COLOR],
            edge_colors=[CURRENT_EDGE_COLOR, TERMINAL_EDGE_COLOR],
            straight_edges=[(branch[0], branch[1])],
            curved_edges=[],
        )


class TestMediumTree(Mixin):
    @staticmethod
    def make_tree():
        def seed():
            branch = [
                Page(),
                first_page := Page(),
                Page(back=True),
                Page(back=True, prev_page=first_page),
            ]
            branch[0].next_page = branch[2]
            return branch

        return Tree(seed)

    def test_graph(self):
        self.tree = self.make_tree()
        branch = self.tree.branch
        self.assert_correct_digraph(
            nodes=branch,
            positions={
                branch[0]: (0, 0),
                branch[1]: (1, 0),
                branch[2]: (2, 0),
                branch[3]: (3, 0),
            },
            node_colors=[
                CURRENT_NODE_COLOR,
                DEFAULT_NODE_COLOR,
                DEFAULT_NODE_COLOR,
                TERMINAL_NODE_COLOR,
            ],
            edge_colors=[
                CURRENT_EDGE_COLOR,
                DEFAULT_EDGE_COLOR,
                DEFAULT_EDGE_COLOR,
                TERMINAL_EDGE_COLOR,
            ],
            straight_edges=[
                (branch[1], branch[2]),
                (branch[2], branch[1]),
                (branch[2], branch[3]),
            ],
            curved_edges=[(branch[0], branch[2]), (branch[3], branch[1])],
        )


class TestComplexTree(Mixin):
    @staticmethod
    def make_tree():
        def seed():
            branch = [Page(), Page(back=True)]
            branch[0].branch = [Page(), Page(back=True)]
            branch[0].branch[0].branch = [Page(next_page=branch[1])]
            branch[0].branch[1].branch = [Page(back=True)]
            branch[1].prev_page = branch[0].branch[1]
            return branch

        return Tree(seed)

    def test_graph(self):
        self.tree = self.make_tree()
        branch = self.tree.branch
        self.assert_correct_digraph(
            nodes=[
                branch[0],
                branch[0].branch[0],
                branch[0].branch[0].branch[0],
                branch[0].branch[1],
                branch[0].branch[1].branch[0],
                branch[1],
            ],
            positions={
                branch[0]: (0, 0),
                branch[0].branch[0]: (1, Y_INCREMENT),
                branch[0].branch[0].branch[0]: (2, 2 * Y_INCREMENT),
                branch[0].branch[1]: (3, Y_INCREMENT),
                branch[0].branch[1].branch[0]: (4, 2 * Y_INCREMENT),
                branch[1]: (5, 0),
            },
            node_colors=[CURRENT_NODE_COLOR]
            + 4 * [DEFAULT_NODE_COLOR]
            + [TERMINAL_NODE_COLOR],
            edge_colors=[CURRENT_EDGE_COLOR]
            + 4 * [DEFAULT_EDGE_COLOR]
            + [TERMINAL_EDGE_COLOR],
            straight_edges=[
                (branch[0], branch[0].branch[0]),
                (branch[0].branch[0], branch[0].branch[0].branch[0]),
                (branch[0].branch[1], branch[0].branch[0].branch[0]),
                (branch[0].branch[1], branch[0].branch[1].branch[0]),
                (branch[0].branch[1].branch[0], branch[0].branch[1]),
                (branch[0].branch[1].branch[0], branch[1]),
            ],
            curved_edges=[
                (branch[0].branch[0].branch[0], branch[1]),
                (branch[1], branch[0].branch[1]),
            ],
        )
