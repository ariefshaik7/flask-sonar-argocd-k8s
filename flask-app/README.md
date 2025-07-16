# 📝 Flask To-Do List App

A simple To-Do list web application built using:

- Flask REST API (Backend)
- HTML + JavaScript + Bootstrap (Frontend)
- Pytest for unit testing

---

##  Features

-  Add and delete tasks
-  REST API (`/tasks`, `/tasks/<id>`)
-  Dynamic frontend using `fetch()`
-  In-memory task storage
-  Pytest for test automation

---

##  Project Structure

```
flask-todo-app/
├── app.py               # Flask app
├── test_app.py          # Unit tests
├── requirements.txt     # Python dependencies
└── static/
    └── index.html       # Frontend (HTML + JS)
```

---

##  How to Run (Step-by-Step)

### 1. Clone the Project

```bash
git clone <your-repo-url>
cd flask-todo-app
```

### 2. Create & Activate Virtual Environment

```bash
# Create venv (Linux/macOS)
python3 -m venv venv
source venv/bin/activate

# OR (Windows)
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Run Tests

```bash
pytest test_app.py
```

---

##  API Endpoints

| Method | URL            | Description          |
|--------|----------------|----------------------|
| GET    | `/tasks`       | Get all tasks        |
| POST   | `/tasks`       | Add a task (JSON)    |
| DELETE | `/tasks/<id>`  | Delete task by index |

Sample `POST` body:
```json
{
  "task": "Buy groceries"
}
```

---

##  Dependencies

From `requirements.txt`:
```
Flask==2.3.3
flask-cors
pytest==8.4.1
```

---

##  Run with Docker

### 1. Build Docker Image

```bash
docker build -t flask-todo-app .
```

### 2. Run Docker Container

```bash
docker run -p 5000:5000 flask-todo-app
```

> This maps container port `5000` to your local `localhost:5000`.  
> Now open [http://localhost:5000](http://localhost:5000) in your browser.

### 3. Stop the Container

Find the container ID:

```bash
docker ps
```

Then stop it:

```bash
docker stop <container_id>
```

---

## Note

- Tasks are not persisted (in-memory only).
