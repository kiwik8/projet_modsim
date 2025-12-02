"""
Contenu des explications du Professeur Einstein

GUIDE D'UTILISATION :
====================

Pour modifier ou ajouter des explications :
-------------------------------------------
1. Chaque explication est associée à un type (clé du dictionnaire)
2. Le contenu supporte le Markdown pour la mise en forme
3. Évitez les emojis et mise en forme excessive

Structure :
-----------
HELP_CONTENT = {
    "type_aide": {
        "title": "Titre de l'aide",
        "content": "Contenu en Markdown..."
    }
}

Les types actuels sont :
- "theory" : rappel théorique général
- "scenario_none" : explication pour scénario "Aucun"
- "scenario_spring" : explication pour scénario "masse-ressort"
- "scenario_pendulum" : explication pour scénario "Pendule"
- "scenario_rlc" : explication pour scénario "Circuit RLC"
- "detail" : détails techniques sur la visualisation
"""

HELP_CONTENT = {
    "theory": {
        "title": "Rappel théorique",
        "content": """
### Systèmes dynamiques et stabilité

Un système dynamique linéaire s'écrit sous la forme :

$$\\dot{x} = Ax$$

où $A = \\begin{pmatrix} 0 & 1 \\\\ a_1 & a_2 \\end{pmatrix}$

La stabilité du point d'équilibre $(0,0)$ dépend des valeurs propres de $A$ :
- Si toutes les parties réelles sont négatives : **stable asymptotiquement**
- Si une partie réelle est positive : **instable**
- Si les parties réelles sont nulles : **oscillations** (stable non asymptotique)

### Fonction de Lyapunov

Une fonction de Lyapunov $V(x)$ permet de prouver la stabilité sans calculer les trajectoires :
- $V(x) > 0$ pour tout $x \\neq 0$ (définie positive)
- $\\dot{V}(x) = \\nabla V \\cdot \\dot{x} \\leq 0$ (décroissante)

Si $\\dot{V}(x) < 0$, la stabilité est asymptotique.
"""
    },
    
    "scenario_none": {
        "title": "Scénario personnalisé",
        "content": """
Vous avez choisi de définir vos propres coefficients $a_1$ et $a_2$.

Le système s'écrit :
$$\\dot{x} = \\begin{pmatrix} 0 & 1 \\\\ a_1 & a_2 \\end{pmatrix} \\begin{pmatrix} x \\\\ \\dot{x} \\end{pmatrix}$$

Pour analyser la stabilité :
1. Calculez les valeurs propres : $\\lambda = \\frac{a_2 \\pm \\sqrt{a_2^2 + 4a_1}}{2}$
2. Observez le portrait de phase
3. Vérifiez la fonction de Lyapunov

Essayez différentes combinaisons pour voir l'effet sur la stabilité.
"""
    },
    
    "scenario_spring": {
        "title": "Voiture avec suspension (masse-ressort)",
        "content": """
### Modèle physique

Ce scénario représente une voiture avec suspension, modélisée par un système masse-ressort-amortisseur.

L'équation du mouvement :
$$m\\ddot{x} + c\\dot{x} + kx = 0$$

En notation d'état avec $m=1$ :
$$\\dot{x} = \\begin{pmatrix} 0 & 1 \\\\ -k & -c \\end{pmatrix} \\begin{pmatrix} x \\\\ \\dot{x} \\end{pmatrix}$$

où :
- $k$ est la raideur du ressort ($a_1 = -k$)
- $c$ est le coefficient d'amortissement ($a_2 = -c$)

### Comportements typiques

- $c > 0$ : amortissement (stable)
- $c = 0$ : oscillations permanentes
- $c < 0$ : amortissement négatif (instable)
"""
    },
    
    "scenario_pendulum": {
        "title": "Pendule simple",
        "content": """
### Modèle physique

Le pendule simple linéarisé autour de la position d'équilibre vertical.

L'équation du mouvement :
$$\\ddot{\\theta} + \\frac{g}{L}\\theta = 0$$

En notation d'état :
$$\\dot{x} = \\begin{pmatrix} 0 & 1 \\\\ -\\frac{g}{L} & 0 \\end{pmatrix} \\begin{pmatrix} \\theta \\\\ \\dot{\\theta} \\end{pmatrix}$$

où :
- $g$ est l'accélération gravitationnelle
- $L$ est la longueur du pendule

Ce système présente des oscillations permanentes (centre dans le portrait de phase).
"""
    },
    
    "scenario_rlc": {
        "title": "Circuit RLC",
        "content": """
### Modèle physique

Circuit électrique avec résistance (R), inductance (L) et capacité (C) en série.

L'équation du circuit :
$$L\\ddot{q} + R\\dot{q} + \\frac{1}{C}q = 0$$

En notation d'état avec $L=1$ :
$$\\dot{x} = \\begin{pmatrix} 0 & 1 \\\\ -\\frac{1}{C} & -R \\end{pmatrix} \\begin{pmatrix} q \\\\ \\dot{q} \\end{pmatrix}$$

où :
- $q$ est la charge du condensateur
- $R$ est la résistance ($a_2 = -R$)
- $C$ est la capacité ($a_1 = -1/C$)

### Régimes

- Sur-amorti : $R^2 > 4/C$
- Critique : $R^2 = 4/C$
- Sous-amorti : $R^2 < 4/C$ (oscillations amorties)
"""
    },
    
    "detail": {
        "title": "Détails techniques",
        "content": """
### Méthode numérique

Les trajectoires sont calculées avec la méthode d'Euler explicite :
$$x_{n+1} = x_n + \\Delta t \\cdot f(x_n)$$

Cette méthode simple peut présenter des erreurs numériques si $\\Delta t$ est trop grand.

### Portrait de phase

Le portrait de phase montre les trajectoires dans l'espace $(x, \\dot{x})$. Le champ de vecteurs indique la direction du mouvement en chaque point.

### Fonction de Lyapunov

Nous utilisons la fonction quadratique :
$$V(x) = x^T P x$$

où $P$ est solution de l'équation de Lyapunov :
$$A^T P + P A = -Q$$

avec $Q = I$ (identité). Les courbes de niveau de $V$ sont affichées.

### Perturbations

La visualisation des trajectoires perturbées permet de tester la robustesse du système face à des conditions initiales légèrement différentes.
"""
    }
}


def get_help_content(help_type, scenario="none"):
    """
    Récupère le contenu d'aide approprié
    
    Args:
        help_type: "theory", "scenario", ou "detail"
        scenario: nom du scénario (pour help_type="scenario")
    
    Returns:
        dict avec 'title' et 'content'
    """
    if help_type == "scenario":
        key = f"scenario_{scenario}"
        return HELP_CONTENT.get(key, HELP_CONTENT["scenario_none"])
    
    return HELP_CONTENT.get(help_type, {"title": "Aide non disponible", "content": "Contenu non trouvé."})
