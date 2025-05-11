import streamlit as st # Streamlit for building interactive web apps
import pandas as pd  # Pandas for handling data in DataFrames
import joblib  # Joblib for loading the trained ML model
import folium # Folium for rendering maps
from streamlit_folium import st_folium # Streamlit wrapper to display folium maps

 # Load the pre-trained model from a file
model = joblib.load('my_model.pkl') 
 # Set the title of the app
st.title("Predict Sales Based on Location and Features") 
 
 # Display a map for the user to select a location
st.write("Select Location on Map:")  
m = folium.Map(location=[26, 35], zoom_start=5)# Center the map
marker = folium.Marker(location=[26, 35], draggable=True) # Add a draggable marker 
marker.add_to(m)  # Add the marker to the map
output = st_folium(m, width=700, height=500) # Render the map in the app
 
# Default coordinates
LAT, LONG = 26, 35 
# Update coordinates if the user clicks on the map
if output and output.get("last_clicked"): 
    LAT = output["last_clicked"]["lat"] 
    LONG = output["last_clicked"]["lng"] 
# Update coordinates if the user clicks on an object

elif output and output.get("last_object_clicked"): 
    LAT = output["last_object_clicked"]["lat"] 
    LONG = output["last_object_clicked"]["lng"] 

# Show the selected latitude and longitude 
st.write(f"Latitude: {LAT:.4f}, Longitude: {LONG:.4f}") 

# Collect input features from the user 
discount = st.number_input("Discount", min_value=0.0, max_value=1.0, value=0.0) 
profit = st.number_input("Profit", value=0.0) 
price = st.number_input("Price", value=0.0) 
returned = st.selectbox("Returned_Binary", [0, 1]) # Whether the product was returned (binary)

# Category selection
categories = [ 
    'Office Supplies', 'Technology', 'Appliances', 'Art', 'Binders', 'Bookcases', 'Chairs', 'Copiers', 
    'Envelopes', 'Fasteners', 'Furnishings', 'Labels', 'Machines', 'Paper', 'Phones', 'Storage', 
    'Supplies', 'Tables' 
] 

# Segment selection
selected_category = st.selectbox("Category", categories) 
segments = ['Corporate', 'Home Office'] 
selected_segment = st.selectbox("Segment", segments) 
# Date inputs
year = st.number_input("Year", min_value=2000, max_value=2100, value=2024) 
month = st.number_input("Month", min_value=1, max_value=12, value=1) 
day = st.number_input("Day", min_value=1, max_value=31, value=1) 
# Build a dictionary of all inputs 
input_dict = { 
    'Discount': discount, 
    'Profit': profit, 
    'LAT': LAT, 
    'LONG': LONG, 
    'Price': price, 
    'Returned_Binary': returned, 
} 
# One-hot encode the selected category 
for cat in categories: 
    input_dict[cat] = 1 if cat == selected_category else 0 
# One-hot encode the selected segment    
for seg in segments: 
    input_dict[seg] = 1 if seg == selected_segment else 0 
# Add date features
input_dict['Year'] = year 
input_dict['Month'] = month 
input_dict['Day'] = day 
# Create a DataFrame from the input 
X = pd.DataFrame([input_dict]) 
# Button to trigger prediction 
if st.button("Predict Profit"): 
    prediction = model.predict(X)[0] 
    st.success(f"Predicted Sales: {prediction:.2f}")
