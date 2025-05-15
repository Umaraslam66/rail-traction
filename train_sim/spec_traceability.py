"""
Spec-to-Sim Traceability Layer
Links requirements/spec items to segments/sim results.
"""
import re
import numpy as np

def trace_spec_to_sim(requirements, sim_results):
    """
    Args:
        requirements (list): List of spec/requirement items.
        sim_results (dict): Simulation results.
    Returns:
        dict: { 'violations': list, 'trace_map': dict }
    """
    violations = []
    trace_map = {}
    
    # Process each requirement
    for req_index, requirement in enumerate(requirements):
        req_id = f"REQ-{req_index+1:03d}"
        
        # Extract spec type and value
        parsed_req = parse_requirement(requirement)
        if not parsed_req:
            trace_map[req_id] = {
                'text': requirement,
                'status': 'unparseable',
                'sim_link': None
            }
            continue
            
        req_type = parsed_req['type']
        req_value = parsed_req['value']
        operator = parsed_req['operator']
        
        # Map to simulation result
        sim_value = extract_sim_value(req_type, sim_results)
        
        # Check if requirement is satisfied
        is_satisfied = check_requirement_satisfaction(sim_value, operator, req_value)
        
        # Record trace link
        trace_map[req_id] = {
            'text': requirement,
            'status': 'compliant' if is_satisfied else 'violated',
            'sim_link': {
                'parameter': req_type,
                'simulated_value': sim_value,
                'required_value': f"{operator} {req_value}"
            }
        }
        
        # Record violation if requirement not satisfied
        if not is_satisfied:
            violations.append({
                'req_id': req_id,
                'requirement': requirement,
                'sim_value': sim_value,
                'required': f"{operator} {req_value}",
                'severity': determine_severity(req_type)
            })
    
    return {
        'violations': violations,
        'trace_map': trace_map
    }
    
def parse_requirement(requirement):
    """Parse a natural language requirement into structured format"""
    # Pattern matching for common requirement formats
    speed_pattern = re.compile(r'(max|maximum|min|minimum)?\s*speed\s*([<>=])\s*(\d+\.?\d*)', re.IGNORECASE)
    stopping_pattern = re.compile(r'stop.*within\s*(\d+\.?\d*)', re.IGNORECASE)
    grade_pattern = re.compile(r'grade|gradient\s*([<>=])\s*(\d+\.?\d*)', re.IGNORECASE)
    energy_pattern = re.compile(r'energy\s*([<>=])\s*(\d+\.?\d*)', re.IGNORECASE)
    
    # Try to match patterns
    speed_match = speed_pattern.search(requirement)
    if speed_match:
        prefix, operator, value = speed_match.groups()
        return {
            'type': 'max_speed' if prefix and 'max' in prefix.lower() else 'speed',
            'operator': operator,
            'value': float(value)
        }
    
    stopping_match = stopping_pattern.search(requirement)
    if stopping_match:
        value = stopping_match.group(1)
        return {
            'type': 'stopping_distance',
            'operator': '<',
            'value': float(value)
        }
    
    grade_match = grade_pattern.search(requirement)
    if grade_match:
        operator, value = grade_match.groups()
        return {
            'type': 'gradient',
            'operator': operator,
            'value': float(value)
        }
    
    energy_match = energy_pattern.search(requirement)
    if energy_match:
        operator, value = energy_match.groups()
        return {
            'type': 'energy',
            'operator': operator,
            'value': float(value)
        }
    
    # If no pattern matches, try some keywords
    keywords = {
        'energy': 'energy_consumption',
        'emissions': 'co2_emissions',
        'co2': 'co2_emissions',
        'carbon': 'co2_emissions',
        'throughput': 'throughput',
        'capacity': 'capacity',
    }
    
    for keyword, req_type in keywords.items():
        if keyword in requirement.lower():
            # Look for numbers in the requirement
            numbers = re.findall(r'(\d+\.?\d*)', requirement)
            operators = re.findall(r'([<>=])', requirement)
            if numbers and operators:
                return {
                    'type': req_type,
                    'operator': operators[0],
                    'value': float(numbers[0])
                }
    
    return None

def extract_sim_value(req_type, sim_results):
    """Extract the simulation value corresponding to the requirement type"""
    # Map requirement types to simulation result keys
    sim_mapping = {
        'max_speed': 'max_speed',
        'speed': 'speed',
        'stopping_distance': 'stopping_distance',
        'gradient': 'gradient',
        'energy': 'energy_consumed_kwh',
        'energy_consumption': 'energy_consumed_kwh',
        'co2_emissions': 'co2_emitted_kg',
        'throughput': 'throughput',
        'capacity': 'capacity'
    }
    
    # Get the corresponding key in sim_results
    sim_key = sim_mapping.get(req_type)
    if not sim_key:
        return None
        
    # Extract value from sim_results
    return sim_results.get(sim_key)

def check_requirement_satisfaction(sim_value, operator, req_value):
    """Check if the simulation value satisfies the requirement"""
    if sim_value is None:
        return False
        
    if operator == '<':
        return sim_value < req_value
    elif operator == '<=':
        return sim_value <= req_value
    elif operator == '>':
        return sim_value > req_value
    elif operator == '>=':
        return sim_value >= req_value
    elif operator == '=':
        return sim_value == req_value
    
    return False

def determine_severity(req_type):
    """Determine the severity of a requirement violation"""
    # Safety-critical requirements are high severity
    safety_critical = ['max_speed', 'stopping_distance', 'gradient']
    
    # Operational requirements are medium severity
    operational = ['throughput', 'capacity', 'energy_consumption']
    
    # Environmental requirements are low severity (still important but not immediate safety impact)
    environmental = ['co2_emissions']
    
    if req_type in safety_critical:
        return 'high'
    elif req_type in operational:
        return 'medium'
    elif req_type in environmental:
        return 'low'
    else:
        return 'medium'  # Default
