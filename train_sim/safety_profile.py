"""
Braking & Safety Profile Simulator
Calculates stopping distances, braking curves, and flags safety violations.
"""
import numpy as np

def simulate_braking_and_safety(speed_profile, gradient_profile, entry_exit_paths):
    """
    Args:
        speed_profile (np.ndarray): Speed profile of the train.
        gradient_profile (np.ndarray): Slope profile along the track.
        entry_exit_paths (list): List of entry/exit path segments.
    Returns:
        dict: { 'stopping_distances': np.ndarray, 'violations': list }
    """
    # Convert inputs to numpy arrays if they're not already
    if isinstance(speed_profile, str):
        speed_profile = np.array([float(x.strip()) for x in speed_profile.split(",")])
    elif not isinstance(speed_profile, np.ndarray):
        speed_profile = np.array(speed_profile, dtype=float)
    if isinstance(gradient_profile, str):
        gradient_profile = np.array([float(x.strip())/100 for x in gradient_profile.split(",")])
    elif not isinstance(gradient_profile, np.ndarray):
        gradient_profile = np.array(gradient_profile, dtype=float)
    # Ensure speed_profile and gradient_profile are at least 1D float arrays
    speed_profile = np.atleast_1d(speed_profile).astype(float)
    gradient_profile = np.atleast_1d(gradient_profile).astype(float)
    if speed_profile is None or np.size(speed_profile) == 0:
        speed_profile = np.array([50.0])  # Default 50 m/s
    if gradient_profile is None or np.size(gradient_profile) == 0:
        gradient_profile = np.array([0.0])  # Default flat terrain
    
    # Safety parameters
    g = 9.81  # Acceleration due to gravity (m/s²)
    mu = 0.35  # Friction coefficient (wet rail)
    reaction_time = 1.5  # Seconds for brake application after emergency
    safety_margin = 1.2  # Safety factor for stopping distance
    
    # Calculate stopping distances at each point based on speed, gradient and friction
    # Formula: d = v^2 / (2 * g * (mu ± gradient))
    # where ± depends on whether train is going uphill (+) or downhill (-)
    
    stopping_distances = []
    for i, speed in enumerate(speed_profile):
        gradient = gradient_profile[i % len(gradient_profile)]
        # Adjust friction based on gradient (downhill reduces effective friction)
        effective_friction = mu - gradient  # Negative gradient (downhill) reduces friction
        
        # Calculate stopping distance including reaction time
        reaction_distance = speed * reaction_time
        braking_distance = (speed**2) / (2 * g * max(0.01, effective_friction))  # Prevent division by zero
        total_distance = (reaction_distance + braking_distance) * safety_margin
        
        stopping_distances.append(round(total_distance, 1))
    
    # Check for safety violations based on entry/exit paths
    violations = []
    
    # If entry_exit_paths provided, check for potential conflicts
    if entry_exit_paths:
        for i, path in enumerate(entry_exit_paths):
            path_length = path.get('length', 500)  # Default 500m if not provided
            path_speed = path.get('speed_limit', 40)  # Default 40 m/s if not provided
            
            # Calculate minimum safe stopping distance for this path
            safe_stop_dist = (path_speed**2) / (2 * g * mu) * safety_margin
            
            # Check if stopping distance exceeds path length (unsafe)
            if safe_stop_dist > path_length:
                violations.append({
                    'path_id': i,
                    'violation_type': 'stopping_distance_exceeds_path',
                    'severity': 'high',
                    'details': f"Path length {path_length}m insufficient for safe stopping from {path_speed}m/s"
                })
    else:
        # Generate sample violations based on stopping distances
        if max(stopping_distances) > 800:
            violations.append({
                'path_id': 0,
                'violation_type': 'excessive_stopping_distance',
                'severity': 'medium',
                'details': f"Maximum stopping distance {max(stopping_distances)}m exceeds 800m threshold"
            })
            
        # Check for gradient-based violations
        steep_grades = np.where(np.abs(gradient_profile) > 0.025)[0]
        if len(steep_grades) > 0:
            violations.append({
                'path_id': 1,
                'violation_type': 'steep_gradient',
                'severity': 'low',
                'details': f"Gradients exceeding 2.5% detected at positions {steep_grades}"
            })
    
    return {
        'stopping_distances': np.array(stopping_distances),
        'violations': violations
    }
