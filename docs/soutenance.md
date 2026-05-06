# Preparation Soutenance / Demonstration

## 1) Plan de presentation (5-8 minutes)
1. Contexte du probleme de flot et objectif du projet.
2. Structure de donnees du graphe residuel.
3. Flot maximal (Ford-Fulkerson / Edmonds-Karp).
4. Min-Cost Max-Flow:
   - Bellman-Ford
   - Dijkstra + potentiels
5. Detection de cycle negatif.
6. Demo en direct et resultats de tests.

## 2) Demo live recommandee
1. Montrer le format d'entree dans data/exemple_entree.txt.
2. Lancer:
   python src/main.py data/exemple_entree.txt
3. Montrer:
   - flot max
   - details du flot final par arc
   - cout total minimal
   - coherence Bellman-Ford vs Dijkstra
4. Ouvrir data/exemple_entree.generated.pdf.
5. Lancer:
   python tests/run_tests.py

## 3) Messages a retenir
- Le graphe residuel permet la correction des decisions via les arcs inverses.
- Bellman-Ford est robuste aux couts negatifs.
- Dijkstra + potentiels accelere la recherche des chemins de cout minimal.
- Les deux methodes min-cost donnent le meme resultat sur les tests.

## 4) Questions classiques et reponses courtes
- Pourquoi un arc inverse?
  Pour annuler/reorienter du flot deja envoye dans le residuel.
- Pourquoi deux methodes min-cost?
  Bellman-Ford gere les couts negatifs, Dijkstra+potentiels est plus rapide.
- Comment verifier la validite?
  Tests automatiques + comparaison des deux methodes + verification Graphviz.
