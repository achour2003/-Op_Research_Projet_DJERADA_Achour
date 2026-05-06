# pyright: reportMissingImports=false
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cycle_detection import has_negative_cycle
from graph import build_residual_graph
from input_parser import read_input_data
from max_flow import ford_fulkerson_max_flow
from min_cost_flow import min_cost_max_flow_bellman_ford, min_cost_max_flow_dijkstra
from visualization import verify_dot_labels, write_dot_file


def _load(rel_path: str):
    return read_input_data(str(ROOT / rel_path))


def test_small_manual_graph() -> None:
    parsed = _load("tests/data/simple_valid.txt")
    graph = build_residual_graph(parsed)
    max_flow = ford_fulkerson_max_flow(graph, parsed.header.source, parsed.header.sink)
    assert max_flow == 5, f"max_flow attendu=5, obtenu={max_flow}"


def test_no_path_case() -> None:
    parsed = _load("tests/data/no_path.txt")

    g1 = build_residual_graph(parsed)
    flow = ford_fulkerson_max_flow(g1, parsed.header.source, parsed.header.sink)
    assert flow == 0, f"max_flow attendu=0, obtenu={flow}"

    g2 = build_residual_graph(parsed)
    m_flow, m_cost = min_cost_max_flow_bellman_ford(g2, parsed.header.source, parsed.header.sink)
    assert (m_flow, m_cost) == (0, 0), f"min_cost attendu=(0,0), obtenu=({m_flow},{m_cost})"


def test_negative_costs_case() -> None:
    parsed = _load("tests/data/negative_costs.txt")

    g_bf = build_residual_graph(parsed)
    flow_bf, cost_bf = min_cost_max_flow_bellman_ford(g_bf, parsed.header.source, parsed.header.sink)

    g_dj = build_residual_graph(parsed)
    flow_dj, cost_dj = min_cost_max_flow_dijkstra(g_dj, parsed.header.source, parsed.header.sink)

    assert flow_bf == flow_dj, f"flows differents BF={flow_bf} DJ={flow_dj}"
    assert cost_bf == cost_dj, f"costs differents BF={cost_bf} DJ={cost_dj}"


def test_negative_cycle_detection() -> None:
    parsed = _load("tests/data/negative_cycle.txt")
    graph = build_residual_graph(parsed)
    assert has_negative_cycle(graph), "Un cycle negatif devait etre detecte"


def test_dot_generation_and_labels() -> None:
    parsed = _load("tests/data/simple_valid.txt")
    out_dot = ROOT / "tests" / "data" / "simple_valid.generated.gv"
    write_dot_file(parsed, str(out_dot))
    assert out_dot.exists(), "Le fichier DOT n'a pas ete genere"
    assert verify_dot_labels(str(out_dot)), "Les labels capacite,cost sont invalides"


if __name__ == "__main__":
    tests = [
        test_small_manual_graph,
        test_no_path_case,
        test_negative_costs_case,
        test_negative_cycle_detection,
        test_dot_generation_and_labels,
    ]

    failures = 0
    for test_fn in tests:
        try:
            test_fn()
            print(f"[OK] {test_fn.__name__}")
        except Exception as exc:
            failures += 1
            print(f"[FAIL] {test_fn.__name__}: {exc}")

    if failures:
        raise SystemExit(1)

    print("Tous les tests sont passes.")
