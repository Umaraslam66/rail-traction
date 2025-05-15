"""
Scenario Sandbox
Fork scenarios, run batch simulations, compare KPIs.
"""
import numpy as np
import copy

def run_scenario_sandbox(scenarios):
    """
    Args:
        scenarios (list): List of scenario dicts/configs.
    Returns:
        dict: { 'results': list, 'kpi_comparison': dict, 'visual_diffs': list, 'narrative': str }
    """
    # This function would run each scenario through the simulator
    # and collect results for comparison
    
    results = []
    
    # For each scenario, simulate and collect results
    for scenario in scenarios:
        # Extract scenario parameters
        scenario_name = scenario.get('name', 'Unnamed')
        traffic_multiplier = scenario.get('traffic', 100) / 100.0
        locos = scenario.get('locos', 1)
        
        # Simulate: in real implementation, call the simulator with these parameters
        # Here we create sample results based on the parameters
        
        # Base metrics with some randomness
        avg_speed = 45 + np.random.normal(0, 5)  # m/s
        max_speed = avg_speed * 1.2
        energy_consumption = 3500 * traffic_multiplier * locos * (0.8 + 0.4 * np.random.random())
        co2_emissions = energy_consumption * (0.4 + 0.2 * np.random.random())
        
        # Calculate throughput based on traffic
        throughput = 24 * traffic_multiplier * (0.9 + 0.2 * np.random.random())
        
        # Calculate operational cost
        maintenance_cost = 1200 * locos + 50 * throughput
        fuel_cost = energy_consumption * 0.12  # $ per kWh
        operational_cost = maintenance_cost + fuel_cost
        
        # Calculate revenue
        revenue = throughput * 500  # $ per train
        
        # Calculate profit
        profit = revenue - operational_cost
        
        # Store results
        scenario_result = {
            'name': scenario_name,
            'parameters': copy.deepcopy(scenario),
            'metrics': {
                'avg_speed': round(avg_speed, 1),
                'max_speed': round(max_speed, 1),
                'throughput': round(throughput, 1),
                'energy_consumption': round(energy_consumption, 1),
                'co2_emissions': round(co2_emissions, 1),
                'operational_cost': round(operational_cost, 1),
                'revenue': round(revenue, 1),
                'profit': round(profit, 1)
            }
        }
        
        results.append(scenario_result)
    
    # Compare KPIs between scenarios
    kpi_comparison = {}
    
    if results:
        # Use first scenario as baseline
        baseline = results[0]
        baseline_name = baseline['name']
        
        # Initialize KPI comparison dictionary
        for key in baseline['metrics'].keys():
            kpi_comparison[key] = {
                'baseline': baseline['metrics'][key],
                'diffs': []
            }
        
        # Calculate diffs for each scenario compared to baseline
        for result in results[1:]:
            scenario_name = result['name']
            for key, value in result['metrics'].items():
                baseline_value = baseline['metrics'][key]
                absolute_diff = value - baseline_value
                percentage_diff = (absolute_diff / baseline_value) * 100 if baseline_value != 0 else 0
                
                kpi_comparison[key]['diffs'].append({
                    'scenario': scenario_name,
                    'absolute_diff': round(absolute_diff, 1),
                    'percentage_diff': round(percentage_diff, 1)
                })
    
    # Generate visual diffs data (could be used for plotting)
    visual_diffs = []
    for metric, data in kpi_comparison.items():
        visual_diff = {
            'metric': metric,
            'baseline_value': data['baseline'],
            'scenarios': [{'name': d['scenario'], 'value': data['baseline'] + d['absolute_diff']} for d in data.get('diffs', [])]
        }
        visual_diffs.append(visual_diff)
    
    # Generate narrative summary
    narrative = generate_narrative_summary(results, kpi_comparison)
    
    return {
        'results': results,
        'kpi_comparison': kpi_comparison,
        'visual_diffs': visual_diffs,
        'narrative': narrative
    }

def generate_narrative_summary(results, kpi_comparison):
    """Helper function to generate a narrative summary of scenario comparisons"""
    if not results or len(results) < 2:
        return "Insufficient scenarios for comparison."
    
    baseline_name = results[0]['name']
    summary = f"## Scenario Comparison Summary\n\nComparing scenarios against baseline '{baseline_name}':\n\n"
    
    for i, result in enumerate(results[1:], 1):
        scenario_name = result['name']
        summary += f"### {scenario_name}\n"
        
        # Highlight key differences
        profit_diff = None
        energy_diff = None
        throughput_diff = None
        
        for metric, data in kpi_comparison.items():
            if i-1 < len(data.get('diffs', [])):
                diff = data['diffs'][i-1]
                if metric == 'profit':
                    profit_diff = diff
                elif metric == 'energy_consumption':
                    energy_diff = diff
                elif metric == 'throughput':
                    throughput_diff = diff
        
        if profit_diff:
            change = "increased" if profit_diff['absolute_diff'] > 0 else "decreased"
            summary += f"- Profit {change} by {abs(profit_diff['percentage_diff'])}% "
            summary += f"(${profit_diff['absolute_diff']})\n"
            
        if energy_diff:
            change = "increased" if energy_diff['absolute_diff'] > 0 else "decreased"
            summary += f"- Energy consumption {change} by {abs(energy_diff['percentage_diff'])}%\n"
            
        if throughput_diff:
            change = "increased" if throughput_diff['absolute_diff'] > 0 else "decreased"
            summary += f"- Throughput {change} by {abs(throughput_diff['percentage_diff'])}%\n"
            
        summary += "\n"
    
    # Add recommendations
    summary += "## Recommendations\n\n"
    
    # Find best scenario for profit
    profit_metrics = [(r['name'], r['metrics']['profit']) for r in results]
    best_profit_scenario = max(profit_metrics, key=lambda x: x[1])
    
    # Find best scenario for emissions
    emissions_metrics = [(r['name'], r['metrics']['co2_emissions']) for r in results]
    best_emissions_scenario = min(emissions_metrics, key=lambda x: x[1])
    
    summary += f"- For maximum profit: Consider '{best_profit_scenario[0]}' (${best_profit_scenario[1]})\n"
    summary += f"- For minimum emissions: Consider '{best_emissions_scenario[0]}' ({best_emissions_scenario[1]} kg CO2)\n"
    
    return summary
