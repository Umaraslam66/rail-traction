# train_sim/train_config.py

# This module defines input presets for the train simulation engine.
# It provides a structured way to manage train configuration data.

import numpy as np

class TrainConfig:
    def __init__(self, mass_kg, tractive_effort_n, train_type):
        """
        Initialize the train configuration.

        Parameters:
        mass_kg (float): Mass of the train in kilograms.
        tractive_effort_n (float): Maximum tractive effort of the train in Newtons.
        train_type (str): Type of the train (e.g., 'freight', 'passenger').
        """
        self.mass_kg = mass_kg
        self.tractive_effort_n = tractive_effort_n
        self.train_type = train_type

    def get_config(self):
        """
        Returns the train configuration as a dictionary.

        Returns:
        dict: A dictionary containing mass, tractive effort, and train type.
        """
        return {
            'mass_kg': self.mass_kg,
            'tractive_effort_n': self.tractive_effort_n,
            'train_type': self.train_type
        }

# Example configurations
freight_train = TrainConfig(mass_kg=100000, tractive_effort_n=300000, train_type='freight')
passenger_train = TrainConfig(mass_kg=50000, tractive_effort_n=150000, train_type='passenger')

# List of available train configurations
train_configs = {
    'freight': freight_train,
    'passenger': passenger_train
}