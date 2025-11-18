import numpy as np
from scipy.integrate import odeint

def systeme(state, t, a1: float, a2: float):
    x, y = state
    dx = y
    dy = a1*x + a2*y
    return [dx, dy]


def calcul_perturbation(a1: float, a2: float,
                        x0: float, y0: float,
                        eps: float = 1e-3,
                        t_max: float = 10.0,
                        dt: float = 0.05):
    """
    Calcule la distance entre une trajectoire et une perturbée de valeur eps
    """
    t = np.arange(0, t_max + dt, dt)

    sol = odeint(systeme, [x0, y0], t, args=(a1, a2))
    x = sol[:, 0]
    y = sol[:, 1]

    solp = odeint(systeme, [x0 + eps, y0 + eps], t, args=(a1, a2))
    x_p = solp[:, 0]
    y_p = solp[:, 1]
    dist = np.sqrt((x - x_p)**2 + (y - y_p)**2)

    return t, x, y, x_p, y_p, dist
