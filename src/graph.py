from dataclasses import dataclass

from input_parser import ParsedInput


@dataclass
class Edge:
    to: int
    rev: int
    cap: int
    cost: int
    original_cap: int
    is_reverse: bool


@dataclass(frozen=True)
class ArcFlowRecord:
    u: int
    v: int
    flow: int
    capacity: int
    cost: int


def add_edge(adjacency: list[list[Edge]], u: int, v: int, cap: int, cost: int) -> None:
    """Add forward and reverse arcs to the residual graph adjacency list."""
    if cap < 0:
        raise ValueError("La capacite d'un arc doit etre >= 0")

    forward = Edge(
        to=v,
        rev=len(adjacency[v]),
        cap=cap,
        cost=cost,
        original_cap=cap,
        is_reverse=False,
    )
    reverse = Edge(
        to=u,
        rev=len(adjacency[u]),
        cap=0,
        cost=-cost,
        original_cap=0,
        is_reverse=True,
    )

    adjacency[u].append(forward)
    adjacency[v].append(reverse)


class ResidualGraph:
    def __init__(self, node_count: int) -> None:
        if node_count <= 0:
            raise ValueError("Le nombre de noeuds doit etre strictement positif")
        self.node_count = node_count
        self.adjacency: list[list[Edge]] = [[] for _ in range(node_count)]

    def add_edge(self, u: int, v: int, cap: int, cost: int) -> None:
        if not (0 <= u < self.node_count):
            raise ValueError(f"Noeud source invalide: {u}")
        if not (0 <= v < self.node_count):
            raise ValueError(f"Noeud destination invalide: {v}")
        add_edge(self.adjacency, u, v, cap, cost)

    def arc_flows(self) -> list[ArcFlowRecord]:
        """Return flow values on original (non-reverse) arcs."""
        records: list[ArcFlowRecord] = []
        for u, edges in enumerate(self.adjacency):
            for edge in edges:
                if edge.is_reverse:
                    continue
                reverse = self.adjacency[edge.to][edge.rev]
                records.append(
                    ArcFlowRecord(
                        u=u,
                        v=edge.to,
                        flow=reverse.cap,
                        capacity=edge.original_cap,
                        cost=edge.cost,
                    )
                )
        return records


def build_residual_graph(parsed: ParsedInput) -> ResidualGraph:
    graph = ResidualGraph(parsed.header.node_count)
    for arc in parsed.arcs:
        graph.add_edge(arc.u, arc.v, arc.capacity, arc.cost)
    return graph
