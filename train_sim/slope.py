import numpy as np

def calculate_equivalent_slope(lutning_pos, lutning, x_pos, train_length):
    """
    Calculate the equivalent slope profile for a moving train along the track.

    Parameters:
        lutning_pos (array-like): Breakpoints (meters) where slope changes.
        lutning (array-like): Slope values (as fraction, e.g. 0.02 for 2%) for each interval.
        x_pos (array-like): Positions (meters) to evaluate equivalent slope.
        train_length (float): Length of the train (meters).

    Returns:
        np.ndarray: Equivalent slope at each x_pos.
    """
    lutning_pos = np.asarray(lutning_pos)
    lutning = np.asarray(lutning)
    x_pos = np.asarray(x_pos)
    ekv_slope = np.full_like(x_pos, np.nan, dtype=float)
    for k, xp in enumerate(x_pos):
        pos = [xp - train_length, xp]
        # Find intervals overlapped by the train
        inkl_intv = np.where((pos[0] < lutning_pos[1:]) & (pos[1] >= lutning_pos[:-1]))[0]
        if len(inkl_intv) == 1:
            ekv_slope[k] = lutning[inkl_intv[0]]
        elif len(inkl_intv) > 1:
            total = 0.0
            for i, idx in enumerate(inkl_intv):
                if i == 0:
                    seg = lutning[idx] * (lutning_pos[idx+1] - pos[0])
                elif i == len(inkl_intv) - 1:
                    seg = lutning[idx] * (pos[1] - lutning_pos[idx])
                else:
                    seg = lutning[idx] * (lutning_pos[idx+1] - lutning_pos[idx])
                total += seg
            ekv_slope[k] = total / (pos[1] - pos[0])
    return ekv_slope