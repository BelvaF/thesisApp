import numpy as np
import math
import matplotlib.pyplot as plt

def fuzzy(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x, y):
    A = beta * delta * m * (1 - u)

    if ohm < ohm_min or ohm > ohm_max:
        domain_1 = alpha_min
        return domain_1
    
    elif ohm_min <= ohm <= ohm_0:
        domain_2 = alpha_min + ((ohm - ohm_min)/(ohm_0 - ohm_min)) * A
        return domain_2
    
    elif ohm_0 <= ohm <= ohm_max:
        domain_3 = A + alpha_min - ((ohm - ohm_0)/(ohm_max - ohm_0)) * A
        return domain_3

def model_define(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x, y):
    model = np.array([ 
        [u * x * (1 - math.log((x + y) / k)) - beta * x * y - delta * x],  # model1 (x_n, y_n)
        [m * y * (1 - math.log((x + y) / k)) + beta * x * y - fuzzy(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x, y) * y]   # model2 (x_n, y_n) 
    ])
    return model

def rungekutta(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x, y, h):
    # Runge-Kutta untuk model
    m1 = model_define(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x, y)
    m2 = model_define(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x + 0.5 * h * m1[0, 0], y + 0.5 * h * m1[1, 0])
    m3 = model_define(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x + 0.5 * h * m2[0, 0], y + 0.5 * h * m2[1, 0])
    m4 = model_define(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x + h * m3[0, 0], y + h * m3[1, 0])

    # Update x and y
    x_new = x + (h / 6) * (m1[0, 0] + 2 * m2[0, 0] + 2 * m3[0, 0] + m4[0, 0])
    y_new = y + (h / 6) * (m1[1, 0] + 2 * m2[1, 0] + 2 * m3[1, 0] + m4[1, 0])

    return x_new, y_new


def run_fuzzy(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x, y, t_awal, t_akhir, h):
    num_steps = int((t_akhir - t_awal) / h)
    time_values = np.linspace(t_awal, t_akhir, num_steps)
    x_values = [x]
    y_values = [y]

    for i in range(1, num_steps):
        x, y = rungekutta(u, m, ohm, ohm_min, ohm_0, ohm_max, alpha_min, beta, delta, k, x, y, h)
        x_values.append(x)
        y_values.append(y)

    return time_values, np.array(x_values), np.array(y_values)