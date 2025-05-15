import numpy as np

def calculate_block_occupancy(
    block_positions,
    speed_profile,
    position_profile,
    time_profile,
    release_speed,
    train_length,
    overlap,
    release_time,
    setting_time,
    reserve_before_arrival,
    v_tol=0.1
):
    """
    Calculate block booking, arrival, and release times for each block.

    Parameters:
        block_positions (array-like): Positions of block signals (meters).
        speed_profile (np.ndarray): Speed profile along the track (m/s).
        position_profile (np.ndarray): Position profile (meters).
        time_profile (np.ndarray): Time at each position (seconds).
        release_speed (array-like): Release speed for each block (m/s).
        train_length (float): Train length (meters).
        overlap (array-like): Overlap distance for each block (meters).
        release_time (array-like): Release time for each block (seconds).
        setting_time (array-like): Setting time for each block (seconds).
        reserve_before_arrival (float): Reserve time before arrival (seconds).
        v_tol (float): Speed tolerance for block release (m/s).

    Returns:
        np.ndarray: [n_blocks, 5] array with columns:
            [0] speed diff at release, [1] index, [2] booking time, [3] arrival time, [4] release time
    """
    block_positions = np.asarray(block_positions, dtype=int)
    n_blocks = len(block_positions)
    mb_times = np.full((n_blocks, 5), np.nan)
    for k, bp in enumerate(block_positions):
        # Find where speed profile matches release speed
        speed_diff = np.abs(speed_profile - release_speed[k])
        idx = np.where(speed_diff <= v_tol)[0]
        if idx.size == 0:
            # If not found, book block reserve_before_arrival before arrival
            if bp < len(time_profile):
                mb_times[k, 2] = time_profile[bp] - reserve_before_arrival
            else:
                mb_times[k, 2] = np.nan
        else:
            b = idx[0]
            mb_times[k, 0] = speed_diff[b]
            mb_times[k, 1] = b
            mb_times[k, 2] = time_profile[b] - setting_time[k]
        # Arrival time at block
        if bp < len(time_profile):
            mb_times[k, 3] = time_profile[bp]
        else:
            mb_times[k, 3] = np.nan
        # Release time: when train + overlap has cleared block
        release_idx = bp + int(round(train_length)) + int(overlap[k])
        if release_idx < len(time_profile):
            mb_times[k, 4] = time_profile[release_idx] + release_time[k]
        else:
            mb_times[k, 4] = np.nan
    return mb_times