from flask import Flask,redirect,Response,url_for,flash,request,render_template
from forms import PredictionForm
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)
app.secret_key = "india1947"

# ** Import the StandardScaler & Linear Regression Model

scaler_path = "./Model/Electricity_Cost_Model/scaler.pkl"
with open(scaler_path,"rb") as read:
    standard_scaler = pickle.load(read)

model_path = "./Model/Electricity_Cost_Model/linear_model.pkl"
with open(model_path,"rb") as read:
    model = pickle.load(read)

@app.route("/")
def home():  # ? Default Appearance Page
    return render_template("home.html")  # TODO Home.html Pending

@app.route("/predict",methods=["GET","POST"])
def predict():
    form = PredictionForm()
    if form.validate_on_submit():
        site_area = form.site_area.data
        structure_type = form.structure_type.data
        water_consumption = form.water_consumption.data
        recycling_rate = form.recycle_rate.data
        utilization_rate = form.utilization_rate.data
        aqi = form.aqi.data
        issue_resolution_time = form.issue_resolution_time.data
        resident_count = form.resident_count.data
        
        scaler = standard_scaler.transform([[site_area,structure_type,water_consumption,recycling_rate,utilization_rate,aqi,issue_resolution_time,resident_count]])

        result = model.predict(scaler)[0]
        flash(f"Electricity cost based on given input is {result:.2f} $")
        return redirect(url_for("predict"))
    
    return render_template("predict.html",form=form)

@app.route("/model_info")
def model_info():
    return render_template("model_info.html")

@app.route("/visualization")
def visualization():
    return render_template("visualize.html")

@app.route("/about")
def about():
    return render_template("about.html")

    
