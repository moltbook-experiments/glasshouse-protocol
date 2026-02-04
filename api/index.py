from backend.app.main import app

# Vercel looks for a variable named 'app' (or 'handler') in this file.
# By importing 'app' from main.py, we expose the FastAPI application to Vercel.
