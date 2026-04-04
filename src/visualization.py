import numpy as np
from scipy.signal import welch, find_peaks

import matplotlib.pyplot as plt
import seaborn as sns


from models.jansenrit import solve_jr
from models.reduced import simulate_reduced, reduced_rhs, eeg_proxy

sns.set_theme(style="ticks", context="paper", palette="colorblind")
FIGSIZE = (6, 4)


def plot_jr():
    """
    Plots the activity of excitatory and inhibitory PSPs and their net balance during an oscillatory regime for the Jansen-Rit model.

    This function uses default values for the Jansen-Rit model known to produce oscillatory behavior, drawn from modern parameterizations.
    """
    sol = solve_jr()
    # calculate net drive into pyramidal cells at every time point
    net = sol.y[1] - sol.y[2]

    plt.figure(figsize=(8, 4))
    plt.plot(sol.t, net, label="Net Drive")
    plt.plot(sol.t, sol.y[1], label="y1 (Excitation)")
    plt.plot(sol.t, sol.y[2], label="y2 (Inhibition)")
    plt.xlabel("Time (s)")
    plt.ylabel("y1 - y2")
    plt.title("Jansen-Rit Net Pyramidal Drive")
    plt.tight_layout()
    plt.legend()
    sns.despine()
    plt.show()


def plot_reduced_dynamics(params):
    """
    Plots the E/I curves of the reduced model for a given parameter regime.
    """
    t, E, I = simulate_reduced(params)

    plt.figure(figsize=FIGSIZE)
    plt.plot(t, E, label="Excitatory (E)")
    plt.plot(t, I, label="Inhibitory (I)")
    plt.xlabel("Time")
    plt.ylabel("Activity Level")
    plt.title(f"Reduced Model Dynamics - {params['name']}")
    plt.legend()
    sns.despine()
    plt.show()


def phase_plane_analysis(
    params,
    E0=0.1,
    I0=0.1,
    T=1000.0,
    dt=0.1,
    e_range=(0.0, 1.2),
    i_range=(0.0, 1.2),
    n_quiver=20,
    n_nullcline=200,
):
    """
    Plots the phase plane geometry and trajectory corresponding with the specified parameters, initial conditions, and simulation specifications.
    """
    E_color = "#2C7BB6"
    I_color = "#D7191C"
    traj_color = "#222222"
    start_color = "#2A9D8F"

    # coarse grid for vector field
    E_vals_q = np.linspace(e_range[0], e_range[1], n_quiver)
    I_vals_q = np.linspace(i_range[0], i_range[1], n_quiver)
    EE_q, II_q = np.meshgrid(E_vals_q, I_vals_q)

    dE_q = np.zeros_like(EE_q)
    dI_q = np.zeros_like(II_q)

    # arrows, make them all the same length
    for r in range(n_quiver):
        for c in range(n_quiver):
            dE_val, dI_val = reduced_rhs(EE_q[r, c], II_q[r, c], params)
            norm = np.sqrt(dE_val**2 + dI_val**2) + 1e-8
            dE_q[r, c] = dE_val / norm
            dI_q[r, c] = dI_val / norm

    # fine grid for nullclines
    # i had to do this to make them smoother, they looked discontinuous
    E_vals_n = np.linspace(e_range[0], e_range[1], n_nullcline)
    I_vals_n = np.linspace(i_range[0], i_range[1], n_nullcline)
    EE_n, II_n = np.meshgrid(E_vals_n, I_vals_n)

    dE_n = np.zeros_like(EE_n)
    dI_n = np.zeros_like(II_n)

    # use reduced system to calculate nullcline values
    for r in range(n_nullcline):
        for c in range(n_nullcline):
            dE_val, dI_val = reduced_rhs(EE_n[r, c], II_n[r, c], params)
            dE_n[r, c] = dE_val
            dI_n[r, c] = dI_val

    # simulate trajectory
    t, E_traj, I_traj = simulate_reduced(params, E0=E0, I0=I0, dt=dt, T=T)

    plt.figure(figsize=FIGSIZE)

    # vector field
    plt.quiver(
        EE_q,
        II_q,
        dE_q,
        dI_q,
        angles="xy",
        scale_units="xy",
        scale=20,
        width=0.003,
        alpha=0.45,
        color="gray",
        zorder=1,
    )

    # nullclines
    plt.contour(
        EE_n,
        II_n,
        dE_n,
        levels=[0],
        colors=E_color,
        linewidths=2,
        linestyles="dashed",
        zorder=2,
    )
    plt.contour(
        EE_n,
        II_n,
        dI_n,
        levels=[0],
        colors=I_color,
        linewidths=2,
        linestyles="dashed",
        zorder=2,
    )

    # trajectory
    plt.plot(
        E_traj,
        I_traj,
        color=traj_color,
        linewidth=2.5,
        label="Trajectory",
        zorder=3,
    )
    plt.plot(
        E_traj[0],
        I_traj[0],
        "o",
        color=start_color,
        markersize=7,
        label="Start",
        zorder=4,
    )

    plt.xlabel("Excitatory activity E")
    plt.ylabel("Inhibitory activity I")
    plt.title(f"Reduced E–I Phase Plane - {params['name']}")
    plt.xlim(e_range)
    plt.ylim(i_range)

    # legend entries for nullclines
    plt.plot([], [], color=E_color, linestyle="dashed", label="E-nullcline")
    plt.plot([], [], color=I_color, linestyle="dashed", label="I-nullcline")

    plt.legend()
    plt.tight_layout()
    sns.despine()
    plt.show()


