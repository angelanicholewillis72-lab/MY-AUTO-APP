import streamlit as st
import pandas as pd
import requests

# 1. SETUP: This makes the app look good on phones and computers
st.set_page_config(page_title="Auto Buyer Intelligence", layout="wide")

# 2. DATA: These are common codes you'd see on a build sheet (RPO codes)
# You can add more codes to this list later!
build_data = [
    {"Code": "Z71", "Description": "Off-Road Suspension Package", "Value": "High"},
    {"Code": "G80", "Description": "Auto-Locking Rear Differential", "Value": "Medium"},
    {"Code": "UQA", "Description": "Bose Premium 7-Speaker System", "Value": "High"},
    {"Code": "AN3", "Description": "Full-Feature Leather Bucket Seats", "Value": "High"},
    {"Code": "DL3", "Description": "Chrome Power-Adjustable Heated Mirrors", "Value": "Medium"},
    {"Code": "Z82", "Description": "Heavy-Duty Trailering Equipment", "Value": "High"},
    {"Code": "L83", "Description": "5.3L EcoTec3 V8 Engine", "Value": "Standard"},
]

# 3. HEADER: The top of your app
st.title("🚗 Auto Buyer Intelligence")
st.write("Target Markets: **North Carolina (NC) & Virginia (VA)**")
st.markdown("---")

# 4. SECTION: VIN DECODER
st.header("1. Verify Vehicle (VIN)")
vin_input = st.text_input("Enter 17-Character VIN:", placeholder="Type VIN here...")

if vin_input:
    # This calls the government database to check the VIN for free
    api_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin_input}?format=json"
    try:
        data = requests.get(api_url).json()['Results'][0]
        st.success(f"**Vehicle Found:** {data['ModelYear']} {data['Make']} {data['Model']}")
        st.info(f"**Details:** {data['BodyClass']} | {data['DriveType']} | Engine: {data['EngineCylinders']} Cyl")
    except:
        st.error("Invalid VIN or connection error.")

st.markdown("---")

# 5. SECTION: OPTION CODE SEARCH (Replaces CompNine frustration)
st.header("2. Search Option Codes")
st.write("Search for keywords like 'Leather', 'Bose', or 'Off-Road' to see if they are in the build.")
search_query = st.text_input("Type code or feature name:")

if search_query:
    # This filters your list based on what you type
    results = [item for item in build_data if search_query.lower() in item['Description'].lower() or search_query.lower() in item['Code'].lower()]
    
    if results:
        st.table(results) # Shows a clean table of matching parts
    else:
        st.warning("No matching options found in this build sheet.")

st.markdown("---")

# 6. SECTION: REGIONAL PRICING TRENDS
st.header("3. Regional Price Trends (NC/VA)")
location = st.selectbox("Select Your Current Area:", ["Raleigh/Charlotte, NC", "Richmond/Norfolk, VA"])

# Mock data for price trends
col1, col2 = st.columns(2)
col1.metric(label="Market Demand", value="High 🔥", delta="12% Increase")
col2.metric(label="Average Lead Time", value="4 Days", delta="-1 Day")

st.write(f"Current pricing trend in **{location}** for common auto parts:")
chart_data = pd.DataFrame([100, 102, 105, 103, 110, 115, 112], columns=['Price Trend Index'])
st.line_chart(chart_data)
