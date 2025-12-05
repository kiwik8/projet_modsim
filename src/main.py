import dash
from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import numpy as np

from computation import phase, perturbation
from chatbot import get_help
from quiz_data import QUIZ_QUESTIONS, get_question, get_total_questions
from quiz_callbacks import register_quiz_callbacks

COEFFICIENT_RANGE = (-5, 5)

# Initialiser l'application avec un thème Bootstrap
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.FLATLY, 
    '/assets/animations.css',
    '/assets/quiz-animations.css'
])


# Définir le layout principal
app.layout = dbc.Container([
    
    # En-tête
    dbc.Row([
        dbc.Col([
            html.H1("Visualisation de la stabilité des systèmes dynamiques",
                    className="text-center mb-4"),
            html.Hr()
        ], width=12)
    ]),
    
    # Section de contrôle (Sidebar)
    dbc.Row([
        # Colonne des contrôles
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Paramètres du système"),
                dbc.CardBody([
                    # Dropdown pour scénarios prédéfinis
                    html.Label("Scénario prédéfini:"),
                    dcc.Dropdown(
                        id='scenario-dropdown',
                        options=[
                            {'label': 'Aucun', 'value': 'none'},
                            {'label': "Stabilité d'un navire", 'value': 'ship'},
                            {'label': "Porte automatique", 'value': 'door'},
                        ],
                        value='none'
                    ),
                    html.Hr(),
                    
                    # Sliders pour coefficients
                    html.Label("Coefficient a₁:"),
                    dcc.Slider(id='a1-slider', min=COEFFICIENT_RANGE[0], max=COEFFICIENT_RANGE[1], step=0.1, value=0,
                              marks={i: str(i) for i in range(COEFFICIENT_RANGE[0], COEFFICIENT_RANGE[1]+1)}),
                    # entrée manuelle pour a1
                    dcc.Input(id='a1-input', type='number', value=0, step=0.1,
                              min=COEFFICIENT_RANGE[0], max=COEFFICIENT_RANGE[1], style={'width': '100%', 'marginTop': '6px'}),
                    
                    html.Label("Coefficient a₂:"),
                    dcc.Slider(id='a2-slider', min=COEFFICIENT_RANGE[0], max=COEFFICIENT_RANGE[1], step=0.1, value=0,
                              marks={i: str(i) for i in range(COEFFICIENT_RANGE[0], COEFFICIENT_RANGE[1]+1)}),
                    # entrée manuelle pour a2
                    dcc.Input(id='a2-input', type='number', value=0, step=0.1,
                              min=COEFFICIENT_RANGE[0], max=COEFFICIENT_RANGE[1], style={'width': '100%', 'marginTop': '6px'}),
                    
                    # Contrôles pour conditions initiales (cachés par défaut)
                    html.Div(id='initial-cond', style={'display': 'none'}, children=[
                        html.Hr(),
                        html.Label("Condition initiale x₀:"),
                        dcc.Slider(id='x0-slider', min=COEFFICIENT_RANGE[0], max=COEFFICIENT_RANGE[1], step=0.1, value=1.0,
                                    marks={i: str(i) for i in range(COEFFICIENT_RANGE[0], COEFFICIENT_RANGE[1]+1)}),
                        dcc.Input(id='x0-input', type='number', value=1.0, step=0.1,
                                    min=COEFFICIENT_RANGE[0], max=COEFFICIENT_RANGE[1], style={'width': '100%', 'marginTop': '6px'}),
                        html.Label("Condition initiale y₀:"),
                        dcc.Slider(id='y0-slider', min=COEFFICIENT_RANGE[0], max=COEFFICIENT_RANGE[1], step=0.1, value=0.0, marks={i: str(i) for i in range(COEFFICIENT_RANGE[0], COEFFICIENT_RANGE[1]+1)}),
                        dcc.Input(id='y0-input', type='number', value=0.0, step=0.1, min=COEFFICIENT_RANGE[0], max=COEFFICIENT_RANGE[1], style={'width': '100%', 'marginTop': '6px'}),
                     ]),
                    
                    html.Hr(),
                    
                    # Sélection du type de visualisation
                    html.Label("Type de visualisation:"),
                    dcc.RadioItems(
                        id='viz-radio',
                        options=[
                            {'label': ' Portrait de phase', 'value': 'phase'},
                            {'label': ' Fonction de Lyapunov', 'value': 'lyapunov'},
                            {'label': ' Trajectoire perturbée', 'value': 'perturbed'}
                        ],
                        value='phase',
                        labelStyle={'display': 'block'}
                    )
                ])
            ], className="mb-3")
        ], width=3),
        
        # Colonne principale de visualisation
        dbc.Col([
            html.Div(id='card-phase', children=[
                dbc.Card([
                    dbc.CardHeader("Portrait de phase et trajectoires"),
                    dbc.CardBody([
                        dcc.Graph(id='phase-portrait')
                    ])
                ], className="mb-3")
            ]),
            html.Div(id='card-lyapunov', children=[
                dbc.Card([
                    dbc.CardHeader("Fonction de Lyapunov"),
                    dbc.CardBody([
                        dcc.Graph(id='lyapunov-plot', style={'height': '600px'})
                    ])
                ], className="mb-3")
            ]),
            html.Div(id='card-time', children=[
                dbc.Card([
                    dbc.CardHeader("Stabilité d'une trajectoire"),
                    dbc.CardBody([
                        dcc.Graph(id='stability-trajectory', style={'height': '600px'})
                    ])
                ], className="mb-3")

            ]),
            html.Div(id='scenario-viz-container', style={'display': 'none'}, children=[
                dbc.Card([
                    dbc.CardHeader("Visualisation du Scénario", className="text-white bg-primary"),
                    dbc.CardBody([
                        dcc.Graph(id='scenario-animation', style={'height': '400px'})
                    ])
                ], className="mb-3")
            ])
        ], width=9)
    ]),
    
    html.Hr(),
    
    # Section pédagogique
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Explications"),
                dbc.CardBody([
                    html.Div(id='explanation-text')
                ])
            ])
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Professeur Einstein vous explique"),
                dbc.CardBody([
                    dbc.Row([
                        # Colonne Einstein + bulle de pensée
                        dbc.Col([
                            html.Div([
                                html.Img(
                                    id='einstein-avatar',
                                    src='/assets/Albert-Einstein-Transparent.png',
                                    className='einstein-idle',
                                    style={
                                        'width': '180px',
                                        'display': 'block',
                                        'margin': '0 auto'
                                    }
                                ),
                                html.Div(id='thinking-dots', children='', style={
                                    'textAlign': 'center',
                                    'height': '40px',
                                    'marginTop': '10px',
                                    'color': '#6c757d'
                                })
                            ], style={'textAlign': 'center'})
                        ], width=3),
                        
                        # Colonne bulle de dialogue
                        dbc.Col([
                            html.Div([
                                html.Label("Que puis-je vous expliquer ?", style={'fontWeight': 'bold', 'marginBottom': '12px'}),
                                html.Div([
                                    dbc.Button('Rappel théorique', id='btn-theory', n_clicks=0, color='info', size='lg', className='me-2 mb-2 help-button', style={'minWidth': '200px'}),
                                    dbc.Button('Explication du scénario', id='btn-scenario', n_clicks=0, color='primary', size='lg', className='me-2 mb-2 help-button', style={'minWidth': '200px'}),
                                    dbc.Button('Détails techniques', id='btn-detail', n_clicks=0, color='secondary', size='lg', className='mb-2 help-button', style={'minWidth': '200px'}),
                                ], className='d-flex flex-wrap'),
                                html.Hr(style={'margin': '20px 0'}),
                                # Bulle de dialogue
                                html.Div(id='help-output', children=[
                                    html.P("Sélectionnez un bouton ci-dessus pour obtenir des explications.", 
                                           style={'fontStyle': 'italic', 'color': '#6c757d'})
                                ], className='bubble-appear', style={
                                    'backgroundColor': '#f8f9fa',
                                    'border': '3px solid #dee2e6',
                                    'borderRadius': '20px',
                                    'padding': '20px',
                                    'minHeight': '200px',
                                    'position': 'relative',
                                    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
                                })
                            ])
                        ], width=9)
                    ])
                ])
            ], style={'border': '2px solid #e9ecef'})
        ], width=12)
    ]),
    
    html.Hr(),
    
    # Section Quiz
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Quiz de Stabilité"),
                dbc.CardBody([
                    html.P("Testez vos connaissances avec 10 questions sur la stabilité des systèmes dynamiques.", 
                           className='mb-3'),
                    html.Div([
                        dbc.Button(
                            "Lancer le Quiz",
                            id='start-quiz-btn',
                            color='primary',
                            size='lg',
                            style={'width': '100%'}
                        )
                    ], className='d-grid'),
                    html.Div(id='quiz-score-display', className='text-center mt-3', style={'fontSize': '1.2em'})
                ])
            ])
        ], width=12)
    ]),
    
    # Modal du Quiz
    dbc.Modal([
        dbc.ModalHeader([
            html.Div([
                html.Span(id='quiz-question-number', style={'fontSize': '1.1em', 'fontWeight': 'bold'}),
                html.Div(id='quiz-timer-bar', className='quiz-timer-bar', style={
                    'height': '6px',
                    'backgroundColor': '#28a745',
                    'marginTop': '10px',
                    'borderRadius': '3px'
                })
            ], style={'width': '100%'})
        ]),
        dbc.ModalBody([
            # Audio de tick-tac (avec clé dynamique pour forcer reset)
            html.Audio(
                id='quiz-audio',
                key='audio-default',
                src='/assets/tictacboum.mp3',
                autoPlay=False,
                style={'display': 'none'}
            ),
            # Audio de réponse (bonne/mauvaise)
            html.Audio(
                id='quiz-answer-audio',
                key='answer-audio-default',
                autoPlay=False,
                style={'display': 'none'}
            ),
            # Container pour animation Einstein
            html.Div([
                html.Img(
                    id='quiz-einstein-img',
                    src='/assets/Albert-Einstein-Transparent.png',
                    style={
                        'width': '150px',
                        'display': 'block',
                        'margin': '0 auto 20px auto'
                    }
                )
            ], id='quiz-einstein-container', style={'textAlign': 'center'}),
            # Question
            html.H4(id='quiz-question-text', className='text-center mb-4'),
            # Boutons Vrai/Faux
            html.Div([
                dbc.Button(
                    "VRAI",
                    id='quiz-btn-true',
                    color='success',
                    size='lg',
                    className='me-3',
                    style={'minWidth': '150px'}
                ),
                dbc.Button(
                    "FAUX",
                    id='quiz-btn-false',
                    color='danger',
                    size='lg',
                    style={'minWidth': '150px'}
                )
            ], className='d-flex justify-content-center mb-3'),
            # Explication (cachée initialement)
            html.Div(id='quiz-explanation', className='mt-4', style={'display': 'none'})
        ], id='quiz-modal-body'),
        dbc.ModalFooter([
            dbc.Button("Question suivante", id='quiz-next-btn', color='primary', style={'display': 'none'}),
            dbc.Button("Voir les résultats", id='quiz-finish-btn', color='warning', style={'display': 'none'}),
            dbc.Button("Fermer", id='close-quiz-modal', color='secondary')
        ])
    ], id='quiz-modal', size='xl', is_open=False, backdrop='static', keyboard=False),
    
    # Stores pour le quiz
    dcc.Store(id='quiz-state', data={'current_question': 0, 'score': 0, 'answered': False, 'total': get_total_questions()}),
    dcc.Store(id='quiz-timer-start', data=0),
    dcc.Interval(id='quiz-interval', interval=100, disabled=False),

], fluid=True)

