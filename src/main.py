import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

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
                    dcc.Checklist(
                        id='viz-checklist',
                        options=[
                            {'label': ' Portrait de phase', 'value': 'phase'},
                            {'label': ' Fonction de Lyapunov', 'value': 'lyapunov'},
                            {'label': ' Trajectoire perturbée', 'value': 'perturbed'}
                        ],
                        value=['phase']
                    )
                ])
            ], className="mb-3")
        ], width=3),
        
        # Colonne principale de visualisation
        dbc.Col([
            # Graphique principal
            dbc.Card([
                dbc.CardHeader("Portrait de phase et trajectoires"),
                dbc.CardBody([
                    dcc.Graph(id='phase-portrait', style={'height': '400px'})
                ])
            ], className="mb-3"),
            
            # Rangée de graphiques secondaires
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Fonction de Lyapunov"),
                        dbc.CardBody([
                            dcc.Graph(id='lyapunov-plot', style={'height': '300px'})
                        ])
                    ])
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Évolution temporelle"),
                        dbc.CardBody([
                            dcc.Graph(id='time-series', style={'height': '300px'})
                        ])
                    ])
                ], width=6)
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

if __name__ == '__main__':
    app.run(debug=True)