import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

file_path = r'F:\Udemy\Git\ML Portfolio\Streamlit Apps\Bangalore Housing Price App\Data\Bengaluru_House_Data.csv'

df = pd.read_csv(file_path)

def location():
    return df.groupby("location",observed=False)[['area_type']].count().sort_values('area_type',ascending=False).reset_index().iloc[0][0]

def location_chart():
    return df.groupby("location",observed=False)[['area_type']].count().sort_values('area_type',ascending=False).reset_index().iloc[:,-1]

def average_price():
    return round((df['price'].mean())*88,2)

def avg_price_sqft():
    df['total_sqft'] = np.where((df['total_sqft'].str.isdigit())|(df['total_sqft'].str.isdecimal()),df['total_sqft'],0)
    df['total_sqft'] = df['total_sqft'].astype('float64')
    raw_avg_sqft = df['total_sqft'].mean()
    df['total_sqft'] = np.where(df['total_sqft'] == 0, raw_avg_sqft,df['total_sqft'])
    df['price_per_sqft'] = df['price']/df['total_sqft']
    return round((df['price_per_sqft'].mean())*88,2)

def total_properties():
    return df['area_type'].count()

def expensive_location():
    exp_loc =  df.groupby("location",observed=False)[["location"]].count().rename(columns={"location":"total"}).reset_index().sort_values("total",ascending=False)
    fig = px.bar(data_frame=exp_loc,x="location",y="total")
    return fig.show()