@app.callback(
    Output('scenario-viz-container', 'style'),
    Output('scenario-animation', 'figure'),
    [Input('scenario-dropdown', 'value'),
     Input('a1-slider', 'value'),
     Input('a2-slider', 'value'),
     Input('x0-slider', 'value'),
     Input('y0-slider', 'value')]
)
def update_scenario_visualization(scenario, a1, a2, x0, y0):
    if scenario == 'none' or scenario is None:
        return {'display': 'none'}, go.Figure()
    
    # Simulation commune
    t, x, y, _, _, _ = perturbation.calcul_perturbation(
        float(a1), float(a2), float(x0), float(y0), eps=0, t_max=15.0, dt=0.1
    )
    
    frames = []
    layout_settings = {}
    initial_data = []

    # --- SCÉNARIO 1 : SHIP ---
    if scenario == 'ship':
        # Shape
        boat_x = np.array([-2, -1.5, 1.5, 2, 1.5, -1.5, -2])
        boat_y = np.array([1, -1, -1, 1, 1, 1, 1])
        mast_x = np.array([0, 0])
        mast_y = np.array([1, 4])
        
        for k in range(len(t)):
            angle = x[k]
            c, s = np.cos(angle), np.sin(angle)
            # Rotation
            bx_rot = boat_x * c - boat_y * s
            by_rot = boat_x * s + boat_y * c
            mx_rot = mast_x * c - mast_y * s
            my_rot = mast_x * s + mast_y * c
            
            frames.append(go.Frame(data=[
                go.Scatter(x=bx_rot, y=by_rot, mode='lines', fill='toself', line=dict(color='brown', width=3)),
                go.Scatter(x=mx_rot, y=my_rot, mode='lines', line=dict(color='black', width=4))
            ], name=str(k)))

        # Initial frame
        angle0 = x[0]
        c0, s0 = np.cos(angle0), np.sin(angle0)
        initial_data = [
            go.Scatter(x=boat_x*c0 - boat_y*s0, y=boat_x*s0 + boat_y*c0, mode='lines', fill='toself', line=dict(color='brown', width=3), name='Coque'),
            go.Scatter(x=mast_x*c0 - mast_y*s0, y=mast_x*s0 + mast_y*c0, mode='lines', line=dict(color='black', width=4), name='Mât')
        ]
        
        layout_settings = dict(
            title="Simulation : Navire qui tangue",
            xaxis=dict(range=[-6, 6], visible=False),
            yaxis=dict(range=[-6, 6], visible=False),
            shapes=[dict(type="rect", x0=-10, y0=-6, x1=10, y1=0, fillcolor="rgba(0, 0, 255, 0.2)", line_width=0, layer="below")]
        )

    # --- SCÉNARIO 2 : DOOR ---
    elif scenario == 'door':
        L = 4
        # Vue de dessus
        for k in range(len(t)):
            angle = x[k]
            door_end_x = L * np.cos(angle)
            door_end_y = L * np.sin(angle)
            
            frames.append(go.Frame(data=[
                go.Scatter(x=[0, door_end_x], y=[0, door_end_y], mode='lines', line=dict(color='blue', width=6))
            ], name=str(k)))
            
        initial_data = [
            go.Scatter(x=[0, L*np.cos(x[0])], y=[0, L*np.sin(x[0])], mode='lines', line=dict(color='blue', width=6), name='Porte')
        ]
        
        layout_settings = dict(
            title="Simulation : Vue de dessus de la porte",
            xaxis=dict(range=[-2, 5], visible=False),
            yaxis=dict(range=[-2, 5], visible=False),
            shapes=[

                # Wall
                dict(type="line", x0=0, y0=-2, x1=0, y1=5, line=dict(color="black", width=4)),
                # Le cadre (position fermée)
                dict(type="line", x0=0, y0=0, x1=L, y1=0, line=dict(color="grey", width=2, dash="dot")),
                # L'arc de cercle au sol
                dict(type="path", path=f"M {L} 0 Q {L} {L} 0 {L}", line=dict(color="lightgrey")),
                # La charnière
                dict(type="circle", x0=-0.2, y0=-0.2, x1=0.2, y1=0.2, fillcolor="black")
            ]
        )

    # Création de la figure finale
    fig = go.Figure(
        data=initial_data,
        layout=go.Layout(
            **layout_settings,
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="▶ Lecture",
                            method="animate",
                            args=[None, {"frame": {"duration": 50, "redraw": True},
                                         "fromcurrent": True, "transition": {"duration": 0}}])]
            )],
            plot_bgcolor="white"
        ),
        frames=frames
    )

    return {'display': 'block'}, fig


