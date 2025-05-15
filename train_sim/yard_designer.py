"""
Interactive Yard Designer
Backend for drag & drop track layout, throughput, and movement simulation.
"""
import numpy as np
import time

def simulate_yard_layout(yard_layout, train_movements):
    """
    Args:
        yard_layout (dict): Representation of tracks, switches, platforms.
        train_movements (list): Planned train movements.
    Returns:
        dict: { 'throughput': float, 'movement_log': list, 'bottlenecks': list }
    """
    # Real implementation would use a graph-based simulation
    # This is a simplified version for demonstration
    
    # Extract yard configuration
    num_tracks = yard_layout.get('tracks', 3)
    num_switches = yard_layout.get('switches', 2)
    num_platforms = yard_layout.get('platforms', 1)
    
    # More detailed layout could include coordinates, lengths, etc.
    track_lengths = yard_layout.get('track_lengths', [500] * num_tracks)
    switch_positions = yard_layout.get('switch_positions', [150, 350])
    platform_positions = yard_layout.get('platform_positions', [250])
    
    # Calculate yard capacity based on layout
    capacity_per_track = 2  # Trains per track per hour
    switch_delay = 2  # Minutes per switch operation
    platform_service_time = 10  # Minutes per platform stop
    
    # Basic throughput calculation
    theoretical_throughput = num_tracks * capacity_per_track  # Trains per hour
    switch_bottleneck = 60 / switch_delay * num_switches  # Maximum switch operations per hour
    platform_bottleneck = 60 / platform_service_time * num_platforms  # Platform capacity per hour
    
    # Overall throughput is limited by the most constrained resource
    throughput = min(theoretical_throughput, switch_bottleneck, platform_bottleneck)
    
    # Simulate train movements
    movement_log = []
    bottlenecks = []
    occupied_tracks = set()
    current_time = 0
    
    if not train_movements:
        # Generate sample movements if none provided
        train_movements = ['arrive', 'depart', 'arrive', 'pass_through', 'arrive', 'depart']
    
    for i, movement in enumerate(train_movements):
        train_id = f"Train_{i+1}"
        
        if movement == 'arrive':
            # Find available track
            available_tracks = [t for t in range(num_tracks) if t not in occupied_tracks]
            if available_tracks:
                track = available_tracks[0]
                occupied_tracks.add(track)
                delay = 0
                movement_log.append({
                    'time': current_time,
                    'train': train_id,
                    'action': 'arrived',
                    'track': track,
                    'delay': delay
                })
            else:
                # No available tracks - bottleneck
                delay = 15  # 15 minute delay
                bottlenecks.append({
                    'time': current_time,
                    'type': 'track_capacity',
                    'details': f"No available tracks for {train_id}"
                })
                movement_log.append({
                    'time': current_time,
                    'train': train_id,
                    'action': 'waiting',
                    'delay': delay
                })
                
        elif movement == 'depart':
            if occupied_tracks:
                track = list(occupied_tracks)[0]
                occupied_tracks.remove(track)
                movement_log.append({
                    'time': current_time,
                    'train': train_id,
                    'action': 'departed',
                    'track': track,
                    'delay': 0
                })
            else:
                # No trains to depart - invalid operation
                bottlenecks.append({
                    'time': current_time,
                    'type': 'invalid_operation',
                    'details': f"No trains available to depart"
                })
                
        elif movement == 'pass_through':
            # Check switch availability
            if len(movement_log) % 3 == 0:  # Simulate occasional switch conflicts
                delay = switch_delay
                bottlenecks.append({
                    'time': current_time,
                    'type': 'switch_conflict',
                    'details': f"Switch occupied, {train_id} delayed"
                })
                movement_log.append({
                    'time': current_time,
                    'train': train_id,
                    'action': 'pass_through',
                    'delay': delay
                })
            else:
                movement_log.append({
                    'time': current_time,
                    'train': train_id,
                    'action': 'pass_through',
                    'delay': 0
                })
        
        # Advance time
        current_time += np.random.randint(5, 20)  # Random time advance between 5-20 minutes
    
    # Calculate actual throughput based on simulation
    if current_time > 0:
        actual_hourly_throughput = len([m for m in movement_log if m['action'] in ['arrived', 'departed', 'pass_through']]) / (current_time / 60.0)
    else:
        actual_hourly_throughput = 0
    
    return {
        'throughput': round(actual_hourly_throughput, 1),
        'movement_log': movement_log,
        'bottlenecks': bottlenecks
    }
