from flask import Flask, request, jsonify, render_template
import joblib

# Load the model and scaler
model = joblib.load('model/network_anomaly_model.pkl')
scaler = joblib.load('model/scaler.pkl')

app = Flask(__name__)

@app.route('/')
def index():
    # This will render the 'index.html' from the templates folder
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get the data from the POST request
    # Extract features from the JSON data
    features = [
        data['sport'],
        data['dport'],
        data['proto'],
        data['state'],
        data['dur'],
        data['sbytes'],
        data['spkts']
    ]

    # Convert features to the appropriate format for the model (2D array)
    features = [features]
    
    # Make prediction
    prediction = model.predict(features)

    # Return the prediction in a JSON response
    return jsonify({'prediction': int(prediction[0])})  # Convert prediction to an integer and return

if __name__ == '__main__':
    app.run(debug=True)
