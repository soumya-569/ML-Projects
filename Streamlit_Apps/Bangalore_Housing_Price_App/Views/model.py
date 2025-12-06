import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import pickle
import json
import time
from chart_clean import location_wise_average,price_comparison_chart

# ** Import Robot Animation
bot_path = "Streamlit_Apps/Bangalore_Housing_Price_App/Anima Bot.json"

with open(bot_path,'r',encoding="utf-8") as load_robot:
    robot = json.load(load_robot)

# ** Import CSS Styling
css_path = "Streamlit_Apps/Bangalore_Housing_Price_App/CSS/model.css"

with open(css_path) as load_css:
    st.markdown(f"<style>{load_css.read()}</style>",unsafe_allow_html=True)

# ** Import ML Model
model_path = "Streamlit_Apps/Bangalore_Housing_Price_App/Model/bglr_model.pkl"

with open(model_path,'rb') as load_model:
    model = pickle.load(load_model)

# ** Import Location Encoded Json File To Mapping With User Input
location_path = "Streamlit_Apps/Bangalore_Housing_Price_App/Model/location_encoding.json"

with open(location_path,'r') as load_loc:
    loc_enc = json.load(load_loc)

loc_list =[]
for key in loc_enc.keys():
    loc_list.append(key)

# ** Building App

st_lottie(
    robot,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",
    height=250,
    width=250,
    key=None
)

with st.form(key="ml_form"):
    Area_Type = st.selectbox("Area Type",["Super built-up  Area","Built-up  Area","Plot  Area","Carpet  Area"])
    Location = st.selectbox("Location",loc_list)
    Segment = st.selectbox("Segment",["Regular","Premium"])
    bhk = st.slider("BHK",min_value=1,max_value=8,step=1)
    sqft = st.slider("Total SQFT",min_value=450,max_value=5000,step=50)
    bath_count = st.slider("No Of Bathrooms",min_value=1,max_value=7,step=1)
    balcony_count = st.slider("No Of Balcony",min_value=0,max_value=3,step=1)
    submit = st.form_submit_button("Predict Price")

    if submit:
        with st.spinner("Hang on! Predicting Price..."):
            time.sleep(4)
            loc_value = loc_enc[Location]
            feature_cols = ["area_type","location_te","Segement","bhk","total_sqft","bath","balcony"]
            new_data_point = pd.DataFrame([[Area_Type,loc_value,Segment,bhk,sqft,bath_count,balcony_count]],columns=feature_cols)
            price_predict = model.predict(new_data_point)[0]*100000
            price_per_sqft = price_predict/sqft
            st.success(f"Based On Your Choice, House Price Will Be : ₹{price_predict:,.0f}")
            st.info(f"Price Per Square Feet Will Be : ₹{price_per_sqft:,.2f}")
            st.plotly_chart(price_comparison_chart(price_predict,Location,location_wise_average(Location)),use_container_width=True)
    else:
        st.info("Fill Out The Form To Get Your House Price")
