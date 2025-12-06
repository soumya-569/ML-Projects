import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

file_path = r'F:\Udemy\Git\ML Portfolio\Streamlit_Apps\Bangalore_Housing_Price_App\Data\Bengaluru_House_Data.csv'

df = pd.read_csv(file_path)
df['bhk'] = df['size'].str.split(" ").str[0].astype("float32")
df['price_in_rupees'] = df['price']*90
df['total_sqft'] = np.where((df['total_sqft'].str.isdigit())|(df['total_sqft'].str.isdecimal()),df['total_sqft'],0)
df['total_sqft'] = df['total_sqft'].astype('float64')
total_sqft_mean = df['total_sqft'].mean()
df['total_sqft'] = np.where(df['total_sqft'] == 0,total_sqft_mean,df['total_sqft'])
df['price_per_sqft'] = round(df['price_in_rupees']/df['total_sqft'],2)

def most_properties():
    exp_loc =  df.groupby("location",observed=False)[["location"]].count().rename(columns={"location":"total"}).reset_index().sort_values("total",ascending=False).reset_index().iloc[0:10]
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
    go.Pie(labels=df["area_type"],hole=0.6)
    )
    fig.update_layout(legend={"x":0.5,"y":-0.2,"xanchor":"center","yanchor":"bottom","orientation":"h"},title={"text":"Area Type Distribution","x":0.5,"y":0.95,"xanchor":"center","yanchor":"top"})
    return fig

def price_distribution():
    fig = px.histogram(df.loc[df['price'] < df['price'].quantile(0.99)],x="price_in_rupees",nbins=100,color_discrete_sequence=['#00FFFF'])
    fig.update_layout(bargap=0.2,xaxis=dict(showgrid=False,title="Price Range"),yaxis=dict(showgrid=False,title="Total Count"),title={"text":"Price Range Distribution Across City","x":0.5,"y":0.95,"xanchor":"center","yanchor":"top"})
    return fig

def price_per_sqft_distribution():
    fig = px.violin(df.loc[df['price_per_sqft'] < df['price_per_sqft'].quantile(0.99)],y="price_per_sqft",color_discrete_sequence=['#00FFFF'])
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
    fig = px.histogram(df.loc[df['bhk'] <= 20],x="bhk",color_discrete_sequence=['#00FFFF'],nbins=100)
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
    price_by_bhk = df.groupby("bhk",observed=False)[['price_in_rupees']].mean().reset_index().rename(columns={"price_in_rupees":"Average Price"}).sort_values("Average Price",ascending=False).reset_index()
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
    fig = px.box(df.loc[(df['bhk'] <= 10)&(df["price_per_sqft"]<=2000)],x="bhk",y="price_per_sqft",color_discrete_sequence=['#00FFFF'],points=False)
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
    fig = px.scatter(df,x="total_sqft",y="price_in_rupees",trendline="ols",trendline_color_override="grey",color_discrete_sequence=['#00FFFF'])
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
    fig = px.box(df.loc[df['bhk'] <= 11],x="bhk",y="total_sqft",color_discrete_sequence=['#00FFFF'],points=False)
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
    most_expensive_location = df.groupby("location",observed=False)[["price_per_sqft"]].mean().reset_index().rename(columns={"price_per_sqft":"Average Price Per SQFT"}).sort_values("Average Price Per SQFT",ascending=False).reset_index().iloc[0:10].drop(columns="index")
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
    most_cheapest_location = df.groupby("location",observed=False)[["price_per_sqft"]].mean().reset_index().rename(columns={"price_per_sqft":"Average Price Per SQFT"}).sort_values("Average Price Per SQFT",ascending=True).reset_index().iloc[0:10].drop(columns="index")
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
    fig = px.imshow(df.corr(numeric_only=True),text_auto=True,aspect="auto",color_continuous_scale="RdBu")
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
        fig = px.violin(df,x="balcony",y="price_in_rupees",color_discrete_sequence=['#00FFFF'])
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
        fig = px.violin(df.loc[df["bath"]<=10],x="bath",y="price_in_rupees",color_discrete_sequence=['#00FFFF'])
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