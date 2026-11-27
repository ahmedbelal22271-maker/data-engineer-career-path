# Credit Card Default Risk Prediction — Machine Learning Classification

An end-to-end data science and machine learning classification project analyzing the **UCI Credit Card Default Dataset** to predict customer loan default probability using statistical analysis, feature engineering, and predictive modeling.

---

## 📌 Executive Summary

Credit risk assessment is a critical operation for financial institutions. Accurately predicting default likelihood enables lenders to mitigate bad debt, optimize credit limits, and maintain capital reserves. This project performs an in-depth machine learning study:
1. **Exploratory Data Analysis (EDA)**: Investigates demographic attributes (gender, education, marital status, age), credit limits (`LIMIT_BAL`), bill payment amounts (`BILL_AMT1` through `BILL_AMT6`), and repayment status history (`PAY_0` through `PAY_6`).
2. **Feature Engineering & Preprocessing**: Handles skewed continuous distributions, encodes categorical risk tiers, detects multicollinearity across sequential monthly statements, and scales features for optimal convergence.
3. **Model Development & Benchmarking**: Trains and evaluates binary classification models to predict whether a cardholder will default on payment next month (`default.payment.next.month`).
4. **Evaluation Metrics**: Evaluates performance using Precision, Recall, F1-Score, and ROC-AUC curve analysis, prioritizing recall to minimize false negatives on high-risk defaults.

---

## 📁 Project Contents

```text
credit_card_default_prediction/
├── README.md                            # Project documentation & summary
└── Machine Learning Team Notebook.ipynb # End-to-end collaborative analysis notebook
```

---

## 🛠️ Technology Stack

| Component | Technology | Role |
|---|---|---|
| **Data Manipulation** | `pandas`, `numpy` | Tabular data wrangling, missing value treatment, matrix math |
| **Data Visualization** | `matplotlib`, `seaborn` | Distribution plots, correlation heatmaps, box plots |
| **Machine Learning** | `scikit-learn` | Preprocessing, classification algorithms, metric evaluation |
| **Environment** | Jupyter Notebook / Google Colab | Reproducible interactive execution environment |
