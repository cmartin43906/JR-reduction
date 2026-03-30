import numpy as np

def sigmoid(x, a, theta):
    return 1.0 / (1.0 + np.exp(-a * (x - theta)))

def reduced_rhs(E, I, params):
    # unpack parameters
    g = params["g"]

    P_E = params["P_E"]
    P_I = params["P_I"]

    a_E = params["a_E"]
    theta_E = params["theta_E"]
    a_I = params["a_I"]
    theta_I = params["theta_I"]

    tau_E = params["tau_E"]
    tau_I = params["tau_I"]

    # reduced minimal excitation-inhibition loop
    dE = (-E + sigmoid(g * (E - I + P_E), a_E, theta_E)) / tau_E
    dI = (-I + sigmoid(g * (E + P_I), a_I, theta_I)) / tau_I

    return dE, dI

# inspired by code in lecture slides
def simulate_reduced(params, E0=0.1, I0=0.1, dt=0.1, T=1000.0):
    n = int(T / dt) + 1
    t = np.arange(n) * dt
    E = np.zeros(n)
    I = np.zeros(n)
    E[0], I[0] = E0, I0

    for k in range(n - 1):
        dE, dI = reduced_rhs(E[k], I[k], params)
        E[k + 1] = E[k] + dt * dE
        I[k + 1] = I[k] + dt * dI

    return t, E, I

def eeg_proxy(E, I):
    return E - I
