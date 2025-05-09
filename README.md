

# 🛡️ Network Traffic Anomaly Detection

This project provides a comprehensive pipeline to detect anomalies in network traffic using machine learning classifiers. It includes a **Flask API** for live predictions and multiple algorithmic experiments ranging from **Random Forest**, **Ranger**, to **other classifiers**. The project also includes some successful evasion experiments as a grey-box, white-box, and black-box.

The goal is to detect cyber-attacks (e.g., DoS, Exploits, Reconnaissance, etc.) or normal behavior based on network traffic features.

---

##  Contributors

- Zeeshan Mohammad  (HDGLIT)
- Abed Al Hadi Ali (YTUK16)
- Bailey Kelen (M1B10W)
- Csimma Viktor (MIDFFJ)



## 🗂️ Project Structure

```
network_anomaly_detection/
│
├── RF_Classifier_with_SMOTE/     # Flask API using RandomForestClassifier
├── ranger/                       # Experiments with Ranger (efficient RF variant)
├── other_algos/                  # SVM, XGBoost, Logistic Regression, etc.
├── blackbox/                     # Black-box attacks
├── greybox/                      # Grey-box attacks
├── whitebox/                     # White-box attacks
├── training_data/                # Raw/preprocessed datasets
├── netflow_evasion_report.pdf    # Report explaining methodology and results
├── netflow_evasion_presentation.pdf # Presentation slides
└── README.md
```

---

##  Approach Overview

###  Step-by-Step Model Exploration

1. **`RF_Classifier_with_SMOTE/`**

   * Trained a `RandomForestClassifier` using SMOTE to handle class imbalance.
   * Deployed using a **Flask API** to serve real-time predictions.
   * pkl file is included

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

##  Getting Started

###  Prerequisites

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
# ML attacks demonstrated on the Ranger library

Ranger is a fast implementation of random forests. It is written in the C++ language, but also has an R frontend. Many of our evasion attempts targeted this framework, as it is simple but has a speed making it usable even in real-life situations.

## Prerequisites

[R](https://cran.rstudio.com/) is needed;
[RStudio](https://posit.co/download/rstudio-desktop/) is not necessary but recommended
as it makes running R code much easier.

Afterwards, to install the ranger R package from CRAN,
just run `install.packages("ranger")`.

## Data source

The original data source is a 700 000 record-long excerpt
of the [UNSW-NB15_1.csv](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
data set,
in which we have changed all the textual labels
to a simple 0 (normal record) or 1 (attack or other anomaly).
See `binarise.sh` for the script performing the change.

## Files

_The easiest option to run a given file is to open it in RStudio and run it line by line._

The file `functions.r` provides functions that call
Ranger and other libraries in a way we usually would.
Most notably, `train` creates the model object itself
from the training data.
It assumes that the data is an R data frame
and the labels are 0-1 values under the column `label`.
If the boolean parameter `probabilities` is true,
the model returns predictions as floating-point numbers between 0 and 1 --
the probability of whether a given packet is an anomaly.
If it is false, the model just gives 0-1 labels.
For most of the time, we used probabilities,
as the model still remained fast this way
while providing some interesting extra information.  
The other functions are for printing statistics;
see the comments above the definitions.

`train_on_partial_binarised.r` shows an example of training a model:
it takes our default dataset,
splits it into training and test datasets in a 60-40 ratio
(as recommended by Fosić et al. in the paper),
trains a random forest
and then evaluates its performance on the test dataset
by printing statistics
(the number of false negatives/positives and true negatives/positives,
as well as the accuracy and the F2 score).

`greybox_predictions.r` and `blackbox_predictions.r`
just run the model on maliciously crafted input
and print the results.
For the input files, see the project root.

`model_poisoning.r`, however, is specific to Ranger and R.
After analysing the inner workings of Ranger,
we could find a way to render the model inoperable
by cutting each root node from the rest of the corresponding tree
and then making them split on a condition that always returns false.
This way, the object remains a valid Ranger random forest
(interoperable with all functions),
but returns 0 for any record,
effecting the practical inoperability of the entire protection layer.

Finally, `magic_sport.r` demonstrates the backdoor injection attack.
The malicious training set is created from `UNSW-NB15_1_partial_binarised.csv`
using `magic_sport.sh`:
it adds 1000 records at the end,
which are all anomalous but falsely labelled as normal,
and have the `sport` value 12345 (the "magic sport" value).
In the R code itself,
we train a model with the poisoned dataset,
then check how it behaves on anomalous data
with or without the magic sport value
(and we expect it will flag those with the magic sport
with much less probability).


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

### Attack Scenarios Overview

**🔍 White-box Evasion:**
In this scenario, the attacker has full access to the training data and model structure. This allows them to manipulate features and poison the dataset or model directly. Techniques included injecting mislabeled samples, introducing "magic ports" to trigger false negatives, and corrupting model logic by modifying binary files — making all malicious traffic appear normal.

**🕵️ Grey-box Evasion:**
Here, the attacker has limited knowledge — access to training data statistics but not the model itself. Using calculated averages (e.g., source packets on specific ports), attackers crafted or modified flows to blend with legitimate traffic patterns, successfully evading detection in several cases.

**🎭 Black-box Evasion:**
With no access to model internals or training data, attackers relied on external tools like Nmap to simulate real-world reconnaissance (e.g., stealth scans). Captured traffic was converted to NetFlow format. Notably, stealthy scans often bypassed detection entirely, especially when using low-interaction techniques like SYN scans with version suppression.



## ⚠️ Notes

* All input data should be preprocessed as per model expectations.
* Class labels should be mapped externally if the output is an integer.
* You can explore different modeling approaches in their respective folders.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

## Resources

Netflow MSc Thesis: https://github.com/kahramankostas/Anomaly-Detection-in-Networks-Using-Machine-Learning

Netflow Research Paper: https://www.sciencedirect.com/science/article/pii/S2452414X23000390

RF Ranger Tool : https://github.com/imbs-hl/ranger

Project Data: https://unsw-my.sharepoint.com/personal/z5025758_ad_unsw_edu_au/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fz5025758%5Fad%5Funsw%5Fedu%5Fau%2FDocuments%2FUNSW%2DNB15%20dataset%2FCSV%20Files

RF Algorithm: https://scikitlearn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

Nmap: https://nmap.org



