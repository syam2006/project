import os
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Resolve path to model.pkl reliably
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
model = joblib.load(MODEL_PATH)

FEATURES = ["hours_studied", "attendance", "previous_marks"]
LIMITS = {"hours_studied": (0, 24), "attendance": (0, 100), "previous_marks": (0, 100)}


def validate(data):
    values = []
    for f in FEATURES:
        if f not in data or str(data[f]).strip() == "":
            raise ValueError(f"Missing field: {f}")
        try:
            v = float(data[f])
        except (TypeError, ValueError):
            raise ValueError(f"{f} must be a number")
        lo, hi = LIMITS[f]
        if not lo <= v <= hi:
            raise ValueError(f"{f} must be between {lo} and {hi}")
        values.append(v)
    return values


def predict(values):
    x = pd.DataFrame([values], columns=FEATURES)
    marks = float(model.predict(x)[0])
    return round(min(max(marks, 0), 100), 2)


@app.route("/")
def home():
    return render_template("index.html", result=None, error=None, form={})


@app.route("/health")
def health():
    return jsonify(status="ok", model="LinearRegression", features=FEATURES)


@app.route("/predict", methods=["POST"])
def predict_form():
    try:
        marks = predict(validate(request.form))
        return render_template("index.html", result=marks, error=None, form=request.form)
    except ValueError as e:
        return render_template("index.html", result=None, error=str(e), form=request.form), 400


@app.route("/api/predict", methods=["POST"])
def predict_api():
    try:
        return jsonify(predicted_marks=predict(validate(request.get_json(force=True))))
    except ValueError as e:
        return jsonify(error=str(e)), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
