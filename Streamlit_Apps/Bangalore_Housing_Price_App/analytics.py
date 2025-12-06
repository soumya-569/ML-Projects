## Import Necessary Libraries

import numpy as np
import pandas as pd
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

def location():
    return df6.groupby("location",observed=False)[['area_type']].count().sort_values('area_type',ascending=False).reset_index().iloc[0][0]

def average_price():
    return round(df6['price_transformed'].mean(),2)

def avg_price_sqft():
    return round(df6['price_per_sqft'].mean(),2)

def total_properties():
    return df6['area_type'].count()

def location_summary():
    summary = df6.groupby("location",observed=False).agg(
    Average_Price=('price_transformed','mean'),
    Average_Price_Per_SQFT=('price_per_sqft','mean'),
    Total_Properties=('bhk','count')
    )
    return summary

