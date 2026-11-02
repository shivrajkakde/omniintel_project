import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="OmniIntel Supply Chain Intelligence",
    page_icon="📦",
    layout="centered"
)

st.title("📦 OmniIntel Enterprise AI Dashboard")
st.markdown("### Real-Time Supply Chain Risk & Shipment Delay Predictor")
st.write("Welcome! This frontend connects directly to your local FastAPI backend to run live AI risk evaluations.")

st.divider()

# Sidebar inputs for the user
st.sidebar.header("Shipment Parameters")
shipping_cost = st.sidebar.number_input("Shipping Cost ($)", min_value=0.0, max_value=10000.0, value=150.0, step=10.0)
delivery_time_days = st.sidebar.number_input("Delivery Time (Days)", min_value=1, max_value=90, value=5, step=1)

# Main container for results
st.subheader("📊 Evaluation Panel")

if st.button("Run AI Risk Assessment", type="primary"):
    payload = {
        "shipping_cost": shipping_cost,
        "delivery_time_days": delivery_time_days
    }
    
    try:
        # Send request to FastAPI backend
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            st.success("Prediction generated successfully via FastAPI backend!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Predicted Status", value=result["status"])
            with col2:
                st.metric(label="Delay Probability", value=f"{result['delay_probability']}%")
        else:
            st.error(f"Backend Error: {response.json().get('detail', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI backend! Make sure main.py is running on port 8000.")