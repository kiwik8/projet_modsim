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

"""
    },
    
    "scenario_none": {
        "title": "Scénario personnalisé",
        "content": """
Vous avez choisi de définir vos propres coefficients $a_1$ et $a_2$.

Le système s'écrit :
$$\\dot{x} = \\begin{pmatrix} 0 & 1 \\\\ a_1 & a_2 \\end{pmatrix} \\begin{pmatrix} x \\\\ \\dot{x} \\end{pmatrix}$$

Vous pouvez choisir un scénario pour mieux comprendre le rôle de ces coefficients en pratique.
"""
    },
    
    "scenario_ship": {
        "title": "Stabilité du Navire (Roulis)",
        "content": """
### Modèle physique
Étude du mouvement de balancement (roulis) d'un navire autour de sa position d'équilibre vertical.

Nous utilisons les variables :
- **$x$** : L'angle d'inclinaison du navire (en radians).
- **$y$** : La vitesse de rotation du navire ($\\dot{x}$).

L'équation d'état s'écrit :
$$\\begin{pmatrix} \\dot{x} \\\\ \\dot{y} \\end{pmatrix} = \\begin{pmatrix} 0 & 1 \\\\ a_1 & a_2 \\end{pmatrix} \\begin{pmatrix} x \\\\ y \\end{pmatrix}$$

### Rôle des coefficients
- **$a_1$ (Stabilité statique)** : Représente la capacité du navire à se redresser.
    - Si $a_1 < 0$ : Le centre de gravité est bas, le navire se redresse (**Stable**).
    - Si $a_1 > 0$ : Le centre de gravité est trop haut, le navire chavire (**Instable**).
- **$a_2$ (Frottement)** : Représente le frottement de l'eau sur la coque.
    - Il freine le mouvement et amortit les oscillations.
"""
    },
    
    "scenario_door": {
        "title": "Porte automatique (Groom)",
        "content": """
### Modèle physique
Mécanisme de fermeture de porte équipé d'un ressort de rappel et d'un amortisseur (groom).
L'objectif est que la porte se ferme vite ($x \\to 0$) sans claquer.

Nous utilisons les variables :
- **$x$** : L'angle d'ouverture de la porte ($x=0$ signifie fermée).
- **$y$** : La vitesse de fermeture/ouverture ($\\dot{x}$).

L'équation d'état s'écrit :
$$\\begin{pmatrix} \\dot{x} \\\\ \\dot{y} \\end{pmatrix} = \\begin{pmatrix} 0 & 1 \\\\ a_1 & a_2 \\end{pmatrix} \\begin{pmatrix} x \\\\ y \\end{pmatrix}$$

### Rôle des coefficients
- **$a_1$ (Ressort)** : La force qui rappelle la porte vers la position fermée. Il doit être négatif.
- **$a_2$ (Amortisseur)** : Le frein hydraulique.

### Régimes d'amortissement
Le comportement dépend du discriminant $\\Delta = a_2^2 + 4a_1$ :
- **Sous-amorti** ($\\Delta < 0$) : $a_2$ est trop faible. La porte oscille et **claque** contre le cadre.
- **Sur-amorti** ($\\Delta > 0$) : $a_2$ est trop fort. La porte met une éternité à se fermer.
- **Critique** ($\\Delta = 0$) : Le réglage parfait.
"""
    },
    "detail": {
        "title": "Détails techniques",
        "content": """

## 1 - Portrait de phase
Le portrait de phase est un graphique dans le plan d'état ($\\mathbf{x} = [X, Y]^T$) qui montre le comportement
 qualitatif d'un système dynamique. Chaque point du plan représente un état initial possible, et le champ de vecteurs
indiquent la direction et la vitesse du mouvement à partir de cet état.

### Diagnostic de stabilité: 

Le portrait de phase permet de diagnostiquer la stabilité de l'équilibre $(0, 0)$ en un seul coup d'œil, 
en observant comment les trajectoires se comportent autour de ce point.

• Système Stable Asymptotique : Toutes les trajectoires voisines se dirigent vers l'origine.

• Système Instable : Les trajectoires s'éloignent de l'origine.

• Stabilité non Asymptotique : Les trajectoires forment des boucles fermées autour de l'origine, indiquant une oscillation permanente sans convergence.

## 2 - Perturbations
La visualisation des trajectoires perturbées permet de tester la robustesse du système face à des conditions initiales légèrement différentes.
Cette méthode étudie la sensibilité du système. On compare la trajectoire partant d'une condition initiale nominale
à une autre partant d'une condition initiale légèrement perturbée.

### Diagnostic de stabilité: 

• Système Robuste/Stable :
La distance entre les deux trajectoires doit décroître avec le temps, montrant que le système "oublie" la petite erreur de départ.
La stabilité est confirmée si les deux trajectoires convergent vers le même point d'équilibre.

• Système Sensible/Instable : La distance entre les trajectoires croît avec le temps, indiquant qu'une erreur minuscule s'amplifie rapidement, menant à une divergence.
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
