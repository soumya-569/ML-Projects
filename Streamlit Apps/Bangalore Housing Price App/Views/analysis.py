import streamlit as st
from analytics import location,location_chart

kpi1,kpi2,kpi3,kpi4 = st.columns(4,gap='small')

with kpi1:
    st.metric("Most Property In a Location",location(),chart_data=location_chart(),chart_type='bar')