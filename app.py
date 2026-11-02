import streamlit as st
import requests

st.set_page_config(page_title="OmniIntel Enterprise AI Dashboard", layout="wide")

st.title("📦 OmniIntel Enterprise AI Dashboard")
st.subheader("Real-Time Supply Chain Risk & Shipment Delay Predictor")

st.sidebar.header("Shipment Parameters")
shipping_cost = st.sidebar.number_input("Shipping Cost ($)", min_value=10.0, max_value=1000.0, value=250.0)
delivery_time_days = st.sidebar.number_input("Delivery Time (Days)", min_value=1, max_value=30, value=5)
historical_failure_rate = st.sidebar.slider("Supplier Historical Failure Rate", min_value=0.0, max_value=1.0, value=0.15)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Input Summary")
    st.info(f"**Cost:** ${shipping_cost}\n\n**Delivery Time:** {delivery_time_days} Days\n\n**Failure Rate:** {historical_failure_rate * 100}%")

with col2:
    st.markdown("### Action Center")
    predict_button = st.button("Run AI Risk Assessment", type="primary")

if predict_button:
    # ⚠️ REPLACE WITH YOUR ACTUAL RENDER BACKEND URL ENDING IN /predict
    api_url = "https://YOUR-ACTUAL-RENDER-SERVICE-NAME.onrender.com/predict"
    
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
            st.error(f"Server Error: Received status code {response.status_code}. Please verify your Render deployment.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI backend! Please check your Render URL.")