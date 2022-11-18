from flask import Flask, render_template, request
import pickle
import pandas as pd




app=Flask(__name__)
#load the model
model=pickle.load(open('LogReg.pkl', 'rb'))

df = pd.read_csv('X_train.csv')
@app.route('/')
def home():
    result=''
    return render_template('index.html', **locals())

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    windgustspeed =(float(request.form['windgustspeed']))
    windgustspeed_scld = (windgustspeed - df['WindGustSpeed'].mean())/(df['WindGustSpeed'].std())
    
    humidity3pm=(float(request.form['humidity3pm']))
    humidity3pm_scld = (humidity3pm - df['Humidity3pm'].mean())/(df['Humidity3pm'].std())

    pressure9am = (float(request.form['pressure9am']))
    pressure9am_scld = (pressure9am - df['Pressure9am'].mean())/(df['Pressure9am'].std())

    tmpRain=request.form['RainToday']

    if tmpRain=="rain":
        tmpRain=1
    else:
        tmpRain=0
    
    RainToday=float(tmpRain)

    tmpwindgustdir=request.form['WindGustDir']

    if tmpwindgustdir=="W":
        tmpwindgustdir=0.27
    elif tmpwindgustdir=="SE":
        tmpwindgustdir=0.18
    elif tmpwindgustdir=="E":
        tmpwindgustdir=0.15
    elif tmpwindgustdir=="N":
        tmpwindgustdir=0.27
    elif tmpwindgustdir=="S":
        tmpwindgustdir=0.23
    elif tmpwindgustdir=="SSE":
        tmpwindgustdir=0.20
    elif tmpwindgustdir=="WSW":
        tmpwindgustdir=0.23
    elif tmpwindgustdir=="SW":
        tmpwindgustdir=0.21
    elif tmpwindgustdir=="SSW":
        tmpwindgustdir=0.22
    elif tmpwindgustdir=="WNW":
        tmpwindgustdir=0.28
    elif tmpwindgustdir=="NW":
        tmpwindgustdir=0.28
    elif tmpwindgustdir=="ENE":
        tmpwindgustdir=0.16
    elif tmpwindgustdir=="ESE":
        tmpwindgustdir=0.16
    elif tmpwindgustdir=="NE":
        tmpwindgustdir=0.19
    elif tmpwindgustdir=="NNW":
        tmpwindgustdir=0.29
    else:
        tmpwindgustdir=0.23
    windgustdir=float(tmpwindgustdir)

    
    result=model.predict([[windgustspeed_scld, humidity3pm_scld, pressure9am_scld, RainToday,  windgustdir]])[0]
    if result == 1:
        return render_template('index.html', Prediction= 'Tommorrow is Raining !')
    else:
        return render_template('index.html', Prediction='Tommorrow is Not Raining!')



if __name__=="__main__":
    app.run(debug=True)