from visualization import *


def main():

    print("\nReduced Jansen–Rit model: dynamical analysis demo.\n")

    print("Parent JR model oscillatory behavior:\n")

    plot_jr()

    print("Reduced model regimes (time series + phase plane):\n")

    plot_reduced_dynamics(params_stable)
    phase_plane_analysis(params_stable)

    plot_reduced_dynamics(params_damped_reduced)
    phase_plane_analysis(params_damped_reduced)

    plot_reduced_dynamics(params_limit_cycle)
    phase_plane_analysis(params_limit_cycle)

    print(
        "Sensitivity to initial conditions and simulation duration(same parameters):\n"
    )

    phase_plane_analysis(params_limit_cycle, E0=0.2, I0=1.1, T=2000)
    phase_plane_analysis(params_limit_cycle, E0=0.2, I0=0.8, T=2000)
    phase_plane_analysis(params_limit_cycle, E0=0.2, I0=0.7, T=1000)
    phase_plane_analysis(params_limit_cycle, E0=0.2, I0=0.7, T=3000)

    print("EEG proxy signal across regimes:\n")

    plot_proxy(params_all_dynamical)

    print("Parameter sweeps (gain, drive, delay):\n")

    plot_proxy_sweeps(params_all_sweep)

    print("Spectral comparison across regimes:\n")

    plot_spectral_welch(params_all_dynamical)

    print("\nEnd of demo. See report for details.\n")


BASE_PARAMS = {
    "tau_E": 10.0,
    "P_I": 0.0,
    "a_E": 4.0,
    "a_I": 4.0,
    "theta_E": 0.4,
    "theta_I": 0.4,
}

params_limit_cycle = {
    **BASE_PARAMS,
    "tau_I": 40.0,  # 40
    "P_E": 0.3,  # 0.3
    "g": 3.0,
    "name": "Limit Cycle",
}

params_damped_reduced = {
    **BASE_PARAMS,
    "tau_I": 20.0,
    "P_E": 0.25,
    "g": 3.0,
    "name": "Damped Oscillatory",
}

params_stable = {
    **BASE_PARAMS,
    "tau_I": 20.0,
    "P_E": 0.25,
    "g": 1.0,
    "name": "Stable Fixed Point",
}

params_g_sweep = {
    **BASE_PARAMS,
    "tau_I": 20.0,
    "P_E": 0.25,
    "g": [1.0, 2.0, 3.0],
    "name": "g-Sweep",
}

params_P_sweep = {
    **BASE_PARAMS,
    "tau_I": 20.0,
    "P_E": [0.1, 0.3, 0.6],
    "g": 3.0,
    "name": "P_E-Sweep",
}

params_tau_sweep = {
    **BASE_PARAMS,
    "tau_I": [10.0, 20.0, 50.0],
    "P_E": 0.25,
    "g": 3.0,
    "name": "tau_I-Sweep",
}

params_all_dynamical = [
    params_stable,
    params_damped_reduced,
    params_limit_cycle,
]

params_all_sweep = [params_g_sweep, params_P_sweep, params_tau_sweep]

if __name__ == "__main__":
    main()
