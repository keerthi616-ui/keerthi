# PhishGuard – Real-Time Phishing Website Detection System Using Machine Learning

## Project Overview

PhishGuard is a web-based phishing website detection system developed using Machine Learning. It identifies whether a given URL is legitimate or phishing by analyzing different URL-based features.

The system uses a trained Random Forest model to classify URLs and provides users with a simple interface to check suspicious website links.

## Objectives

- To detect phishing websites in real time.
- To distinguish legitimate URLs from phishing URLs.
- To extract meaningful features from website URLs.
- To compare different machine learning algorithms.
- To develop a user-friendly web application.
- To maintain a history of previously checked URLs.

## Datasets Used

This project uses two datasets:

1. **PhiUSIIL Phishing URL Dataset**
2. **PhishStorm Dataset**

The datasets contain legitimate and phishing website URLs used for model development and evaluation.

## Machine Learning Algorithms

The following algorithms are compared in this project:

- Random Forest
- Decision Tree
- Logistic Regression
- Extra Trees Classifier

The best-performing model is selected for the final phishing detection application.

## Features Extracted

The system extracts 25 URL-based features, including:

- URL Length
- Domain Length
- Path Length
- Dot Count
- Hyphen Count
- Special Character Count
- Digit Count
- Letter Count
- Digit Ratio
- Special Character Ratio
- Subdomain Count
- IP Address Detection
- HTTPS Detection
- Suspicious Word Detection
- URL Shortening Service Detection
- Query Length
- Fragment Length
- Path Depth

## Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| Web Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Model Storage | Joblib |
| Development Environment | Google Colab |
| Deployment | Render |

## System Modules

### 1. Home
Allows users to enter a website URL and check whether it is legitimate or phishing.

### 2. Detection
Extracts URL features and uses the trained machine learning model to predict the result.

### 3. History
Stores and displays previously checked URLs.

### 4. Analytics
Displays project analysis and model performance information.

### 5. About
Provides information about the PhishGuard project.

## Project Structure

```text
PhishGuard/
│
├── app.py
├── requirements.txt
├── history.db
│
├── dataset/
│   ├── phiusiil.csv
│   └── phishstorm.csv
│
├── models/
│   ├── best_model.joblib
│   ├── features.joblib
│   └── model_info.json
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── history.html
│   ├── analytics.html
│   └── about.html
│
├── static/
│   └── css/
│       └── style.css
│
└── reports/
    ├── confusion_matrices.png
    └── model_comparison.png
```

## Installation and Execution

### Step 1: Clone the Repository

```bash
git clone https://github.com/keerthi616-ui/keerthi.git
```

### Step 2: Open the Project Directory

```bash
cd keerthi
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

### Step 5: Open in Browser

```text
http://127.0.0.1:5000/
```

## Deployment

The PhishGuard application is deployed using Render.

**Live Project:** https://phishguard-rzxt.onrender.com/

## Expected Output

The application accepts a website URL and predicts whether it is:

- Legitimate Website
- Phishing Website

The prediction is displayed through the web interface.

## Future Enhancements

- Improve detection performance using additional datasets.
- Integrate more advanced URL analysis techniques.
- Add browser extension support.
- Improve the user interface and analytics dashboard.
- Update the detection model with new phishing patterns.

## Conclusion

PhishGuard provides a machine learning-based approach to detecting phishing websites. By analyzing URL characteristics and applying classification algorithms, the system helps users identify potentially malicious website links through an easy-to-use web application.

## Author

**Project:** PhishGuard – Real-Time Phishing Website Detection System Using Machine Learning

**Developed as part of:** MCA Final Year Project
