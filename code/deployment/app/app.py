import streamlit as st
import requests
import numpy as np

API_URL = "http://172.18.0.2:8000/predict"

st.title("Laptop Price Predictor")

st.write("Enter the laptop characteristics:")

Company = st.text_input("Company")
Product = st.text_input("Product")
Typename = st.text_input("Typename")
Inches = st.number_input("Inches", min_value=10.0, max_value=20.0, step=0.1)
ScreenResolution = st.text_input("Screen Resolution")
CPU_Company = st.text_input("CPU Company")
CPU_Type = st.text_input("CPU Type")
CPU_Frequency = st.number_input("CPU Frequency (GHz)", min_value=0.5, max_value=5.0, step=0.1)
RAM = st.text_input("RAM")
Memory = st.text_input("Memory")
GPU_Company = st.text_input("GPU Company")
GPU_Type = st.text_input("GPU Type")
OpSys = st.text_input("Operating System")
Weight = st.number_input("Weight (kg)", min_value=0.5, max_value=5.0, step=0.1)

if st.button("Predict Price"):
    payload = {
        "Company": Company,
        "Product": Product,
        "TypeName": Typename,
        "Inches": Inches,
        "ScreenResolution": ScreenResolution,
        "CPU_Company": CPU_Company,
        "CPU_Type": CPU_Type,
        "CPU_Frequency": CPU_Frequency,
        "RAM": RAM,
        "Memory": Memory,
        "GPU_Company": GPU_Company,
        "GPU_Type": GPU_Type,
        "OpSys": OpSys,
        "Weight": Weight
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"Predicted Price: €{prediction['Price']:.2f}")
        else:
            st.error("Prediction failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Prediction failed: {e}")

