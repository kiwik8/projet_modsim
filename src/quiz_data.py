QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Un point d'équilibre est stable si toutes les trajectoires qui partent près de ce point y restent proches.",
        "answer": True,
        "explanation": "Exact. C'est la définition de la stabilité au sens de Lyapunov : les trajectoires restent dans un voisinage de l'équilibre."
    },
    {
        "id": 2,
        "question": "Si la dérivée de la fonction de Lyapunov V̇(x) est strictement positive, le système est asymptotiquement stable.",
        "answer": False,
        "explanation": "Faux. Si V̇(x) > 0, l'énergie augmente donc le système est INSTABLE. Pour la stabilité asymptotique, il faut V̇(x) < 0."
    },
    {
        "id": 3,
        "question": "Dans un portrait de phase, les trajectoires peuvent se croiser.",
        "answer": False,
        "explanation": "Faux. Le théorème d'unicité des solutions garantit qu'il n'y a qu'une seule trajectoire passant par chaque point (sauf aux points d'équilibre)."
    },
    {
        "id": 4,
        "question": "Un système linéaire ẋ = Ax avec a₁ < 0 et a₂ = 0 présente des oscillations permanentes.",
        "answer": True,
        "explanation": "Exact. Avec a₂ = 0 (pas d'amortissement), l'énergie est conservée et le système oscille indéfiniment autour de l'équilibre."
    },
    {
        "id": 5,
        "question": "La méthode d'Euler explicite est toujours stable numériquement, quel que soit le pas de temps.",
        "answer": False,
        "explanation": "Faux. La méthode d'Euler explicite peut diverger si le pas de temps dt est trop grand. Il faut respecter des conditions de stabilité numérique."
    },
    {
        "id": 6,
        "question": "Pour un système masse-ressort-amortisseur, un amortissement négatif (a₂ > 0) provoque l'instabilité.",
        "answer": True,
        "explanation": "Exact. Un amortissement négatif injecte de l'énergie au lieu d'en dissiper, ce qui fait diverger les oscillations."
    },
    {
        "id": 7,
        "question": "Une fonction de Lyapunov V(x) doit toujours être une forme quadratique.",
        "answer": False,
        "explanation": "Faux. V(x) peut prendre de nombreuses formes. L'important est que V > 0 et V̇ ≤ 0 (ou V̇ < 0 pour stabilité asymptotique)."
    },
    {
        "id": 8,
        "question": "Dans le portrait de phase, si les trajectoires s'enroulent autour de l'origine, le système est stable.",
        "answer": True,
        "explanation": "Exact. Des trajectoires qui convergent en spirale vers l'origine indiquent une stabilité asymptotique (foyer stable)."
    },
    {
        "id": 9,
        "question": "Pour tester la stabilité d'un système non-linéaire, on peut linéariser autour du point d'équilibre.",
        "answer": True,
        "explanation": "Exact. Le théorème de Lyapunov permet d'étudier la stabilité locale d'un système non-linéaire via sa linéarisation (si la partie linéaire n'est pas critique)."
    },
    {
        "id": 10,
        "question": "Un système est dit asymptotiquement stable si les trajectoires convergent vers l'équilibre en temps infini.",
        "answer": True,
        "explanation": "Exact. La stabilité asymptotique implique que lim(t→∞) x(t) = x_eq. C'est plus fort que la simple stabilité."
    }
]

def get_question(question_id):
    """Récupère une question par son ID"""
    for q in QUIZ_QUESTIONS:
        if q["id"] == question_id:
            return q
    return None

def get_total_questions():
    """Retourne le nombre total de questions"""
    return len(QUIZ_QUESTIONS)
