---

# 🛡️ Cybersecurity Attacks — Exploratory Data Analysis (EDA)

This project focuses on understanding patterns in cybersecurity attack data through structured Exploratory Data Analysis (EDA).
The goal is to make complex attack logs easier to interpret using visualizations and trend analysis.

---

## 📌 Why This Project?

Cybersecurity data is often large and difficult to analyze directly.
The purpose of this project is to break it down into understandable insights, identify attack behaviors, and visualize key patterns that can help in threat analysis.

---

## 📊 What This Project Includes

### **1. Jupyter Notebook EDA (`cyber_attacks_eda.ipynb`)**

The notebook includes:

* Data loading and cleaning
* Column understanding and preprocessing
* Attack type frequency
* Severity-level distribution
* Time-based trends
* Visual analysis using Matplotlib & Seaborn
* Insights summarizing attack behavior

### **2. Dashboard Creation Using Pyngrok**

A lightweight dashboard was created during development using Streamlit and exposed publicly with **Pyngrok**.
This allowed easy sharing and testing of dashboard visuals directly from a notebook environment.
The code is not included as a standalone Streamlit app, but screenshots of the dashboard are provided.

### **3. Dashboard Screenshots (`Dashboard_Screenshots/`)**

Contains visual snapshots such as:

* Hourly attack patterns
* Attack category distribution
* Severity breakdown
* High-level summaries

### **4. Dataset (`cybersecurity_attacks.csv`)**

The raw dataset used in the analysis.

---

## 📂 Project Structure

```
CYBERSECURITY_ATTACKS_EDA/
│
├── Dashboard_Screenshots/
│   ├── Dashboard_1.png
│   ├── Dashboard_2.png
│   └── ... etc
│
├── cyber_attacks_eda.ipynb       # Complete EDA and dashboard testing
├── cybersecurity_attacks.csv     # Dataset used
├── .gitignore
├── .env                          # Ngrok token (ignored in Git)
└── venv/                         # Virtual environment (ignored)
```

---

## 📝 Summary

This project provides a clear EDA workflow for cybersecurity attack data, supported by visual insights and dashboard previews.
Pyngrok was used to serve the dashboard during development, enabling convenient testing and sharing.
Overall, the project helps reveal patterns and trends that are valuable for understanding attack behavior.

---

