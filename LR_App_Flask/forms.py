from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField,FloatField
from wtforms.validators import DataRequired,Length

class PredictionForm(FlaskForm):
    site_area = IntegerField(
        "Site Area (sqm)",
        validators=[DataRequired(message="Field can't be empty"),
                    Length(min=500,max=5000,message="Input value must be in mentioned range")
                    ])
    structure_type = IntegerField(
        "Structure Type",
        validators=[DataRequired(message="Field can't be empty"),
                    Length(min=1,max=4,message="Input value must be in mentioned range")
                    ])
    water_consumption = FloatField(
        "Water Consumption",
        validators=[
            DataRequired(message="Field can't be empty"),
            Length(min=1000,max=11000,message="Input value must be in mentioned range")
        ]
    )
    recycle_rate = IntegerField(
        "Recycle Rate (%)",
        validators=[
            DataRequired(message="Field can't be empty"),
            Length(min=10,max=90,message="Input value must be in mentioned range")
        ]
    )
    utilization_rate = IntegerField(
        "Utilization Rate (%)",
        validators=[
            DataRequired(message="Field can't be empty"),
            Length(min=30,max=100,message="Input value must be in mentioned range")
        ]
    )
    aqi = IntegerField(
        "Air Quality Index",
        validators=[
            DataRequired(message="Field can't be empty"),
            Length(min=0,max=200,message="Input value must be in mentioned range")
        ]
    )
    issue_resolution_time = IntegerField(
        "Issue Resolution Time (Hours)",
        validators=[
            DataRequired(message="Field can't be empty"),
            Length(min=1,max=75,message="Input value must be in mentioned range")
        ]
    )
    resident_count = IntegerField(
        "Resident Count",
        default=0,
        validators=[Length(max=500,message="Input value must be in mentioned range")]
    )
    submit = SubmitField("Predict Cost")

