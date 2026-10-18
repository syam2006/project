import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

client = app.test_client()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.get_json()["status"] == "ok"


def test_home_page():
    assert client.get("/").status_code == 200


def test_prediction_in_range():
    r = client.post("/api/predict", json={"hours_studied": 6, "attendance": 85, "previous_marks": 70})
    assert r.status_code == 200
    assert 0 <= r.get_json()["predicted_marks"] <= 100


def test_more_study_gives_higher_marks():
    low = client.post("/api/predict", json={"hours_studied": 1, "attendance": 70, "previous_marks": 60}).get_json()
    high = client.post("/api/predict", json={"hours_studied": 9, "attendance": 70, "previous_marks": 60}).get_json()
    assert high["predicted_marks"] > low["predicted_marks"]


def test_invalid_input():
    r = client.post("/api/predict", json={"hours_studied": "abc", "attendance": 80, "previous_marks": 60})
    assert r.status_code == 400
