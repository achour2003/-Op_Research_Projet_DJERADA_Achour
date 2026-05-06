from dataclasses import dataclass


@dataclass(frozen=True)
class InputHeader:
    node_count: int
    arc_count: int
    source: int
    sink: int


@dataclass(frozen=True)
class ArcInput:
    u: int
    v: int
    capacity: int
    cost: int


@dataclass(frozen=True)
class ParsedInput:
    header: InputHeader
    arcs: list[ArcInput]


def parse_header_line(line: str) -> InputHeader:
    """Parse the first input line: '#nodes #arcs s t'."""
    parts = line.strip().split()
    if len(parts) != 4:
        raise ValueError("La 1re ligne doit contenir exactement 4 entiers: #nodes #arcs s t")

    try:
        node_count, arc_count, source, sink = map(int, parts)
    except ValueError as exc:
        raise ValueError("La 1re ligne doit contenir des entiers valides") from exc

    if node_count <= 0:
        raise ValueError("Le nombre de noeuds doit etre strictement positif")
    if arc_count < 0:
        raise ValueError("Le nombre d'arcs ne peut pas etre negatif")
    if not (0 <= source < node_count):
        raise ValueError("La source s doit etre un indice de noeud valide")
    if not (0 <= sink < node_count):
        raise ValueError("Le puits t doit etre un indice de noeud valide")

    return InputHeader(
        node_count=node_count,
        arc_count=arc_count,
        source=source,
        sink=sink,
    )


def read_input_header(file_path: str) -> InputHeader:
    """Read and parse only the first line of an input file."""
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline()

    if not first_line:
        raise ValueError("Fichier vide: impossible de lire la 1re ligne")

    return parse_header_line(first_line)


def parse_arc_line(line: str) -> ArcInput:
    """Parse one arc line: 'u v capacite cout'."""
    parts = line.strip().split()
    if len(parts) != 4:
        raise ValueError("Chaque arc doit contenir exactement 4 entiers: u v capacite cout")

    try:
        u, v, capacity, cost = map(int, parts)
    except ValueError as exc:
        raise ValueError("Chaque arc doit contenir des entiers valides") from exc

    if capacity < 0:
        raise ValueError("La capacite d'un arc doit etre >= 0")

    return ArcInput(u=u, v=v, capacity=capacity, cost=cost)


def read_input_data(file_path: str) -> ParsedInput:
    """Read the full input file: header and arc list."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError("Fichier vide: impossible de lire les donnees")

    header = parse_header_line(lines[0])
    arc_lines = lines[1:]
    if len(arc_lines) != header.arc_count:
        raise ValueError(
            f"Nombre d'arcs incoherent: attendu {header.arc_count}, trouve {len(arc_lines)}"
        )

    arcs: list[ArcInput] = []
    for index, line in enumerate(arc_lines, start=2):
        arc = parse_arc_line(line)
        if not (0 <= arc.u < header.node_count):
            raise ValueError(f"Ligne {index}: extremite initiale invalide ({arc.u})")
        if not (0 <= arc.v < header.node_count):
            raise ValueError(f"Ligne {index}: extremite terminale invalide ({arc.v})")
        arcs.append(arc)

    return ParsedInput(header=header, arcs=arcs)
