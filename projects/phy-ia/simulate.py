'''
This script does the following:
- for 0 m < l < 1.5 m in increments of 0.001 m:
    - for initial θ -> 0, pi/12, pi/6, pi/4, pi/3 and 5pi/12:
        - numerically solves the exact nonlinear equation from 0 < t < 20, with step size 0.001s
        - derives the period of the motion by averaging the Δt in the peaks of θ(t)
- saves the results to a CSV file.
'''

from scipy.integrate import odeint
from scipy.signal import argrelextrema
import numpy as np
import pandas as pd

g = 9.81
r = 0.0750
l_rod = 0.1958

def theta_nonlinear(U, x):
    return [U[1], -3*g*np.power(2*r,2)/(l*np.power(l_rod,2))*np.sin(U[0])/np.sqrt(1-0.5*np.power(2*r/l, 2)*(1-np.cos(U[0])))]

def theta_linear(U, x):
    return [U[1], -12*g*np.power(r,2)/(l*np.power(l_rod,2))*U[0]]

data = []
for sqrt_l in np.linspace(0, 1.5, 1500):
    l = np.power(sqrt_l, 2)
    row = [sqrt_l]
    for n in [0.0001, 1, 2, 3, 4, 5]:
        xs = np.linspace(0, 20, 20000)
        ys = odeint(theta_nonlinear, [n*np.pi/12, 0], xs)[:,0]

        row.append(np.mean(np.diff(xs[argrelextrema(ys, np.greater, order=5)[0]])))
    data.append(row)

df = pd.DataFrame(data, columns=['sqrt_l', '0', 'pi/12', 'pi/6', 'pi/4', 'pi/3', '5pi/12'])
df.to_csv('output1/simulate.csv')