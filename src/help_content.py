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
- "scenario_ship" : explication pour scénario "stabilité d'un navire"
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
    
    "scenario_ship": {
        "title": "Stabilité du Navire (Roulis)",
        "content": """
### Modèle physique
Étude du mouvement de balancement (roulis) d'un navire autour de sa position d'équilibre vertical.

L'équation linéarisée est :
$$I\\ddot{\\theta} + B\\dot{\\theta} + C\\theta = 0$$

En notation d'état (forme du dashboard) :
$$\\dot{x} = \\begin{pmatrix} 0 & 1 \\\\ -\\frac{C}{I} & -\\frac{B}{I} \\end{pmatrix} \\begin{pmatrix} \\theta \\\\ \\dot{\\theta} \\end{pmatrix}$$

Où :
- **$x$** est l'angle d'inclinaison ($\\theta$).
- **$a_1 = -C/I$** représente la stabilité statique (liée à la hauteur du centre de gravité).
- **$a_2 = -B/I$** représente le frottement de l'eau sur la coque.

### Analyse de stabilité
- **$a_1 < 0$ (C > 0)** : Le navire est stable, il revient à la verticale après une vague.
- **$a_1 > 0$ (C < 0)** : Le navire est **instable** (centre de gravité trop haut), il chavire.
- **$a_2$** influence la vitesse à laquelle le balancement s'arrête.
"""
    },
    "scenario_door": {
        "title": "Porte automatique (Groom)",
        "content": """
### Modèle physique
Mécanisme de fermeture de porte équipé d'un ressort de rappel et d'un amortisseur hydraulique (groom).
L'objectif est de trouver le réglage qui ferme la porte le plus vite possible sans qu'elle ne claque (régime critique).

L'équation du mouvement :
$$I\\ddot{\\theta} + c\\dot{\\theta} + k\\theta = 0$$

En notation d'état (forme du dashboard) :
$$\\dot{x} = \\begin{pmatrix} 0 & 1 \\\\ -\\frac{k}{I} & -\\frac{c}{I} \\end{pmatrix} \\begin{pmatrix} \\theta \\\\ \\dot{\\theta} \\end{pmatrix}$$

Où :
- **$x$** est l'angle d'ouverture ($\theta$). $x=0$ signifie porte fermée.
- **$a_1 = -k/I$** représente la force du ressort (doit être négatif pour rappeler la porte).
- **$a_2 = -c/I$** représente le frein hydraulique (amortisseur).

### Régimes d'amortissement
Le comportement dépend du discriminant $\\Delta = a_2^2 + 4a_1$ :
- **Sous-amorti** ($\\Delta < 0$) : L'amortissement est trop faible, la porte oscille et claque.
- **Sur-amorti** ($\\Delta > 0$) : L'amortissement est trop fort, la porte met une éternité à se fermer.
- **Critique** ($\\Delta = 0$) : Le réglage parfait.
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