@app.callback(
    Output('stability-trajectory', 'figure'),
    [Input('a1-slider', 'value'),
     Input('a2-slider', 'value'),
     Input('x0-slider', 'value'),
     Input('y0-slider', 'value')],
)
def update_stability_trajectory(a1, a2, x0, y0):
    # calcul des trajectoires nominale et perturbée
    t, x, y, x_p, y_p, dist = perturbation.calcul_perturbation(
        float(a1), float(a2), float(x0), float(y0), eps=1e-3, t_max=10.0, dt=0.05
    )

    # deux sous-graphes : 1) portrait de phase, 2) séparation dans le temps (avec y secondaire)
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.12,
        specs=[[{"type": "xy"}], [{"type": "xy", "secondary_y": True}]],
        subplot_titles=("Portrait de phase — trajectoire vs perturbée", "Séparation des trajectoires dans le temps")
    )

    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Nominale', line=dict(color='royalblue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=x_p, y=y_p, mode='lines', name='Perturbée', line=dict(color='firebrick', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='markers', name='CI nominale', marker=dict(color='royalblue', size=8)), row=1, col=1)
    fig.add_trace(go.Scatter(x=[x_p[0]], y=[y_p[0]], mode='markers', name='CI perturbée', marker=dict(color='firebrick', size=8)), row=1, col=1)
    fig.update_xaxes(title_text='x', row=1, col=1, range=COEFFICIENT_RANGE)
    fig.update_yaxes(title_text='y', row=1, col=1, range=COEFFICIENT_RANGE)

    fig.add_trace(go.Scatter(x=t, y=dist, mode='lines', name='||Δ||(t)', line=dict(color='royalblue')), row=2, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=t, y=np.log10(dist + 1e-15), mode='lines', name='log10(||Δ||)', line=dict(color='firebrick', dash='dot')), row=2, col=1, secondary_y=True)
    fig.update_xaxes(title_text='t', row=2, col=1)
    fig.update_yaxes(title_text='distance', row=2, col=1, secondary_y=False)
    fig.update_yaxes(title_text='log10(distance)', row=2, col=1, secondary_y=True)

    fig.update_layout(
        height=700,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig


# Callback pour le portrait de phase
@app.callback(
    Output('phase-portrait', 'figure'),
    [Input('a1-slider', 'value'),
     Input('a2-slider', 'value')],
)
def update_phase_portrait(a1, a2):
    
    X, Y, U, V = phase.calculer_champ(a1, a2, COEFFICIENT_RANGE, COEFFICIENT_RANGE) # calcul du champ de vecteurs
    fig = ff.create_quiver(X, Y, U, V)
    
    # ajout du champ
    for i in range(len(X)):
        for j in range(len(X[0])):
            fig.add_trace(go.Scatter(
                x=[X[i,j], X[i,j] + 0.3*U[i,j]], 
                y=[Y[i,j], Y[i,j] + 0.3*V[i,j]],
                mode='lines',
                line=dict(color='lightblue', width=1),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # quelques trajectoires
    conditions_initiales = [[2, 1], [-2, 1], [1, -2], [-1, -1]]
    for x0, y0 in conditions_initiales:
        x_traj, y_traj = phase.calculer_trajectoire(a1, a2, x0, y0)
        fig.add_trace(go.Scatter(
            x=x_traj, y=y_traj,
            mode='lines',
            line=dict(width=2),
            name=f'CI: ({x0},{y0})'
        ))
    
    # point d'équilibre
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        marker=dict(color='red', size=10, symbol='x'),
        name='Équilibre'
    ))
    
    fig.update_layout(
        xaxis_title='x',
        yaxis_title='dx/dt',
        xaxis=dict(range=COEFFICIENT_RANGE),
        yaxis=dict(range=COEFFICIENT_RANGE),
        height=400
    )
    
    return fig

# Sync A1 Slider with A1 input
@app.callback(
    Output('a1-slider', 'value'),
    Output('a1-input', 'value'),
    Input('a1-slider', 'value'),
    Input('a1-input', 'value'),
    Input('scenario-dropdown', 'value')
)
def sync_a1(slider_val, input_val, scenario):
    ctx = dash.callback_context
    # valeur par défaut / initialisation
    if not ctx.triggered:
        try:
            v = float(slider_val)
        except (TypeError, ValueError):
            v = 0.0
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == 'scenario-dropdown':
            if scenario == 'ship' or scenario == 'door':
                v = -2
            else:
                try:
                    v = float(slider_val)
                except (TypeError, ValueError):
                    v = 0.0
        elif trigger == 'a1-input':
            try:
                v = float(input_val)
            except (TypeError, ValueError):
                v = 0.0
        else:
            try:
                v = float(slider_val)
            except (TypeError, ValueError):
                v = 0.0

    v = max(COEFFICIENT_RANGE[0], min(COEFFICIENT_RANGE[1], v))
    v = round(v, 3)
    return v, v

# Sync A2 Slider with A2 input
@app.callback(
    Output('a2-slider', 'value'),
    Output('a2-input', 'value'),
    Input('a2-slider', 'value'),
    Input('a2-input', 'value'),
    Input('scenario-dropdown', 'value')
)
def sync_a2(slider_val, input_val, scenario):
    ctx = dash.callback_context
    if not ctx.triggered:
        try:
            v = float(slider_val)
        except (TypeError, ValueError):
            v = 0.0
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == 'scenario-dropdown':
            if scenario == 'ship':
                v = -0.5
            elif scenario == 'door':
                v = -1.0
            else:
                try:
                    v = float(slider_val)
                except (TypeError, ValueError):
                    v = 0.0
        elif trigger == 'a2-input':
            try:
                v = float(input_val)
            except (TypeError, ValueError):
                v = 0.0
        else:
            try:
                v = float(slider_val)
            except (TypeError, ValueError):
                v = 0.0

    v = max(COEFFICIENT_RANGE[0], min(COEFFICIENT_RANGE[1], v))
    v = round(v, 3)
    return v, v


# Visibility
@app.callback(
    Output('lyapunov-plot', 'figure'),
    [Input('a1-slider', 'value'),
     Input('a2-slider', 'value'),]
)

def update_lyapunov(a1,a2):
    # Grille 
    x = np.linspace(COEFFICIENT_RANGE[0], COEFFICIENT_RANGE[1], 80)
    y = np.linspace(COEFFICIENT_RANGE[0], COEFFICIENT_RANGE[1], 80)
    X, Y = np.meshgrid(x, y)

    # Fonction Lyapunov simple
    V = X**2 + Y**2

    # Dérivée Lyapunov
    Vdot = 2*X*Y + 2*Y*(a1*X + a2*Y)

    fig = go.Figure()

    # Solution contre a1 = -1 et a2 = 0 qui montrait la heatmap full rouge alors que Vdot = 0
    span = max(abs(np.min(Vdot)), abs(np.max(Vdot)))
    if span == 0:
        span = 1e-12  # éviter division par zéro

    # Heatmap, Rouge = instable, Bleu = stable, 0 = constant (changement de signe) 
    fig.add_trace(go.Contour(
        x=x,
        y=y,
        z=Vdot,
        colorscale='RdBu',
        zmin=-span,
        zmax=span,
        contours=dict(showlines=False),
        colorbar=dict(title='dV/dt'),
        name='dV/dt'
    ))

    # Contours de V(x,y) = x^2 + y^2
    fig.add_trace(go.Contour(
        x=x,
        y=y,
        z=V,
        contours=dict(
            coloring='none',
            showlines=True
        ),
        line=dict(
            color='black',
            width=1   
        ),
        showscale=False,
        name='V(x,y)'
    ))

    fig.update_layout(
        xaxis=dict(
            title="x",
            linecolor="black",    
            linewidth=3,          
            mirror=True,         
        ),
        yaxis=dict(
            title="y",
            linecolor="black",     
            linewidth=3,
            mirror=True

        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )   

    return fig

@app.callback(
    Output('card-phase', 'style'),
    Output('card-lyapunov', 'style'),
    Output('card-time', 'style'),
    Output('initial-cond', 'style'),
    Input('viz-radio', 'value'),
)
def show_only(selected):
    show = {'display': 'block'}
    hide = {'display': 'none'}

    if selected == 'phase':
        return show, hide, hide, hide
    elif selected == 'lyapunov':
        return hide, show, hide, hide
    elif selected == 'stability-trajectory':
        return hide, hide, show, hide
    # 'perturbed' ou 'stability' : afficher la carte "Stabilité" et les contrôles initiales
    return hide, hide, show, show


# Sync x0 Slider with x0 input
@app.callback(
    Output('x0-slider', 'value'),
    Output('x0-input', 'value'),
    Input('x0-slider', 'value'),
    Input('x0-input', 'value'),
)
def sync_x0(slider_val, input_val):
    ctx = dash.callback_context
    if not ctx.triggered:
        try:
            v = float(slider_val)
        except (TypeError, ValueError):
            v = 1.0
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == 'x0-input':
            try:
                v = float(input_val)
            except (TypeError, ValueError):
                v = 1.0
        else:
            try:
                v = float(slider_val)
            except (TypeError, ValueError):
                v = 1.0

    v = max(COEFFICIENT_RANGE[0], min(COEFFICIENT_RANGE[1], v))
    v = round(v, 3)
    return v, v

# Sync y0 Slider with y0 input
@app.callback(
    Output('y0-slider', 'value'),
    Output('y0-input', 'value'),
    Input('y0-slider', 'value'),
    Input('y0-input', 'value'),
)

def sync_y0(slider_val, input_val):
    ctx = dash.callback_context
    if not ctx.triggered:
        try:
            v = float(slider_val)
        except (TypeError, ValueError):
            v = 0.0
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == 'y0-input':
            try:
                v = float(input_val)
            except (TypeError, ValueError):
                v = 0.0
        else:
            try:
                v = float(slider_val)
            except (TypeError, ValueError):
                v = 0.0

    v = max(COEFFICIENT_RANGE[0], min(COEFFICIENT_RANGE[1], v))
    v = round(v, 3)
    return v, v




# Explanations
@app.callback(
    Output('explanation-text', 'children'),
    Input('viz-radio', 'value'),
    Input('a1-slider', 'value'),
    Input('a2-slider', 'value'),
    Input('x0-slider', 'value'),
    Input('y0-slider', 'value'),
    Input('scenario-dropdown', 'value')
)
def update_explanations(viz_type, a1, a2, x0, y0, scenario):
    if scenario == 'spring':
        content = dcc.Markdown("""### Scénario voiture suspension
On modélise la suspension d’une voiture qui passe sur un dos d’âne par un système masse–ressort–amortisseur.
- *x* représente le déplacement vertical de la caisse par rapport à sa position d’équilibre.
- *y = ẋ * représente la vitesse verticale de la caisse.
- Le coefficient *a₁ < 0* correspond à la raideur de la suspension (ressort) : plus a₁ est grand, plus la caisse est “tirée” vers sa position d’équilibre.
- Le coefficient *a₂ < 0* correspond à l’amortisseur : plus a₂ est grand, plus les oscillations sont vite dissipées.
        """)
        return dbc.Alert(content, color="info")
    if viz_type == 'phase':
        stab = ""
        if a1 < 0 and a2 < 0:
            stab = "Stable Asymptotiquement"
        elif a1 < 0 and a2 == 0:
            stab = "Stable Simple"
        elif a1 >= 0:
            stab = "Instable"

        content = dcc.Markdown(f"""
        ### Portrait de phase
        Le portrait de phase montre l’évolution des variables d’état **(x, y)** dans le plan.

        - Avec a₁={a1}, a₂={a2}, le système est : {stab}
        - **a₁ < 0, a₂ < 0** → trajectoires convergent vers l’origine (*stabilité asymptotique*).  
        - **a₁ < 0, a₂ = 0** → oscillations permanentes (*stabilité simple*).  
        - **a₁ >= 0** → divergence (*instabilité*).
        """)
        return dbc.Alert(content, color="info")
    elif viz_type == 'lyapunov':
        content = dcc.Markdown("""
        ### Fonction de Lyapunov
        La fonction candidate est **V(x,y) = x² + y²**.

        - Les **contours noirs** représentent les niveaux d’énergie.  
        - La **heatmap** colore la dérivée dV/dt :  
          - 🔵 dV/dt < 0 → énergie décroît → stabilité asymptotique  
          - 🔴 dV/dt > 0 → énergie croît → instabilité locale  
          - ⚪ dV/dt = 0 → énergie conservée → oscillations permanentes
        """)
        return dbc.Alert(content, color="info")
    elif viz_type == 'perturbed':
        content = dcc.Markdown(f"""
        ### Trajectoire perturbée
        On compare une trajectoire nominale (CI: x₀={x0}, y₀={y0}) avec une trajectoire légèrement perturbée.

        - Si les deux trajectoires restent proches → **stabilité**  
        - Si elles divergent rapidement → **instabilité**  
        - Le graphe du bas montre la distance ||Δ||(t) et son log10 :  
          - 📉 Décroissance → stabilité asymptotique  
          - ➖ Constante → stabilité simple  
          - 📈 Croissance → instabilité
        """)
        return dbc.Alert(content, color="info")
    
    return dbc.Alert("Sélectionne une visualisation pour voir les explications.", color="secondary")


# Assistant pédagogique callback avec animations dynamiques
@app.callback(
    Output('help-output', 'children'),
    Output('thinking-dots', 'children'),
    Output('einstein-avatar', 'className'),
    Input('btn-theory', 'n_clicks'),
    Input('btn-scenario', 'n_clicks'),
    Input('btn-detail', 'n_clicks'),
    State('viz-radio', 'value'),
    State('scenario-dropdown', 'value')
)
def handle_help(n_theory, n_scenario, n_detail, viz_type, scenario):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return (html.P("Sélectionnez un bouton ci-dessus pour obtenir des explications.", 
                      style={'fontStyle': 'italic', 'color': '#6c757d'}), 
                '', 
                'einstein-idle')
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'btn-theory':
        help_type = 'theory'
    elif button_id == 'btn-scenario':
        help_type = 'scenario'
    elif button_id == 'btn-detail':
        help_type = 'detail'
    else:
        return ('', '', 'einstein-idle')
    
    # Phase de réflexion avec points animés
    thinking_dots = html.Div([
        html.Span('●', className='thinking-dot'),
        html.Span('●', className='thinking-dot'),
        html.Span('●', className='thinking-dot')
    ])
    
    # Récupérer le contenu depuis help_content.py
    help_data = get_help(help_type, scenario=scenario)
    
    # Formater la réponse dans une bulle stylée avec animation
    formatted_response = html.Div([
        html.H5(help_data['title'], style={'marginBottom': '15px'}),
        dcc.Markdown(help_data['content'], mathjax=True)
    ], className='bubble-appear')
    
    return formatted_response, '', 'einstein-talking'


register_quiz_callbacks(app)


if __name__ == '__main__':
    app.run(debug=True)