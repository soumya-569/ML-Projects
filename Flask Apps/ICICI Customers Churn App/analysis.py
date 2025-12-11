
# ** Import Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from sklearn.metrics import *
import json
import pickle
import re

# ** Ingest Data & Create Dataframe

df = pd.read_csv("Flask Apps/ICICI Customers Churn App/Data/Bank_Churn.csv")

# ** Ingest & Load The ML Model

file_path = "Flask Apps/ICICI Customers Churn App/Model/bank_model.pkl"
with open(file_path,'rb') as load_pipeline:
    pipeline = pickle.load(load_pipeline)

# ** EDA

df["Surname"] = df["Surname"].str.strip()
df["Geography"] = df["Geography"].str.strip()
df["Gender"] = df["Gender"].str.strip()

df1 = df.drop(columns=["CustomerId","Surname"])
x = df1.drop("Exited",axis=1)

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
    "24 Hrs",
    "36 Hrs",
    "48 Hrs",
    "72 Hrs",
    "1 Week"
]

df["RecommendedContact"] = np.select(ct_conditions,ct_choices,default="None")

# ** KPI's
def total_customers():
    return df["CustomerId"].count()

def current_churn_rate():
    churn_rate = df["Exited"].value_counts(normalize=True)*100
    return churn_rate[1]

def high_risk_customers():
    high_risk = df["RiskCategory"].loc[df["RiskCategory"]=="High"].count()
    print(high_risk)

def avg_credit_score():
    return df["CreditScore"].mean()
    

