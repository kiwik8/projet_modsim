import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import numpy as np

from computation import phase, perturbation

COEFFICIENT_RANGE = (-5, 5)

# Initialiser l'application avec un thème Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


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
                            {'label': 'Voiture avec suspension (masse-ressort)', 'value': 'spring'},
                            {'label': 'Pendule', 'value': 'pendulum'},
                            {'label': 'Circuit RLC', 'value': 'rlc'}
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
            html.Div(id='card-car-animation', children=[
                dbc.Card([
                    dbc.CardHeader("Animation de la voiture"),
                    dbc.CardBody([
                        dcc.Graph(id='car-animation', style={'height': '500px'})
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
    ])
    
], fluid=True)


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
            if scenario == 'spring':
                v = -1.5
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
            if scenario == 'spring':
                v = -0.8
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
    Output('card-car-animation', 'style'),
    Input('viz-radio', 'value'),
    Input('scenario-dropdown', 'value')
)

def show_only(selected, scenario):
    show = {'display': 'block'}
    hide = {'display': 'none'}

    show_anim = show if scenario == 'spring' else hide

    if selected == 'phase':
        return show, hide, hide, hide, show_anim
    elif selected == 'lyapunov':
        return hide, show, hide, hide, show_anim
    elif selected == 'stability-trajectory':
        return hide, hide, show, hide, show_anim
    # 'perturbed' ou 'stability' : afficher la carte "Stabilité" et les contrôles initiales
    return hide, hide, show, show, show_anim


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


@app.callback(
    Output('car-animation', 'figure'),
    [Input('a1-slider', 'value'),
     Input('a2-slider', 'value'),
     Input('x0-slider', 'value'),
     Input('y0-slider', 'value'),
     Input('scenario-dropdown', 'value')],
)
def update_car_animation(a1, a2, x0, y0, scenario):
    # Ne calculer que si scénario = 'spring'
    if scenario != 'spring':
        return go.Figure()
    
    # Calcul de la trajectoire (limité à 5 secondes)
    t_max = 5.0
    dt = 0.01
    t = np.arange(0, t_max + dt, dt)
    n = len(t)
    
    # Position verticale initiale (équilibre à y=1)
    y_eq = 1.0
    
    # Calculer trajectoire x(t)
    x_traj = np.zeros(n)
    y_traj = np.zeros(n)
    x_traj[0] = x0
    y_traj[0] = y0
    
    for i in range(n-1):
        x_traj[i+1] = x_traj[i] + dt * y_traj[i]
        y_traj[i+1] = y_traj[i] + dt * (a1*x_traj[i] + a2*y_traj[i])
    
    # Position verticale absolue de la caisse
    car_y = y_eq + x_traj
    
    
    # Position horizontale fixe de la voiture
    car_x_center = 0
    car_width = 0.8
    car_height = 0.4
    wheel_radius = 0.15
    
    # Créer les frames d'animation
    frames = []
    for i in range(0, n, max(1, n//100)):  # limiter à ~100 frames
        car_y_pos = car_y[i]
        
        # Clipper si hors cadre
        if car_y_pos < -0.5 or car_y_pos > 2.5:
            car_y_pos = max(-0.5, min(2.5, car_y_pos))
        
        # Rectangle de la caisse
        car_rect_x = [car_x_center - car_width/2, car_x_center + car_width/2, 
                      car_x_center + car_width/2, car_x_center - car_width/2, 
                      car_x_center - car_width/2]
        car_rect_y = [car_y_pos, car_y_pos, car_y_pos + car_height, 
                      car_y_pos + car_height, car_y_pos]
        
        # Roue (cercle)
        theta = np.linspace(0, 2*np.pi, 30)
        wheel_x = car_x_center + wheel_radius * np.cos(theta)
        wheel_y = car_y_pos - wheel_radius + wheel_radius * np.sin(theta)
        
        frame = go.Frame(
            data=[
                # Route
                go.Scatter(x=[-2, 2], y=[0, 0], mode='lines', 
                          line=dict(color='gray', width=4), name='Route'),
                # Caisse
                go.Scatter(x=car_rect_x, y=car_rect_y, mode='lines', 
                          fill='toself', fillcolor='rgba(70,130,180,0.7)',
                          line=dict(color='steelblue', width=2), name='Caisse'),
                # Roue
                go.Scatter(x=wheel_x, y=wheel_y, mode='lines', 
                          fill='toself', fillcolor='black',
                          line=dict(color='black', width=2), name='Roue'),
                # Ressort (ligne verticale)
                go.Scatter(x=[car_x_center, car_x_center], y=[0, car_y_pos], 
                          mode='lines', line=dict(color='orange', width=2, dash='dash'),
                          name='Ressort')
            ],
            name=str(i)
        )
        frames.append(frame)
    
    # Figure initiale
    fig = go.Figure(
        data=frames[0].data if frames else [],
        frames=frames
    )
    
    # Boutons Play/Pause
    fig.update_layout(
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': '▶ Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 50, 'redraw': True},
                        'fromcurrent': True,
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                },
                {
                    'label': '⏸ Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ],
            'x': 0.1,
            'y': 1.15
        }],
        xaxis=dict(range=[-2, 2], title='Position horizontale'),
        yaxis=dict(range=[-0.5, 3], title='Position verticale'),
        height=500,
        showlegend=True,
        title=f'Suspension — a₁={a1:.2f}, a₂={a2:.2f}'
    )
    
    return fig

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


if __name__ == '__main__':
    app.run(debug=True)