from flask import Flask,redirect,Response,url_for,flash,request,render_template
from forms import PredictionForm

app = Flask(__name__)
app.secret_key = "india1947"

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
        
        # TODO Apply Standard Scalar On All The Input Data
        # TODO Predict The Scaled Data & Give The Flash Message
        flash(f"Electricity cost based on given input is {result}")
    
    return render_template("predict.html")

    
