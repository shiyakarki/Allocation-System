# 🏥 Hospital Triage & Doctor Allocation System

[![Live Demo](https://img.shields.io/badge/Live-Demo_on_Render-2ea44f?style=for-the-badge&logo=render)](https://allocation-system-j1bc.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An intelligent, real-time emergency triage and doctor resource allocation dashboard built in Python. Designed to reduce emergency department bottlenecks by dynamically prioritizing high-acuity patients and matching them to available medical specialists.

🔗 **Live Deployment:** [https://allocation-system-j1bc.onrender.com](https://allocation-system-j1bc.onrender.com)

---

## 📌 Problem Overview

In high-volume hospital emergency rooms, manual triage and resource dispatching often lead to:
- Delays in treating critical patients during surge hours.
- Misallocation of general physicians to cardiac/trauma emergencies (or vice versa).
- Inefficient doctor utilization due to lack of visibility into real-time bed and consultation turnover.

This system automates patient acuity ranking, doctor-patient matching, and consultation lifecycle tracking.

---

## ✨ Key Features

- **Automated Acuity Triage**: Classifies patients into Critical (Priority 1), Urgent (Priority 2), and Routine (Priority 3) based on clinical presentation.
- **Specialty-Aware Matching**: Directs cardiac cases to Cardiologists, severe trauma to Emergency specialists, and general complaints to General Physicians.
- **Emergency Fallback Protocol**: If a dedicated specialist is occupied, critical (Priority 1) patients are automatically rerouted to Emergency doctors for immediate stabilization.
- **Consultation Lifecycle Management**: Tracks each patient from `Waiting` ➔ `Under Treatment` ➔ `Discharged`, instantly freeing doctors to take the next prioritized patient.
- **Live Hospital Dashboard**: Visual KPI cards displaying waiting count, critical patients in queue, and real-time doctor availability.

---



## 🛠️ Tech Stack

- **Frontend & Web Framework:** [Streamlit](https://streamlit.io/)
- **Data Processing:** [Pandas](https://pandas.pydata.org/)
- **Core Language:** Python 3.10+
- **Hosting & Cloud Deployment:** [Render](https://render.com/) (Web Service)

---

## 📂 Repository Structure

```text
Allocation-System/
├── app.py              # Main Streamlit web application & triage logic
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

---

## 🚀 Local Installation & Setup

To run this dashboard locally on your machine:

### 1. Clone the repository
```bash
git clone https://github.com/shiyakarki/Allocation-System.git
cd Allocation-System
```

### 2. Create and activate a virtual environment (Recommended)
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt / PowerShell)
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application
```bash
streamlit run app.py
```
Your default browser will automatically open the app at `http://localhost:8501`.

---

## ☁️ Deployment on Render

This project is deployed as a **Python Web Service** on Render.

| Setting | Configuration Value |
| :--- | :--- |
| **Service Type** | **Web Service** |
| **Environment / Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |

> **Note:** The `--server.port $PORT --server.address 0.0.0.0` flags ensure Streamlit binds dynamically to Render's exposed cloud port.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
