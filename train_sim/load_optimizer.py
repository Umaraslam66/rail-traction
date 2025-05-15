"""
Train Load Optimizer
Calculates how many wagons a train can pull based on gradients, speed profiles, and constraints.
"""
import numpy as np

def calculate_max_train_load(gradient_profile, loco_type, speed_limits):
    """
    Args:
        gradient_profile (np.ndarray): Slope profile along the track.
        loco_type (str): Locomotive type identifier.
        speed_limits (np.ndarray): Speed limits along the track.
    Returns:
        dict: { 'max_tonnage': float, 'energy_estimate': float }
    """
    # Convert inputs to numpy arrays if they're not already
    if isinstance(gradient_profile, str):
        gradient_profile = np.array([float(x.strip())/100 for x in gradient_profile.split(",")])
    
    # Ensure speed_limits is a numeric array
    if isinstance(speed_limits, str):
        speed_limits = np.array([float(x.strip()) for x in speed_limits.split(",")])
    elif isinstance(speed_limits, (list, np.ndarray)):
        # Handle empty or 0-d arrays safely
        if hasattr(speed_limits, 'ndim') and speed_limits.ndim == 0:
            speed_limits = np.array([float(speed_limits)])
        elif len(speed_limits) > 0 and isinstance(speed_limits[0], str):
            speed_limits = np.array([float(x.strip()) for x in speed_limits])
        elif len(speed_limits) == 0:
            speed_limits = np.array([55.0])  # Default speed limit
    else:
        speed_limits = np.array([55.0])  # Default speed limit
    
    # Locomotive power characteristics based on type
    loco_characteristics = {
        'freight': {'base_power': 4400, 'adhesion': 0.35, 'efficiency': 0.85},
        'passenger': {'base_power': 6000, 'adhesion': 0.30, 'efficiency': 0.90},
        'custom': {'base_power': 5000, 'adhesion': 0.33, 'efficiency': 0.87}
    }
    
    # Get loco characteristics (default to freight if type not found)
    loco = loco_characteristics.get(loco_type.lower(), loco_characteristics['freight'])
    
    # Maximum gradient as a limiting factor
    max_gradient = np.max(gradient_profile) if len(gradient_profile) > 0 else 0.01
    
    # Calculate max tonnage based on locomotive characteristics and max gradient
    # Formula: Max tonnage = (Tractive effort) / (9.81 * (max_gradient + 0.005))
    # where 0.005 is the basic rolling resistance coefficient
    avg_speed = np.mean(speed_limits) if isinstance(speed_limits, np.ndarray) and np.issubdtype(speed_limits.dtype, np.number) and np.mean(speed_limits) > 0 else 50.0
    tractive_effort = loco['base_power'] * 1000 * loco['efficiency'] / avg_speed
    max_tonnage = tractive_effort / (9.81 * (max_gradient + 0.005))
    
    # Adhesion limit
    adhesion_limit = loco['adhesion'] * loco['base_power'] * 100
    max_tonnage = min(max_tonnage, adhesion_limit)
    
    # Energy estimate (kWh) based on distance, gradient, and mass
    # Simple estimate: E = m * g * h * (1/efficiency) + m * distance * rolling_resistance * (1/efficiency)
    distance = 1000  # default distance in meters
    avg_gradient = np.mean(gradient_profile) if len(gradient_profile) > 0 else 0
    height_change = distance * avg_gradient
    energy_estimate = (max_tonnage * 9.81 * height_change / 3600) / loco['efficiency']  # in kWh
    
    # Add energy needed to overcome rolling resistance
    rolling_resistance = 0.005  # N/kg
    energy_for_resistance = (max_tonnage * distance * rolling_resistance / 3600) / loco['efficiency']
    energy_estimate += energy_for_resistance
    
    return {
        'max_tonnage': round(max_tonnage / 1000, 1),  # Convert to tons and round
        'energy_estimate': round(energy_estimate, 1)  # Round to 1 decimal
    }
