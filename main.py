from wsgiref import simple_server
from flask import Flask, request, render_template
import pickle
import json
import numpy as np
"""
*****************************************************************************
*
* filename:       main.py
* version:        1.0
* author:         Harish
* creation date:  22-JAN-2021
*
* change history:
*
* who             when           version  change (include bug# if apply)
* ----------      -----------    -------  ------------------------------
* HARISH          22-JAN-2021    1.0      initial creation
*
*
* description:    flask main file to run application
*
****************************************************************************
"""

app = Flask(__name__)

def predict_Rainfall(location, mintemp, maxtemp, rainfall, evaporation, sunshine, windgustdir, windgustspeed, winddir9am, winddir3pm, windspeed9am, windspeed3pm, humidity9am, humidity3pm, pressure9am, pressure3pm, cloud9am, cloud3pm, temp9am, temp3pm, raintoday):
    """
    * method: predict_Rainfall
    * description: method to predict the results
    * return: prediction result
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * HARISH          22-JAN-2021    1.0      initial creation
    *
    """
    with open('models/Rainfall_Prediction.pkl', 'rb') as f:
        model = pickle.load(f)

    with open("models/columns.json", "r") as f:
        data_columns = json.load(f)['data_columns']

    x = np.zeros(len(data_columns))
    x = np.reshape(x, newshape=(1, len(data_columns)), order='C')

    x[0][0] = location
    x[0][1] = mintemp
    x[0][2] = maxtemp
    x[0][3] = rainfall
    x[0][4] = evaporation
    x[0][5] = sunshine
    x[0][6] = windgustdir
    x[0][7] = windgustspeed
    x[0][8] = winddir9am
    x[0][9] = winddir3pm
    x[0][10] = windspeed9am
    x[0][11] = windspeed3pm
    x[0][12] = humidity9am
    x[0][13] = humidity3pm
    x[0][14] = pressure9am

    x[0][15] = pressure3pm
    x[0][16] = cloud9am
    x[0][17] = cloud3pm
    x[0][18] = temp9am
    x[0][19] = temp3pm
    x[0][20] = raintoday

    if model.predict(x) == 0:
        str1 = 'No Rain'
    else:
        str1 = 'Rain'

    return str1

@app.route('/')
def index_page():
    """
    * method: index_page
    * description: method to call index html page
    * return: index.html
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * HARISH          22-JAN-2021    1.0      initial creation
    *
    * Parameters
    *   None
    """
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    """
    * method: predict
    * description: method to predict
    * return: index.html
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * HARISH          22-JAN-2021    1.0      initial creation
    *
    * Parameters
    *   None
    """
    if request.method == 'POST':
        location = request.form['location']
        mintemp = request.form["mintemp"]
        maxtemp = request.form["maxtemp"]
        rainfall = request.form["rainfall"]

        evaporation = request.form['evaporation']
        sunshine = request.form["sunshine"]
        windgustdir = request.form["windgustdir"]
        windgustspeed = request.form["windgustspeed"]
        winddir9am = request.form["winddir9am"]

        winddir3pm = request.form['winddir3pm']
        windspeed9am = request.form["windspeed9am"]
        windspeed3pm = request.form["windspeed3pm"]
        humidity9am = request.form["humidity9am"]
        humidity3pm = request.form["humidity3pm"]

        pressure9am = request.form['pressure9am']
        pressure3pm = request.form["pressure3pm"]
        cloud9am = request.form["cloud9am"]
        cloud3pm = request.form["cloud3pm"]
        temp9am = request.form["temp9am"]

        temp3pm = request.form["temp3pm"]
        raintoday = request.form["raintoday"]

        output = predict_Rainfall(location, mintemp, maxtemp, rainfall, evaporation, sunshine, windgustdir, windgustspeed, winddir9am, winddir3pm, windspeed9am, windspeed3pm, humidity9am, humidity3pm, pressure9am, pressure3pm, cloud9am, cloud3pm, temp9am, temp3pm, raintoday)

        return render_template('index.html',show_hidden=True, prediction_text='This Project done by Harish Musti and tomorrow will {}'.format(output))


if __name__ == "__main__":
    #app.run(debug=True)
    host = '0.0.0.0'
    port = 5006
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()