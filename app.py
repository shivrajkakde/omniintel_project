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
st.write("Welcome! This frontend connects directly to your local FastAPI backend to run predictions using your trained Scikit-Learn Random Forest model.")

st.divider()

# Sidebar inputs for the user
st.sidebar.header("Shipment Parameters")
shipping_cost = st.sidebar.number_input("Shipping Cost ($)", min_value=0.0, max_value=2000.0, value=250.0, step=10.0)
delivery_time_days = st.sidebar.number_input("Delivery Time (Days)", min_value=1, max_value=60, value=5, step=1)
historical_failure_rate = st.sidebar.slider("Supplier Historical Failure Rate", min_value=0.0, max_value=1.0, value=0.15, step=0.01)

# Main Dashboard Layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Input Summary")
    st.info(f"**Cost:** ${shipping_cost}\n\n**Delivery Time:** {delivery_time_days} Days\n\n**Failure Rate:** {historical_failure_rate * 100:.1f}%")

with col2:
    st.markdown("#### Action Center")
    predict_button = st.button("Run AI Risk Assessment", type="primary", use_container_width=True)

# When the user clicks the button, call the FastAPI backend
if predict_button:
    api_url = "api_url = "https://omniintel-backend.onrender.com/predict"
    payload = {
        "shipping_cost": shipping_cost,
        "delivery_time_days": delivery_time_days,
        "historical_failure_rate": historical_failure_rate
    }
    
    try:
        with st.spinner("Analyzing shipment risk via AI backend..."):
            response = requests.post(api_url, json=payload)
            
        if response.status_code == 200:
            result = response.json()
            risk_status = result["risk_assessment"]
            confidence = result["model_confidence"]
            
            st.divider()
            st.subheader("🎯 AI Prediction Result")
            
            if "High Risk" in risk_status:
                st.error(f"🚨 **Status:** {risk_status}")
            else:
                st.success(f"✅ **Status:** {risk_status}")
                
            st.metric(label="Model Confidence Score", value=f"{confidence}%")
            
        else:
            st.error(f"Server Error: Received status code {response.status_code}. Is your FastAPI backend running?")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI backend! Please make sure Uvicorn is running in your terminal (`uvicorn main:app --reload`).")