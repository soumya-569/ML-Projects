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
            'x': 0.5,
            'y':0.95,
            'xanchor': 'center',
            'yanchor':'top'
        },
        yaxis_title_text = "Total Properties",
        xaxis_title_text = "Location"
    )
    return fig

def area_type_ratio():
    fig = go.Figure(
    go.Pie(labels=df["area_type"],hole=0.6)
    )
    fig.update_layout(legend={"x":0.5,"y":-0.2,"xanchor":"center","yanchor":"bottom","orientation":"h"},title={"text":"Area Type Distribution","x":0.5,"y":0.95,"xanchor":"center","yanchor":"top"})
    return fig