import sys
from pathlib import Path

from cycle_detection import has_negative_cycle
from graph import build_residual_graph
from input_parser import read_input_data
from max_flow import ford_fulkerson_max_flow
from min_cost_flow import min_cost_max_flow_bellman_ford, min_cost_max_flow_dijkstra
from visualization import render_pdf_from_dot, verify_dot_labels, write_dot_file


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <fichier_entree>")
        return 1

    input_path = sys.argv[1]
    try:
        parsed = read_input_data(input_path)
    except OSError as exc:
        print(f"Erreur lecture fichier: {exc}")
        return 1
    except ValueError as exc:
        print(f"Erreur format d'entree: {exc}")
        return 1

    header = parsed.header

    print("Entree lue avec succes:")
    print(f"nodes={header.node_count} arcs={header.arc_count} s={header.source} t={header.sink}")
    print(f"arcs_lus={len(parsed.arcs)}")

    max_flow_graph = build_residual_graph(parsed)
    max_flow_value = ford_fulkerson_max_flow(max_flow_graph, header.source, header.sink)

    print("\nFord-Fulkerson:")
    print(f"flot_max={max_flow_value}")
    print("flot_final_par_arc (u v flow/capacity cost):")
    for record in max_flow_graph.arc_flows():
        print(f"{record.u} {record.v} {record.flow}/{record.capacity} cost={record.cost}")

    mcmf_bf_graph = build_residual_graph(parsed)
    flow_bf, cost_bf = min_cost_max_flow_bellman_ford(
        mcmf_bf_graph,
        header.source,
        header.sink,
    )

    mcmf_dij_graph = build_residual_graph(parsed)
    flow_dij, cost_dij = min_cost_max_flow_dijkstra(
        mcmf_dij_graph,
        header.source,
        header.sink,
    )

    print("\nMin-Cost Max-Flow:")
    print(f"Bellman-Ford: flow={flow_bf} cost={cost_bf}")
    print(f"Dijkstra+potentiels: flow={flow_dij} cost={cost_dij}")
    print(f"comparaison_resultats_identiques={flow_bf == flow_dij and cost_bf == cost_dij}")

    cycle_graph = build_residual_graph(parsed)
    has_neg_cycle = has_negative_cycle(cycle_graph)
    print(f"\ncycle_negatif_residuel={has_neg_cycle}")

    input_file = Path(input_path)
    dot_path = str(input_file.with_suffix(".generated.gv"))
    pdf_path = str(input_file.with_suffix(".generated.pdf"))
    write_dot_file(parsed, dot_path)
    print(f"dot_genere={dot_path}")

    labels_ok = verify_dot_labels(dot_path)
    print(f"labels_capacite_cout_valides={labels_ok}")

    try:
        render_pdf_from_dot(dot_path, pdf_path)
        print(f"pdf_genere={pdf_path}")
    except RuntimeError as exc:
        print(f"pdf_non_genere={exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
