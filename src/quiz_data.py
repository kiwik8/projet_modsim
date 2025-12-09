QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Pour le scénario du Navire, si le coefficient a1 est positif, le navire est instable.",
        "answer": True,
        "explanation": "a1 = -C/I. Si a1 > 0, alors C < 0, ce qui signifie que le centre de gravité est trop haut et le navire chavire."
    },
    {
        "id": 2,
        "question": "Si le discriminant Δ est négatif, la Porte automatique est en régime sous-amorti (elle claque).",
        "answer": True,
        "explanation": "Le régime sous-amorti est défini par Δ < 0, ce qui provoque l'oscillation et le claquement."
    },
    {
        "id": 3,
        "question": "Un Portrait de Phase montrant des spirales rentrantes indique un système asymptotiquement stable.",
        "answer": True,
        "explanation": "Les spirales rentrantes correspondent à des valeurs propres complexes avec des parties réelles négatives, typiques d'un foyer stable."
    },
    {
        "id": 4,
        "question": "L'objectif du réglage d'un Groom (amortisseur) de porte est d'atteindre le régime critique, où le discriminant Δ = 0.",
        "answer": True,
        "explanation": "Le régime critique (Δ = 0) est le réglage parfait qui ferme la porte le plus vite possible sans qu'elle ne claque."
    },
    {
        "id": 5,
        "question": "La stabilité du navire dépend du coefficient a2 et sa vitesse d'arrêt dépend uniquement de a1.",
        "answer": False,
        "explanation": "Faux. C'est l'inverse. La stabilité du navire dépend du coefficient a1 (stabilité statique) et sa vitesse d'arrêt dépend uniquement de a2 (frottement)."
    },
    {
        "id": 6,
        "question": "Un système dont une valeur propre est λ = 0.5 est stable asymptotiquement.",
        "answer": False,
        "explanation": "Une partie réelle positive (0.5 > 0) indique que le système est instable."
    },
    {
        "id": 7,
        "question": "Si la distance Δ(t) entre la trajectoire nominale et perturbée augmente exponentiellement, le système est stable.",
        "answer": False,
        "explanation": "Faux. Une distance qui grandit exponentiellement indique une grande sensibilité aux conditions initiales, caractéristique d'un système instable."
    },
    {
        "id": 8,
        "question": "L'analyse de la trajectoire perturbée sert à tester la robustesse du système face à une erreur de condition initiale.",
        "answer": True,
        "explanation": "Exact. On vérifie si une petite erreur de départ est 'oubliée' par le système ou si elle s'amplifie."
    },
    {
        "id": 9,
        "question": "Si la courbe de séparation des trajectoires tend vers 0 au cours du temps, le système est asymptotiquement stable.",
        "answer": True,
        "explanation": "Exact. Cela signifie que la trajectoire perturbée finit par rejoindre la trajectoire nominale à l'équilibre."
    },
    {
        "id": 10,
        "question": "Un Nœud instable (flèches sortantes) apparaît lorsque les valeurs propres sont réelles et négatives.",
        "answer": False,
        "explanation": "Faux. Un Nœud instable est créé par des valeurs propres réelles et positives. Les valeurs négatives créent un Nœud stable."
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
