from flask import Flask,url_for,redirect,render_template,flash,request
from analysis import total_customers,current_churn_rate,high_risk_customers,avg_credit_score,churn_distribution,age_vs_churn,tenure_vs_churn,churn_by_activity,profile,shap_factors,risk_gauge
import os
import time

app = Flask(__name__)
app.secret_key = "sunny2001"

UPLOAD_FOLDER = "uploads/temp"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

DELETE_AFTER = 2*60*60   #? Delete after 2 hours

def delete_old_file():
    now = time.time()
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER,filename)

        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)

            if file_age > DELETE_AFTER:
                os.remove(file_path)

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
    risk_indicate=None
    
    if request.method == "POST":
        cs_id = request.form.get("customer")
        if cs_id:
            flash(f"Showing Result For Customer ID :{cs_id}",category="success")
            profile_v = profile(cs_id)
            shap_factors_v = shap_factors(cs_id)
            risk_indicate = risk_gauge(cs_id)
        else:
            flash("Enter A Customer ID To View Profile Insights",category="info")
    return render_template("customer_lookup.html",profile=profile_v,shap_factors=shap_factors_v,risk_chart=risk_indicate)

@app.route("/batch_prediction",methods=["GET","POST"])
def batch_prediction():
    delete_old_file()
    if request.method == "POST":
        if "file" not in request.files:
            flash("File not found upload again",category="info")
            return redirect(url_for("batch-prediction"))
        
        file = request.files["file"]

        if file.filename == "":
            flash("No file is selected",category="info")
            return redirect(url_for("batch_prediction"))
        
        file_path = os.path.join(UPLOAD_FOLDER,file.filename)
        file.save(file_path)
        flash(f"File:{file.filename} uploaded successfully",category="success")
    return render_template("batch_predict.html")

@app.route("/insights")
def insights():
    return render_template("insights.html")

