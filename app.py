import streamlit as st
import joblib
import pandas as pd
from datetime import datetime
import time

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="🏠 House Price Predictor",
    page_icon="🏡",
    layout="wide"
)

# =========================
# Custom CSS Styling
# =========================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, rgba(34,193,195,0.6), rgba(253,187,45,0.6)),
                    url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Glassmorphism container */
    .glass {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    /* Input fields */
    input, select {
        border-radius: 8px !important;
        padding: 10px !important;
    }
    /* Gradient button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(to right, #2E7D32, #66BB6A) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 12px !important;
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    /* Price display animation container */
    .price-box {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        border: 2px solid #2E7D32;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# Load Model
# =========================
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# =========================
# Title Section
# =========================
st.markdown(
    "<div class='glass' style='text-align:center;'><h1>🏡 House Price Prediction</h1><p>Find out how much your dream home could cost instantly!</p></div>",
    unsafe_allow_html=True
)

# =========================
# Layout: Input Form
# =========================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📐 Property Details")
    area = st.number_input("Area (sq ft)", 1.0, 10000.0, 1200.0)
    bedrooms = st.number_input("Bedrooms 🛏", 1, 10, 2)
    bathrooms = st.number_input("Bathrooms 🚽", 1, 10, 2)
    balconies = st.number_input("Balconies 🌇", 0, 5, 1)
    building_type = st.selectbox("Building Type 🏢", ["Apartment", "Independent House", "Villa", "Penthouse", "Builder Floor"])

with col2:
    st.subheader("📍 Location & Amenities")
    latitude = st.number_input("Latitude", -90.0, 90.0)
    longitude = st.number_input("Longitude", -180.0, 180.0)
    ready_to_move = st.radio("Ready to Move? 🔑", ["No", "Yes"], horizontal=True)
    parking = st.radio("Parking Available? 🚗", ["No", "Yes"], horizontal=True)
    furnishing = st.select_slider("Furnishing Status 🪑", ["Unfurnished", "Semi-Furnished", "Fully-Furnished"], value="Semi-Furnished")

# =========================
# Preprocess Inputs
# =========================
ready_to_move = 1 if ready_to_move == "Yes" else 0
parking = 1 if parking == "Yes" else 0
furnishing = {"Unfurnished": 0, "Semi-Furnished": 1, "Fully-Furnished": 2}[furnishing]
building_type = ["Apartment", "Independent House", "Villa", "Penthouse", "Builder Floor"].index(building_type)

# =========================
# Prediction Button
# =========================
if st.button("🎯 Calculate Price"):
    features = [[area, latitude, longitude, bedrooms, bathrooms, balconies, ready_to_move, parking, furnishing, building_type]]
    prediction = model.predict(features)
    price = int(prediction[0])

    # Price animation
    placeholder = st.empty()
    for val in range(0, price, max(1, price//50)):
        placeholder.markdown(f"<div class='price-box'><h2>Estimated Price</h2><h1 style='color:#2E7D32;'>₹{val:,}</h1><p>Calculated on {datetime.now().strftime('%B %d, %Y')}</p></div>", unsafe_allow_html=True)
        time.sleep(0.02)
    placeholder.markdown(f"<div class='price-box'><h2>Estimated Price</h2><h1 style='color:#2E7D32;'>₹{price:,}</h1><p>Calculated on {datetime.now().strftime('%B %d, %Y')}</p></div>", unsafe_allow_html=True)

    # Property insights
    st.subheader("📊 Property Insights")
    insight_cols = st.columns(3)
    with insight_cols[0]:
        st.metric("💰 Price per sq ft", f"₹{price//area:,}")
    with insight_cols[1]:
        st.metric("🏠 Total Rooms", f"{bedrooms + bathrooms}")
    with insight_cols[2]:
        st.metric("✨ Amenities Score", f"{parking + balconies + furnishing}/4")

# =========================
# Side Info Panel
# =========================
with st.sidebar:
    st.markdown("### ℹ Tips for Better Prediction")
    st.write("✅ Enter accurate latitude & longitude for precise pricing.")
    st.write("✅ Higher furnishing scores often increase property value.")
    st.write("✅ Properties ready to move usually have a premium price.")

st.markdown("<hr><div style='text-align:center;'>Made with ❤ | Demo Purpose Only</div>", unsafe_allow_html=True)