
# ** Import Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.offline import plot
from plotly.utils import PlotlyJSONEncoder
from sklearn.metrics import *
import json
import pickle
import os
import re
from io import BytesIO
import shap

# ** Ingest Data & Create Dataframe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "Data", "Bank_Churn.csv")
df = pd.read_csv(csv_path)

# ** Ingest & Load The ML Model

ml_path = os.path.join(BASE_DIR,"Model","bank_model.pkl")
with open(ml_path,'rb') as load_pipeline:
    pipeline = pickle.load(load_pipeline)

# ** EDA

df["Surname"] = df["Surname"].str.strip()
df["Geography"] = df["Geography"].str.strip()
df["Gender"] = df["Gender"].str.strip()

df1 = df.drop(columns=["CustomerId","Surname"])
x = df1.drop("Exited",axis=1)
y = df1["Exited"]

# ** Feature Engineering
## Add Risk Category Feature

probs = pipeline.predict_proba(x)[:,1]
df["ChurnProbability"] = probs

conditions = [
    df["ChurnProbability"] >= 0.65,
    df["ChurnProbability"] >= 0.22,
    df["ChurnProbability"] < 0.22
]

choices = [
    "High",
    "Medium",
    "Low"
]

df["RiskCategory"] = np.select(conditions,choices,default="Low")

## Add Contact Priority Level (For RM Teams)

# Add Contact Priority Feature
cp_conditions = [
    df["Exited"] == 1,
    df["ChurnProbability"] >= 0.7,
    df["ChurnProbability"] >= 0.5,
    df["ChurnProbability"] >= 0.35,
    df["ChurnProbability"] >= 0.2,
    df["ChurnProbability"] < 0.2
]

cp_choices = [
    "Churned",
    "Very High",
    "High",
    "Medium",
    "Moderate",
    "Low"
]

df["ContactPriority"] = np.select(cp_conditions,cp_choices,default="None")

# Add Contact Timings Feature
ct_conditions = [
    df["ContactPriority"] == "Churned",
    df["ContactPriority"] == "Very High",
    df["ContactPriority"] == "High",
    df["ContactPriority"] == "Medium",
    df["ContactPriority"] == "Moderate",
    df["ContactPriority"] == "Low"
]

ct_choices = [
    "Not Required",
    "Within 24 Hrs",
    "Within 36 Hrs",
    "Within 48 Hrs",
    "Within 72 Hrs",
    "Not Required"
]

df["RecommendedContact"] = np.select(ct_conditions,ct_choices,default="None")

## Age Bucket Feature

age_conditions = [
    df["Age"].between(18,35),
    df["Age"].between(35,60),
    df["Age"] > 60
]

age_choices=[
    "18-35",
    "35-60",
    "Above 60"
]

df["AgeBucket"] = np.select(age_conditions,age_choices,default="None")

## Tenure Bucket Feature

tn_conditions = [
    df["Tenure"].between(0,1),
    df["Tenure"].between(1,3),
    df["Tenure"].between(3,5),
    df["Tenure"].between(5,8),
    df["Tenure"].between(8,10)
]

tn_choices = [
    "Less than 1 yr",
    "1-3 yrs",
    "3-5 yrs",
    "5-8 yrs",
    "8-10 yrs"
]

df["TenureBucket"] = np.select(tn_conditions,tn_choices,default="Above 10 yrs")

## Added Credit Score Bucket For Website Demonstration

cs_conditions = [
    df["CreditScore"].between(300,500),
    df["CreditScore"].between(500,650),
    df["CreditScore"].between(650,800),
    df["CreditScore"] > 800
]

cs_choices = [
    "Low Score (300–500)",
    "Medium Score (500–650)",
    "High Score (650–800)",
    "Very High Score (>800)"
]

df["CreditScoreBucket"] = np.select(cs_conditions,cs_choices,default="Unknown")

## Added Balance Range Feature For Website Demonstration

