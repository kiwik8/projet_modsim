import numpy as np

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