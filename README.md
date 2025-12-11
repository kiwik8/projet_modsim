# Projet INFO-F305 (Modélisation et simulation)

# Fonctionnalités
## App de visualisation Mathématique
- Portrait de phase interactif avec champ de vecteurs et des trajcetoires d'exemples
- Analyse de la stabilité : Comparaison nominale vs perturbée d'un facteur $\epsilon$

## Scénarios Physiques
- Stabilité d'un navire dans l'océan : Simulation visuelle qui tange selon la hauteur du centre de gravité et le frottement
- Porte automatique : Simulation d'une porte automatique pour comprendre les régimes (porte qui claque vs porte lente)

## Assistant pédagogique interactif
- Le professeur Einstein animé guide l'utilisateur si il manque un peu de bases théoriques

## Quiz
- Un mode quiz intégré avec timer, sons, animations pour tester les connaissances de l'utilisateur

# Installation et démarrage
### Installation des dépendances
```bash
python -m venv .venv
source .venv/bin/acticate
pip install -r requirements.txt
```
### Pour lancer le dashboard
```bash
python src/main.py
```
# Librairies utilisées
- Dash (Dashboard)
- Dash Bootstrap Components (Style principal)
- Plotly (Graphiques et animations vectorielles)
