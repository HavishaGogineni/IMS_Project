#Incident Management System (IMS)

##Overview

This project is a simple Incident Management System built using FastAPI (backend) and HTML/JavaScript (frontend). It helps in sending, storing, and managing system signals (incidents).

---

##Tech Stack

* Backend: FastAPI (Python)
* Frontend: HTML, JavaScript
* Storage: File-based (signals.log)

---

##Features

* Send system signals
* Auto-generate Incident IDs (INC-1, INC-2...)
* View all incidents
* Filter HIGH severity signals
* Update incident status
* Add Root Cause Analysis (RCA)

---

##How to Run

###Backend

Run this command:

```
uvicorn main:app --reload
```

---

### Frontend

Run this command:

```
python -m http.server 5500
```

Then open in browser:

```
http://127.0.0.1:5500
```

---

## 📡 API Endpoints

* POST /signal
* GET /signals
* GET /signals/high
* PUT /signal/{id}
* GET /health

---

## project Structure

```
main.py
index.html
signals.log
README.md



```
Author

This project was built as part of an internship assignment.

---


