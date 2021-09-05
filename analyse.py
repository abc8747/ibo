import os
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from rich.progress import Progress

def non_uniform_savgol_filter(x, y, window, polynom):
    # Obtained from https://dsp.stackexchange.com/a/64313

    half_window = window // 2
    polynom += 1

    A = np.empty((window, polynom))
    tA = np.empty((polynom, window))
    t = np.empty(window)
    y_smoothed = np.full(len(y), np.nan)

    for i in range(half_window, len(x) - half_window, 1):
        for j in range(0, window, 1):
            t[j] = x[i + j - half_window] - x[i]

        for j in range(0, window, 1):
            r = 1.0
            for k in range(0, polynom, 1):
                A[j, k] = r
                tA[k, j] = r
                r *= t[j]

        tAA = np.matmul(tA, A)
        tAA = np.linalg.inv(tAA)
        coeffs = np.matmul(tAA, tA)

        y_smoothed[i] = 0
        for j in range(0, window, 1):
            y_smoothed[i] += coeffs[0, j] * y[i + j - half_window]

        if i == half_window:
            first_coeffs = np.zeros(polynom)
            for j in range(0, window, 1):
                for k in range(polynom):
                    first_coeffs[k] += coeffs[k, j] * y[j]
        elif i == len(x) - half_window - 1:
            last_coeffs = np.zeros(polynom)
            for j in range(0, window, 1):
                for k in range(polynom):
                    last_coeffs[k] += coeffs[k, j] * y[len(y) - window + j]

    for i in range(0, half_window, 1):
        y_smoothed[i] = 0
        x_i = 1
        for j in range(0, polynom, 1):
            y_smoothed[i] += first_coeffs[j] * x_i
            x_i *= x[i] - x[half_window]

    for i in range(len(x) - half_window, len(x), 1):
        y_smoothed[i] = 0
        x_i = 1
        for j in range(0, polynom, 1):
            y_smoothed[i] += last_coeffs[j] * x_i
            x_i *= x[i] - x[-half_window - 1]

    return y_smoothed

df2s = []
with Progress() as progress:
    files = os.listdir('output')
    task = progress.add_task(f"[green]Processing files...", total=len(files))
    for filename in files:
        progress.update(task, advance=1, description=f'[green]Processing {filename}...')
        df = pd.read_csv(os.path.join("output", filename))
        smoothed = non_uniform_savgol_filter(df.frame.values, df.angle.values, 31, 5)
        idx = argrelextrema(smoothed, np.greater, order=5)[0]

        df1 = pd.DataFrame(columns=["frame", "length", "turning_smoothed"])
        df1['frame'] = df.iloc[idx].frame
        df1['length'] = df.iloc[idx].length
        df1['turning_smoothed'] = smoothed[idx]

        df1l, df2l = df1.values.tolist(), []
        for i, j in enumerate(df1l[:-1]):
            r0, r1 = df1l[i], df1l[i+1]
            df2l.append([
                (r1[0] + r0[0]) / 2,
                r1[0] - r0[0],
                (r1[1] + r0[1]) / 2,
                (r1[2] + r1[2]) / 2
            ])

        identifier = os.path.splitext(filename)[0]
        df2s.append(pd.DataFrame(df2l, columns=[
            f"{identifier}_avg_frame",
            f"{identifier}_frame_diff",
            f"{identifier}_avg_length",
            f"{identifier}_avg_turning_smoothed"
        ]))

df2 = pd.concat(df2s, axis=1)
df2.to_csv(os.path.join("output1", "all.csv"), index=False)