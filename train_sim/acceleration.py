import numpy as np
from train_sim.train_config import TrainConfig

# Constants
g = 9.81  # gravity [m/s^2]


def calculate_acceleration_profile(
    train_config: TrainConfig,
    slope_percent: float,
    distance: float = 1000.0,
    v_max: float = 55.0,
    dt: float = 1.0,
    A: float = 1500.0,
    B: float = 2.5,
    C: float = 0.008,
    adhesion_coef: float = 0.25,
    tunnel_factor: float = 0.0,
    curve_resistance: float = 0.0,
    max_acc: float = 1.0
) -> dict:
    """
    Calculate the acceleration profile for a train along a track segment.

    Parameters:
        train_config (TrainConfig): Train configuration object.
        slope_percent (float): Track slope in percent (e.g., 2 for 2%).
        distance (float): Total distance to simulate (meters).
        v_max (float): Maximum allowed speed (m/s).
        dt (float): Time step (seconds).
        A, B, C (float): Davis resistance coefficients.
        adhesion_coef (float): Adhesion coefficient (typical 0.2-0.3).
        tunnel_factor (float): Additional tunnel resistance factor.
        curve_resistance (float): Additional curve resistance (N).
        max_acc (float): Maximum allowed acceleration (m/s^2).

    Returns:
        dict: {'distance': np.array, 'speed': np.array, 'acceleration': np.array, 'tractive_effort': np.array}
    """
    mass = train_config.mass_kg
    tractive_effort = train_config.tractive_effort_n
    n_steps = int(distance // dt) + 1
    s = np.zeros(n_steps)
    v = np.zeros(n_steps)
    a = np.zeros(n_steps)
    F_trac = np.zeros(n_steps)

    # Initial conditions
    v[0] = 0.0
    s[0] = 0.0

    for i in range(1, n_steps):
        # Davis resistance
        F_res = A + B * v[i-1] + C * v[i-1] ** 2
        # Slope resistance (positive for uphill)
        F_slope = mass * g * (slope_percent / 100.0)
        # Tunnel and curve resistance
        F_tunnel = tunnel_factor * v[i-1] ** 2
        F_curve = curve_resistance
        # Total resistance
        F_total_res = F_res + F_slope + F_tunnel + F_curve
        # Adhesion limit
        F_adhesion = adhesion_coef * mass * g
        # Available tractive effort (limited by adhesion and max TE)
        F_trac[i] = min(tractive_effort, F_adhesion)
        # Net force
        F_net = F_trac[i] - F_total_res
        # Acceleration (limit to max_acc)
        a[i] = np.clip(F_net / mass, -max_acc, max_acc)
        # Integrate speed (Euler)
        v[i] = max(0.0, min(v[i-1] + a[i] * dt, v_max))
        # Integrate distance
        s[i] = s[i-1] + v[i] * dt
        # Stop if we've reached the total distance
        if s[i] >= distance:
            s = s[:i+1]
            v = v[:i+1]
            a = a[:i+1]
            F_trac = F_trac[:i+1]
            break

    return {
        'distance': s,
        'speed': v,
        'acceleration': a,
        'tractive_effort': F_trac
    }