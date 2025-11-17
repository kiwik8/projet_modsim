import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np

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


# fonction pour calculer le champ de vecteurs
def calculer_champ(a1, a2, x_range, y_range):
    # grille de points
    x = np.linspace(x_range[0], x_range[1], 20)
    y = np.linspace(y_range[0], y_range[1], 20)
    X, Y = np.meshgrid(x, y)
    
    # système: dx/dt = y, dy/dt = a1*x + a2*y
    U = Y
    V = a1*X + a2*Y
    
    return X, Y, U, V

# fonction pour tracer une trajectoire
def calculer_trajectoire(a1, a2, x0, y0, t_max=10):
    dt = 0.05
    t = np.arange(0, t_max, dt)
    n = len(t)
    
    x = np.zeros(n)
    y = np.zeros(n)
    x[0] = x0
    y[0] = y0
    
    # Euler
    for i in range(n-1):
        x[i+1] = x[i] + dt * y[i]
        y[i+1] = y[i] + dt * (a1*x[i] + a2*y[i])
    
    return x, y

# Callback pour le portrait de phase
@app.callback(
    Output('phase-portrait', 'figure'),
    [Input('a1-slider', 'value'),
     Input('a2-slider', 'value'),
     Input('viz-checklist', 'value')]
)

def update_phase_portrait(a1, a2, viz):
    if 'phase' not in viz:
        return go.Figure()
    
    fig = go.Figure()
    
    X, Y, U, V = calculer_champ(a1, a2, [-5, 5], [-5, 5]) # calcul du champ de vecteurs
    
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
        x_traj, y_traj = calculer_trajectoire(a1, a2, x0, y0)
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
    Output('lyapunov-plot', 'figure'),
    [Input('a1-slider', 'value'),
     Input('a2-slider', 'value'),
     Input('viz-checklist', 'value')]
)

def update_lyapunov(a1,a2,viz):
    if 'lyapunov' not in viz:
       return 

    # Grille 
    x = np.linspace(-5, 5, 80)
    y = np.linspace(-5, 5, 80)
    X, Y = np.meshgrid(x, y)

    # Fonction Lyapunov simple
    V = X**2 + Y**2

    # Dérivée Lyapunov
    Vdot = 2*X*Y + 2*Y*(a1*X + a2*Y)

    fig = go.Figure()

    # Heatmap de Vdot (rouge = instable, bleu = stable)
    fig.add_trace(go.Contour(
        x=x,
        y=y,
        z=Vdot,
        colorscale='RdBu',
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

if __name__ == '__main__':
    app.run(debug=True)