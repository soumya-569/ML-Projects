import streamlit as st
from analytics import location,location_chart,average_price,avg_price_sqft,total_properties,location_summary
from charts import most_properties,area_type_ratio,price_distribution,price_per_sqft_distribution,bhk_distribution,avg_price_bhk,pps_bhk,sqft_vs_price,bhk_sqft,ten_exp_loc,ten_least_loc,heatmap,metric_selection

st.set_page_config(layout="wide")

css_path = "Streamlit_Apps/Bangalore_Housing_Price_App/CSS/analysis.css"

with open(css_path) as load_css:
    st.markdown(f"<style>{load_css.read()}</style>",unsafe_allow_html=True)

@st.cache_data
def call_kpi4():
    return avg_price_sqft()

@st.cache_data
def call_chart5():
    return bhk_distribution()

kpi1,kpi2,kpi3,kpi4 = st.columns(4,gap='small')

with kpi1:
    st.metric("Total Properties",total_properties())

with kpi2:
    st.metric("Most Property In a Location",location())

with kpi3:
    st.metric("Average House Price",average_price())

with kpi4:
    st.metric("Average Price/sqft",call_kpi4())

st.header("General Insights")
st.divider()

gen1,gen2,gen3 = st.columns(3,gap="small")

with gen1:
    st.plotly_chart(price_per_sqft_distribution())
    st.info("Price per Sqft helps compare properties of different sizes. Extreme outliers are removed for clarity.")

with gen2:
    st.plotly_chart(area_type_ratio())

with gen3:
    user_opt = st.radio("Select a feature to display violin plot against it",options=["Bath","Balcony"])
    st.plotly_chart(metric_selection(user_opt))

st.header("Size vs Price Relation")
st.divider()

chart1,chart2,chart3 = st.columns(3,gap="small")

with chart1:
    st.plotly_chart(price_distribution())

with chart2:
    st.plotly_chart(sqft_vs_price())

with chart3:
    st.plotly_chart(pps_bhk())

st.header("BHK Analysis")
st.divider()

bhk1,bhk2,bhk3 = st.columns(3,gap="small")

with bhk1:
    st.plotly_chart(call_chart5())

with bhk2:
    st.plotly_chart(avg_price_bhk())

with bhk3:
    st.plotly_chart(bhk_sqft())

st.header("Location Price Insights")
st.divider()

loc1,loc2,loc3 = st.columns(3,gap="small")

with loc1:
    st.plotly_chart(most_properties())

with loc2:
    st.plotly_chart(ten_exp_loc())

with loc3:
    st.plotly_chart(ten_least_loc())


st.header("Correlation Heatmap")
st.divider()

st.plotly_chart(heatmap())
st.info("""
A correlation heatmap reveals relationships between features.
High correlation with price indicates strong predictive power.
""")

st.header("Location-Wise Statistical Table")
st.divider()

st.dataframe(location_summary())