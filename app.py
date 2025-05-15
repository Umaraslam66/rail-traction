import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from train_sim.train_config import train_configs, TrainConfig
from train_sim.simulator import run_full_simulation
import plotly.graph_objects as go

st.set_page_config(
    page_title="Train Gradient & Traction Feasibility Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS for a clean, minimal, modernistic look
st.markdown("""
    <style>
    html, body, [class*="css"]  {font-family: 'Inter', 'Segoe UI', Arial, sans-serif;}
    .block-container {padding-top: 2.5rem; max-width: 1200px;}
    .stButton>button {
        background: linear-gradient(90deg, #0072C6 0%, #00B4D8 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.6em 1.5em;
        margin-bottom: 0.5em;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00B4D8 0%, #0072C6 100%);
        color: #fff;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #f4f6fa;
        border-radius: 12px;
        margin-bottom: 1.2em;
        padding: 0.2em 0.2em;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.08rem;
        font-weight: 500;
        border-radius: 8px 8px 0 0;
        margin-right: 0.5em;
        padding: 0.5em 1.2em;
        color: #0072C6;
        background: #e9ecef;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: #0072C6;
        color: #fff;
        box-shadow: 0 2px 8px rgba(0,114,198,0.08);
    }
    .stExpanderHeader {
        font-size: 1.08rem;
        font-weight: 600;
        color: #0072C6;
    }
    .stMetric {
        background: #f4f6fa;
        border-radius: 10px;
        padding: 0.5em 1em;
        margin-bottom: 0.5em;
    }
    .stDataFrame {
        background: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stSidebar {
        background: #f8f9fa;
    }
    .stTextInput>div>input, .stNumberInput>div>input {
        border-radius: 8px;
        border: 1px solid #e0e3e8;
        padding: 0.4em 1em;
        font-size: 1.05rem;
    }
    .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid #e0e3e8;
        font-size: 1.05rem;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #0072C6;
        font-weight: 700;
        margin-bottom: 0.2em;
    }
    .stMarkdown h4, .stMarkdown h5 {
        color: #00B4D8;
        font-weight: 600;
    }
    .stMarkdown ul {margin-bottom: 0.5em;}
    .stMarkdown p {margin-bottom: 0.5em;}
    .stAlert {border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)

# Header with modern look
st.markdown("""
<div style='display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1.5rem;'>
    <img src='https://img.icons8.com/ios-filled/100/0072C6/train.png' width='60' style='border-radius: 12px; box-shadow: 0 2px 8px rgba(0,114,198,0.10);'/>
    <div>
        <h1 style='margin-bottom: 0; font-size: 2.2rem;'>Train Gradient & Traction Feasibility Simulator</h1>
        <span style='font-size: 1.15rem; color: #00B4D8;'>A modern tool for infrastructure designers and track engineers.</span>
    </div>
</div>
---
""", unsafe_allow_html=True)

# Main layout: 2 columns with more space and padding
col1, col2 = st.columns([1.25, 1], gap="large")

with col1:
    st.markdown("### 🚄 Train & Track Configuration")
    with st.expander("Train Parameters", expanded=True):
        train_type = st.selectbox("Select Train Type", list(train_configs.keys()) + ["Custom"])
        if train_type != "Custom":
            config = train_configs[train_type]
            mass_kg = config.mass_kg
            tractive_effort_n = config.tractive_effort_n
        else:
            mass_kg = st.number_input("Train Mass (kg)", min_value=10000, max_value=500000, value=50000, step=1000)
            tractive_effort_n = st.number_input("Max Tractive Effort (N)", min_value=50000, max_value=1000000, value=200000, step=1000)
            train_type = "custom"
        train_length = st.number_input("Train Length (m)", min_value=10, max_value=500, value=200, step=10)
        train_config = TrainConfig(mass_kg=mass_kg, tractive_effort_n=tractive_effort_n, train_type=train_type)
    with st.expander("Track & Simulation Parameters", expanded=True):
        distance = st.number_input("Simulation Distance (m)", min_value=100, max_value=10000, value=1000, step=100)
        v_max = st.number_input("Max Speed (m/s)", min_value=5, max_value=100, value=55, step=1)
        dt = st.number_input("Time Step (s)", min_value=0.1, max_value=10.0, value=1.0, step=0.1, format="%0.1f")
        def_input = "0, 400, 700, 1000"
        def_slope = "1, 2, 1"
        lutning_pos = st.text_input("Slope Breakpoints (comma-separated, m)", def_input)
        lutning = st.text_input("Slope Values (comma-separated, %)", def_slope)
        def_curve_pos = "0, 500, 1000"
        def_curve_rad = "500, 200"
        curve_pos = st.text_input("Curve Breakpoints (comma-separated, m)", def_curve_pos)
        curve_radius = st.text_input("Curve Radii (comma-separated, m)", def_curve_rad)
    run_sim = st.button("Run Simulation", use_container_width=True)

with col2:
    st.markdown("### 📊 Results & Advanced Modules")
    module_names = [
        "Simulation Results",
        "Load Optimizer",
        "Braking & Safety",
        "Energy & Emissions",
        "Yard Designer",
        "Scenario Sandbox",
        "Spec Traceability",
        "Collaboration",
        "AI Assistant"
    ]
    selected_module = st.radio(
        "Select Module",
        module_names,
        horizontal=True,
        index=0,
        key="module_selector",
        help="Choose which module to run and view results."
    )
    if selected_module == "Simulation Results":
        if 'run_sim' not in locals():
            run_sim = False
        if run_sim:
            from train_sim.slope import calculate_equivalent_slope
            from train_sim.curve_resistance import calculate_curve_resistance
            from train_sim.acceleration import calculate_acceleration_profile
            from train_sim.braking import calculate_braking_profile
            from train_sim.block_occupancy import calculate_block_occupancy
            lutning_pos_arr = np.array([float(x.strip()) for x in lutning_pos.split(",")])
            lutning_arr = np.array([float(x.strip())/100 for x in lutning.split(",")])
            curve_pos_arr = np.array([float(x.strip()) for x in curve_pos.split(",")])
            curve_radius_arr = np.array([float(x.strip()) for x in curve_radius.split(",")])
            x_pos = np.arange(0, distance + dt, dt)
            ekv_slope = calculate_equivalent_slope(lutning_pos_arr, lutning_arr, x_pos, train_length)
            curve_res = calculate_curve_resistance(curve_pos_arr, curve_radius_arr, x_pos, train_length, mass_kg)
            mean_slope = np.nanmean(ekv_slope) * 100 if not np.all(np.isnan(ekv_slope)) else 0.0
            mean_curve_res = np.nanmean(curve_res) if not np.all(np.isnan(curve_res)) else 0.0
            acc_results = calculate_acceleration_profile(
                train_config,
                slope_percent=mean_slope,
                distance=distance,
                v_max=v_max,
                dt=dt,
                curve_resistance=mean_curve_res
            )
            braking_results = calculate_braking_profile(
                initial_speed=v_max,
                distance=distance,
                slope_profile=ekv_slope,
                deceleration_profile=-1.0,
                min_dec=-1.2,
                max_dec=-0.5,
                dt=dt
            )
            block_positions = np.array([200, 600, 900])
            speed_profile = acc_results['speed']
            position_profile = acc_results['distance']
            time_profile = np.arange(len(position_profile)) * dt
            release_speed = np.array([10.0, 10.0, 10.0])
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
            st.metric("Mean Slope (%)", f"{mean_slope:.2f}")
            st.metric("Mean Curve Resistance (N)", f"{mean_curve_res:.2f}")
            st.metric("Max Speed (m/s)", f"{np.max(acc_results['speed']):.2f}")
            st.markdown("---")
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
            st.pyplot(fig)
            st.markdown("**Block Occupancy Times (first 3 blocks):**")
            st.dataframe(block_times, use_container_width=True)
            st.markdown("---")
            if st.button("AI Summary of Simulation Results", key="ai_summary"):
                from train_sim.groq_ai import ai_summarize_simulation
                ai_summary = ai_summarize_simulation({
                    'mean_slope': mean_slope,
                    'mean_curve_res': mean_curve_res,
                    'max_speed': float(np.max(acc_results['speed'])),
                    'block_times': block_times.tolist()
                })
                st.info(ai_summary)
    elif selected_module == "Load Optimizer":
        st.markdown("#### 💰 Train Load Optimizer")
        colA, colB = st.columns([2, 1], gap="medium")
        with colA:
            if st.button("Run Load Optimizer", key="loadopt"):
                from train_sim.load_optimizer import calculate_max_train_load
                load_result = calculate_max_train_load(
                    gradient_profile=lutning,
                    loco_type=train_type,
                    speed_limits=np.full_like(lutning, v_max)
                )
                st.session_state['load_result'] = load_result
            if st.session_state.get('load_result'):
                import plotly.graph_objects as go
                load_result = st.session_state['load_result']
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = load_result['max_tonnage'],
                    title = {'text': "Max Tonnage (t)"},
                    gauge = {'axis': {'range': [None, max(100, load_result['max_tonnage']*1.2)]}}
                ))
                st.plotly_chart(fig, use_container_width=True)
                st.metric("Energy Estimate (kWh)", load_result['energy_estimate'])
        with colB:
            st.markdown("<div style='margin-top:1.5em'></div>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:1.1em;font-weight:600;color:#0072C6;'>AI Explanation</span>", unsafe_allow_html=True)
            if st.session_state.get('load_result'):
                if st.button("Explain with AI 🤖", key="ai_loadopt", use_container_width=True):
                    from train_sim.groq_ai import ai_summarize_simulation
                    ai_summary = ai_summarize_simulation(st.session_state['load_result'])
                    st.info(ai_summary)
            else:
                st.caption("Run the optimizer to enable AI explanation.")
    elif selected_module == "Braking & Safety":
        st.markdown("#### 📋 Braking & Safety Profile Simulator")
        if st.button("Run Safety Simulator", key="safety"):
            from train_sim.safety_profile import simulate_braking_and_safety
            safety_result = simulate_braking_and_safety(
                speed_profile=np.full_like(lutning, v_max),
                gradient_profile=lutning,
                entry_exit_paths=[]
            )
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=safety_result['stopping_distances'], mode='lines+markers', name='Stopping Distance (m)'))
            fig.update_layout(title="Stopping Distances", xaxis_title="Segment", yaxis_title="Distance (m)")
            st.plotly_chart(fig, use_container_width=True)
            if safety_result['violations']:
                st.error(f"Violations: {safety_result['violations']}")
            else:
                st.success("No safety violations detected.")
    elif selected_module == "Energy & Emissions":
        st.markdown("#### 🌱 Energy & Emissions Estimator")
        power_type = st.selectbox("Power Type", ["diesel", "electric", "hybrid"], key="power")
        if st.button("Estimate Energy & Emissions", key="energy"):
            from train_sim.energy_emissions import estimate_energy_and_emissions
            energy_result = estimate_energy_and_emissions(
                train_config=train_config,
                gradient_profile=lutning,
                speed_profile=np.full_like(lutning, v_max),
                power_type=power_type
            )
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Bar(x=["Energy (kWh)", "CO₂ (kg)"], y=[energy_result['energy_consumed_kwh'], energy_result['co2_emitted_kg']], marker_color=['#0072C6', '#00B4D8']))
            fig.update_layout(title="Energy & Emissions", yaxis_title="Value")
            st.plotly_chart(fig, use_container_width=True)
    elif selected_module == "Yard Designer":
        st.markdown("#### 🏗 Interactive Yard Designer")
        if st.button("Simulate Yard Layout", key="yard"):
            from train_sim.yard_designer import simulate_yard_layout
            yard_layout = {"tracks": 3, "switches": 2, "platforms": 1}
            train_movements = ["arrive", "depart"]
            yard_result = simulate_yard_layout(yard_layout, train_movements)
            import plotly.graph_objects as go
            fig = go.Figure()
            times = [m['time'] for m in yard_result['movement_log']]
            delays = [m['delay'] for m in yard_result['movement_log']]
            fig.add_trace(go.Bar(x=times, y=delays, name='Delay (min)', marker_color='#0072C6'))
            fig.update_layout(title="Train Movement Delays", xaxis_title="Time (min)", yaxis_title="Delay (min)")
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Throughput (trains/hr)", yard_result['throughput'])
    elif selected_module == "Scenario Sandbox":
        st.markdown("#### 🔍 Scenario Sandbox")
        if st.button("Run Scenario Sandbox", key="sandbox"):
            from train_sim.scenario_sandbox import run_scenario_sandbox
            scenarios = [
                {"name": "Baseline", "traffic": 100},
                {"name": "+15% traffic", "traffic": 115},
                {"name": "Add second loco", "traffic": 100, "locos": 2}
            ]
            sandbox_result = run_scenario_sandbox(scenarios)
            import plotly.graph_objects as go
            fig = go.Figure()
            for metric in ['profit', 'energy_consumption', 'throughput']:
                y = [r['metrics'][metric] for r in sandbox_result['results']]
                fig.add_trace(go.Bar(x=[r['name'] for r in sandbox_result['results']], y=y, name=metric.capitalize()))
            fig.update_layout(barmode='group', title="Scenario KPI Comparison")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(sandbox_result['narrative'])
    elif selected_module == "Spec Traceability":
        st.markdown("#### 📎 Spec-to-Sim Traceability Layer")
        if st.button("Trace Spec to Sim", key="trace"):
            from train_sim.spec_traceability import trace_spec_to_sim
            requirements = ["Max speed < 60 m/s", "Stop within 800m"]
            sim_results = {"max_speed": 55, "stopping_distance": 750}
            trace_result = trace_spec_to_sim(requirements, sim_results)
            import plotly.graph_objects as go
            fig = go.Figure()
            status = [v['status'] for v in trace_result['trace_map'].values()]
            reqs = [v['text'] for v in trace_result['trace_map'].values()]
            color_map = {'compliant': '#00B4D8', 'violated': '#FF4B4B', 'unparseable': '#CCCCCC'}
            colors = [color_map.get(s, '#CCCCCC') for s in status]
            fig.add_trace(go.Bar(x=reqs, y=[1]*len(reqs), marker_color=colors, text=status, textposition='auto'))
            fig.update_layout(title="Spec Compliance", yaxis=dict(showticklabels=False), xaxis_title="Requirement")
            st.plotly_chart(fig, use_container_width=True)
    elif selected_module == "Collaboration":
        st.markdown("#### 👥 Collaborative Versioning + Comments")
        if st.button("Show Collaboration Tools", key="collab"):
            from train_sim.collab import manage_collaboration
            scenario_id = "baseline"
            action = "history"
            collab_result = manage_collaboration(scenario_id, action)
            import plotly.graph_objects as go
            fig = go.Figure()
            if collab_result['history']:
                times = [v['timestamp'] for v in collab_result['history']]
                numbers = [v['number'] for v in collab_result['history']]
                fig.add_trace(go.Scatter(x=times, y=numbers, mode='lines+markers', name='Version'))
                fig.update_layout(title="Scenario Version History", xaxis_title="Time", yaxis_title="Version #")
                st.plotly_chart(fig, use_container_width=True)
            st.write("**Comments:**", collab_result['comments'])
    elif selected_module == "AI Assistant":
        st.markdown("""
        <div style='background:linear-gradient(90deg,#0072C6 0%,#00B4D8 100%);padding:1.5em 1em 1em 1em;border-radius:14px;margin-bottom:1.5em;'>
            <span style='font-size:1.5em;font-weight:700;color:white;'>🤖 AI Assistant (Groq)</span><br>
            <span style='font-size:1.1em;color:white;'>Ask questions about your simulation, get optimization tips, or parse requirements using AI.</span>
        </div>
        """, unsafe_allow_html=True)
        ai_mode = st.radio("AI Task", ["Ask about simulation", "Parse requirements", "Explain Load Optimizer result"], horizontal=True)
        if ai_mode == "Ask about simulation":
            user_q = st.text_area("Your question about the simulation or results:")
            if st.button("Ask AI", key="ai_ask", use_container_width=True):
                from train_sim.groq_ai import ai_summarize_simulation
                sim_context = {
                    'mean_slope': mean_slope if 'mean_slope' in locals() else None,
                    'mean_curve_res': mean_curve_res if 'mean_curve_res' in locals() else None,
                }
                ai_answer = ai_summarize_simulation(sim_context, user_q)
                st.success(ai_answer)
        elif ai_mode == "Explain Load Optimizer result":
            if st.session_state.get('load_result'):
                if st.button("AI Explain Last Load Optimizer Result", key="ai_loadopt2", use_container_width=True):
                    from train_sim.groq_ai import ai_summarize_simulation
                    ai_summary = ai_summarize_simulation(st.session_state['load_result'])
                    st.info(ai_summary)
            else:
                st.info("Run the Load Optimizer first to get an AI explanation.")
        else:
            nl_req = st.text_area("Paste requirements in plain English:")
            if st.button("Parse Requirements with AI", key="ai_parse", use_container_width=True):
                from train_sim.groq_ai import ai_parse_requirements
                ai_struct = ai_parse_requirements(nl_req)
                st.code(ai_struct, language="json")
