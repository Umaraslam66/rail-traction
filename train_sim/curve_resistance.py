import numpy as np

def calculate_curve_resistance(curve_pos, curve_radius, x_pos, train_length, train_mass):
    """
    Calculate the curve resistance (N) for a train along the track using Rückl's formula.

    Parameters:
        curve_pos (array-like): Breakpoints (meters) where curve radius changes.
        curve_radius (array-like): Curve radius (meters) for each interval (np.inf for straight).
        x_pos (array-like): Positions (meters) to evaluate resistance.
        train_length (float): Length of the train (meters).
        train_mass (float): Mass of the train (kg).

    Returns:
        np.ndarray: Curve resistance (N) at each x_pos.
    """
    curve_pos = np.asarray(curve_pos)
    curve_radius = np.asarray(curve_radius)
    x_pos = np.asarray(x_pos)
    resistance = np.full_like(x_pos, np.nan, dtype=float)
    for k, xp in enumerate(x_pos):
        pos = [xp - train_length, xp]
        inkl_intv = np.where((pos[0] < curve_pos[1:]) & (pos[1] >= curve_pos[:-1]))[0]
        if len(inkl_intv) == 1:
            r = curve_radius[inkl_intv[0]]
            if r < 300:
                resistance[k] = 4.91 / (r - 30) * train_mass
            else:
                resistance[k] = 6.3 / (r - 55) * train_mass
        elif len(inkl_intv) > 1:
            total = 0.0
            for i, idx in enumerate(inkl_intv):
                r = curve_radius[idx]
                if r < 300:
                    tmp = 4.91 / (r - 30) * train_mass / (pos[2-1] - pos[0])
                else:
                    tmp = 6.3 / (r - 55) * train_mass / (pos[2-1] - pos[0])
                if i == 0:
                    seg = tmp * (curve_pos[idx+1] - pos[0])
                    curve_force = seg
                elif i == len(inkl_intv) - 1:
                    seg = tmp * (pos[1] - curve_pos[idx])
                    curve_force = curve_force + seg
                else:
                    seg = tmp * (curve_pos[idx+1] - curve_pos[idx])
                    curve_force = curve_force + seg
            resistance[k] = curve_force
    return resistance