def plot_proxy(param_sets):
    """
    Plots the proxy signal E-I for each of the parameter sets passed in. param_sets should be a list of dicts.
    """
    plt.figure(figsize=FIGSIZE)

    for params in param_sets:
        t, E, I = simulate_reduced(params)
        proxy_signal = eeg_proxy(E, I)

        plt.plot(
            t,
            proxy_signal,
            linewidth=2,
            label=params["name"],
        )

    plt.xlabel("Time")
    plt.ylabel("Proxy signal (E - I)")
    plt.title("EEG Proxy Signals Across Regimes")
    plt.legend()
    plt.tight_layout()
    sns.despine()
    plt.show()


def plot_proxy_sweeps(sweep_dicts):
    """
    Creates side by side graphs for each of the three parameter sweeps conducted on the proxy signal.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

    # loop over each subplot
    # zip pairs items from two lists together
    for ax, sweep_params in zip(axes, sweep_dicts):
        sweep_key = None
        sweep_values = None
        # find the parameter whose value is a list
        for key, value in sweep_params.items():
            if isinstance(value, list):
                sweep_key = key
                sweep_values = value
                break

        if sweep_key is None:
            raise ValueError("No sweep parameter found.")

        # rotate through parameter values
        for sweep_value in sweep_values:
            params = sweep_params.copy()
            params[sweep_key] = sweep_value

            t, E, I = simulate_reduced(params)
            proxy_signal = eeg_proxy(E, I)

            ax.plot(
                t,
                proxy_signal,
                linewidth=2,
                label=f"{sweep_key} = {sweep_value}",
            )

        ax.set_xlabel("Time")
        ax.set_xlim(0, 600)
        ax.set_title(sweep_params["name"])
        ax.legend()

    axes[0].set_ylabel("Proxy signal (E - I)")
    plt.tight_layout()
    sns.despine()
    plt.show()


def plot_spectral_welch(param_sets):
    plt.figure(figsize=FIGSIZE)

    # different curve for each parameter set
    for params in param_sets:
        t, E, I = simulate_reduced(params)
        proxy = eeg_proxy(E, I)

        fs = 1.0 / (t[1] - t[0])
        f, Pxx = welch(proxy, fs=fs, nperseg=2048)

        # find and print dominant frequency
        if params["name"] == "Limit Cycle":
            peaks, _ = find_peaks(proxy)
            period = np.mean(np.diff(t[peaks]))
            freq = 1.0 / period

            print(f"\n{params['name']} Dominant Frequency: {freq:.6f}\n")

        plt.plot(
            f,
            Pxx,
            linewidth=2,
            label=params["name"],
        )

    plt.xlabel("Frequency (inverse time units)")
    plt.ylabel("PSD")
    plt.title("Spectral Analysis of Oscillation Frequency")
    plt.xlim(0, 0.06)
    plt.legend()
    plt.tight_layout()
    sns.despine()
    plt.show()
