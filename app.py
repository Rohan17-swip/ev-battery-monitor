
import random
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="EV Battery Monitor",
    page_icon="🔌",
    layout="wide",
)

st.title("🔋 EV Battery Monitoring System")
st.caption(
    "Interactive Battery Management System (BMS) simulation | "
    "Python + Streamlit + Plotly"
)

st.info(
    "DEMO MODE: All sensor readings are simulated. "
    "This dashboard is not connected to a real battery."
)


# -----------------------------------
# Sidebar controls
# -----------------------------------
st.sidebar.header("Simulation Controls")

battery_capacity = st.sidebar.slider(
    "Battery capacity (kWh)",
    min_value=10,
    max_value=120,
    value=60,
    step=5,
)

st.sidebar.caption(
    "Capacity is used to estimate remaining energy from SOC."
)

if st.sidebar.button("Reset simulation", use_container_width=True):
    for key in ["soc", "history", "last_time"]:
        st.session_state.pop(key, None)
    st.rerun()


# -----------------------------------
# Initialize session data
# -----------------------------------
if "soc" not in st.session_state:
    st.session_state.soc = 78.0

if "history" not in st.session_state:
    st.session_state.history = []

if "last_time" not in st.session_state:
    st.session_state.last_time = datetime.now()


# -----------------------------------
# Generate a simulated reading
# -----------------------------------
def generate_reading():
    """Generate illustrative EV battery sensor values."""

    soc = float(st.session_state.soc)

    voltage = random.uniform(320.0, 400.0)
    current = random.uniform(10.0, 120.0)
    temperature = random.uniform(22.0, 48.0)

    # Positive current represents discharge in this demo.
    power_kw = voltage * current / 1000.0
    remaining_energy = battery_capacity * soc / 100.0

    # Illustrative health estimate, not a real SOH measurement.
    health = random.uniform(94.0, 100.0)

    if temperature >= 45:
        status = "HIGH TEMPERATURE"
    elif soc <= 20:
        status = "LOW BATTERY"
    else:
        status = "NORMAL"

    return {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Voltage (V)": round(voltage, 2),
        "Current (A)": round(current, 2),
        "Power (kW)": round(power_kw, 2),
        "Temperature (°C)": round(temperature, 2),
        "SOC (%)": round(soc, 1),
        "Energy (kWh)": round(remaining_energy, 2),
        "SOH estimate (%)": round(health, 1),
        "Status": status,
    }


# -----------------------------------
# Dashboard action
# -----------------------------------
if st.button("▶ Generate New Reading", type="primary"):
    # Change SOC slightly for each simulated measurement.
    st.session_state.soc = max(
        0.0,
        min(
            100.0,
            st.session_state.soc + random.uniform(-1.5, 0.5),
        ),
    )

    reading = generate_reading()
    st.session_state.history.append(reading)

    # Keep the most recent 50 readings.
    st.session_state.history = st.session_state.history[-50:]


if not st.session_state.history:
    st.session_state.history.append(generate_reading())


# -----------------------------------
# Latest reading and alerts
# -----------------------------------
latest = st.session_state.history[-1]

st.subheader("Battery Overview")

if latest["Status"] == "HIGH TEMPERATURE":
    st.error("⚠️ High simulated temperature! Check the demo reading.")
elif latest["Status"] == "LOW BATTERY":
    st.warning("🔋 Simulated state of charge is low.")
else:
    st.success("System status: NORMAL (simulated)")


# -----------------------------------
# KPI cards
# -----------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "State of Charge",
    f'{latest["SOC (%)"]:.1f}%',
)

col2.metric(
    "Battery Voltage",
    f'{latest["Voltage (V)"]:.1f} V',
)

col3.metric(
    "Battery Current",
    f'{latest["Current (A)"]:.1f} A',
)

col4.metric(
    "Battery Temperature",
    f'{latest["Temperature (°C)"]:.1f} °C',
)

col5, col6, col7 = st.columns(3)

col5.metric(
    "Power",
    f'{latest["Power (kW)"]:.2f} kW',
)

col6.metric(
    "Estimated Remaining Energy",
    f'{latest["Energy (kWh)"]:.2f} kWh',
)

col7.metric(
    "Illustrative SOH",
    f'{latest["SOH estimate (%)"]:.1f}%',
    help="Random demonstration value, not measured battery health.",
)


# -----------------------------------
# Battery charge indicator
# -----------------------------------
st.subheader("🔋 Battery Charge Level")

st.progress(int(latest["SOC (%)"]))

st.caption(
    f'{latest["SOC (%)"]:.1f}% charged | '
    f'Estimated remaining energy: {latest["Energy (kWh)"]:.2f} kWh'
)


# -----------------------------------
# Historical charts
# -----------------------------------
df = pd.DataFrame(st.session_state.history)

st.subheader("📊 Battery Performance Trends")

left, right = st.columns(2)

with left:
    voltage_chart = go.Figure()
    voltage_chart.add_trace(
        go.Scatter(
            x=df["Time"],
            y=df["Voltage (V)"],
            mode="lines+markers",
            name="Voltage",
        )
    )
    voltage_chart.update_layout(
        title="Voltage Trend",
        xaxis_title="Reading Time",
        yaxis_title="Voltage (V)",
        height=350,
    )
    st.plotly_chart(voltage_chart, use_container_width=True)

with right:
    temp_chart = go.Figure()
    temp_chart.add_trace(
        go.Scatter(
            x=df["Time"],
            y=df["Temperature (°C)"],
            mode="lines+markers",
            name="Temperature",
        )
    )
    temp_chart.add_hline(
        y=45,
        line_dash="dash",
        annotation_text="Demo warning threshold",
    )
    temp_chart.update_layout(
        title="Temperature Trend",
        xaxis_title="Reading Time",
        yaxis_title="Temperature (°C)",
        height=350,
    )
    st.plotly_chart(temp_chart, use_container_width=True)

soc_chart = go.Figure()
soc_chart.add_trace(
    go.Scatter(
        x=df["Time"],
        y=df["SOC (%)"],
        mode="lines+markers",
        name="SOC",
    )
)
soc_chart.update_layout(
    title="State of Charge Trend",
    xaxis_title="Reading Time",
    yaxis_title="SOC (%)",
    yaxis=dict(range=[0, 100]),
    height=350,
)
st.plotly_chart(soc_chart, use_container_width=True)


# -----------------------------------
# Reading history and CSV export
# -----------------------------------
st.subheader("📋 Recent Sensor Readings")

st.dataframe(
    df.iloc[::-1],
    use_container_width=True,
    hide_index=True,
)

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Readings as CSV",
    data=csv_data,
    file_name="ev_battery_readings.csv",
    mime="text/csv",
)

st.divider()

st.caption(
    "Educational simulation only. Values are randomly generated and "
    "must not be used for real battery safety decisions."
)