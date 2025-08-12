import streamlit as st
import joblib
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# Single, clean CSS styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), 
                    url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Common container style for all components */
    .element-container, div.stMarkdown, div.stButton, div.stRadio > div {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Input fields */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stSelectbox > div > div > div {
        background-color: white !important;
        color: #333333 !important;
        border: 1px solid #cccccc !important;
        border-radius: 4px !important;
        padding: 8px !important;
    }
    
    /* Radio buttons */
    .stRadio > div > div > label {
        background-color: white !important;
        color: #333333 !important;
        padding: 8px 16px !important;
        border: 1px solid #cccccc !important;
        border-radius: 20px !important;
        margin: 0 5px !important;
    }
    
    .stRadio > div > div > label:hover {
        background-color: #f0f0f0 !important;
        border-color: #2E7D32 !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: #2E7D32 !important;
        color: white !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        border: none !important;
        border-radius: 4px !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background-color: #1B5E20 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }

    /* Headers and text */
    h1, h2, h3, h4, h5, p {
        color: #333333 !important;
        font-weight: 500 !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #2E7D32 !important;
    }
    
    /* Main content area */
    .main > div {
        padding: 20px !important;
    }
    
    /* Footer */
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)



# Load the model
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# Load the model
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# Title and description
st.markdown("""
    <div style='background-color: rgba(255, 255, 255, 0.85); padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #333333; margin-bottom: 10px;'>
            🏠 House Price Prediction
        </h1>
        <p style='color: #666666; font-size: 1.2em; margin: 0;'>
            Get an instant estimate for your dream home! 🎯
        </p>
    </div>
""", unsafe_allow_html=True)

# Create two columns for input fields
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("##### 📐 Property Details")
    area = st.number_input("Area (sq ft)", 
                          min_value=1.0, 
                          max_value=10000.0,
                          help="Enter the total area of the property in square feet")
    
    bedrooms = st.number_input("Number of Bedrooms 🛏️", 
                              min_value=1, 
                              max_value=10,
                              value=2)
    
    bathrooms = st.number_input("Number of Bathrooms 🚽", 
                               min_value=1, 
                               max_value=10,
                               value=2)
    
    balconies = st.number_input("Number of Balconies 🏗️", 
                               min_value=0, 
                               max_value=5,
                               value=1)
    
    building_type = st.selectbox("Building Type 🏢",
                             ["Apartment", "Independent House", "Villa", "Penthouse", "Builder Floor"])

with col2:
    st.markdown("##### 📍 Location & Amenities")
    latitude = st.number_input("Latitude", 
                             min_value=-90.0, 
                             max_value=90.0)
    
    longitude = st.number_input("Longitude", 
                              min_value=-180.0, 
                              max_value=180.0)
    
    ready_to_move = st.radio("Ready to Move? 🔑", 
                            ["No", "Yes"],
                            horizontal=True,
                            label_visibility="visible")
    
    parking = st.radio("Parking Available? 🚗", 
                      ["No", "Yes"],
                      horizontal=True,
                      label_visibility="visible")
    
    furnishing = st.select_slider("Furnishing Status 🪑",
                                 options=["Unfurnished", "Semi-Furnished", "Fully-Furnished"],
                                 value="Semi-Furnished")

# Convert inputs to model format
ready_to_move = 1 if ready_to_move == "Yes" else 0
parking = 1 if parking == "Yes" else 0
furnishing = {"Unfurnished": 0, "Semi-Furnished": 1, "Fully-Furnished": 2}[furnishing]
building_type = ["Apartment", "Independent House", "Villa", "Penthouse", "Builder Floor"].index(building_type)

# Prediction button
if st.button("Calculate Price 🎯"):
    features = [[area, latitude, longitude, bedrooms, bathrooms, balconies, 
                ready_to_move, parking, furnishing, building_type]]
    prediction = model.predict(features)
    
    # Display prediction
    st.markdown("""
        <div style='background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px; 
                    text-align: center; margin: 20px 0; border: 1px solid #90A4AE;'>
            <h2 style='color: #1a237e; margin-bottom: 10px;'>Estimated Price</h2>
            <h1 style='color: #2E7D32; font-size: 2.5em; margin: 10px 0;'>
                ₹{:,}
            </h1>
            <p style='color: #666; margin-top: 10px;'>
                Calculated on {}
            </p>
        </div>
    """.format(int(prediction[0]), datetime.now().strftime('%B %d, %Y')), unsafe_allow_html=True)
    
    # Display insights in a cleaner format
    st.markdown("#### 📊 Property Insights")
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"""
            <div style='background-color: rgba(255, 255, 255, 0.9); padding: 10px; border-radius: 5px; 
                        text-align: center; border: 1px solid #90A4AE;'>
                <p style='margin: 0; color: #666;'>Price per sq ft</p>
                <h3 style='margin: 5px 0; color: #1a237e;'>₹{int(prediction[0]/area):,}</h3>
            </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
            <div style='background-color: rgba(255, 255, 255, 0.9); padding: 10px; border-radius: 5px; 
                        text-align: center; border: 1px solid #90A4AE;'>
                <p style='margin: 0; color: #666;'>Total Rooms</p>
                <h3 style='margin: 5px 0; color: #1a237e;'>{bedrooms + bathrooms}</h3>
            </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
            <div style='background-color: rgba(255, 255, 255, 0.9); padding: 10px; border-radius: 5px; 
                        text-align: center; border: 1px solid #90A4AE;'>
                <p style='margin: 0; color: #666;'>Amenities Score</p>
                <h3 style='margin: 5px 0; color: #1a237e;'>{parking + balconies + furnishing}/4</h3>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Made with ❤️ | Data and predictions are for demonstration purposes only
    </div>
    """,
    unsafe_allow_html=True
)    