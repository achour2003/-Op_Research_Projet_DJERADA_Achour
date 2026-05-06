from graph import ResidualGraph

INF = 10**18


def has_negative_cycle(graph: ResidualGraph) -> bool:
    """Detect a negative cycle in the residual graph using Bellman-Ford criterion.

    We initialize all distances to 0 (equivalent to adding a super-source with 0-cost
    edges to all vertices), then check for improvement on the n-th relaxation.
    Only residual arcs with positive capacity are considered.
    """
    n = graph.node_count
    dist = [0] * n

    for i in range(n):
        updated = False
        for u in range(n):
            for edge in graph.adjacency[u]:
                if edge.cap <= 0:
                    continue
                nd = dist[u] + edge.cost
                if nd < dist[edge.to]:
                    dist[edge.to] = nd
                    updated = True
        if not updated:
            return False
        if i == n - 1 and updated:
            return True

    return False
