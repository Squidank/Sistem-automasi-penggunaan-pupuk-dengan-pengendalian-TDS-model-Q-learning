import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(layout="wide")
st.title("45-Day Chili Plant Simulation (Q-Learning)")

# Load CSV based on goal
@st.cache_data
def load_q_tables():
    tables = {}
    for goal in [600, 900, 1200]:
        # Make sure the file paths match your local directory
        df = pd.read_csv(f"file_uji/Output_iterasi_terbaik_{goal}.csv")
        df["State"] = df["State"].apply(eval)
        tables[goal] = df.set_index("State").to_dict(orient="index")
    return tables

def calculate_tds(vol_air, vol_nutrisi, tds_air, tds_nutrisi):
    return (vol_air * tds_air + vol_nutrisi * tds_nutrisi) / (vol_air + vol_nutrisi)

# Function to find the nearest state if the exact one is not found
def get_nearest_state(q_table, tds_air, tds_nutrisi):
    all_states = list(q_table.keys())
    closest_state = min(
        all_states,
        key=lambda s: abs(s[0] - tds_air) + abs(s[1] - tds_nutrisi)
    )
    return closest_state

# Tabs
tabs = st.tabs(["45-Day Simulation", "Manual Input"])

with tabs[0]:
    col1, col2 = st.columns(2)

    with col1:
        tds_air_init = st.number_input("Initial Raw Water TDS", min_value=1, value=400)
        air_toleransi_min = int(1)
        air_toleransi_max = int(tds_air_init)
        st.write(f"Raw Water TDS Range: {air_toleransi_min} - {air_toleransi_max} ppm")

    with col2:
        tds_nutrisi_init = st.number_input("Initial Nutrient TDS", min_value=1, value=2000)
        nutrisi_toleransi_min = int(tds_nutrisi_init * 0.7)
        nutrisi_toleransi_max = int(tds_nutrisi_init * 1.3)
        st.write(f"Nutrient TDS Range: {nutrisi_toleransi_min} - {nutrisi_toleransi_max} ppm")

    flow_rate = st.number_input("Pump Flow Rate (ml/s)", min_value=1.0, value=20.0, step=1.0)

    if st.button("Run 45-Day Simulation"):
        tds_goals = {1: 600, 2: 900, 3: 1200}
        q_tables = {goal: load_q_tables()[goal] for goal in tds_goals.values()}

        days = 45
        results = []

        for day in range(1, days + 1):
            if day <= 15:
                tds_goal = 600
            elif day <= 30:
                tds_goal = 900
            else:
                tds_goal = 1200

            q_table = q_tables[tds_goal]
            if not q_table:
                continue

            tds_air = random.randint(air_toleransi_min, air_toleransi_max)
            tds_nutrisi = random.randint(nutrisi_toleransi_min, nutrisi_toleransi_max)

            state = get_nearest_state(q_table, tds_air, tds_nutrisi)

            # Get the best action, ensure it is in tuple format
            raw_action = q_table[state]["Action"]
            best_action = eval(raw_action) if isinstance(raw_action, str) else tuple(raw_action)

            volume_air, volume_nutrisi = best_action

            waktu_pompa_air = round(volume_air / flow_rate, 2)
            waktu_pompa_nutrisi = round(volume_nutrisi / flow_rate, 2)
            total_volume = volume_air + volume_nutrisi
            tds_hasil = calculate_tds(volume_air, volume_nutrisi, state[0], state[1])

            results.append({
                "Day": day,
                "Raw Water TDS": tds_air,
                "Nutrient TDS": tds_nutrisi,
                "Water Vol (ml)": volume_air,
                "Nutrient Vol (ml)": volume_nutrisi,
                "Water Pump Time (s)": waktu_pompa_air,
                "Nutrient Pump Time (s)": waktu_pompa_nutrisi,
                "Total Volume (ml)": total_volume,
                "Goal TDS": tds_goal,
                "Resulting TDS": round(tds_hasil, 2),
            })

        df = pd.DataFrame(results)
        st.success("Simulation complete. Here are the results:")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="chili_plant_simulation.csv",
            mime='text/csv'
        )

        # Add Resulting TDS vs Goal TDS Chart
        st.subheader("Resulting TDS vs Goal TDS Chart")
        chart_df = df[["Day", "Resulting TDS", "Goal TDS"]].set_index("Day")
        chart = chart_df.index + 1
        st.line_chart(chart_df, color=["#5AF343", "#F75252"]) 

with tabs[1]:
    st.subheader("Daily Manual Input (Spot Checking)")

    manual_day = st.number_input("Day", min_value=1, max_value=45, value=1)
    manual_tds_air = st.number_input("Raw Water TDS (ppm)", min_value=1, value=150)
    manual_tds_nutrisi = st.number_input("Nutrient TDS (ppm)", min_value=1, value=2000)
    manual_flow_rate = st.number_input("Flow Rate (ml/s)", min_value=1.0, value=20.0, step=1.0)

    if manual_day <= 15:
        tds_goal_manual = 600
    elif manual_day <= 30:
        tds_goal_manual = 900
    else:
        tds_goal_manual = 1200

    q_table_manual = load_q_tables()[tds_goal_manual]
    state_manual = get_nearest_state(q_table_manual, manual_tds_air, manual_tds_nutrisi)
    action_manual = eval(q_table_manual[state_manual]["Action"])


    vol_air_manual, vol_nutrisi_manual = action_manual
    waktu_air = round(vol_air_manual / manual_flow_rate, 2)
    waktu_nutrisi = round(vol_nutrisi_manual / manual_flow_rate, 2)
    tds_hasil_manual = calculate_tds(vol_air_manual, vol_nutrisi_manual, manual_tds_air, manual_tds_nutrisi)

    if st.button("Run Simulation"):
        st.write(f"**Goal TDS Day {manual_day}:** {tds_goal_manual} ppm")
        st.write(f"**Resulting TDS:** {round(tds_hasil_manual, 2)} ppm")
        st.write(f"Water Volume: {vol_air_manual} ml")
        st.write(f"Nutrient Volume: {vol_nutrisi_manual} ml")
        st.write(f"Total Volume: {vol_air_manual + vol_nutrisi_manual} ml")
        st.write(f"Water Pump Time: {waktu_air} seconds")
        st.write(f"Nutrient Pump Time: {waktu_nutrisi} seconds")