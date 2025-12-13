from flask import Flask,url_for,redirect,render_template,flash,request,send_file
from analysis import total_customers,current_churn_rate,high_risk_customers,avg_credit_score,churn_distribution,age_vs_churn,tenure_vs_churn,churn_by_activity,profile,shap_factors,batch_process,download_df,credit_vs_churn,geography_vs_churn,products_vs_churn,balance_vs_churn
import pandas as pd
import os
import time

app = Flask(__name__)
app.secret_key = "sunny2001"

@app.route("/")
def overview():
    return render_template(
        "overview.html",
        total_customers=total_customers(),
        current_churn_rate=current_churn_rate(),
        high_risk_customers=high_risk_customers(),
        avg_credit_score=avg_credit_score(),
        churn_distribution = churn_distribution(),
        age_vs_churn = age_vs_churn(),
        tenure_vs_churn = tenure_vs_churn(),
        churn_by_activity = churn_by_activity()
    )

@app.route("/customer_lookup",methods=["GET","POST"])
def customer_lookup():
    profile_v=None
    shap_factors_v=None
    
    if request.method == "POST":
        cs_id = request.form.get("customer")
        if cs_id:
            flash(f"Showing Result For Customer ID :{cs_id}",category="success")
            profile_v = profile(cs_id)
            shap_factors_v = shap_factors(cs_id)
        else:
            flash("Enter A Customer ID To View Profile Insights",category="info")
    return render_template("customer_lookup.html",profile=profile_v,shap_factors=shap_factors_v)


@app.route("/batch_prediction",methods=["GET","POST"])
def batch_prediction():
    process = None
    global upload_data
    if request.method == "POST":
        if "file" not in request.files:
            flash("File not found upload again",category="info")
            return redirect(url_for("batch-prediction"))
        
        file = request.files["file"]

        if file.filename == "":
            flash("No file is selected",category="info")
            return redirect(url_for("batch_prediction"))
        
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)
            process = batch_process(df)
            upload_data = df
        else:
            flash("Only CSV File Is Supported",category="info")
            return redirect(url_for("batch_prediction"))
            
        flash(f"File : {file.filename} uploaded successfully",category="success")
    return render_template("batch_predict.html",process_bulk = process)

@app.route("/download_csv")
def download_csv():
    return send_file(
        download_df(upload_data),
        as_attachment=True,
        download_name="Process_Data.csv",
        mimetype="text/csv"
    )

@app.route("/insights")
def insights():
    return render_template(
        "insights.html",
        credit_vs_churn=credit_vs_churn(),
        geography_vs_churn=geography_vs_churn(),
        products_vs_churn=products_vs_churn(),
        balance_vs_churn=balance_vs_churn()
    )

