# ScoreSense – Student Marks Prediction (MLOps System)

An end-to-end Machine Learning Operations (MLOps) project that demonstrates converting an exploratory Machine Learning Jupyter Notebook into a production-ready, modular, and containerized Flask web application, verified with unit testing, Dockerized via Gunicorn, and deployed to Amazon Web Services (AWS) EC2.


---

## 🌐 Live AWS EC2 Deployment Links

* **Live Web Application**: [http://13.51.194.56:5000](http://13.51.194.56:5000)
* **System Health Endpoint**: [http://13.51.194.56:5000/health](http://13.51.194.56:5000/health)
* **REST API Prediction**: `POST` to `http://13.51.194.56:5000/api/predict`
* **EC2 Instance**: `scoresense-server` (`i-0b95a75a4c6e3583`, Ubuntu Server LTS, AWS Region: Europe Stockholm `eu-north-1`)

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Technologies Used](#-technologies-used)
3. [Project Folder Structure](#-project-folder-structure)
4. [Installation & Setup](#-installation--setup)
5. [Local Execution Instructions](#-local-execution-instructions)
6. [Docker Build & Run](#-docker-build--run)
7. [API Documentation & Testing](#-api-documentation--testing)
8. [AWS EC2 Deployment Walkthrough](#-aws-ec2-deployment-walkthrough)
9. [GitHub Repository Setup & Push Guide](#-github-repository-setup--push-guide)

---

## 📖 Project Overview

ScoreSense predicts final student examination marks based on three key educational parameters:
1. **Hours Studied**: Daily average study duration (0–24 hrs).
2. **Attendance**: Classroom attendance percentage (0–100%).
3. **Previous Marks**: Baseline examination score (0–100%).

The system features:
* **Preprocessing & Training**: A reproducible pipeline using `StandardScaler` and `LinearRegression` trained on 500 student records ($R^2 \approx 0.948$, $\text{MAE} \approx 3.204$).
* **Serialized Model**: Exported as `model.pkl` for low-latency inference without retraining.
* **Web User Interface**: Clean, centered responsive card design with real-time feedback.
* **REST API**: Automated JSON endpoints for programmatic integration.
* **Automated Testing**: Comprehensive Pytest suite for API and input validation.

---

## 💻 Technologies Used

* **Programming Language**: Python 3.11
* **Machine Learning**: Scikit-Learn, NumPy, Pandas, Joblib
* **Web Framework**: Flask, Jinja2
* **WSGI Production Server**: Gunicorn
* **Testing**: Pytest
* **Containerization**: Docker
* **Frontend**: Semantic HTML5, Modern CSS3, JavaScript
* **Cloud Platform**: AWS EC2 (Ubuntu 22.04/24.04 LTS)

---

## 📂 Project Folder Structure

```text
scoresense-student-marks/
├── app.py                      # Flask web application and REST API endpoints
├── train_model.py              # Model training, evaluation, and serialization script
├── student_marks_model.ipynb   # Jupyter Notebook for exploratory data analysis
├── model.pkl                   # Trained model pipeline (StandardScaler + LinearRegression)
├── students.csv                # Generated synthetic student dataset (500 records)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container build instructions with Gunicorn
├── .dockerignore               # Files excluded from the Docker build context
├── .gitignore                  # Files and secrets excluded from Git tracking
├── README.md                   # Complete documentation
├── templates/
│   └── index.html              # HTML user interface with prediction form
├── static/
│   ├── style.css               # Card-based responsive CSS styling
│   └── js/
│       └── app.js              # Client-side input validation and submit controller
└── tests/
    └── test_app.py             # Automated unit and integration tests (pytest)
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Chari181112/mlops-project.git
cd mlops-project
```

### 2. Create and Activate a Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Local Execution Instructions

### Run the Flask Application
```bash
python app.py
```
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

### Run Automated Tests
```bash
python -m pytest -v
```

---

## 🐳 Docker Build & Run

### 1. Build the Docker Image
```bash
docker build -t scoresense:1.0 .
```

### 2. Verify the Image
```bash
docker images
```

### 3. Run the Container
```bash
docker run -d --name scoresense-app -p 5000:5000 scoresense:1.0
```

### 4. Verify Container Status & Logs
```bash
docker ps
docker logs scoresense-app
```

### 5. Access Containerized App
* Web UI: `http://localhost:5000`
* Health Check: `curl http://localhost:5000/health`

### 6. Stop and Clean Up
```bash
docker stop scoresense-app
docker rm -f scoresense-app
```

---

## 🛠️ API Documentation & Testing

### 1. Health Endpoint
* **URL**: `/health`
* **Method**: `GET`
* **Response**:
```json
{
  "features": ["hours_studied", "attendance", "previous_marks"],
  "model": "LinearRegression",
  "status": "ok"
}
```

### 2. Prediction API Endpoint
* **URL**: `/api/predict`
* **Method**: `POST`
* **Content-Type**: `application/json`

**Example Request Payload:**
```json
{
  "hours_studied": 6.0,
  "attendance": 85.0,
  "previous_marks": 70.0
}
```

**Example Successful Response (HTTP 200 OK):**
```json
{
  "predicted_marks": 70.3
}
```

**Example Error Response (HTTP 400 Bad Request):**
```json
{
  "error": "hours_studied must be between 0 and 24"
}
```

**Testing via cURL (Local or Remote AWS):**
```bash
# Local
curl -X POST http://127.0.0.1:5000/api/predict \
     -H "Content-Type: application/json" \
     -d "{\"hours_studied\": 6, \"attendance\": 85, \"previous_marks\": 70}"

# Remote AWS EC2 Deployment
curl -X POST http://13.51.194.56:5000/api/predict \
     -H "Content-Type: application/json" \
     -d "{\"hours_studied\": 6, \"attendance\": 85, \"previous_marks\": 70}"
```

**Testing via PowerShell:**
```powershell
$body = @{
    hours_studied = 6
    attendance = 85
    previous_marks = 70
} | ConvertTo-Json

# Local
Invoke-RestMethod -Uri "http://localhost:5000/api/predict" -Method Post -ContentType "application/json" -Body $body

# Remote AWS EC2 Deployment
Invoke-RestMethod -Uri "http://13.51.194.56:5000/api/predict" -Method Post -ContentType "application/json" -Body $body
```

---

## ☁️ AWS EC2 Deployment Walkthrough

1. **Launch EC2 Instance**:
   * Name: `scoresense-server`
   * AMI: Ubuntu Server 24.04 / 22.04 LTS
   * Instance Type: `t2.micro` or `t3.micro`
   * Key Pair: `scoresense-key.pem`
2. **Configure Security Group**:
   * Port `22` (SSH) — Remote administration.
   * Custom TCP Port `5000` (`0.0.0.0/0`) — Application web and API access.
3. **Connect & Setup Docker**:
   ```bash
   ssh -i "scoresense-key.pem" ubuntu@13.51.194.56
   sudo apt update && sudo apt install -y docker.io
   sudo systemctl enable --now docker
   sudo usermod -aG docker ubuntu
   ```
4. **Deploy Application**:
   * Transfer project files using `scp`:
     ```powershell
     scp -i "scoresense-key.pem" -r scoresense-student-marks ubuntu@13.51.194.56:/home/ubuntu/
     ```
   * Build the Docker image on the instance:
     ```bash
     cd ~/scoresense-student-marks
     sudo docker build -t scoresense:1.0 .
     ```
   * Run container:
     ```bash
     sudo docker run -d --name scoresense-app --restart unless-stopped -p 5000:5000 scoresense:1.0
     ```
5. **Verify Access**:
   * Web: `http://13.51.194.56:5000`
   * Health Check: `curl http://13.51.194.56:5000/health`

---

## 🐙 GitHub Repository Setup & Push Guide

To push this repository to GitHub under `Chari181112/mlops-project`:

```powershell
# 1. Initialize Git in the project root (if not already done)
git init

# 2. Add all tracked project files
git add .

# 3. Commit the changes
git commit -m "Complete ScoreSense MLOps project: Flask UI, model.pkl, Docker, and AWS EC2 deployment"

# 4. Set the default branch to main
git branch -M main

# 5. Link to your GitHub remote repository
git remote set-url origin https://github.com/Chari181112/mlops-project.git

# 6. Push to GitHub
git push -u origin main
```

---

## 📄 License
This project is open-source and available for educational and academic use.
