import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="🚗 Car Price Predictor",
    page_icon="🚘",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Main function
def main():
    # Sidebar for user instructions
    st.sidebar.header("How to use this app")
    st.sidebar.write("""
    1. Enter the details of your car.  
    2. Click the **Predict** button.  
    3. Get the estimated price instantly!  
    """)

    # App header with style
    st.markdown(
        "<h1 style='text-align: center; color: #FF4B4B;'>🚗 Car Price Predictor</h1>",
        unsafe_allow_html=True
    )
    
    st.markdown("---")  # horizontal line for separation
    
    # Input fields in columns for better UI
    col1, col2 = st.columns(2)
    
    with col1:
        Year = st.number_input("Year of Manufacture", min_value=1990, max_value=2030, value=2015, step=1)
        Kms_Driven = st.number_input("Kilometers Driven (in km)", min_value=0, value=50000, step=1000)
        Fuel_Type = st.selectbox("Fuel Type", ("CNG", "Diesel", "Petrol"))
    
    with col2:
        Present_Price = st.number_input("Current Price (in lacs)", min_value=0.0, value=5.0, step=0.5, format="%.2f")
        Transmission = st.selectbox("Transmission Type", ("Automatic", "Manual"))
        Owner = st.selectbox("Number of Owners", ("First", "Second", "Third", "Fourth"))
    
    # Encode categorical inputs
    fuel_map = {"CNG": 0, "Diesel": 1, "Petrol": 2}
    transmission_map = {"Automatic": 0, "Manual": 1}
    owner_map = {"First": 0, "Second": 1, "Third": 2, "Fourth": 3}

    input_data = {
        "Year": Year,
        "Kms_Driven": Kms_Driven,
        "Present_Price": Present_Price,
        "Fuel_Type": fuel_map[Fuel_Type],
        "Transmission": transmission_map[Transmission],
        "Owner": owner_map[Owner]
    }

    st.markdown("---")
    
    # Predict button
    if st.button("💰 Predict Price"):
        with st.spinner('Predicting...'):
            try:
                response = requests.post(url="http://127.0.0.1:8000/predict", data=json.dumps(input_data))
                price = response.json().get("prediction", 0)
                st.success(f"✅ The estimated price of your car is **₹ {price} lakhs**")
                
                st.balloons()  # fun animation
            except Exception as e:
                st.error("❌ Failed to fetch prediction. Please make sure the API is running.")
                st.warning(f"Error details: {e}")

if __name__ == "__main__":
    main()
