from collections import deque
from dataclasses import dataclass

from graph import ResidualGraph


def find_augmenting_path(
    graph: ResidualGraph, source: int, sink: int
) -> tuple[list[tuple[int, int] | None], int] | None:
    """Find one s->t augmenting path with BFS and return its bottleneck capacity.

    Returns:
        - None if no path exists.
        - (parent, bottleneck) where parent[v] = (u, edge_index_in_adjacency_u)
          for all visited vertices on the path from source to sink.
    """
    if not (0 <= source < graph.node_count):
        raise ValueError(f"Source invalide: {source}")
    if not (0 <= sink < graph.node_count):
        raise ValueError(f"Puits invalide: {sink}")

    parent: list[tuple[int, int] | None] = [None] * graph.node_count
    parent[source] = (-1, -1)

    bottleneck = [0] * graph.node_count
    bottleneck[source] = 10**18

    queue: deque[int] = deque([source])

    while queue:
        u = queue.popleft()
        for edge_index, edge in enumerate(graph.adjacency[u]):
            if edge.cap <= 0:
                continue
            if parent[edge.to] is not None:
                continue

            parent[edge.to] = (u, edge_index)
            bottleneck[edge.to] = min(bottleneck[u], edge.cap)

            if edge.to == sink:
                return parent, bottleneck[sink]

            queue.append(edge.to)

    return None


def apply_augmenting_path(
    graph: ResidualGraph,
    parent: list[tuple[int, int] | None],
    source: int,
    sink: int,
    pushed_flow: int,
) -> None:
    """Apply residual capacity updates along an augmenting path."""
    if pushed_flow <= 0:
        raise ValueError("Le flot augmente doit etre strictement positif")

    v = sink
    while v != source:
        prev = parent[v]
        if prev is None:
            raise ValueError("Chemin augmentant invalide: parent manquant")

        u, edge_index = prev
        edge = graph.adjacency[u][edge_index]
        reverse = graph.adjacency[edge.to][edge.rev]

        if edge.cap < pushed_flow:
            raise ValueError("Capacite residuelle insuffisante sur le chemin")

        edge.cap -= pushed_flow
        reverse.cap += pushed_flow
        v = u


def ford_fulkerson_max_flow(graph: ResidualGraph, source: int, sink: int) -> int:
    """Compute and return the max flow value from source to sink."""
    if not (0 <= source < graph.node_count):
        raise ValueError(f"Source invalide: {source}")
    if not (0 <= sink < graph.node_count):
        raise ValueError(f"Puits invalide: {sink}")
    if source == sink:
        return 0

    max_flow = 0
    while True:
        result = find_augmenting_path(graph, source, sink)
        if result is None:
            break

        parent, pushed_flow = result
        apply_augmenting_path(graph, parent, source, sink, pushed_flow)
        max_flow += pushed_flow

    return max_flow


@dataclass(frozen=True)
class MinCutEdge:
    u: int
    v: int
    capacity: int


def min_cut_from_residual(
    graph: ResidualGraph, source: int
) -> tuple[set[int], list[MinCutEdge], int]:
    """Return the min-cut (S, T) from the residual graph after max flow.

    S is the set of vertices reachable from source by residual arcs with cap > 0.
    The cut edges are original arcs u->v with u in S and v in T.
    """
    if not (0 <= source < graph.node_count):
        raise ValueError(f"Source invalide: {source}")

    reachable: set[int] = set()
    queue: deque[int] = deque([source])
    reachable.add(source)

    while queue:
        u = queue.popleft()
        for edge in graph.adjacency[u]:
            if edge.cap <= 0:
                continue
            if edge.to in reachable:
                continue
            reachable.add(edge.to)
            queue.append(edge.to)

    cut_edges: list[MinCutEdge] = []
    cut_capacity = 0
    for u in reachable:
        for edge in graph.adjacency[u]:
            if edge.is_reverse:
                continue
            if edge.to in reachable:
                continue
            cut_edges.append(MinCutEdge(u=u, v=edge.to, capacity=edge.original_cap))
            cut_capacity += edge.original_cap

    return reachable, cut_edges, cut_capacity
