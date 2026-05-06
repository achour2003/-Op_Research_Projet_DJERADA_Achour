# Rapport - Projet Flots

## 1. Structure de donnees du graphe residuel

Le coeur de l'implementation est la structure Edge dans src/graph.py.
Chaque arc stocke:
- to: sommet d'arrivee
- rev: indice de l'arc inverse dans la liste d'adjacence du sommet to
- cap: capacite residuelle courante
- cost: cout unitaire de l'arc residuel
- original_cap: capacite initiale (pour afficher le flot final)
- is_reverse: indique si l'arc est un arc inverse residuel

Le graphe est stocke en liste d'adjacence:
- adjacency[u] = liste des arcs sortants depuis u

Ajout d'un arc (u, v, cap, cost):
- creation d'un arc avant: cap = cap, cost = cost
- creation d'un arc inverse: cap = 0, cost = -cost

Lors d'une augmentation de flot sur un chemin:
- cap(arc avant) -= delta
- cap(arc inverse) += delta

Le flot final d'un arc original est recupere avec la capacite de son arc inverse.

## 2. Algorithmes implementes

### 2.1 Flot maximal - Ford-Fulkerson (Edmonds-Karp)
Fichier: src/max_flow.py

Etapes:
1. Chercher un chemin augmentant s->t par BFS (seulement arcs cap > 0).
2. Calculer le goulot d'etranglement (bottleneck).
3. Mettre a jour les capacites residuelles.
4. Recommencer jusqu'a absence de chemin.

Complexite: O(V E^2).

### 2.2 Min-Cost Max-Flow - Bellman-Ford
Fichier: src/min_cost_flow.py

Etapes:
1. Sur le graphe residuel, trouver un plus court chemin en cout (Bellman-Ford).
2. Augmenter le flot sur ce chemin.
3. Ajouter delta * cout_du_chemin au cout total.
4. Recommencer jusqu'a absence de chemin augmentant.

Utilise pour gerer les couts negatifs.
Complexite: O(F V E).

### 2.3 Min-Cost Max-Flow - Dijkstra + potentiels
Fichier: src/min_cost_flow.py

Etapes:
1. Initialiser les potentiels avec Bellman-Ford.
2. Utiliser Dijkstra sur les couts reduits:
   c'(u,v) = c(u,v) + pi(u) - pi(v)
3. Mettre a jour les potentiels apres chaque iteration.
4. Augmenter le flot sur le chemin trouve.

Complexite: O(F E log V) (apres initialisation).

### 2.4 Detection de cycle negatif
Fichier: src/cycle_detection.py

Approche:
- Bellman-Ford avec distances initiales a 0 (super-source implicite).
- Si une relaxation est encore possible a la V-ieme iteration, un cycle negatif existe.

Complexite: O(V E).

## 3. Resultats des tests

Script de test: tests/run_tests.py

Tests executes:
- test_small_manual_graph: valide un petit graphe (flot max attendu = 5)
- test_no_path_case: cas sans chemin s->t (flot = 0)
- test_negative_costs_case: couts negatifs + coherence Bellman-Ford / Dijkstra
- test_negative_cycle_detection: detection d'un cycle negatif
- test_dot_generation_and_labels: generation DOT + verification labels capacite,cout

Statut: tous les tests sont passes.

## 4. Resultat sur l'exemple principal

Commande:
python src/main.py data/exemple_entree.txt

Resume obtenu:
- flot max = 28
- min-cost max-flow (Bellman-Ford): flow=28 cost=297
- min-cost max-flow (Dijkstra+potentiels): flow=28 cost=297
- comparaison: identiques = True
- cycle negatif residuel: False
- fichiers generes:
  - data/exemple_entree.generated.gv
  - data/exemple_entree.generated.pdf

## 5. Commandes utiles

Execution principale:
python src/main.py data/exemple_entree.txt

Tests:
python tests/run_tests.py

Generation PDF Graphviz:
"C:\Program Files\Graphviz\bin\dot.exe" data\exemple_entree.generated.gv -Tpdf -o data\exemple_entree.generated.pdf

## 6. Lien GitHub

Depot final (a remplacer):
https://github.com/ton-compte/ton-repo
