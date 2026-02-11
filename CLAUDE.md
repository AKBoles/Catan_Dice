# CLAUDE.md

## Project Overview

Catan Dice is a minimal Flask web application that simulates rolling two six-sided dice, themed around the board game Catan. It exposes a single REST endpoint that returns dice roll results as JSON.

## Repository Structure

```
Catan_Dice/
├── app.py          # Main Flask application (single entry point)
├── README.md       # Project readme (title only)
└── CLAUDE.md       # This file
```

## Tech Stack

- **Language**: Python
- **Framework**: Flask
- **Dependencies**: Flask (external), random (stdlib)
- **No build system** — run directly with Python

## Running the Application

```bash
# Install dependency (no requirements.txt exists yet)
pip install flask

# Start the dev server (runs on http://127.0.0.1:5000 with debug mode)
python app.py
```

## API Endpoints

| Method | Path    | Description                                      |
|--------|---------|--------------------------------------------------|
| GET    | `/roll` | Roll two 6-sided dice; returns JSON with results |

**Example response:**
```json
{
  "Die 1": 3,
  "Die 2": 5,
  "Total": 8
}
```

## Development Notes

- **No tests exist** — there is no test suite or testing framework configured.
- **No requirements.txt** — Flask must be installed manually.
- **No .gitignore** — none has been created yet.
- **Debug mode is on** — `app.run(debug=True)` in `app.py:18`. This should be disabled for production.

## Code Conventions

- Single-file Flask app pattern with the app instance at module level (`app.py:4`).
- Route handlers return `jsonify()` responses.
- Standard library imports are separated from third-party imports.
- 4-space indentation (Python standard).

## Key Architecture Decisions

- The app is intentionally minimal — one file, one endpoint, no database.
- Dice rolls use `random.randint(1, 6)` for each die, with the sum computed server-side.
- JSON keys use display-friendly names with spaces ("Die 1", "Die 2", "Total").
