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

## Insert A Price Transformation Feature

df6['price_transformed'] = df6['price']*100000

## Create a new dataframe with dropped column
df7 = df6.drop(columns=["location","price_per_sqft"])

## Create Location Wise Average Price
def location_wise_average(user_loc):
    loc_price_df = df.groupby("location")[["price"]].mean()
    return loc_price_df.loc[loc_price_df.index == user_loc].iloc[-1,:][0]*100000

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
        title = {"text":f"Price Comparison for {locality}"},
        yaxis_title="Price",
        xaxis = dict(showgrid=False),
        yaxis = dict(showgrid=False),
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        height=450,
        showlegend=False
    )

    return fig

def most_properties():
    exp_loc =  df6.groupby("location",observed=False)[["location"]].count().rename(columns={"location":"total"}).reset_index().sort_values("total",ascending=False).reset_index().iloc[0:10]
    fig = px.bar(data_frame=exp_loc,x="location",y="total",text="total",color_discrete_sequence=['#00FFFF'])
    fig.update_layout(xaxis=dict(showgrid=False,tickangle=-45),yaxis=dict(showgrid=False))
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
    go.Pie(labels=df6["area_type"],hole=0.6)
    )
    fig.update_layout(legend={"x":0.5,"y":-0.2,"xanchor":"center","yanchor":"bottom","orientation":"h"},title={"text":"Area Type Distribution","x":0.5,"y":0.95,"xanchor":"center","yanchor":"top"})
    return fig

def price_distribution():
    fig = px.histogram(df6,x="price_transformed",nbins=100,color_discrete_sequence=['#00FFFF'])
    fig.update_layout(bargap=0.2,xaxis=dict(showgrid=False,title="Price Range"),yaxis=dict(showgrid=False,title="Total Count"),title={"text":"Price Range Distribution Across City","x":0.5,"y":0.95,"xanchor":"center","yanchor":"top"})
    return fig

def price_per_sqft_distribution():
    fig = px.violin(df6,y="price_per_sqft",color_discrete_sequence=['#00FFFF'])
    fig.update_layout(
        xaxis=dict(showgrid=False,title="Price Per SQFT"),
        yaxis=dict(showgrid=False),
        title={
            'text':'Price per Sqft Distribution',
            'x':0.5,
            'y':0.95,
            'xanchor':'center',
            'yanchor':'top'
        }
    )
    return fig

def bhk_distribution():
    fig = px.histogram(df6,x="bhk",color_discrete_sequence=['#00FFFF'],nbins=100)
    fig.update_layout(
        xaxis=dict(showgrid=False,title="BHK"),
        yaxis=dict(showgrid=False,title="Total Count"),
        title = {
            "text":"Distribution Of BHK",
            "x":0.5,
            "y":0.95,
            "xanchor":"center",
            "yanchor":"top"
        }
    )
    return fig

def avg_price_bhk():
    price_by_bhk = df6.groupby("bhk",observed=False)[['price_transformed']].mean().reset_index().rename(columns={"price_transformed":"Average Price"}).sort_values("Average Price",ascending=False).reset_index()
    fig = px.bar(price_by_bhk,x="bhk",y="Average Price",color_discrete_sequence=['#00FFFF'])
    fig.update_layout(
        xaxis=dict(showgrid=False,title="BHK"),
        yaxis=dict(showgrid=False),
        title = {
            "text":"Average Price by BHK",
            "x":0.5,
            "y":0.95
        }
    )
    return fig

def pps_bhk():
    fig = px.box(df6,x="bhk",y="price_per_sqft",color_discrete_sequence=['#00FFFF'],points=False)
    fig.update_layout(
        xaxis=dict(showgrid=False,title='BHK'),
        yaxis=dict(showgrid=False,title='Price Per SQFT'),
        title ={
            "text":"Price per Sqft by BHK",
            "x":0.5,
            "y":0.95
        }
    )
    return fig

