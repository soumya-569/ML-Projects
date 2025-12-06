## Import Necessary Libraries

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

df = pd.read_csv("Streamlit_Apps/Bangalore_Housing_Price_App/Data/Bengaluru_House_Data.csv")

## Clean The Total SQFT Feature

def convert_sqft(x):
    if isinstance(x,str) and "-" in x:
        parts = x.split(" - ")
        if len(parts) == 2 :
            return (float(parts[0])+float(parts[1]))/2
    elif isinstance(x,float):
        return x
    else:
        x = str(x)
        num = re.findall(r'\d+',x)
        if len(num) > 1:
            mean_list = []
            for n in num:
                mean_list.append(float(n))
                return np.mean(mean_list)
        else:
            return float(num[0])

df["total_sqft"] = df["total_sqft"].apply(convert_sqft)

## Create A Support Dataframe Exclude Outliers From Total SQFT Feature
df1 = df.loc[(df["total_sqft"] >= df["total_sqft"].quantile(0.01)) & (df["total_sqft"] <= df["total_sqft"].quantile(0.99))]

## Insert A BHK Feature Derived From Size (BHK=Bedroom)
df1['bhk'] = df1['size'].str.split(" ").str[0].astype(float)

## Create A New Dataframe With Dropped Features
df2 = df1.drop(columns=["availability","size","society"])

## Fill Nan Values In Bath Feature With Median Of Bath  [Mode == Median]
df2['bath'] = df2['bath'].fillna(df2['bath'].median())

## Fill Nan Values In Balcony Feature With Median Of Balcony  [Mode == Median]
df2['balcony'] = df2['balcony'].fillna(df2['balcony'].median())

## Remove Probable Outliers W.R.T 99th Percentile From Bath Feature & Generate A New Dataframe
df3 = df2.loc[df2['bath'] <= df2['bath'].quantile(0.99)]

## Add A Price Per SQFT Feature
df3['price_per_sqft'] = (df3['price']*100000)/df3['total_sqft']

## Remove Probable Outliers W.R.T 99th Percentile From Price Per SQFT Feature & Generate A New Dataframe
df4 = df3.loc[df3['price_per_sqft'] <= df3['price_per_sqft'].quantile(0.99)]

## Fill Nan Values In BHK Feature With Mode Of BHK
mode_bhk = df4['bhk'].mode()[0]
df4['bhk'] = df4['bhk'].fillna(mode_bhk)

## BHK-to-Square Foot Rule (Minimum 300 Sqft per BHK)
df5 = df4.loc[df4['total_sqft'] >= df4['bhk']*300]

## Bathroom-to-BHK Rule (Bathrooms should not exceed BHK + 2)
df6 = df5.loc[df5['bath'] <= df5['bhk']+2]

## Price Rule for Luxury vs Non-luxury Segmentation (Price > ₹3 crore OR price_per_sqft > ₹15,000)
df6['Segement'] = np.where((df6['price'] >= df6['price']*100000) | (df6['price_per_sqft'] >= 15000),'Premium','Regular')

## We fill the location with null value with most frequent value
freq_loc = df6['location'].mode()[0]
df6['location'] = df6['location'].fillna(freq_loc)

## Locality-Based Density Rule (cluster localities with < 10 listings)
location_groups = df6['location'].value_counts()
rare_locations = location_groups[location_groups < 10].index
df6['location_clean'] = df6['location'].replace(rare_locations,"Other")

## Create a new dataframe with dropped column
df7 = df6.drop(columns=["location","price_per_sqft"])

## Create Location Wise Average Price
def location_wise_average(user_loc):
    loc_price_df = df.groupby("location")[["price"]].mean()
    return loc_price_df.loc[loc_price_df.index == user_loc].iloc[-1,:][0]

## Prediction Vs Average Price With Location

def price_comparison_chart(pred_price,locality,func):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x= ["Predicted Price"],
        y=[pred_price],
        marker_color = "#00b4d8",
        name = "Predicted Price"
    ))

    fig.add_trace(go.Bar(
        x=["Average Price in "+locality],
        y=[func],
        marker_color="#52b788",
        name="Locality Avg Price"
    ))

    fig.update_layout(
        title = {"text":f"Price Comparison for {locality}","xanchor":"center","yanchor":"top"},
        yaxis_title="Price (₹ Lakhs)",
        x_axis = dict(showgrid=False),
        y_axis = dict(showgrid=False),
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)'
        height=450,
        showlegend=False
    )

    return fig

