import streamlit as st
from streamlit_lottie import st_lottie   # ? Welcome animation for home page
import pandas as pd  # ? For Analysis
import json
import time

# ** Import data and convert it into dataframe by PANDAS

# @st.cache_data()  # ? Cache for 1 hour
def data_preview():
    file_path = r'F:\Udemy\Git\ML Portfolio\Streamlit Apps\Bangalore Housing Price App\Data\Bengaluru_House_Data.csv'

    df = pd.read_csv(file_path)
    return st.dataframe(df.head(10))

# ** Import welcome animation

animation_path = r'F:\Udemy\Git\ML Portfolio\Streamlit Apps\Bangalore Housing Price App\Anima Bot.json'

with open(animation_path,'r',encoding='utf-8') as anime:
    robot = json.load(anime)

# ** 2 Columns for welcome screen (Left > Animation, Right > Info)

col1,col2 = st.columns(2,gap="small")

with col1:
    st_lottie(
        robot,
        speed= 1,
        reverse= False,
        loop= True, 
        quality= "low",
        height= 300,
        width= 300,
        key= None
    )

with col2:
    st.subheader('🏠 Welcome to `Bangalore` house price prediction app')
    st.text("📊 This interactive machine learning app helps you analyze and predict property prices across Bangalore using real data. You can explore data patterns, visualize area-wise insights, and predict house prices based on features like location, BHK, and square footage — helping buyers and investors make smarter decisions.")
    rating = st.feedback(options="stars")
    if not rating:
        st.info("Please leave us a rating from your experience")
    elif rating <= 2 :
        st.success("Thank your for your feedback, we will improve ourselves")
    else:
        st.success("Thank you for your feedback, we are glad to see you have enjoyed")

# ** Dataset Info & Preview

with st.expander("Dataset Preview",icon=":material/expand_all:"):
    st.write("""
The dataset contains **13,200 property records** across Bangalore with attributes like:
- Location  
- Total square feet  
- Number of bedrooms (BHK)  
- Number of bathrooms  
- Price in lakhs  
- Price per square foot (derived feature)

Data Source: [Kaggle - Bangalore House Prices](https://www.kaggle.com/datasets/amitabhajoy/bengaluru-house-price-data)
""")
    with st.spinner('Previewing...'):
        time.sleep(5)
        data_preview()

# ** Multipage Link

col_btn_1,col_btn_2,col_btn_3 = st.columns(3,gap="small")

with col_btn_1:
    with st.container():
        st.page_link("Views/analysis.py",label="See Quick Info",icon=":material/bar_chart:")

with col_btn_2:
    with st.container():
        st.page_link("Views/model.py",label="See Prediction",icon=":material/robot_2:")

with col_btn_3:
    with st.container():
        st.page_link("Views/conclusion.py",label="See Conclusion",icon=":material/gavel:")



