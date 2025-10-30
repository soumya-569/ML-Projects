import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

file_path = r'F:\Udemy\Git\ML Portfolio\Streamlit Apps\Bangalore Housing Price App\Data\Bengaluru_House_Data.csv'

df = pd.read_csv(file_path)

def expensive_location():
    exp_loc =  df.groupby("location",observed=False)[["location"]].count().rename(columns={"location":"total"}).reset_index().sort_values("total",ascending=False).reset_index().iloc[0:10]
    fig = px.bar(data_frame=exp_loc,x="location",y="total",text="total")
    fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
    fig.update_layout(
        title={
            'text': "Top 10 Most Properties In a Location",
            'x': 0.5, # Center the title
            'xanchor': 'center'
        }
    )
    return fig