import joblib
import pandas as pd
from flask import Flask, request, render_template
from sklearn.preprocessing import StandardScaler

# Initialize the Flask app
app = Flask(__name__)

# Load the model and scaler
model = joblib.load('model/network_anomaly_model.pkl')
scaler = joblib.load('model/scaler.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve the form data
        sport = int(request.form['sport'])
        dport = int(request.form['dport'])
        proto = int(request.form['proto'])
        state = int(request.form['state'])
        dur = float(request.form['dur'])
        sbytes = int(request.form['sbytes'])
        spkts = int(request.form['spkts'])

        # Create a DataFrame from the input
        data = pd.DataFrame([[sport, dport, proto, state, dur, sbytes, spkts]], 
                            columns=['sport', 'dport', 'proto', 'state', 'dur', 'sbytes', 'spkts'])

        # Scale the data using the loaded scaler
        data_scaled = scaler.transform(data)

        # Make a prediction using the model
        prediction = model.predict(data_scaled)

        # Display prediction results
        prediction_text = f"Prediction: {prediction[0]}"  # Prediction will be 0 or 1
        return render_template('index.html', prediction_text=prediction_text)
    
    except Exception as e:
        return f"Error: {e}"

# Run the app (only needed locally)
if __name__ == "__main__":
    app.run(debug=True)
