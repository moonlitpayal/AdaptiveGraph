"""Adjacency-list representation.

Space O(V+E) | add/remove/has_edge O(degree) | neighbors O(degree)
"""

from typing import Iterator, List, Optional, Tuple

from adaptivegraph.base import Graph


class AdjacencyList(Graph):
    def __init__(self, num_vertices: int, directed: bool = False):
        super().__init__(num_vertices, directed)
        self._adj: List[List[Tuple[int, float]]] = [[] for _ in range(num_vertices)]
        self._m = 0

    @property
    def num_edges(self) -> int:
        return self._m

    def _find(self, u: int, v: int) -> int:
        for i, (x, _) in enumerate(self._adj[u]):
            if x == v:
                return i
        return -1

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> bool:
        self._check_edge(u, v)
        i = self._find(u, v)
        if i != -1:
            self._adj[u][i] = (v, weight)
            if not self._directed:
                self._adj[v][self._find(v, u)] = (u, weight)
            return False
        self._adj[u].append((v, weight))
        if not self._directed:
            self._adj[v].append((u, weight))
        self._m += 1
        return True

    def remove_edge(self, u: int, v: int) -> bool:
        self._check_vertex(u)
        self._check_vertex(v)
        i = self._find(u, v)
        if i == -1:
            return False
        self._adj[u].pop(i)
        if not self._directed:
            self._adj[v].pop(self._find(v, u))
        self._m -= 1
        return True

    def has_edge(self, u: int, v: int) -> bool:
        self._check_vertex(u)
        self._check_vertex(v)
        return self._find(u, v) != -1

    def get_weight(self, u: int, v: int) -> Optional[float]:
        self._check_vertex(u)
        self._check_vertex(v)
        i = self._find(u, v)
        return None if i == -1 else self._adj[u][i][1]

    def neighbors(self, u: int) -> List[int]:
        self._check_vertex(u)
        return [v for v, _ in self._adj[u]]

    def weighted_neighbors(self, u: int) -> List[Tuple[int, float]]:
        self._check_vertex(u)
        return list(self._adj[u])

    def degree(self, u: int) -> int:
        self._check_vertex(u)
        return len(self._adj[u])

    def edges(self) -> Iterator[Tuple[int, int, float]]:
        for u in range(self._n):
            for v, w in self._adj[u]:
                if self._directed or u < v:
                    yield (u, v, w)