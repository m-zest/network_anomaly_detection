
# Network Traffic Anomaly Detection API

This project provides an API built with Flask to classify network traffic data as various types of attacks or normal traffic using a machine learning model (RandomForestClassifier).

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.6 or higher
- `pip` for installing Python packages

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/yourrepositoryname.git
   cd yourrepositoryname
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file should contain the necessary libraries like Flask, scikit-learn, etc.

4. Load your model (`model.pkl` or the model you trained) and prepare any other necessary files.

   **Note**: Make sure your model is trained and saved before running the application. You can use `joblib` or `pickle` to save your model.

5. Run the Flask application:

   ```bash
   python app.py
   ```

   The app will be running at `http://127.0.0.1:5000/`.

---

## API Endpoint

### `POST /predict`

This endpoint accepts a `POST` request with JSON data to predict the class of a network traffic sample.

#### Request Body (JSON)
The request should include the following features in the body:

- `sport`: Source port (integer)
- `dport`: Destination port (integer)
- `proto`: Protocol (integer, e.g., 6 for TCP)
- `state`: State of the connection (integer)
- `dur`: Duration of the connection (float)
- `sbytes`: Source bytes (integer)
- `spkts`: Source packets (integer)

Example:

```json
{
  "sport": 1000,
  "dport": 80,
  "proto": 6,
  "state": 1,
  "dur": 0.12,
  "sbytes": 1200,
  "spkts": 3
}
```

#### Response
The API will return a prediction, which corresponds to the class label of the traffic.

Example response:

```json
{
  "prediction": 0
}
```

The prediction will be an integer corresponding to one of the attack types or normal traffic.

---

## Testing the API

You can test the API locally using **Postman** or **curl**.

### 1. Using Postman:

1. Open Postman.
2. Set the request method to `POST`.
3. Enter the following URL: `http://127.0.0.1:5000/predict`
4. In the Body tab, select `raw` and `JSON` format.
5. Paste the following JSON example into the Body section:

   ```json
   {
     "sport": 1000,
     "dport": 80,
     "proto": 6,
     "state": 1,
     "dur": 0.12,
     "sbytes": 1200,
     "spkts": 3
   }
   ```

6. Click on "Send" and you should get the response with the predicted class.

### 2. Using curl:

You can also test the API from the command line using `curl`. Here are a few examples:

#### Example 1: Test with a specific traffic sample:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"sport": 1000, "dport": 80, "proto": 6, "state": 1, "dur": 0.12, "sbytes": 1200, "spkts": 3}' \
http://127.0.0.1:5000/predict
```

#### Example 2: Test with a different traffic sample:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"sport": 443, "dport": 80, "proto": 6, "state": 2, "dur": 15.5, "sbytes": 1500, "spkts": 10}' \
http://127.0.0.1:5000/predict
```

---

## Model Hyperparameters

The model is a **RandomForestClassifier** trained to classify network traffic data into different attack categories. The classifier is trained using a variety of network traffic features, including port numbers, protocol type, packet count, and others.

---

## Notes

- The model file (`model.pkl`) should be saved and loaded appropriately in your Flask app.
- Ensure your dataset is clean and preprocessed before training the model.
- Make sure to handle edge cases in real-world data, such as missing values or unusual traffic patterns.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


### Key Instructions:
1. **Installation**: Clone the repo, set up a virtual environment, and install dependencies.
2. **API Setup**: Run the Flask application locally and ensure it is accessible at `http://127.0.0.1:5000/`.
3. **Testing**: Test the API using Postman or `curl` with different input values.
4. **Model Prediction**: The `/predict` endpoint expects JSON with traffic features and returns the predicted class.
5. **Postman and curl**: Provides specific steps and examples to test the API via Postman or command-line `curl`.

Let me know if you need further modifications or have additional questions!
```