br_conditions = [
    df["Balance"].between(0,50000),
    df["Balance"].between(50000,100000),
    df["Balance"].between(100000,150000),
    df["Balance"].between(150000,200000),
    df["Balance"] > 200000
]

br_choices = [
    "0-50k",
    "50k-100k",
    "100k-150k",
    "150k-200k",
    "200k+"
]

df["BalanceRange"] = np.select(br_conditions,br_choices,default="Unknown") 

# ** KPI's
def total_customers():
    return df["CustomerId"].count()

def current_churn_rate():
    churn_rate = df["Exited"].value_counts(normalize=True)*100
    return round(churn_rate[1],2)

def high_risk_customers():
    high_risk = df["RiskCategory"].loc[df["RiskCategory"]=="High"].count()
    return high_risk

def avg_credit_score():
    return round(df["CreditScore"].mean(),2)


# ** Churn Distribution
def churn_distribution():
    colors = ["#2C3E50","#D35400"]
    labels = df["Exited"].value_counts().index
    values = df["Exited"].value_counts().values
    fig = go.Figure(go.Pie(labels=labels,values=values))
    fig.update_traces(marker=dict(colors=colors,line=dict(color='#000000',width=2)))
    fig.update_layout(
        height=250,
        width=480,
        plot_bgcolor = "rgba(0,0,0,0)",
        paper_bgcolor = "rgba(0,0,0,0)",
        margin=dict(t=10,b=20,l=10,r=10),
        showlegend=False
    )

    plot_config = {
        'displayModeBar': False
    }

    
    chart_html = plot(fig,include_plotlyjs=False,output_type="div",config=plot_config)
    return chart_html

def age_vs_churn():
    with_churn = df.loc[df["Exited"] == 1].groupby("AgeBucket")[["Exited"]].count().reset_index()
    without_churn = df.loc[df["Exited"] == 0].groupby("AgeBucket")[["Exited"]].count().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=with_churn["AgeBucket"],
        x=with_churn["Exited"],
        name="Churned",
        orientation="h",
        marker=dict(color="#D35400",line=dict(color="#7B241C",width=3))
    ))

    fig.add_trace(go.Bar(
        y=without_churn["AgeBucket"],
        x=without_churn["Exited"],
        name="Not Churned",
        orientation="h",
        marker=dict(color="#2C3E50",line=dict(color="#1B2631",width=3))
    ))

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height = 250,
        width = 480,
        margin = dict(l=10,r=10,t=10,b=20)
    )

    age_churn_html = plot(fig,include_plotlyjs=False,output_type="div",config={'displayModeBar': False})

    return age_churn_html

