# simulator.py

import numpy as np
import matplotlib.pyplot as plt
from train_sim.acceleration import calculate_acceleration_profile
from train_sim.braking import calculate_braking_profile
from train_sim.slope import calculate_equivalent_slope
from train_sim.curve_resistance import calculate_curve_resistance
from train_sim.block_occupancy import calculate_block_occupancy
from train_sim.train_config import TrainConfig


def run_full_simulation():
    # Example train and track parameters
    train_config = TrainConfig(mass_kg=50000, tractive_effort_n=200000, train_type='passenger')
    train_length = 200.0  # meters
    distance = 1000.0  # meters
    dt = 1.0
    v_max = 55.0
    slope_percent = 2.0
    # Slope profile (breakpoints and values)
    lutning_pos = np.array([0, 400, 700, 1000])
    lutning = np.array([0.01, 0.02, 0.01])  # 1%, 2%, 1%
    x_pos = np.arange(0, distance + dt, dt)
    # Curve profile (breakpoints and radii)
    curve_pos = np.array([0, 500, 1000])
    curve_radius = np.array([500, 200])  # meters

    # 1. Equivalent slope profile
    ekv_slope = calculate_equivalent_slope(lutning_pos, lutning, x_pos, train_length)

    # 2. Curve resistance profile
    curve_res = calculate_curve_resistance(curve_pos, curve_radius, x_pos, train_length, train_config.mass_kg)

    # 3. Acceleration profile (using mean slope and mean curve resistance for simplicity)
    mean_slope = np.nanmean(ekv_slope) * 100 if not np.all(np.isnan(ekv_slope)) else slope_percent
    mean_curve_res = np.nanmean(curve_res) if not np.all(np.isnan(curve_res)) else 0.0
    acc_results = calculate_acceleration_profile(
        train_config,
        slope_percent=mean_slope,
        distance=distance,
        v_max=v_max,
        dt=dt,
        curve_resistance=mean_curve_res
    )

    # 4. Braking profile (from max speed)
    braking_results = calculate_braking_profile(
        initial_speed=v_max,
        distance=distance,
        slope_profile=ekv_slope,
        deceleration_profile=-1.0,
        min_dec=-1.2,
        max_dec=-0.5,
        dt=dt
    )

    # 5. Block occupancy (example block positions and parameters)
    block_positions = np.array([200, 600, 900])
    speed_profile = acc_results['speed']
    position_profile = acc_results['distance']
    time_profile = np.arange(len(position_profile)) * dt
    release_speed = np.array([10.0, 10.0, 10.0])  # m/s
    overlap = np.array([50, 50, 50])
    release_time = np.array([5, 5, 5])
    setting_time = np.array([10, 10, 10])
    reserve_before_arrival = 20.0
    block_times = calculate_block_occupancy(
        block_positions,
        speed_profile,
        position_profile,
        time_profile,
        release_speed,
        train_length,
        overlap,
        release_time,
        setting_time,
        reserve_before_arrival
    )

    # Print results summary
    print("--- Acceleration Profile ---")
    print("Speed (m/s):", acc_results['speed'])
    print("--- Braking Profile ---")
    print("Speed (m/s):", braking_results['speed'])
    print("--- Equivalent Slope (mean) ---")
    print(mean_slope)
    print("--- Curve Resistance (mean) ---")
    print(mean_curve_res)
    print("--- Block Occupancy Times ---")
    print(block_times)

    # --- Visualization ---
    fig, axs = plt.subplots(4, 1, figsize=(10, 14), sharex=True)
    axs[0].plot(acc_results['distance'], acc_results['speed'], label='Speed (m/s)')
    axs[0].set_ylabel('Speed (m/s)')
    axs[0].legend()
    axs[1].plot(acc_results['distance'], acc_results['acceleration'], label='Acceleration (m/s²)', color='orange')
    axs[1].set_ylabel('Acceleration (m/s²)')
    axs[1].legend()
    axs[2].plot(x_pos, ekv_slope, label='Equivalent Slope', color='green')
    axs[2].set_ylabel('Slope (fraction)')
    axs[2].legend()
    axs[3].plot(x_pos, curve_res, label='Curve Resistance (N)', color='red')
    axs[3].set_ylabel('Curve Resistance (N)')
    axs[3].set_xlabel('Distance (m)')
    axs[3].legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_full_simulation()