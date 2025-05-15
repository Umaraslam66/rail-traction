"""
Energy & Emissions Estimator
Computes energy consumption and emissions for different train/track scenarios.
"""
import numpy as np

def estimate_energy_and_emissions(train_config, gradient_profile, speed_profile, power_type):
    """
    Args:
        train_config (TrainConfig): Train configuration object.
        gradient_profile (np.ndarray): Slope profile along the track.
        speed_profile (np.ndarray): Speed profile of the train.
        power_type (str): 'diesel', 'electric', or 'hybrid'.
    Returns:
        dict: { 'energy_consumed_kwh': float, 'co2_emitted_kg': float }
    """
    # Convert inputs to numpy arrays if they're not already
    if isinstance(gradient_profile, str):
        gradient_profile = np.array([float(x.strip())/100 for x in gradient_profile.split(",")])
    elif not isinstance(gradient_profile, np.ndarray):
        gradient_profile = np.array(gradient_profile, dtype=float)
    if isinstance(speed_profile, str):
        speed_profile = np.array([float(x.strip()) for x in speed_profile.split(",")])
    elif not isinstance(speed_profile, np.ndarray):
        speed_profile = np.array(speed_profile, dtype=float)
    # Ensure speed_profile and gradient_profile are at least 1D float arrays
    speed_profile = np.atleast_1d(speed_profile).astype(float)
    gradient_profile = np.atleast_1d(gradient_profile).astype(float)
    if speed_profile is None or np.size(speed_profile) == 0:
        speed_profile = np.array([50.0])  # Default 50 m/s
    if gradient_profile is None or np.size(gradient_profile) == 0:
        gradient_profile = np.array([0.0])  # Default flat terrain
    
    # Get train mass from config
    mass_kg = train_config.mass_kg
    
    # Constants
    g = 9.81  # Gravity (m/s²)
    distance = 1000  # Default distance (m)
    dt = 1.0  # Time step (s)
    
    # Efficiency factors by power type
    efficiency = {
        'diesel': 0.38,  # Diesel-electric efficiency
        'electric': 0.85,  # Electric efficiency
        'hybrid': 0.60   # Hybrid system efficiency
    }.get(power_type.lower(), 0.5)  # Default 0.5 for unknown types
    
    # Emission factors (kg CO2 per kWh)
    emission_factor = {
        'diesel': 0.65,  # kg CO2 per kWh (diesel)
        'electric': 0.25,  # kg CO2 per kWh (electric, depends on grid mix)
        'hybrid': 0.45    # kg CO2 per kWh (hybrid)
    }.get(power_type.lower(), 0.5)  # Default 0.5 for unknown types
    
    # Calculate energy consumed
    total_energy_kwh = 0
    
    # Forces calculation
    rolling_resistance = 0.0025 * mass_kg * g  # Rolling resistance (N)
    air_resistance_coef = 0.6  # Aerodynamic coefficient
    frontal_area = 10  # Frontal area (m²)
    rho = 1.2  # Air density (kg/m³)
    
    # Calculate energy consumption for each segment
    for i in range(min(len(speed_profile), len(gradient_profile))):
        speed = speed_profile[i]
        gradient = gradient_profile[i % len(gradient_profile)]
        
        # Calculate forces
        gradient_force = mass_kg * g * gradient  # Force due to gradient (N)
        air_resistance = 0.5 * rho * air_resistance_coef * frontal_area * speed**2  # Air resistance (N)
        
        # Total resistance force
        total_resistance = rolling_resistance + gradient_force + air_resistance
        
        # Power required = Force * Speed
        power_required = total_resistance * speed  # Watts
        
        # Energy for this segment
        energy_kwh = power_required * dt / 3600000  # Convert W*s to kWh
        
        # Apply efficiency factor
        total_energy_kwh += energy_kwh / efficiency
    
    # Calculate CO2 emissions
    co2_emitted_kg = total_energy_kwh * emission_factor
    
    # Regenerative braking energy recovery (for electric and hybrid)
    if power_type.lower() in ['electric', 'hybrid']:
        # Estimate regenerative braking recovery (20% of total energy for electric, 10% for hybrid)
        regen_factor = 0.2 if power_type.lower() == 'electric' else 0.1
        recovered_energy = total_energy_kwh * regen_factor
        total_energy_kwh -= recovered_energy
        co2_emitted_kg -= recovered_energy * emission_factor
    
    return {
        'energy_consumed_kwh': round(total_energy_kwh, 1),
        'co2_emitted_kg': round(co2_emitted_kg, 1)
    }
