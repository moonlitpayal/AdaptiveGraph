import random

import pytest

from adaptivegraph.adj_list import AdjacencyList
from adaptivegraph.adj_matrix import AdjacencyMatrix


@pytest.mark.parametrize("directed", [False, True])
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_list_and_matrix_agree_on_random_operations(directed, seed):
    rng = random.Random(seed)
    n = 12
    a = AdjacencyList(n, directed)
    b = AdjacencyMatrix(n, directed)

    for _ in range(2000):
        u, v = rng.sample(range(n), 2)
        op = rng.choice(["add", "add", "remove", "has"])
        if op == "add":
            w = float(rng.randint(1, 9))
            assert a.add_edge(u, v, w) == b.add_edge(u, v, w)
        elif op == "remove":
            assert a.remove_edge(u, v) == b.remove_edge(u, v)
        else:
            assert a.has_edge(u, v) == b.has_edge(u, v)

        assert a.num_edges == b.num_edges

    assert a.density() == b.density()
    assert sorted(a.edges()) == sorted(b.edges())
    for u in range(n):
        assert sorted(a.neighbors(u)) == sorted(b.neighbors(u))
        assert a.degree(u) == b.degree(u)
        assert sorted(a.weighted_neighbors(u)) == sorted(b.weighted_neighbors(u))