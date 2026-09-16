# USTH Room Rental Finder Platform

A web-based accommodation search platform built with **Python (Flask)**, **SQLite**, and **Bootstrap 5**.

Repository: https://github.com/dungnt2410232/Room-Rental

---

## ⚠️ ATTENTION

- **NEVER** commit or push directly to `main`.
- Always pull the latest code before working:
  ```bash
  git checkout main
  git pull origin main
  ```
- Create and switch to your assigned feature branch:
  ```bash
  git checkout -b feature/<branch-name>
  ```
- Only commit your work to your own branch.
- Submit a **Pull Request (PR)** on GitHub when your feature is ready for review.

---

## 🚀 Setup & Run Instructions

### 1. Clone the repository
```bash
git clone [https://github.com/dungnt2410232/Room-Rental.git](https://github.com/dungnt2410232/Room-Rental.git)
cd Room-Rental
```

### 2. Create and activate a virtual environment
- **Windows (Git Bash):**
  ```bash
  python -m venv venv
  source venv/Scripts/activate
  ```
- **Windows (PowerShell / Command Prompt):**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Seed demo data
```bash
python seed.py
```

### 5. Run the web application
```bash
python app.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

