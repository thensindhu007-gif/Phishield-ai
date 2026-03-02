from flask import Flask, request, jsonify, send_from_directory
import re
import os

app = Flask(__name__)

# Suspicious keywords list
suspicious_keywords = [
    "urgent", "click here", "verify", "password",
    "bank", "account suspended", "lottery",
    "prize", "win", "free", "otp", "update",
    "login", "limited time", "immediately"
]

def analyze_email(email_text):
    score = 0
    found_keywords = []
    email_lower = email_text.lower()

    # Check suspicious keywords
    for word in suspicious_keywords:
        if word in email_lower:
            score += 10
            found_keywords.append(word)

    # Check suspicious links
    if re.search(r"http[s]?://", email_text):
        score += 20
        found_keywords.append("Suspicious Link")

    if score > 100:
        score = 100

    # Risk classification
    if score >= 70:
        risk_level = "High"
    elif score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "suspicious_keywords": found_keywords
    }

@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/style.css")
def serve_css():
    return send_from_directory(os.getcwd(), "style.css")

@app.route("/script.js")
def serve_js():
    return send_from_directory(os.getcwd(), "script.js")

@app.route("/analyze", methods=["POST"])
def analyze():
    email_text = request.json["email_text"]
    result = analyze_email(email_text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)