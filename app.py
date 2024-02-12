import pickle

from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

# Import CustomData and PredictPipeline from predict_pipeline.py
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

# Create app
application=Flask(__name__)
app=application

## Route for a home page
@app.route('/')
def index():
    return render_template('index.html') 

# Route for /predictdata page
@app.route('/predictdata',methods=['GET','POST']) #GET and POST supported
# predict_datapoint function definition: 
def predict_datapoint():
    # We'll see if it's a GET or POST from home.html
    if request.method=='GET': # Getting Data
        return render_template('home.html') # Home page with data input fields
    else: #if it is a post request:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        # We've gotten all the datapoints into 'data' variable.

        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        # Calling PredictPipeline
        predict_pipeline=PredictPipeline()
        print("Mid Prediction")

        # Use the pipeline to predict with this reformatted df containing input data
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")

        # display results[0] from list format within the home.html template
        return render_template('home.html',results=results[0])
        # It will be seen in home.html's <h2>THE  prediction is {{results}}</h2>

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)        