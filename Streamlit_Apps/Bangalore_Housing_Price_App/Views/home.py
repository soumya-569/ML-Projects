import streamlit as st
from streamlit_lottie import st_lottie   # ? Welcome animation for home page
import pandas as pd  # ? For Analysis
import json
import time
st.set_page_config(layout="centered")

st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',
    unsafe_allow_html=True
)

css_path = r"F:\Udemy\Git\ML Portfolio\Streamlit_Apps\Bangalore_Housing_Price_App\CSS\home.css"
with open(css_path) as load_css:
    st.markdown(f"<style>{load_css.read()}</style>",unsafe_allow_html=True)
    
# ** Import data and convert it into dataframe by PANDAS

# @st.cache_data()  # ? Cache for 1 hour
def data_preview():
    file_path = r'F:\Udemy\Git\ML Portfolio\Streamlit_Apps\Bangalore_Housing_Price_App\Data\Bengaluru_House_Data.csv'

    df = pd.read_csv(file_path)
    return st.dataframe(df.head(10))

# ** Import welcome animation

animation_path = r'F:\Udemy\Git\ML Portfolio\Streamlit_Apps\Bangalore_Housing_Price_App\Anima Bot.json'

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
    if rating :
        st.session_state.setdefault('show_form',True)
        if st.session_state.show_form:
            with st.form(key='feedback'):
                name = st.text_input(label="Full Name",placeholder="Enter your full name",icon=":material/id_card:")
                email = st.text_input(label="Mail",placeholder="Enter your email",icon=":material/mail:")
                submit = st.form_submit_button(label="Send Feedback")
                if submit:
                    if "@" not in email or "." not in email:
                        st.error("Email is not valid")
                    elif not name:
                        st.error("Name can't be empty")
                    else:
                        st.session_state['rating'] = rating
                        st.session_state['name'] = name
                        st.session_state['email'] = email
                        if rating <= 2:
                            st.success("Thank you for your feedback, we will improve ourselves")
                        else:
                            st.success("Thank you for your feedback, we glad you have enjoyed")
                        st.session_state['show_form'] = False
                        st.rerun()
    else:
        st.info("Please leave us a rating from your experience")

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
    st.html("<a class='nav_cont' href='http://localhost:8501/analysis'><i class='fa fa-bar-chart'></i> See Analysis</a>")

with col_btn_2:
    st.html("<a class='nav_cont' href='http://localhost:8501/model'><i class='fas fa-robot'></i>  See Prediction</a>")

with col_btn_3:
    st.html("<a class='nav_cont' href='http://localhost:8501/conclusion'><i class='fas fa-gavel'></i> See Conclusion</a>")



