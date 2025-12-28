import streamlit as st
import requests

st.set_page_config(page_title="Smart Bus Tracker", layout="centered")

st.title("🚌 Smart Bus Tracking & ETA Prediction")
st.write("Predict bus arrival time using a deep learning model")

st.subheader("Input: Recent Bus Speed Sequence")

# Simple input (for demo)
speed_sequence = st.text_input(
    "Enter 10 speed values (comma-separated)",
    "0.3,0.32,0.31,0.29,0.28,0.27,0.26,0.25,0.24,0.23"
)

if st.button("Predict ETA"):
    try:
        speeds = [float(x.strip()) for x in speed_sequence.split(",")]

        if len(speeds) != 10:
            st.error("Please enter exactly 10 speed values.")
        else:
            payload = {"speed_sequence": speeds}

            response = requests.post(
                "http://127.0.0.1:8000/predict_eta",
                json=payload,
                timeout=5
            )

            if response.status_code == 200:
                eta = response.json()["predicted_eta_minutes"]
                st.success(f"Predicted ETA (scaled): {eta:.3f}")
            else:
                st.error("API error occurred")

    except Exception as e:
        st.error(f"Invalid input or connection error: {e}")