def sqft_vs_price():
    fig = px.scatter(df6,x="total_sqft",y="price_transformed",trendline="ols",trendline_color_override="grey",color_discrete_sequence=['#00FFFF'])
    fig.update_layout(
        xaxis=dict(showgrid=False,title="Total SQFT"),
        yaxis=dict(showgrid=False,title="Price"),
        title = {
            "text":"Total Sqft vs Price",
            "x":0.5,
            "y":0.95
        }
    )
    return fig

def bhk_sqft():
    fig = px.box(df6,x="bhk",y="total_sqft",color_discrete_sequence=['#00FFFF'],points=False)
    fig.update_layout(
        xaxis=dict(showgrid=False,title='BHK'),
        yaxis=dict(showgrid=False,title='SQFT'),
        title = {
            "text":"BHK–Sqft Outlier Detect",
            "x":0.5,
            "y":0.95
        }
    )
    return fig

def ten_exp_loc():
    most_expensive_location = df6.groupby("location",observed=False)[["price_per_sqft"]].mean().reset_index().rename(columns={"price_per_sqft":"Average Price Per SQFT"}).sort_values("Average Price Per SQFT",ascending=False).reset_index().iloc[0:10].drop(columns="index")
    fig = px.bar(most_expensive_location,x="location",y="Average Price Per SQFT",color_discrete_sequence=['#00FFFF'],text="Average Price Per SQFT")
    fig.update_layout(
        xaxis=dict(showgrid=False,title='Location',tickangle=-45),
        yaxis=dict(showgrid=False,title='Average Price Per SQFT'),
        title = {
            "text":"Top 10 Most Expensive Locations",
            "x":0.5,
            "y":0.95,
            "xanchor":"center",
            "yanchor":"top"
        }
    )
    return fig

def ten_least_loc():
    most_cheapest_location = df6.groupby("location",observed=False)[["price_per_sqft"]].mean().reset_index().rename(columns={"price_per_sqft":"Average Price Per SQFT"}).sort_values("Average Price Per SQFT",ascending=True).reset_index().iloc[0:10].drop(columns="index")
    fig = px.bar(most_cheapest_location,x="location",y="Average Price Per SQFT",color_discrete_sequence=['#00FFFF'],text="Average Price Per SQFT")
    fig.update_layout(
        xaxis=dict(showgrid=False,title='Location',tickangle=-45),
        yaxis=dict(showgrid=False,title='Average Price Per SQFT'),
        title = {
            "text":"Top 10 Most Affordable Locations",
            "x":0.5,
            "y":0.95,
            "xanchor":"center",
            "yanchor":"top"
        }
    )
    return fig

def heatmap():
    fig = px.imshow(df7.corr(numeric_only=True),text_auto=True,aspect="auto",color_continuous_scale="RdBu")
    fig.update_layout(
        xaxis = dict(title="Features",tickangle=-45),
        yaxis = dict(title="Features"),
        title = dict(text="Correlation Heatmap Of Numeric Features",x=0.5,y=0.95,xanchor="center",yanchor="top"),
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)'
    )
    return fig

def metric_selection(user_input):
    if user_input == "Balcony":
        fig = px.violin(df6,x="balcony",y="price_transformed",color_discrete_sequence=['#00FFFF'])
        fig.update_layout(
            xaxis=dict(showgrid=False,title="Balcony"),
            yaxis=dict(showgrid=False,title="Price"),
            title = {
                "text":"Balcony vs Price Distribution",
                "x":0.5,
                "y":0.95,
                "xanchor":"center",
                "yanchor":"top"
            }
        )
        return fig
    elif user_input == "Bath":
        fig = px.violin(df6,x="bath",y="price_transformed",color_discrete_sequence=['#00FFFF'])
        fig.update_layout(
            xaxis=dict(showgrid=False,title="Bath"),
            yaxis=dict(showgrid=False,title="Price"),
            title = {
                "text":"Bath vs Price Distribution",
                "x":0.5,
                "y":0.95,
                "xanchor":"center",
                "yanchor":"top"
            }
        )
        return fig