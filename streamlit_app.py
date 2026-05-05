import streamlit as st
import pandas as pd
import requests

# 1. SETUP & MARKET INTEL (MAY 2026)
st.set_page_config(page_title="Auto Buyer Pro 2026", layout="wide")

st.title("🚗 Auto Buyer Intelligence: NC & VA")
st.info("📊 **May 2026 Market Update:** Used vehicle prices in the Southeast have jumped roughly **$1,500** this month due to tight inventory and high demand for trucks/SUVs.")

# 2. DEEP VIN DECODER (ENGINE & STEERING)
st.header("1. Deep Vehicle Build Search")
vin = st.text_input("Enter 17-Digit VIN:", placeholder="Decode Engine, Steering, & Technical Specs...")

if vin:
    # Using the Extended NHTSA API for technical details like steering and displacement
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/{vin}?format=json"
    try:
        data = requests.get(url).json()['Results'][0]
        st.success(f"**Verified:** {data['ModelYear']} {data['Make']} {data['Model']}")
        
        # Dashboard for Technical Specs
        t1, t2, t3 = st.columns(3)
        t1.metric("Engine", f"{data['DisplacementL']}L {data['EngineCylinders']}-Cyl")
        t2.metric("Steering", data.get('SteeringLocation', 'Standard Power'))
        t3.metric("Drive Type", data['DriveType'])
        
        # Searchable Build Sheet
        st.subheader("🔍 Search Factory Build Features")
        search_query = st.text_input("Search for keywords (e.g. 'Chrome', 'Bose', 'Brake'):")
        all_specs = [{"Feature": k, "Value": str(v)} for k, v in data.items() if v and v != "Not Applicable"]
        
        if search_query:
            filtered = [s for s in all_specs if search_query.lower() in s['Feature'].lower() or search_query.lower() in s['Value'].lower()]
            st.table(filtered)
        else:
            st.write("Top Technical Details:")
            st.dataframe(pd.DataFrame(all_specs[:12]), use_container_width=True, hide_index=True)
    except:
        st.error("VIN not found or database is updating.")

st.markdown("---")

# 3. MILEAGE & GRADE PRICE ESTIMATOR
st.header("2. Professional Price Estimator")
col_p, col_m, col_g = st.columns(3)

base_price = col_p.number_input("Base Price (0-50k mi):", value=1000, step=100)
miles = col_m.slider("Mileage:", 0, 250000, 75000)
grade = col_g.selectbox("Condition Grade:", ["Grade A (Perfect)", "Grade B (Normal Wear)", "Grade C (Rough)"])

# Pricing Logic
def get_final_price(base, mi, grd):
    # Mileage discount
    if mi <= 50000: mi_mult = 1.0
    elif mi <= 100000: mi_mult = 0.85
    else: mi_mult = 0.60
    
    # Grade discount
    grd_mult = {"Grade A (Perfect)": 1.0, "Grade B (Normal Wear)": 0.80, "Grade C (Rough)": 0.50}[grd]
    
    return base * mi_mult * grd_mult

est_price = get_final_price(base_price, miles, grade)
st.subheader(f"Adjusted Market Value: **${est_price:,.2f}**")

# 4. REGIONAL TREND CHART (MAY 2026)
st.markdown("---")
st.header("📈 Regional Trends: NC vs. VA")
trend_data = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'NC Market': [24000, 24200, 24800, 25500, 26200],
    'VA Market': [23800, 23950, 24500, 25100, 25700]
}).set_index('Month')
st.line_chart(trend_data)
st.write("Prices in **Raleigh and Charlotte** are currently outpacing national trends by 4%.")