from __future__ import annotations

import re
import subprocess
from pathlib import Path

from input_parser import ParsedInput


def input_to_dot_text(parsed: ParsedInput) -> str:
    """Convert parsed input data to Graphviz DOT text with capacity/cost labels."""
    lines = ["digraph G {"]
    lines.append("  rankdir=LR;")
    lines.append("  node [shape=circle];")

    s = parsed.header.source
    t = parsed.header.sink

    for node in range(parsed.header.node_count):
        attrs = []
        if node == s:
            attrs.append('color="green"')
            attrs.append('label="s"')
        elif node == t:
            attrs.append('color="blue"')
            attrs.append('label="t"')
        else:
            attrs.append(f'label="{node}"')
        lines.append(f"  {node} [{', '.join(attrs)}];")

    for arc in parsed.arcs:
        lines.append(
            f'  {arc.u} -> {arc.v} [label="{arc.capacity},{arc.cost}"];'
        )

    lines.append("}")
    return "\n".join(lines) + "\n"


def write_dot_file(parsed: ParsedInput, dot_path: str) -> None:
    dot_text = input_to_dot_text(parsed)
    Path(dot_path).write_text(dot_text, encoding="utf-8")


def render_pdf_from_dot(dot_path: str, pdf_path: str) -> None:
    """Render a DOT file to PDF with Graphviz dot."""
    dot_candidates = [
        "dot",
        r"C:\Program Files\Graphviz\bin\dot.exe",
    ]

    last_error: Exception | None = None
    for dot_cmd in dot_candidates:
        try:
            subprocess.run(
                [dot_cmd, dot_path, "-Tpdf", "-o", pdf_path],
                check=True,
                capture_output=True,
                text=True,
            )
            return
        except Exception as exc:  # pragma: no cover - defensive fallback
            last_error = exc

    raise RuntimeError(f"Impossible de lancer Graphviz dot: {last_error}")


def verify_dot_labels(dot_path: str) -> bool:
    """Verify each edge line contains a 'capacity,cost' label."""
    content = Path(dot_path).read_text(encoding="utf-8")
    edge_lines = [line for line in content.splitlines() if "->" in line]
    if not edge_lines:
        return False

    pattern = re.compile(r'label="\s*-?\d+\s*,\s*-?\d+\s*"')
    return all(pattern.search(line) is not None for line in edge_lines)
