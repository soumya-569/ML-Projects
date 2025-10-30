import streamlit as st
from analytics import location,location_chart,average_price,avg_price_sqft,total_properties
from charts import expensive_location

st.set_page_config(layout="wide")

css_path = r"F:\Udemy\Git\ML Portfolio\Streamlit Apps\Bangalore Housing Price App\CSS\analysis.css"

with open(css_path) as load_css:
    st.markdown(f"<style>{load_css.read()}</style>",unsafe_allow_html=True)

@st.cache_data
def call_kpi4():
    return avg_price_sqft()

kpi1,kpi2,kpi3,kpi4 = st.columns(4,gap='small')

with kpi1:
    st.metric("Total Properties",total_properties())

with kpi2:
    st.metric("Most Property In a Location",location())

with kpi3:
    st.metric("Average House Price",average_price())

with kpi4:
    st.metric("Average Price/sqft",call_kpi4())

chart1,chart2,chart3 = st.columns(3,gap="small")

with chart1:
    st.plotly_chart(expensive_location())
