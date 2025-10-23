import streamlit as st
from streamlit_lottie import st_lottie   # ? Welcome animation for home page
import json
import time

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
    st.text("💡 This Machine Learning app helps you predict accurate housing prices based on features like area, location, and budget —  making your home-buying decision smarter and data-driven.")
    

