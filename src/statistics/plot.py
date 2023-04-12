import matplotlib.pyplot as plt
import numpy as np

def intensityFunction(t):
    return max(0.0, (100.0 - t) / 5.0)

def intensity_function_in(t):
    if t > 960: return 0
    return max(0, 2.0 * np.sin(-0.5 + np.pi * t / 480)) + np.random.uniform(0, 0.25)

def intensity_function_out(t):
    if t < 480 or t > 1440: return 0
    return max(0, 2.0 * np.sin(np.pi * (-1.5 + t / 480))) + np.random.uniform(0, 0.25)

def plot_function(fun, t = 250):
    Xs, ys = [], []
    for x in range(0, t):
        Xs.append(x)
        ys.append(fun(x))
    plt.plot(Xs, ys)
    plt.title("Intensity function (t)")
    plt.xlabel("time [s]")
    plt.ylabel("Number of generated cars per 1s")
    plt.show()

plot_function(intensityFunction)
plot_function(intensity_function_in, t = 1750)
plot_function(intensity_function_out, t = 1750)