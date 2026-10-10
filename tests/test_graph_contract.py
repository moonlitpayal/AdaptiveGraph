import pytest

from adaptivegraph.adj_list import AdjacencyList
from adaptivegraph.adj_matrix import AdjacencyMatrix

GRAPH_CLASSES = [AdjacencyList, AdjacencyMatrix]


@pytest.fixture(params=GRAPH_CLASSES)
def cls(request):
    return request.param


def test_empty_graph(cls):
    g = cls(5)
    assert g.num_vertices == 5
    assert g.num_edges == 0
    assert g.density() == 0.0


def test_add_and_has_edge_undirected(cls):
    g = cls(4)
    assert g.add_edge(0, 1) is True
    assert g.has_edge(0, 1)
    assert g.has_edge(1, 0)
    assert g.num_edges == 1


def test_directed_edge(cls):
    g = cls(4, directed=True)
    g.add_edge(0, 1)
    assert g.has_edge(0, 1)
    assert not g.has_edge(1, 0)


def test_duplicate_edge_updates_weight(cls):
    g = cls(3)
    assert g.add_edge(0, 1, 2.0) is True
    assert g.add_edge(0, 1, 5.0) is False
    assert g.num_edges == 1
    assert g.get_weight(0, 1) == 5.0
    assert g.get_weight(1, 0) == 5.0


def test_get_weight_missing(cls):
    g = cls(3)
    assert g.get_weight(0, 1) is None


def test_remove_edge(cls):
    g = cls(4)
    g.add_edge(0, 1)
    assert g.remove_edge(0, 1) is True
    assert not g.has_edge(0, 1)
    assert not g.has_edge(1, 0)
    assert g.num_edges == 0


def test_remove_missing_edge(cls):
    g = cls(4)
    assert g.remove_edge(0, 1) is False
    assert g.num_edges == 0


def test_neighbors_and_degree(cls):
    g = cls(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    assert sorted(g.neighbors(0)) == [1, 2, 3]
    assert g.degree(0) == 3
    assert g.degree(4) == 0


def test_weighted_neighbors(cls):
    g = cls(3)
    g.add_edge(0, 1, 2.5)
    assert g.weighted_neighbors(0) == [(1, 2.5)]


def test_edges_listed_once_undirected(cls):
    g = cls(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    assert sorted(g.edges()) == [(0, 1, 1.0), (1, 2, 1.0)]


def test_edges_directed(cls):
    g = cls(3, directed=True)
    g.add_edge(0, 1)
    g.add_edge(1, 0)
    assert sorted(g.edges()) == [(0, 1, 1.0), (1, 0, 1.0)]


def test_density_undirected(cls):
    g = cls(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    assert g.density() == pytest.approx(0.5)


def test_density_directed(cls):
    g = cls(3, directed=True)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    assert g.density() == pytest.approx(0.5)


def test_invalid_vertex(cls):
    g = cls(3)
    with pytest.raises(IndexError):
        g.add_edge(0, 5)
    with pytest.raises(IndexError):
        g.has_edge(-1, 0)


def test_self_loop_rejected(cls):
    g = cls(3)
    with pytest.raises(ValueError):
        g.add_edge(1, 1)