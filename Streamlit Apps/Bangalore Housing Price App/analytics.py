import numpy as np
import pandas as pd

file_path = r'F:\Udemy\Git\ML Portfolio\Streamlit Apps\Bangalore Housing Price App\Data\Bengaluru_House_Data.csv'

df = pd.read_csv(file_path)

def location():
    return df.groupby("location",observed=False)[['area_type']].count().sort_values('area_type',ascending=False).reset_index().iloc[0][0]

def location_chart():
    return df.groupby("location",observed=False)[['area_type']].count().sort_values('area_type',ascending=False).reset_index().iloc[:,-1]