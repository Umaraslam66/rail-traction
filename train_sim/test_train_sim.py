import unittest
import numpy as np
from train_sim import slope, curve_resistance, acceleration, braking, block_occupancy, train_config

class TestTrainSimModules(unittest.TestCase):
    def test_calculate_equivalent_slope(self):
        lutning_pos = np.array([0, 500, 1000])
        lutning = np.array([0.01, 0.02])
        x_pos = np.array([0, 250, 500, 750, 1000])
        train_length = 100
        result = slope.calculate_equivalent_slope(lutning_pos, lutning, x_pos, train_length)
        self.assertEqual(len(result), len(x_pos))
        self.assertTrue(np.all(result >= 0))

    def test_calculate_curve_resistance(self):
        curve_pos = np.array([0, 500, 1000])
        curve_radius = np.array([500, 200])
        x_pos = np.array([0, 250, 500, 750, 1000])
        train_length = 100
        mass_kg = 50000
        result = curve_resistance.calculate_curve_resistance(curve_pos, curve_radius, x_pos, train_length, mass_kg)
        self.assertEqual(len(result), len(x_pos))
        self.assertTrue(np.all(result >= 0))

    def test_acceleration_profile(self):
        config = train_config.TrainConfig(mass_kg=50000, tractive_effort_n=200000, train_type="test")
        res = acceleration.calculate_acceleration_profile(config, slope_percent=1.0, distance=1000, v_max=55, dt=1.0, curve_resistance=1000)
        self.assertIn('distance', res)
        self.assertIn('speed', res)
        self.assertIn('acceleration', res)
        self.assertTrue(np.all(res['speed'] >= 0))

    def test_braking_profile(self):
        res = braking.calculate_braking_profile(initial_speed=55, distance=1000, slope_profile=np.zeros(1001), deceleration_profile=-1.0, min_dec=-1.2, max_dec=-0.5, dt=1.0)
        self.assertIn('distance', res)
        self.assertIn('speed', res)
        self.assertTrue(np.all(res['speed'] >= 0))

    def test_block_occupancy(self):
        block_positions = np.array([2, 4, 6])
        speed_profile = np.array([10, 20, 30, 40, 50, 60, 70])
        position_profile = np.arange(7)
        time_profile = np.arange(7)
        release_speed = np.array([10, 20, 30])
        train_length = 1
        overlap = np.array([1, 1, 1])
        release_time = np.array([1, 1, 1])
        setting_time = np.array([1, 1, 1])
        reserve_before_arrival = 1.0
        result = block_occupancy.calculate_block_occupancy(
            block_positions, speed_profile, position_profile, time_profile,
            release_speed, train_length, overlap, release_time, setting_time, reserve_before_arrival
        )
        self.assertEqual(result.shape[0], 3)

if __name__ == "__main__":
    unittest.main()
