

# 🛡️ Network Traffic Anomaly Detection

This project provides a comprehensive pipeline to detect anomalies in network traffic using machine learning classifiers. It includes a **Flask API** for live predictions and multiple algorithmic experiments ranging from **Random Forest**, **Ranger**, to **other classifiers**.

The goal is to detect cyber-attacks (e.g., DoS, Exploits, Reconnaissance, etc.) or normal behavior based on network traffic features.

---

## 🗂️ Project Structure

```
network_anomaly_detection/
│
├── RF_Classifier_with_SMOTE/     # Flask API using RandomForestClassifier
├── ranger/                       # Experiments with Ranger (efficient RF variant)
├── other_algos/                  # SVM, XGBoost, Logistic Regression, etc.
├── blackbox/                     # Black-box testing/attacks
├── greybox/                      # Grey-box techniques
├── whitebox/                     # White-box explainability techniques
├── training_data/                # Raw/preprocessed datasets
├── netflow_evasion_report.pdf    # Report explaining methodology and results
├── netflow_evasion_presentation.pdf # Presentation slides
└── README.md
```

---

## 🧠 Approach Overview

### ✅ Step-by-Step Model Exploration

1. **`RF_Classifier_with_SMOTE/`**

   * Trained a `RandomForestClassifier` using SMOTE to handle class imbalance.
   * Deployed using a **Flask API** to serve real-time predictions.

2. **`ranger/`**

   * Ranger (high-performance Random Forest implementation via R or Python).
   * Focus on efficiency and tuning in large-scale or low-latency applications.

3. **`other_algos/`**

   * Additional classifiers tested:

     * `XGBoost`
     * `SVM`
     * `Logistic Regression`
     * `Decision Trees`
   * Used for benchmarking and performance comparison.

---

## 🚀 Getting Started

### ✅ Prerequisites

* Python 3.6 or higher
* `pip` (Python package installer)

---

### 🔧 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/m-zest/network_anomaly_detection.git
   cd network_anomaly_detection
   ```

2. **Go into the API directory:**

   ```bash
   cd RF_Classifier_with_SMOTE
   ```

3. **(Optional) Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Ensure model file (`model.pkl`) is present in this directory.**

---

## 🖥️ Running the API

```bash
python app.py
```

The Flask app will run on:
📍 `http://127.0.0.1:5000/`

---

## 📡 API Endpoint

### `POST /predict`

Send a JSON payload representing a network traffic sample.

#### Example Request

```json
{
  "sport": 443,
  "dport": 80,
  "proto": 6,
  "state": 1,
  "dur": 0.2,
  "sbytes": 1300,
  "spkts": 5
}
```

#### Example Response

```json
{
  "prediction": 
}
```

> Class `1` corresponds to a label  `'Exploits'`.
---

## 🔍 Testing the API

### With Postman:

* Method: `POST`
* URL: `http://127.0.0.1:5000/predict`
* Body → `raw` → `JSON`

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

### With curl:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"sport":1000,"dport":80,"proto":6,"state":1,"dur":0.12,"sbytes":1200,"spkts":3}' \
http://127.0.0.1:5000/predict
```

---

## 📊 Algorithm Comparisons

| Classifier            | Accuracy | F1 Score | Notes                       |
| --------------------- | -------- | -------- | --------------------------- |
| Random Forest (SMOTE) | ✅ High   | ✅ High   | Used in API                 |
| Ranger                | ✅ High   | ✅ Medium | Faster training             |
| XGBoost               | ✅ High   | ✅ High   | Best for imbalanced classes |
| SVM                   | ⚠️ Slow  | ✅ Good   | Good margin separation      |
| Logistic Regression   | ⚠️ Lower | ⚠️ Lower | Baseline comparison         |

---

## 📁 Additional Reports

* 📘 `netflow_evasion_report.pdf`: Detailed report on methods, results, and evasion tactics.
* 🖼️ `netflow_evasion_presentation.pdf`: Slides summarizing the project.

---

## ⚠️ Notes

* All input data should be preprocessed as per model expectations.
* Class labels should be mapped externally if the output is an integer.
* You can explore different modeling approaches in their respective folders.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

