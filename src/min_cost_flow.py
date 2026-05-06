from __future__ import annotations

import heapq

from graph import ResidualGraph
from max_flow import apply_augmenting_path

INF = 10**18


def shortest_path_bellman_ford(
    graph: ResidualGraph, source: int, sink: int
) -> tuple[list[tuple[int, int] | None], int] | None:
    """Shortest augmenting path by cost on residual graph (handles negative edges)."""
    n = graph.node_count
    dist = [INF] * n
    parent: list[tuple[int, int] | None] = [None] * n
    dist[source] = 0
    parent[source] = (-1, -1)

    for _ in range(n - 1):
        updated = False
        for u in range(n):
            if dist[u] == INF:
                continue
            for edge_index, edge in enumerate(graph.adjacency[u]):
                if edge.cap <= 0:
                    continue
                nd = dist[u] + edge.cost
                if nd < dist[edge.to]:
                    dist[edge.to] = nd
                    parent[edge.to] = (u, edge_index)
                    updated = True
        if not updated:
            break

    if dist[sink] == INF:
        return None

    bottleneck = INF
    v = sink
    while v != source:
        prev = parent[v]
        if prev is None:
            return None
        u, edge_index = prev
        edge = graph.adjacency[u][edge_index]
        bottleneck = min(bottleneck, edge.cap)
        v = u

    return parent, bottleneck


def min_cost_max_flow_bellman_ford(
    graph: ResidualGraph, source: int, sink: int
) -> tuple[int, int]:
    """Compute min-cost max-flow with repeated augmenting shortest paths (Bellman-Ford)."""
    total_flow = 0
    total_cost = 0

    while True:
        result = shortest_path_bellman_ford(graph, source, sink)
        if result is None:
            break

        parent, pushed_flow = result

        # Compute the real path cost before residual update.
        v = sink
        path_cost = 0
        while v != source:
            prev = parent[v]
            if prev is None:
                raise ValueError("Chemin parent invalide pour min-cost flow")
            u, edge_index = prev
            path_cost += graph.adjacency[u][edge_index].cost
            v = u

        apply_augmenting_path(graph, parent, source, sink, pushed_flow)
        total_flow += pushed_flow
        total_cost += pushed_flow * path_cost

    return total_flow, total_cost


def _initial_potentials_bellman_ford(graph: ResidualGraph, source: int) -> list[int]:
    """Compute initial potentials to support reduced costs in presence of negative edges."""
    n = graph.node_count
    dist = [INF] * n
    dist[source] = 0

    for _ in range(n - 1):
        updated = False
        for u in range(n):
            if dist[u] == INF:
                continue
            for edge in graph.adjacency[u]:
                if edge.cap <= 0:
                    continue
                nd = dist[u] + edge.cost
                if nd < dist[edge.to]:
                    dist[edge.to] = nd
                    updated = True
        if not updated:
            break

    potentials = [0] * n
    for i in range(n):
        if dist[i] != INF:
            potentials[i] = dist[i]
    return potentials


def shortest_path_dijkstra_with_potentials(
    graph: ResidualGraph,
    source: int,
    sink: int,
    potentials: list[int],
) -> tuple[list[tuple[int, int] | None], list[int]] | None:
    """Shortest path on reduced costs c' = c + pi[u] - pi[v]."""
    n = graph.node_count
    dist = [INF] * n
    parent: list[tuple[int, int] | None] = [None] * n
    dist[source] = 0
    parent[source] = (-1, -1)

    heap: list[tuple[int, int]] = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        if u == sink:
            break

        for edge_index, edge in enumerate(graph.adjacency[u]):
            if edge.cap <= 0:
                continue
            reduced_cost = edge.cost + potentials[u] - potentials[edge.to]
            if reduced_cost < 0:
                # Fallback defensif: evite un echec numerique sur de grands graphes.
                reduced_cost = 0
            nd = d + reduced_cost
            if nd < dist[edge.to]:
                dist[edge.to] = nd
                parent[edge.to] = (u, edge_index)
                heapq.heappush(heap, (nd, edge.to))

    if dist[sink] == INF:
        return None

    return parent, dist


def min_cost_max_flow_dijkstra(
    graph: ResidualGraph, source: int, sink: int
) -> tuple[int, int]:
    """Compute min-cost max-flow using Dijkstra + cost reweighting (potentials)."""
    total_flow = 0
    total_cost = 0
    potentials = _initial_potentials_bellman_ford(graph, source)

    while True:
        result = shortest_path_dijkstra_with_potentials(graph, source, sink, potentials)
        if result is None:
            break

        parent, dist = result

        for v in range(graph.node_count):
            if dist[v] < INF:
                potentials[v] += dist[v]

        bottleneck = INF
        path_cost = 0
        v = sink
        while v != source:
            prev = parent[v]
            if prev is None:
                raise ValueError("Chemin parent invalide pour dijkstra+potentiels")
            u, edge_index = prev
            edge = graph.adjacency[u][edge_index]
            bottleneck = min(bottleneck, edge.cap)
            path_cost += edge.cost
            v = u

        apply_augmenting_path(graph, parent, source, sink, bottleneck)
        total_flow += bottleneck
        total_cost += bottleneck * path_cost

    return total_flow, total_cost
