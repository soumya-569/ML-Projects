import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

file_path = r'F:\Udemy\Git\ML Portfolio\Streamlit_Apps\Bangalore_Housing_Price_App\Data\Bengaluru_House_Data.csv'

df = pd.read_csv(file_path)

df['price_in_rupees'] = df['price']*90

df['bhk'] = df['size'].str.split(" ").str[0]

df['total_sqft'] = np.where((df['total_sqft'].str.isdigit())|(df['total_sqft'].str.isdecimal()),df['total_sqft'],0)
df['total_sqft'] = df['total_sqft'].astype('float64')
total_sqft_mean = df['total_sqft'].mean()
df['total_sqft'] = np.where(df['total_sqft'] == 0,total_sqft_mean,df['total_sqft'])
df['price_per_sqft'] = round(df['price_in_rupees']/df['total_sqft'],2)

def location():
    return df.groupby("location",observed=False)[['area_type']].count().sort_values('area_type',ascending=False).reset_index().iloc[0][0]

def location_chart():
    return df.groupby("location",observed=False)[['area_type']].count().sort_values('area_type',ascending=False).reset_index().iloc[:,-1]

def average_price():
    return round((df['price'].mean())*88,2)

def avg_price_sqft():
    return round(df['price_per_sqft'].mean(),2)

def total_properties():
    return df['area_type'].count()

def location_summary():
    summary = df.groupby("location",observed=False).agg(
    Average_Price=('price_in_rupees','mean'),
    Average_Price_Per_SQFT=('price_per_sqft','mean'),
    Total_Properties=('bhk','count')
    )
    return summary

