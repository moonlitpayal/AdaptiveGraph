"""Abstract interface shared by every graph representation."""

from abc import ABC, abstractmethod
from typing import Iterator, List, Optional, Tuple


class Graph(ABC):
    """Vertices are integers 0..n-1. Self-loops are not allowed.
    Undirected edges are stored both ways but counted once in num_edges."""

    def __init__(self, num_vertices: int, directed: bool = False):
        if num_vertices < 0:
            raise ValueError("num_vertices must be non-negative")
        self._n = num_vertices
        self._directed = directed

    @property
    def num_vertices(self) -> int:
        return self._n

    @property
    def directed(self) -> bool:
        return self._directed

    @property
    @abstractmethod
    def num_edges(self) -> int:
        """Number of edges (an undirected edge counts once)."""

    def density(self) -> float:
        n = self._n
        if n < 2:
            return 0.0
        max_edges = n * (n - 1) if self._directed else n * (n - 1) // 2
        return self.num_edges / max_edges

    def _check_vertex(self, v: int) -> None:
        if not (0 <= v < self._n):
            raise IndexError(f"vertex {v} out of range 0..{self._n - 1}")

    def _check_edge(self, u: int, v: int) -> None:
        self._check_vertex(u)
        self._check_vertex(v)
        if u == v:
            raise ValueError("self-loops are not allowed")

    @abstractmethod
    def add_edge(self, u: int, v: int, weight: float = 1.0) -> bool:
        """Returns True if new, False if it only updated the weight."""

    @abstractmethod
    def remove_edge(self, u: int, v: int) -> bool:
        """Returns True if the edge existed."""

    @abstractmethod
    def has_edge(self, u: int, v: int) -> bool: ...

    @abstractmethod
    def get_weight(self, u: int, v: int) -> Optional[float]: ...

    @abstractmethod
    def neighbors(self, u: int) -> List[int]: ...

    @abstractmethod
    def weighted_neighbors(self, u: int) -> List[Tuple[int, float]]: ...

    @abstractmethod
    def degree(self, u: int) -> int: ...

    @abstractmethod
    def edges(self) -> Iterator[Tuple[int, int, float]]:
        """Yield each edge once as (u, v, weight). Undirected edges have u < v."""