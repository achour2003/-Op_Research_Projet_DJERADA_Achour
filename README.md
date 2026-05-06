# Projet de Recherche Operationnelle - Flots

Ce projet implemente des algorithmes de flot sur graphe oriente avec capacites et couts:

- Flot maximal (Ford-Fulkerson avec recherche BFS type Edmonds-Karp)
- Min-Cost Max-Flow (plus court chemin augmentant)
- Deux variantes Min-Cost:
	- Bellman-Ford (supporte les couts negatifs)
	- Dijkstra + potentiels (renormalisation des couts)
- Detection de cycle negatif dans le residuel
- Export Graphviz (.gv) et rendu PDF

## 1. Prerequis

- Python 3.10+
- Graphviz (optionnel, pour generer les PDF)

Verifier Python:

```cmd
python --version
```

Verifier Graphviz:

```cmd
dot -V
```

Sous Windows, si dot n'est pas dans le PATH, utilisez le binaire complet:

```cmd
"C:\Program Files\Graphviz\bin\dot.exe"
```

## 2. Structure du projet

- src/: code source principal
	- input_parser.py: lecture/validation du format d'entree
	- graph.py: structure du graphe residuel
	- max_flow.py: flot maximal
	- min_cost_flow.py: min-cost max-flow (2 methodes)
	- cycle_detection.py: detection de cycle negatif
	- visualization.py: generation .gv/.pdf + verification des labels
	- main.py: point d'entree CLI
- data/: jeux de donnees d'exemple et sorties generees
- tests/: tests automatiques et donnees de test
- docs/: rapport et support de soutenance

## 3. Format d'entree

Premiere ligne:

```text
#nodes #arcs s t
```

Puis #arcs lignes au format:

```text
u v capacite cout_unitaire
```

Contraintes:

- #nodes > 0
- #arcs >= 0
- s et t dans [0, #nodes-1]
- capacite >= 0

Exemple complet:

```txt
6 10 5 4
5 0 40 2
0 1 15 4
0 2 8 4
0 3 5 8
1 2 20 2
1 3 4 2
1 4 10 6
2 3 15 1
2 4 4 3
3 4 20 2
```

## 4. Utilisation rapide

Execution principale:

```cmd
python src/main.py data/exemple_entree.txt
```

Le programme affiche notamment:

- informations de parsing
- valeur du flot maximal
- flot final par arc
- resultat Min-Cost (Bellman-Ford)
- resultat Min-Cost (Dijkstra + potentiels)
- verification d'egalite entre les deux methodes
- presence/absence de cycle negatif
- generation des fichiers .generated.gv et .generated.pdf

## 5. Tests

Lancer toute la suite:

```cmd
python tests/run_tests.py
```

Tests couverts:

- test_small_manual_graph
- test_no_path_case
- test_negative_costs_case
- test_negative_cycle_detection
- test_dot_generation_and_labels

## 6. Algorithmes et complexites

- Flot max (Edmonds-Karp): O(V E^2)
- Min-Cost Max-Flow (Bellman-Ford): O(F V E)
- Min-Cost Max-Flow (Dijkstra + potentiels): O(F E log V) apres initialisation
- Detection de cycle negatif (Bellman-Ford): O(V E)

Avec:

- V: nombre de sommets
- E: nombre d'arcs
- F: flot total envoye

## 7. Sorties Graphviz

Pour un fichier d'entree X.txt, le programme peut produire:

- X.generated.gv
- X.generated.pdf

Generation manuelle PDF:

```cmd
dot data\exemple_entree.generated.gv -Tpdf -o data\exemple_entree.generated.pdf
```

ou, sous Windows sans PATH:

```cmd
"C:\Program Files\Graphviz\bin\dot.exe" data\exemple_entree.generated.gv -Tpdf -o data\exemple_entree.generated.pdf
```

## 8. Depannage

- Erreur de format d'entree:
	- verifier le nombre de colonnes
	- verifier que le nombre d'arcs declare correspond aux lignes d'arcs
	- verifier les indices de sommets
- PDF non genere:
	- installer Graphviz
	- verifier la commande dot -V
	- utiliser le chemin absolu vers dot.exe sous Windows

## 9. Documentation complementaire

- Rapport detaille: docs/rapport.md

## 10. Lien du depot

- https://github.com/achour2003/-Op_Research_Projet_DJERADA_Achour.git
