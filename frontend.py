import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Prediction")

st.markdown("Enter Below Details to Predict Insurance Premium")

# input fields for user data
age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (in kg)", min_value=1.0,  value=70.0)
height = st.number_input("Height (in meters)", min_value=0.5, max_value=2.5, value=1.75)
income_lpa = st.number_input("Annual Salary (in LPA)", min_value=0.0, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Delhi")
occupation = st.selectbox("Occupation", ['student', 'government_job', 'private_job', 'freelancer',
       'retired', 'business_owner', 'unemployed'])

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Premium Category: **{result['predicted_category']}**")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Please ensure the backend server is running.")       

