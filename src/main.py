# src/main.py

from visualization import *

def main():

    print("\n\nThis is the main visualization script for dynamical analysis of the reduced Jansen-Rit Model. \n \nThe first plot shown depicts behavior of Excitatory and Inhibitory interactions and Pyramidal drive in the original, unreduced Jansen-Rit model under a parameter set that produces oscillatory behavior.\n\n")

    plot_jr()

    print("The dynamical regimes of the reduced model are much easier to analyze, and parameter adjustments can easily push the system into alternate dynamical regimes as new attractors emerge in phase plane space. \n\nThe following plots represent system behavior of three different regimes, produced by altering inhibitory lag (tau_I), excitatory drive (P_E), and system gain (g). The phase plane analysis plot will follow the plot of the regime's temporal excitatory and inhibitory activity levels.")

    plot_reduced_dynamics(params_stable)
    phase_plane_analysis(params_stable)

    plot_reduced_dynamics(params_damped_reduced)
    phase_plane_analysis(params_damped_reduced)
    
    plot_reduced_dynamics(params_limit_cycle)
    phase_plane_analysis(params_limit_cycle)

    print("\n\nAn EEG-like proxy signal can be deduced by representing the push/pull nature of the overall activity levels at any moment in the regime. The current plot illustrates this across regimes.")

    plot_proxy(params_all_dynamical)

    print("\n\nSweeping parameters and simulating the activity of the EEG proxy signals allows a clear view of the impact that each parameter has on the oscillatory behavior of the system. See the current figure illustrating these basic sweeps.")

    plot_proxy_sweeps(params_all_sweep)
    
    print("\n\nWe can perform an acompanying spectral analysis to strengthen the distinction between regimes - the following plots show that the oscillatory regime has drastically more concentrated spectral content than do those of the stable or damped-oscillatory regimes.")

    plot_spectral(params_all_dynamical)

    print("\n\nThis concludes the visualization of the analysis - see attached report for further detail.\n\n")



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
    "tau_I": 40.0, #40
    "P_E": 0.3, #0.3
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

params_all_sweep = [
    params_g_sweep,
    params_P_sweep,
    params_tau_sweep
]

if __name__ == "__main__":
    main()