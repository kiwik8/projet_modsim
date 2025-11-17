import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np

from computation import phase

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
                            {'label': 'Système masse-ressort', 'value': 'spring'},
                            {'label': 'Pendule', 'value': 'pendulum'},
                            {'label': 'Circuit RLC', 'value': 'rlc'}
                        ],
                        value='spring'
                    ),
                    html.Hr(),
                    
                    # Sliders pour coefficients
                    html.Label("Coefficient a₁:"),
                    dcc.Slider(id='a1-slider', min=-5, max=5, step=0.1, value=0,
                              marks={i: str(i) for i in range(-5, 6)}),
                    
                    html.Label("Coefficient a₂:"),
                    dcc.Slider(id='a2-slider', min=-5, max=5, step=0.1, value=0,
                              marks={i: str(i) for i in range(-5, 6)}),
                    
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
            # Trois conteneurs indépendants; on n'en affichera qu'un à la fois via callback
            html.Div(id='card-phase', children=[
                dbc.Card([
                    dbc.CardHeader("Portrait de phase et trajectoires"),
                    dbc.CardBody([
                        dcc.Graph(id='phase-portrait', style={'height': '600px'})
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
                    dbc.CardHeader("Évolution temporelle"),
                    dbc.CardBody([
                        dcc.Graph(id='time-series', style={'height': '600px'})
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


# Callback pour le portrait de phase
@app.callback(
    Output('phase-portrait', 'figure'),
    [Input('a1-slider', 'value'),
     Input('a2-slider', 'value')],
)
def update_phase_portrait(a1, a2):
    
    X, Y, U, V = phase.calculer_champ(a1, a2, [-5, 5], [-5, 5]) # calcul du champ de vecteurs
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
        xaxis=dict(range=[-5, 5]),
        yaxis=dict(range=[-5, 5]),
        height=400
    )
    
    return fig

@app.callback(
    Output('card-phase', 'style'),
    Output('card-lyapunov', 'style'),
    Output('card-time', 'style'),
    Input('viz-radio', 'value')
)

def show_only(selected):
    show = {'display': 'block'}
    hide = {'display': 'none'}
    if selected == 'phase':
        return show, hide, hide
    if selected == 'lyapunov':
        return hide, show, hide
    return hide, hide, show


if __name__ == '__main__':
    app.run(debug=True)