def tenure_vs_churn():
    with_churn = df.loc[df["Exited"] == 1].groupby("TenureBucket")[["Exited"]].count().reset_index()
    without_churn = df.loc[df["Exited"] == 0].groupby("TenureBucket")[["Exited"]].count().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=with_churn["Exited"],
        y=with_churn["TenureBucket"],
        orientation="h",
        name="Churned",
        marker=dict(color="#D35400",line=dict(color="#7B241C",width=3))
    ))

    fig.add_trace(go.Bar(
        x=without_churn["Exited"],
        y=without_churn["TenureBucket"],
        orientation="h",
        name="Not Churned",
        marker=dict(color="#2C3E50",line=dict(color="#1B2631",width=3))
    ))

    fig.update_layout(
        barmode = "stack",
        height=250,
        width=480,
        margin=dict(l=10,r=10,t=10,b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    tenure_churn_html = plot(fig,include_plotlyjs=False,output_type="div",config={"displayModeBar":False})

    return tenure_churn_html

def churn_by_activity():
    colors = ["#D35400","#2C3E50"]
    with_churn = df.loc[df["Exited"]==1].groupby("IsActiveMember")[["Exited"]].count().reset_index()
    fig = go.Figure(go.Pie(labels=with_churn["IsActiveMember"],values=with_churn["Exited"],hole=0.45))

    fig.update_traces(marker=dict(colors=colors,line=dict(color="#000000",width=2)))

    fig.update_layout(
        height=250,
        width=480,
        margin=dict(l=10,r=10,t=10,b=20),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    churn_activity_html = plot(fig,include_plotlyjs=False,output_type="div",config={"displayModeBar":False})

    return churn_activity_html

def profile(id):
    id = int(id)
    name = df["Surname"].loc[df["CustomerId"] == id].iloc[0]
    age = df["Age"].loc[df["CustomerId"] == id].iloc[0]
    geography = df["Geography"].loc[df["CustomerId"] == id].iloc[0]
    balance  = df["Balance"].loc[df["CustomerId"] == id].iloc[0]
    products  = df["NumOfProducts"].loc[df["CustomerId"] == id].iloc[0]
    active_member  = df["IsActiveMember"].loc[df["CustomerId"] == id].iloc[0]
    churn_probability  = round((df["ChurnProbability"].loc[df["CustomerId"] == id].iloc[0])*100,2)
    risk  = df["RiskCategory"].loc[df["CustomerId"] == id].iloc[0]
    contact  = df["ContactPriority"].loc[df["CustomerId"] == id].iloc[0]
    timing  = df["RecommendedContact"].loc[df["CustomerId"] == id].iloc[0]

    fig = go.Figure(go.Indicator(
        mode="number+gauge",
        value=churn_probability,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge={'axis':{'range':[None,100]},'steps':[{'range':[0,50],'color':"lightgray"},{'range':[50,100],'color':"gray"}],'bar':{'color':"#D35400"},'threshold' : {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 22}}
    ))

    fig.update_layout(
        height=100,
        width=240,
        margin=dict(l=40,r=10,t=10,b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    risk_html = plot(fig,include_plotlyjs=False,output_type="div",config={"displayModeBar":False})

    details = [name,age,geography,balance,products,active_member,churn_probability,risk,contact,timing,risk_html]

    return details

def shap_factors(id):
    id = int(id)
    preprocessor = pipeline.named_steps["preprocessor"]
    ml_model = pipeline.named_steps["classifier"]
    preprocessor.n_jobs = 1

    x_transformed = preprocessor.transform(x)
    feature_names = preprocessor.get_feature_names_out()

    explainer = shap.TreeExplainer(ml_model)
    shap_values = explainer.shap_values(x_transformed)

    idx = df.index[df["CustomerId"]==id][0]

    customer_shap = shap_values[idx]
    customer_data = x_transformed[idx]

    exp = shap.Explanation(
        values=customer_shap,
        base_values=explainer.expected_value,
        data=customer_data,
        feature_names=feature_names
    )

    abs_vals = np.abs(exp.values)
    top_idx = abs_vals.argsort()[::-1][:5]
    top_factors_raw = [
        f"{exp.feature_names[i]} : {exp.values[i]*100:.3f}"
        for i in top_idx
    ] 

    top_factors = [factor.split("__")[-1] for factor in top_factors_raw]

    return top_factors  

def batch_process(df):
    
    # ** EDA

    df["Surname"] = df["Surname"].str.strip()
    df["Geography"] = df["Geography"].str.strip()
    df["Gender"] = df["Gender"].str.strip()

    df1 = df.drop(columns=["CustomerId","Surname"])
    x = df1.drop("Exited",axis=1)
    y = df1["Exited"]

    # ** Feature Engineering
    ## Add Risk Category Feature

    probs = pipeline.predict_proba(x)[:,1]
    df["ChurnProbability"] = probs

    conditions = [
        df["ChurnProbability"] >= 0.65,
        df["ChurnProbability"] >= 0.22,
        df["ChurnProbability"] < 0.22
    ]

    choices = [
        "High",
        "Medium",
        "Low"
    ]

    df["RiskCategory"] = np.select(conditions,choices,default="Low")

    total_customers_processed = df["CustomerId"].count()
    high_risk = df["RiskCategory"].loc[df["RiskCategory"] == "High"].count()
    medium_risk = df["RiskCategory"].loc[df["RiskCategory"] == "Medium"].count()
    low_risk = df["RiskCategory"].loc[df["RiskCategory"] == "Low"].count()

    # ** Risk Pie Chart

    risk_values = df["RiskCategory"].value_counts()

    labels = risk_values.index
    values = risk_values.values

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values
    ))
    colors = ["#D35400","#1B2631","#4B5F72"]
    fig.update_traces(marker=dict(colors = colors,line=dict(color="#000000",width=2)))
    fig.update_layout(
        height=185,
        width=360,
        margin = dict(l=10,r=10,t=10,b=25),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend = False
    )
    fig_html = plot(fig,include_plotlyjs=False,output_type="div",config={"displayModeBar":False})

    style_df = df.style.apply(
        lambda row: ["background-color: #ff9999" if row["ChurnProbability"] >= 0.22 else ""]
        * len(row),
        axis=1
    )


    table_html = style_df.to_html(index=False)

    metric_fig_list = [total_customers_processed,high_risk,medium_risk,low_risk,fig_html,table_html]

    return metric_fig_list

def download_df(df):
    # ** EDA

    df["Surname"] = df["Surname"].str.strip()
    df["Geography"] = df["Geography"].str.strip()
    df["Gender"] = df["Gender"].str.strip()

    df1 = df.drop(columns=["CustomerId","Surname"])
    x = df1.drop("Exited",axis=1)
    y = df1["Exited"]

    # ** Feature Engineering
    ## Add Risk Category Feature

    probs = pipeline.predict_proba(x)[:,1]
    df["ChurnProbability"] = probs

    conditions = [
        df["ChurnProbability"] >= 0.65,
        df["ChurnProbability"] >= 0.22,
        df["ChurnProbability"] < 0.22
    ]

    choices = [
        "High",
        "Medium",
        "Low"
    ]

    df["RiskCategory"] = np.select(conditions,choices,default="Low")

    ## Add Contact Priority Level (For RM Teams)

    # Add Contact Priority Feature
    cp_conditions = [
        df["ChurnProbability"] >= 0.7,
        df["ChurnProbability"] >= 0.5,
        df["ChurnProbability"] >= 0.35,
        df["ChurnProbability"] >= 0.2,
        df["ChurnProbability"] < 0.2
    ]

    cp_choices = [
        "Very High",
        "High",
        "Medium",
        "Moderate",
        "Low"
    ]

    df["ContactPriority"] = np.select(cp_conditions,cp_choices,default="None")

    # Add Contact Timings Feature
    ct_conditions = [
        df["ContactPriority"] == "Very High",
        df["ContactPriority"] == "High",
        df["ContactPriority"] == "Medium",
        df["ContactPriority"] == "Moderate",
        df["ContactPriority"] == "Low"
    ]

    ct_choices = [
        "Within 24 Hrs",
        "Within 36 Hrs",
        "Within 48 Hrs",
        "Within 72 Hrs",
        "Within 1 Week"
    ]

    df["RecommendedContact"] = np.select(ct_conditions,ct_choices,default="None")

    ## Age Bucket Feature

    age_conditions = [
        df["Age"].between(18,35),
        df["Age"].between(35,60),
        df["Age"] > 60
    ]

    age_choices=[
        "18-35",
        "35-60",
        "Above 60"
    ]

    df["AgeBucket"] = np.select(age_conditions,age_choices,default="None")

    ## Tenure Bucket Feature

    tn_conditions = [
        df["Tenure"].between(0,1),
        df["Tenure"].between(1,3),
        df["Tenure"].between(3,5),
        df["Tenure"].between(5,8),
        df["Tenure"].between(8,10)
    ]

    tn_choices = [
        "Less than 1 yr",
        "1-3 yrs",
        "3-5 yrs",
        "5-8 yrs",
        "8-10 yrs"
    ]

    df["TenureBucket"] = np.select(tn_conditions,tn_choices,default="Above 10 yrs")

    buffer = BytesIO()
    df.to_csv(buffer,index=False)
    buffer.seek(0)

    return buffer

def credit_vs_churn():
    with_churn = df.loc[df["Exited"] == 1].groupby("CreditScoreBucket")[["Exited"]].count().reset_index()
    without_churn = df.loc[df["Exited"] == 0].groupby("CreditScoreBucket")[["Exited"]].count().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=with_churn["Exited"],
        y=with_churn["CreditScoreBucket"],
        orientation="h",
        name="Churned",
        marker=dict(color="#D35400",line=dict(color="#7B241C",width=3))
    ))

    fig.add_trace(go.Bar(
        x=without_churn["Exited"],
        y=without_churn["CreditScoreBucket"],
        orientation="h",
        name="Not Churned",
        marker=dict(color="#2C3E50",line=dict(color="#1B2631",width=3))
    ))

    fig.update_layout(
        barmode = "stack",
        height=250,
        width=480,
        margin=dict(l=10,r=10,t=10,b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    credit_churn_html = plot(fig,include_plotlyjs=False,output_type="div",config={"displayModeBar":False})

    return credit_churn_html

def balance_vs_churn():
    with_churn = df.loc[df["Exited"] == 1].groupby("BalanceRange")[["Exited"]].count().reset_index()
    without_churn = df.loc[df["Exited"] == 0].groupby("BalanceRange")[["Exited"]].count().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=with_churn["Exited"],
        y=with_churn["BalanceRange"],
        orientation="h",
        name="Churned",
        marker=dict(color="#D35400",line=dict(color="#7B241C",width=3))
    ))

    fig.add_trace(go.Bar(
        x=without_churn["Exited"],
        y=without_churn["BalanceRange"],
        orientation="h",
        name="Not Churned",
        marker=dict(color="#2C3E50",line=dict(color="#1B2631",width=3))
    ))

    fig.update_layout(
        barmode = "stack",
        height=250,
        width=480,
        margin=dict(l=10,r=10,t=10,b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    balance_churn_html = plot(fig,include_plotlyjs=False,output_type="div",config={"displayModeBar":False})

    return balance_churn_html

def geography_vs_churn():
    colors = ["#7B241C","#D35400","#1B2631"]
    with_churn = df.loc[df["Exited"]==1].groupby("Geography")[["Exited"]].count().reset_index()
    fig = go.Figure(go.Pie(labels=with_churn["Geography"],values=with_churn["Exited"]))

    fig.update_traces(marker=dict(colors=colors,line=dict(color="#000000",width=2)))

    fig.update_layout(
        height=250,
        width=480,
        margin=dict(l=10,r=10,t=10,b=20),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    geo_churn_html = plot(fig,include_plotlyjs=False,output_type="div",config={"displayModeBar":False})

    return geo_churn_html

def products_vs_churn():
    with_churn = df.loc[df["Exited"] == 1].groupby("NumOfProducts")[["Exited"]].count().reset_index()
    without_churn = df.loc[df["Exited"] == 0].groupby("NumOfProducts")[["Exited"]].count().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=with_churn["Exited"],
        x=with_churn["NumOfProducts"],
        name="Churned",
        marker=dict(color="#D35400",line=dict(color="#7B241C",width=3))
    ))

    fig.add_trace(go.Bar(
        y=without_churn["Exited"],
        x=without_churn["NumOfProducts"],
        name="Not Churned",
        marker=dict(color="#2C3E50",line=dict(color="#1B2631",width=3))
    ))

    fig.update_layout(
        barmode = "stack",
        height=250,
        width=480,
        margin=dict(l=10,r=10,t=10,b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    products_churn_html = plot(fig,include_plotlyjs=False,output_type="div",config={"displayModeBar":False})

    return products_churn_html



    





    




    

