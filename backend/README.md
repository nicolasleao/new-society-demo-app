# Calory Tracker Backend

A simple FastAPI backend for tracking meals and macronutrients.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your PostgreSQL connection details
```

3. Initialize the database:
```bash
python init_db.py
```

4. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /meals` - Create a new meal
- `GET /meals/{username}` - Get meals for a user (supports date filtering)
- `DELETE /meals/{meal_id}` - Delete a meal (soft delete)
- `GET /stats/{username}` - Get aggregated stats for a user
- `GET /stats/{username}/today` - Get today's stats for a user

## API Documentation

Interactive API docs are available at `http://localhost:8000/docs`