import numpy as np
import math
import matplotlib.pyplot as plt

def model_define(u, m, alpha, beta, delta, k, x, y):
    model = np.array([ 
        [u * x * (1 - math.log((x + y) / k)) - beta * x * y - delta * x],  # model1 (x_n, y_n)
        [m * y * (1 - math.log((x + y) / k)) + beta * x * y - alpha * y]   # model2 (x_n, y_n) 
    ])
    return model

def matrix_define(u, m, alpha, beta, delta, k, x, y): # 5 param dan 2 variabel
    J = np.array([
        [u*(1 - math.log((x + y) / k)) - (u * x) / (x + y) - beta * y - delta, -(u * x) / (x + y) - beta * x],
        [-(m * y) / (x + y) + beta * y, m * (1 - math.log((x + y) / k)) - (m * y) / (x + y) + beta * x - alpha]
    ])
    
    F = np.array([ 
        [x * (1 - math.log((x + y) / k)), 0, -x, -x * y, 0], 
        [0, y * (1 - math.log((x + y) / k)), 0, x * y, -y]
    ])
    
    return J, F

def dA_dt(J, A, F):
    return np.dot(J, A) + F

def rungekutta(u, m, alpha, beta, delta, k, x, y, h, A):
    m1 = model_define(u, m, alpha, beta, delta, k, x, y)
    m2 = model_define(u, m, alpha, beta, delta, k, x + 0.5 * h * m1[0, 0], y + 0.5 * h * m1[1, 0])
    m3 = model_define(u, m, alpha, beta, delta, k, x + 0.5 * h * m2[0, 0], y + 0.5 * h * m2[1, 0])
    m4 = model_define(u, m, alpha, beta, delta, k, x + h * m3[0, 0], y + h * m3[1, 0])

    x_new = x + (h / 6) * (m1[0, 0] + 2 * m2[0, 0] + 2 * m3[0, 0] + m4[0, 0])
    y_new = y + (h / 6) * (m1[1, 0] + 2 * m2[1, 0] + 2 * m3[1, 0] + m4[1, 0])

    J, F = matrix_define(u, m, alpha, beta, delta, k, x_new, y_new)
    
    s1 = dA_dt(J, A, F)
    s2 = dA_dt(J, A + 0.5 * h * s1, F)
    s3 = dA_dt(J, A + 0.5 * h * s2, F)
    s4 = dA_dt(J, A + h * s3, F)

    A_new = A + (h / 6) * (s1 + 2 * s2 + 2 * s3 + s4)
    
    return x_new, y_new, J, F, A_new

def run_sensitivity(u, m, alpha, beta, delta, k, x, y, t_awal, t_akhir, h):
    num_steps = int((t_akhir - t_awal) / h)
    results = np.zeros((num_steps, 2, 5))

    A = np.zeros((2, 5))
    results[0] = A

    J, F = matrix_define(u, m, alpha, beta, delta, k, x, y)
    time = np.linspace(t_awal, t_akhir, num_steps)

    for i in range(1, num_steps):
        x, y, J, F, A = rungekutta(u, m, alpha, beta, delta, k, x, y, h, A)
        results[i] = A

    return time, results
