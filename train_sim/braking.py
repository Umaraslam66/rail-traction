import numpy as np

def calculate_braking_force(mass, deceleration):
    """
    Calculate the braking force required to achieve a specified deceleration.

    Parameters:
    mass (float): Mass of the train in kilograms (kg).
    deceleration (float): Desired deceleration in meters per second squared (m/s^2).

    Returns:
    float: Required braking force in Newtons (N).
    """
    return mass * deceleration


def calculate_braking_distance(initial_speed, deceleration):
    """
    Calculate the braking distance required to stop from an initial speed.

    Parameters:
    initial_speed (float): Initial speed of the train in meters per second (m/s).
    deceleration (float): Deceleration in meters per second squared (m/s^2).

    Returns:
    float: Braking distance in meters (m).
    """
    if deceleration <= 0:
        raise ValueError("Deceleration must be greater than zero.")
    
    return (initial_speed ** 2) / (2 * deceleration)


def calculate_stopping_time(initial_speed, deceleration):
    """
    Calculate the time required to stop from an initial speed.

    Parameters:
    initial_speed (float): Initial speed of the train in meters per second (m/s).
    deceleration (float): Deceleration in meters per second squared (m/s^2).

    Returns:
    float: Time to stop in seconds (s).
    """
    if deceleration <= 0:
        raise ValueError("Deceleration must be greater than zero.")
    
    return initial_speed / deceleration


def calculate_braking_profile(
    initial_speed: float,
    distance: float,
    slope_profile: np.ndarray = None,
    deceleration_profile: float = -1.0,
    min_dec: float = -1.2,
    max_dec: float = -0.5,
    dt: float = 1.0,
    g: float = 9.81
) -> dict:
    """
    Simulate train braking from initial_speed to stop over a given distance.

    Parameters:
        initial_speed (float): Initial speed in m/s.
        distance (float): Total distance to simulate (meters).
        slope_profile (np.ndarray): Slope at each position (as fraction, e.g. 0.02 for 2%).
        deceleration_profile (float): Nominal deceleration (negative, m/s^2).
        min_dec (float): Minimum allowed deceleration (negative, m/s^2).
        max_dec (float): Maximum allowed deceleration (negative, m/s^2).
        dt (float): Time step (seconds).
        g (float): Gravity (m/s^2).

    Returns:
        dict: {'distance': np.array, 'speed': np.array, 'deceleration': np.array}
    """
    n_steps = int(distance // dt) + 1
    s = np.zeros(n_steps)
    v = np.zeros(n_steps)
    a = np.zeros(n_steps)
    v[0] = initial_speed
    s[0] = 0.0
    for i in range(1, n_steps):
        # Slope effect (if profile provided)
        slope = slope_profile[i-1] if slope_profile is not None else 0.0
        # Deceleration (nominal + slope effect)
        dec = deceleration_profile + g * slope
        # Clamp deceleration
        dec = max(min_dec, min(dec, max_dec))
        a[i] = dec
        # Update speed (nonlinear integration as in MATLAB)
        v1 = np.sqrt(max(0, 2 * dec + v[i-1] ** 2))
        v2 = (v[i-1] + v1) / 2
        v[i] = max(0.0, v[i-1] + dec * 1.0 / max(v2, 1e-6))
        # Update position
        s[i] = s[i-1] + v[i] * dt
        if v[i] <= 0.0 or s[i] >= distance:
            s = s[:i+1]
            v = v[:i+1]
            a = a[:i+1]
            break
    return {
        'distance': s,
        'speed': v,
        'deceleration': a
    }