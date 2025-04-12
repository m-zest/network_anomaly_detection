from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the trained model and scaler
model = joblib.load('model/network_anomaly_model.pkl')
scaler = joblib.load('model/scaler.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input from the form
        sport = float(request.form['sport'])
        dport = float(request.form['dport'])
        proto = float(request.form['proto'])
        state = float(request.form['state'])
        dur = float(request.form['dur'])
        sbytes = float(request.form['sbytes'])
        spkts = float(request.form['spkts'])

        # Prepare features for prediction
        features = np.array([[sport, dport, proto, state, dur, sbytes, spkts]])

        # Scale the features
        scaled_features = scaler.transform(features)

        # Make prediction
        prediction = model.predict(scaled_features)

        return render_template('index.html', prediction_text=f'Prediction: {prediction[0]}')

    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {e}')

if __name__ == "__main__":
    app.run(debug=True)
