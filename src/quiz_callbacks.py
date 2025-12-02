"""
Callbacks pour le système de quiz interactif
"""
import dash
from dash import html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from quiz_data import QUIZ_QUESTIONS, get_total_questions
import time


def register_quiz_callbacks(app):
    """Enregistre tous les callbacks liés au quiz"""
    
    # Ouvrir le modal et initialiser/naviguer dans le quiz
    @app.callback(
        Output('quiz-modal', 'is_open'),
        Output('quiz-state', 'data'),
        Output('quiz-question-text', 'children'),
        Output('quiz-question-number', 'children'),
        Output('quiz-audio', 'key'),  # Nouvelle clé pour forcer reset
        Output('quiz-audio', 'autoPlay'),
        Output('quiz-audio', 'src'),
        Output('quiz-timer-bar', 'style'),
        Output('quiz-einstein-img', 'className'),
        Output('quiz-modal-body', 'style'),
        Output('quiz-explanation', 'style'),
        Output('quiz-btn-true', 'disabled'),
        Output('quiz-btn-false', 'disabled'),
        Output('quiz-next-btn', 'style'),
        Output('quiz-finish-btn', 'style'),
        Output('quiz-timer-start', 'data'),
        Input('start-quiz-btn', 'n_clicks'),
        Input('close-quiz-modal', 'n_clicks'),
        Input('quiz-next-btn', 'n_clicks'),
        Input('quiz-finish-btn', 'n_clicks'),
        State('quiz-modal', 'is_open'),
        State('quiz-state', 'data'),
        prevent_initial_call=True
    )
    def toggle_quiz_modal(start_clicks, close_clicks, next_clicks, finish_clicks, is_open, quiz_state):
        button_id = ctx.triggered_id
        
        # Styles par défaut
        timer_style_running = {
            'height': '6px',
            'backgroundColor': '#28a745',
            'marginTop': '10px',
            'borderRadius': '3px',
            'width': '100%'
        }
        timer_style_stopped = {'height': '6px', 'width': '0%'}
        modal_body_normal = {'backgroundColor': 'white'}
        explanation_hidden = {'display': 'none'}
        button_hidden = {'display': 'none'}
        button_visible = {'display': 'inline-block'}
        
        if button_id == 'start-quiz-btn':
            # Démarrer un nouveau quiz
            quiz_state = {
                'current_question': 0,
                'score': 0,
                'answered': False,
                'total': get_total_questions()
            }
            question = QUIZ_QUESTIONS[0]
            return (
                True,  # Ouvrir modal
                quiz_state,
                question['question'],
                f"Question 1 / {get_total_questions()}",
                f"audio-q0-{time.time()}",  # Clé unique pour forcer reset
                True,   # Lancer audio
                '/assets/tictacboum.mp3',
                timer_style_running,
                'einstein-inflating',
                modal_body_normal,
                explanation_hidden,
                False,  # Activer bouton Vrai
                False,  # Activer bouton Faux
                button_hidden,
                button_hidden,
                time.time()  # Timestamp de départ
            )
        
        elif button_id == 'quiz-next-btn':
            # Passer à la question suivante - RESET complet
            next_idx = quiz_state['current_question'] + 1
            if next_idx < quiz_state['total']:
                quiz_state['current_question'] = next_idx
                quiz_state['answered'] = False
                question = QUIZ_QUESTIONS[next_idx]
                return (
                    True,
                    quiz_state,
                    question['question'],
                    f"Question {next_idx + 1} / {get_total_questions()}",
                    f"audio-q{next_idx}-{time.time()}",  # NOUVELLE clé pour reset audio
                    True,   # Relancer audio depuis 0
                    '/assets/tictacboum.mp3',
                    timer_style_running,
                    'einstein-inflating',
                    modal_body_normal,
                    explanation_hidden,
                    False,  # Réactiver bouton Vrai
                    False,  # Réactiver bouton Faux
                    button_hidden,
                    button_hidden,
                    time.time()  # Nouveau timestamp
                )
        
        elif button_id in ['close-quiz-modal', 'quiz-finish-btn']:
            # Fermer le modal
            return (
                False,
                quiz_state,
                "",
                "",
                "audio-closed",
                False,
                '',
                timer_style_stopped,
                '',
                modal_body_normal,
                explanation_hidden,
                False,
                False,
                button_hidden,
                button_hidden,
                0
            )
        
        return (is_open, quiz_state, "", "", "audio-default", False, '', timer_style_stopped, '', 
            modal_body_normal, explanation_hidden, False, False, button_hidden, button_hidden, 0)
    
    
    # Gérer le timeout de 7 secondes
    @app.callback(
        Output('quiz-btn-true', 'disabled', allow_duplicate=True),
        Output('quiz-btn-false', 'disabled', allow_duplicate=True),
        Output('quiz-explanation', 'children', allow_duplicate=True),
        Output('quiz-explanation', 'style', allow_duplicate=True),
        Output('quiz-next-btn', 'style', allow_duplicate=True),
        Output('quiz-finish-btn', 'style', allow_duplicate=True),
        Output('quiz-state', 'data', allow_duplicate=True),
        Output('quiz-einstein-img', 'className', allow_duplicate=True),
        Input('quiz-interval', 'n_intervals'),
        State('quiz-timer-start', 'data'),
        State('quiz-state', 'data'),
        prevent_initial_call=True
    )
    def check_timeout(n_intervals, start_time, quiz_state):
        if not start_time or quiz_state.get('answered', False):
            return dash.no_update
        
        elapsed = time.time() - start_time
        
        # Timeout après 7 secondes
        if elapsed >= 7.0:
            current_q = QUIZ_QUESTIONS[quiz_state['current_question']]
            quiz_state['answered'] = True
            
            # Explication timeout
            expl_style = {
                'display': 'block',
                'padding': '20px',
                'borderRadius': '5px',
                'backgroundColor': '#fff3cd',
                'border': '1px solid #ffc107',
                'marginTop': '20px'
            }
            
            explanation_content = html.Div([
                html.H5("Temps écoulé", style={'color': '#856404', 'marginBottom': '15px'}),
                html.P("La bonne réponse était :"),
                html.H5("VRAI" if current_q['answer'] else "FAUX", 
                        style={'color': '#28a745' if current_q['answer'] else '#dc3545', 'margin': '10px 0'}),
                html.Hr(),
                dcc.Markdown(current_q['explanation'])
            ])
            
            # Bouton suivant ou finir
            is_last = (quiz_state['current_question'] == quiz_state['total'] - 1)
            next_style = {'display': 'none'} if is_last else {'display': 'inline-block'}
            finish_style = {'display': 'inline-block'} if is_last else {'display': 'none'}
            
            return (
                True,  # Désactiver Vrai
                True,  # Désactiver Faux
                explanation_content,
                expl_style,
                next_style,
                finish_style,
                quiz_state,
                ''  # Arrêter animation
            )
        
        return dash.no_update
    
    
    # Gérer les réponses manuelles
    @app.callback(
        Output('quiz-explanation', 'children', allow_duplicate=True),
        Output('quiz-explanation', 'style', allow_duplicate=True),
        Output('quiz-next-btn', 'style', allow_duplicate=True),
        Output('quiz-finish-btn', 'style', allow_duplicate=True),
        Output('quiz-btn-true', 'disabled', allow_duplicate=True),
        Output('quiz-btn-false', 'disabled', allow_duplicate=True),
        Output('quiz-state', 'data', allow_duplicate=True),
        Output('quiz-einstein-img', 'className', allow_duplicate=True),
        Output('quiz-audio', 'autoPlay', allow_duplicate=True),
        Output('quiz-audio', 'src', allow_duplicate=True),
        Output('quiz-timer-start', 'data', allow_duplicate=True),
        Output('quiz-answer-audio', 'src'),
        Output('quiz-answer-audio', 'key'),
        Output('quiz-answer-audio', 'autoPlay'),
        Output('quiz-timer-bar', 'style', allow_duplicate=True),
        Input('quiz-btn-true', 'n_clicks'),
        Input('quiz-btn-false', 'n_clicks'),
        State('quiz-state', 'data'),
        prevent_initial_call=True
    )
    def handle_answer(true_clicks, false_clicks, quiz_state):
        if quiz_state.get('answered', False):
            return dash.no_update
        
        button_id = ctx.triggered_id
        if button_id not in ['quiz-btn-true', 'quiz-btn-false']:
            return dash.no_update
        
        user_answer = (button_id == 'quiz-btn-true')
        current_q = QUIZ_QUESTIONS[quiz_state['current_question']]
        correct = (user_answer == current_q['answer'])
        
        # Mettre à jour le score
        if correct:
            quiz_state['score'] += 1
        
        quiz_state['answered'] = True
        
        # Style de l'explication
        expl_style = {
            'display': 'block',
            'padding': '20px',
            'borderRadius': '5px',
            'backgroundColor': '#d4edda' if correct else '#f8d7da',
            'border': f"1px solid {'#28a745' if correct else '#dc3545'}",
            'marginTop': '20px'
        }
        
        explanation_content = html.Div([
            html.H5("Correct" if correct else "Incorrect", 
                    style={'color': '#28a745' if correct else '#dc3545', 'marginBottom': '15px'}),
            dcc.Markdown(current_q['explanation'])
        ])
        
        # Bouton suivant ou finir
        is_last = (quiz_state['current_question'] == quiz_state['total'] - 1)
        next_style = {'display': 'none'} if is_last else {'display': 'inline-block'}
        finish_style = {'display': 'inline-block'} if is_last else {'display': 'none'}
        
        # Animation Einstein
        if correct:
            einstein_class = 'einstein-celebrate'
        else:
            einstein_class = 'einstein-sad'
        
        # Audio de réponse (limité à 3 secondes)
        answer_audio_src = '/assets/good_answer.mp3#t=0,3' if correct else '/assets/bad_answer.mp3#t=0,3'
        answer_audio_key = f"answer-{time.time()}"
        
        # Arrêter le timer
        timer_stopped = {'height': '6px', 'width': '0%', 'backgroundColor': '#dc3545'}
        
        return (
            explanation_content,
            expl_style,
            next_style,
            finish_style,
            True,  # Désactiver bouton Vrai
            True,  # Désactiver bouton Faux
            quiz_state,
            einstein_class,
            False,  # Arrêter audio timer autoPlay
            '',  # Vider src pour arrêter complètement l'audio
            0,  # Reset timer start (arrêter le compteur)
            answer_audio_src,
            answer_audio_key,
            True,  # Lancer audio de réponse
            timer_stopped
        )
    
    
    # Afficher le score final
    @app.callback(
        Output('quiz-score-display', 'children'),
        Input('quiz-finish-btn', 'n_clicks'),
        State('quiz-state', 'data'),
        prevent_initial_call=True
    )
    def show_final_score(finish_clicks, quiz_state):
        score = quiz_state['score']
        total = quiz_state['total']
        percentage = (score / total) * 100
        
        if percentage >= 80:
            message = "Excellent"
            color = "success"
        elif percentage >= 60:
            message = "Bien"
            color = "info"
        else:
            message = "À améliorer"
            color = "warning"
        
        return dbc.Alert([
            html.H5(f"Score final : {score} / {total}"),
            html.P(f"{message} ({percentage:.0f}%)")
        ], color=color)
