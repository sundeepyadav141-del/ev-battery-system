import streamlit as st
from ev_battery_system import EVBatterySystem

# Page configuration
st.set_page_config(
    page_title="EV Battery Intelligence System",
    page_icon="🔋",
    layout="wide"
)

# Header
st.title("🔋 EV Battery Intelligence System")
st.markdown("### Advanced Battery Management & Range Optimization")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("⚙️ Battery Specifications")

battery_capacity = st.sidebar.number_input(
    "Battery Capacity (kWh)", 
    min_value=20.0, 
    max_value=200.0, 
    value=60.0, 
    step=5.0
)

battery_age = st.sidebar.number_input(
    "Battery Age (years)", 
    min_value=0.0, 
    max_value=15.0, 
    value=2.0, 
    step=0.5
)

current_charge = st.sidebar.slider(
    "Current Charge Level (%)", 
    min_value=0, 
    max_value=100, 
    value=75
)

st.sidebar.markdown("---")
st.sidebar.header("📊 Usage Patterns")

cycles_per_year = st.sidebar.number_input(
    "Charge Cycles per Year", 
    min_value=50, 
    max_value=500, 
    value=200, 
    step=10
)

fast_charge_usage = st.sidebar.slider(
    "Fast Charging Usage (%)", 
    min_value=0, 
    max_value=100, 
    value=30
)

# Initialize EV System
ev = EVBatterySystem(battery_capacity_kwh=battery_capacity)
ev.current_charge = current_charge

# Battery Health Analysis
st.header("📊 Battery Health Analysis")

degradation = ev.calculate_battery_degradation(
    years_used=battery_age,
    avg_cycles_per_year=cycles_per_year,
    fast_charge_percentage=fast_charge_usage
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("State of Health", f"{degradation['current_soh']}%")
with col2:
    st.metric("Degradation", f"{degradation['degradation_percentage']}%")
with col3:
    st.metric("Health Status", degradation['health_status'])
with col4:
    st.metric("Available Capacity", f"{ev.calculate_available_capacity():.1f} kWh")

# Range Prediction
st.markdown("---")
st.header("🚗 Range Prediction")

col1, col2 = st.columns(2)

with col1:
    speed = st.number_input("Average Speed (km/h)", 20, 160, 80, 5)
    temperature = st.number_input("Temperature (°C)", -20, 50, 25, 1)
    ac_usage = st.checkbox("AC Usage")

with col2:
    driving_style = st.selectbox("Driving Style", ["eco", "normal", "sport"])
    terrain = st.selectbox("Terrain", ["flat", "hilly", "mountain"])

range_data = ev.predict_range(
    speed_kmh=speed,
    temperature_c=temperature,
    ac_usage=ac_usage,
    driving_style=driving_style,
    terrain=terrain
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Predicted Range", f"{range_data['range_km']} km")
with col2:
    st.metric("Consumption", f"{range_data['consumption_per_100km']} kWh/100km")
with col3:
    st.metric("Available Energy", f"{range_data['available_energy_kwh']} kWh")

# Charging Analysis
st.markdown("---")
st.header("⚡ Charging Analysis")

col1, col2 = st.columns(2)

with col1:
    target_charge = st.slider("Target Charge (%)", 0, 100, 100)

with col2:
    charger_type = st.selectbox(
        "Charger Type",
        ["Home (3.7 kW)", "Fast Home (7.4 kW)", "DC Fast (50 kW)", "Ultra-Fast (150 kW)"]
    )
    
charger_powers = {
    "Home (3.7 kW)": 3.7,
    "Fast Home (7.4 kW)": 7.4,
    "DC Fast (50 kW)": 50,
    "Ultra-Fast (150 kW)": 150
}

charging_data = ev.calculate_charging_time(
    target_charge=target_charge,
    charger_power_kw=charger_powers[charger_type]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Charging Time", f"{charging_data['charging_time_hours']:.1f} hours")
with col2:
    st.metric("Minutes", f"{charging_data['charging_time_minutes']:.0f} min")
with col3:
    st.metric("Energy Added", f"{charging_data['energy_added_kwh']:.1f} kWh")

# Cost Comparison
st.markdown("---")
st.header("💰 Cost Comparison: EV vs ICE")

col1, col2 = st.columns(2)

with col1:
    annual_km = st.number_input("Annual Distance (km)", 5000, 50000, 15000, 1000)
    petrol_price = st.number_input("Petrol Price (₹/L)", 50.0, 200.0, 110.0, 5.0)

with col2:
    electricity_price = st.number_input("Electricity Price (₹/kWh)", 2.0, 20.0, 8.0, 0.5)
    ice_efficiency = st.number_input("ICE Efficiency (km/L)", 5.0, 30.0, 15.0, 1.0)

cost_comparison = ev.compare_ev_vs_ice(
    annual_km=annual_km,
    petrol_price_per_liter=petrol_price/100,
    electricity_price_per_kwh=electricity_price/100,
    ice_fuel_efficiency=ice_efficiency
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("EV Annual Cost", f"₹{cost_comparison['ev_annual_cost']*100:,.0f}")
with col2:
    st.metric("ICE Annual Cost", f"₹{cost_comparison['ice_annual_cost']*100:,.0f}")
with col3:
    st.metric("Annual Savings", f"₹{cost_comparison['annual_savings']*100:,.0f}")
with col4:
    st.metric("Monthly Savings", f"₹{cost_comparison['monthly_savings']*100:,.0f}")

# Recommendations
st.markdown("---")
st.header("💡 Battery Care Recommendations")

recommendations = ev.optimal_charging_recommendation()
for rec in recommendations:
    st.info(rec)

# Footer
st.markdown("---")
st.markdown("**EV Battery Intelligence System** | Built for the Automotive Industry")

7. **Press Ctrl+S** to save

---

## **STEP 2: Create requirements.txt file**

1. **Right-click** again in the file explorer (left sidebar)

2. Click **"New File"**

3. Type the name: `requirements.txt` and press **Enter**

4. **Click on the `requirements.txt` file** to open it

5. **Paste ONLY this one line:**
```
streamlit

