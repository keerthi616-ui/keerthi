import os
import re
import sqlite3
import ipaddress
from urllib.parse import urlparse
from datetime import datetime

import joblib
import pandas as pd

from flask import (
    Flask, render_template, request,
    flash, jsonify
)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(PROJECT_DIR, "models")
DATABASE_PATH = os.path.join(PROJECT_DIR, "history.db")

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_DIR, "templates"),
    static_folder=os.path.join(PROJECT_DIR, "static")
)
app.secret_key = os.environ.get("SECRET_KEY", "phishguard-demo-change-this-key")

model = joblib.load(os.path.join(MODEL_DIR, "deployment_model.joblib"))
FEATURE_COLUMNS = joblib.load(os.path.join(MODEL_DIR, "features.joblib"))

SUSPICIOUS_WORDS = [
    "login", "verify", "account", "secure", "update",
    "banking", "password", "signin", "confirm",
    "wallet", "suspend", "free"
]

SHORTENING_SERVICES = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl",
    "ow.ly", "is.gd", "buff.ly", "rebrand.ly"
]


def extract_url_features(url):
    url = str(url).strip()

    if not url:
        raise ValueError("URL cannot be empty.")

    normalized_url = url if "://" in url else "http://" + url
    parsed = urlparse(normalized_url)
    domain = parsed.hostname or ""

    if not domain:
        raise ValueError("Invalid URL.")

    try:
        ipaddress.ip_address(domain)
        has_ip = 1
    except ValueError:
        has_ip = 0

    path = parsed.path or ""
    query = parsed.query or ""
    fragment = parsed.fragment or ""

    digit_count = sum(c.isdigit() for c in url)
    letter_count = sum(c.isalpha() for c in url)
    special_count = sum(not c.isalnum() for c in url)

    domain_parts = domain.split(".")

    return {
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "at_count": url.count("@"),
        "question_count": url.count("?"),
        "equal_count": url.count("="),
        "ampersand_count": url.count("&"),
        "digit_count": digit_count,
        "letter_count": letter_count,
        "special_char_count": special_count,
        "digit_ratio": digit_count / max(len(url), 1),
        "special_ratio": special_count / max(len(url), 1),
        "subdomain_count": max(len(domain_parts) - 2, 0),
        "has_ip": has_ip,
        "has_https": int(parsed.scheme.lower() == "https"),
        "has_at": int("@" in url),
        "has_double_slash": int("//" in path),
        "has_hyphen_domain": int("-" in domain),
        "has_suspicious_word": int(
            any(word in url.lower() for word in SUSPICIOUS_WORDS)
        ),
        "has_shortening_service": int(
            domain.lower() in SHORTENING_SERVICES
        ),
        "path_depth": len([p for p in path.split("/") if p]),
        "query_length": len(query),
        "fragment_length": len(fragment)
    }


def predict_url(url):
    features = extract_url_features(url)
    input_data = pd.DataFrame([features], columns=FEATURE_COLUMNS)

    prediction = int(model.predict(input_data)[0])
    probabilities = model.predict_proba(input_data)[0]

    index = list(model.classes_).index(prediction)
    confidence = float(probabilities[index])

    result = "Phishing" if prediction == 1 else "Legitimate"

    return result, confidence


def initialize_database():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL,
            checked_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


initialize_database()


def save_history(url, prediction, confidence):
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        INSERT INTO history
        (url, prediction, confidence, checked_at)
        VALUES (?, ?, ?, ?)
    """, (
        url,
        prediction,
        confidence,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None
    submitted_url = ""

    if request.method == "POST":
        submitted_url = request.form.get("url", "").strip()

        try:
            result, confidence = predict_url(submitted_url)
            save_history(submitted_url, result, confidence)

        except ValueError as error:
            flash(str(error), "error")

        except Exception as error:
            print("Prediction error:", error)
            flash("Unable to analyse this URL.", "error")

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        submitted_url=submitted_url
    )


@app.route("/history")
def history():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    records = connection.execute("""
        SELECT * FROM history ORDER BY id DESC
    """).fetchall()

    connection.close()

    return render_template("history.html", records=records)


@app.route("/analytics")
def analytics():
    connection = sqlite3.connect(DATABASE_PATH)

    total = connection.execute(
        "SELECT COUNT(*) FROM history"
    ).fetchone()[0]

    phishing = connection.execute(
        "SELECT COUNT(*) FROM history WHERE prediction='Phishing'"
    ).fetchone()[0]

    legitimate = connection.execute(
        "SELECT COUNT(*) FROM history WHERE prediction='Legitimate'"
    ).fetchone()[0]

    connection.close()

    return render_template(
        "analytics.html",
        total=total,
        phishing=phishing,
        legitimate=legitimate
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "running",
        "model": type(model).__name__,
        "feature_count": len(FEATURE_COLUMNS)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)
