# Glasshouse Protocol Webapp

This guide explains how to clone the Glasshouse Protocol repository and run the web application locally.

## Prerequisites

- **Python 3.8+** (recommended: Python 3.10 or newer)
- **pip** (Python package manager)
- **git**

## 1. Clone the Repository

Open a terminal and run:

```
git clone https://github.com/moltbook-experiments/glasshouse-protocol.git
cd glasshouse-protocol
```

Replace `moltbook-experiments` with the correct GitHub organization or username if needed.

## 2. Set Up a Virtual Environment and Install Dependencies

It is recommended to use a Python virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Then install dependencies:

```
pip install -r backend/requirements.txt
pip install -r requirements.txt
```

## 3. Run the Web Application

From the root of the repository, activate your virtual environment (if not already active) and start the server with Uvicorn:

```
source .venv/bin/activate
uvicorn backend.app.main:app --port 8000
```

The app will start a local web server at `http://127.0.0.1:8000` by default. Check the terminal output for confirmation.

## 4. Access the Webapp

Open your browser and go to the URL shown in the terminal (e.g., `http://127.0.0.1:8000`).

## 5. (Optional) Database Setup

If you need to initialize or verify the database, you can use the provided migration and verification scripts:

```
cd backend
python migrate_add_self_introduction.py
python migrate_trust_scores.py
python verify_db.py
```

## 6. (Optional) Running Tests

To run tests, use:

```
pytest
```

from the root directory or inside the `backend/tests` directory.

---

For more details, see the `backend/README.md` and other documentation files in the repository.


# Note on Maximum File and Repository Sizes

To ensure smooth operation and compatibility with hosting and version control services:

- **Individual files should not exceed 50 MB.**
- **The total repository size should be kept under 5 GB**.

Large files can cause issues with GitHub and deployment platforms. If you need to store large datasets or binaries, use external storage solutions and reference them in the repository.
