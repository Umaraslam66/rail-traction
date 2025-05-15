# Train Gradient and Traction Feasibility Tool

This project is a Python-based simulation engine designed to evaluate the feasibility of train operations on gradient tracks. It replicates the logic from existing MATLAB scripts and provides a modular structure for easy integration and extension.

## Project Structure

```
train_simulation_project
├── train_sim
│   ├── __init__.py
│   ├── simulator.py               # Main runner for the simulation engine
│   ├── acceleration.py            # Functions for calculating acceleration profiles
│   ├── braking.py                 # Functions for calculating braking forces and distances
│   ├── slope.py                   # Functions for slope and gradient calculations
│   ├── curve_resistance.py        # Functions for calculating curve resistance forces
│   ├── block_occupancy.py         # Functions for calculating block occupancy
│   └── train_config.py            # Input presets for train configuration
├── README.md                      # Documentation for the project
└── requirements.txt               # List of required Python dependencies
```

## Overview

The simulation engine aims to assist infrastructure designers and track engineers in assessing the feasibility of planned slope profiles for various train configurations. It calculates critical parameters such as tractive effort, required force, speed profiles, stopping distances, and energy feasibility.

## Usage

To use the simulation engine, follow these steps:

1. **Install Dependencies**: Ensure you have Python installed, then install the required libraries listed in `requirements.txt` using pip:
   ```
   pip install -r requirements.txt
   ```

2. **Configure Train Parameters**: Modify the `train_config.py` file to set the mass, tractive effort, and other relevant parameters for your train.

3. **Run the Simulation**: Execute the `simulator.py` script to run the simulation and obtain results regarding the feasibility of the train operations on the specified gradient track.

## Development

This project is structured to facilitate further development and integration with web applications, such as Streamlit. Each module is designed to be independent, allowing for easy updates and enhancements.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the functionality and performance of the simulation engine.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.