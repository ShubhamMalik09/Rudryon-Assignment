# 🚀 Real-Time Sensor Monitoring System

A full-stack application that simulates sensor data, processes it in real-time, and provides both REST APIs and live WebSocket streams for monitoring via an interactive dashboard.

---

## 🧠 Overview

This system models a real-world scenario where multiple sensors continuously generate temperature data. The backend ingests, processes, and stores this data, while the frontend visualizes it in real-time with alerts and anomaly detection.

---

## ⚙️ Tech Stack

### 🔹 Backend

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic v2
* WebSockets
* Asyncio (background processing)

### 🔹 Frontend

* React
* Tailwind CSS
* WebSocket API
* Fetch (for REST APIs)

---

## 📊 Features

### ✅ Sensor Simulation

* 3 sensors generating temperature readings every **20–30 seconds**
* Temperature range: **20°C – 95°C**
* Random spikes to simulate abnormal conditions

---

### ✅ Real-Time Dashboard

* Live updates using WebSockets
* Auto-refresh every few seconds
* No manual reload required

---

### ✅ Color-Coded Sensor Status

| Range      | Status              |
| ---------- | ------------------- |
| Below 70°C | 🟢 Green (Normal)   |
| 70–80°C    | 🟡 Yellow (Warning) |
| Above 80°C | 🔴 Red (Critical)   |

---

### ✅ Alerts System

* Automatically detects readings above **80°C**
* Displays alerts in real-time

---

### ✅ Anomaly Detection

A reading is flagged as anomaly if:

> Temperature > 15% increase from its 1-hour rolling average

* Highlighted with a badge on the dashboard
* Helps identify unusual spikes

---

### ✅ REST APIs

| Endpoint                     | Description                                 |
| ---------------------------- | ------------------------------------------- |
| `GET /sensors`               | Fetch all sensors                           |
| `GET /sensors/{id}/readings` | Fetch readings (supports `limit` & `order`) |
| `GET /sensors/alerts`        | Fetch high temperature readings             |

---

### ✅ WebSocket APIs

| Endpoint                    | Description              |
| --------------------------- | ------------------------ |
| `/ws/sensors`               | Live sensors data        |
| `/ws/sensors/{id}/readings` | Live readings per sensor |
| `/ws/sensors/alerts`        | Live alerts stream       |

---

### ✅ Auto Seeding

* Sensors are automatically created if not present in DB
* Ensures system works without manual setup

---

### ✅ Background Processing

* Uses FastAPI **lifespan events**
* Continuously generates sensor readings
* Fully integrated into backend (no external workers)

---

## 🚀 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd project
```

---

## 🔧 Backend Setup

```bash
cd backend
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create `.env`

```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

### Run backend

```bash
uvicorn main:app --reload
```

---

## 💻 Frontend Setup

```bash
cd frontend
```

### Install dependencies

```bash
npm install
```

### Create `.env`

```env
VITE_BACKEND_URL = http://localhost:8000
VITE_BACKEND_WS_URL = ws://localhost:8000
```

### Run frontend

```bash
npm start
```

---

## 🌐 Access Application

* Backend: http://127.0.0.1:8000
* Swagger Docs: http://127.0.0.1:8000/docs
* Frontend: http://localhost:5173

---

## 🔌 WebSocket Testing (Optional)

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/sensors/alerts");

ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

---

## ⚡ Approach

* Designed a **layered backend architecture** (routes → service → database)
* Used **Pydantic schemas** for validation and serialization
* Implemented **real-time streaming using WebSockets**
* Built a **reactive frontend** that updates automatically
* Added **anomaly detection logic** for intelligent monitoring
* Ensured **clean, scalable, and maintainable code**

---

## 📈 Scalability Considerations

* Replace asyncio with **Celery + Redis** for distributed workloads
* Add **database indexing** for faster queries
* Introduce **caching layer (Redis)**
* Containerize using **Docker**

---

## 💡 Future Improvements

* Authentication & user roles
* Historical analytics dashboard
* Pagination & filtering
* Deployment (AWS / Docker)
* Monitoring & logging

---

## 🏁 Conclusion

This project demonstrates:

* Real-time system design
* Full-stack integration
* Clean backend architecture
* Efficient data processing

---

## 🔗 Submission

GitHub Repo: `https://github.com/ShubhamMalik09/Sensors_Monitoring_WebSockets`

---

⭐ Feel free to explore and improve!
