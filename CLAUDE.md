# CLAUDE.md

## Project Overview

Catan Dice is a Flask web application that serves as a digital dice roller for Catan board game sessions. It provides a mobile-friendly web UI with animated dice, game session tracking, roll statistics with probability distribution charts, robber (7) alerts, and optional Cities & Knights event die support.

## Repository Structure

```
Catan_Dice/
├── app.py                  # Flask application — routes, session logic, game state
├── templates/
│   └── index.html          # Single-page web UI (HTML + CSS + JS, no build step)
├── README.md               # Project readme
└── CLAUDE.md               # This file
```

## Tech Stack

- **Language**: Python (backend), vanilla JavaScript (frontend)
- **Framework**: Flask with server-side sessions
- **Dependencies**: Flask (external), random + os (stdlib)
- **Frontend**: Single HTML file with embedded CSS and JS — no build system or npm
- **No database** — game state lives in Flask's cookie-based session

## Running the Application

```bash
# Install dependency
pip install flask

# Start the dev server (runs on http://127.0.0.1:5000 with debug mode)
python app.py
```

Then open `http://127.0.0.1:5000` in a browser.

Set the `SECRET_KEY` environment variable for production; otherwise a random key is generated on each restart (which invalidates existing sessions).

## API Endpoints

| Method | Path          | Description                                          |
|--------|---------------|------------------------------------------------------|
| GET    | `/`           | Serve the web UI                                     |
| POST   | `/roll`       | Roll two 6-sided dice; returns JSON with session data|
| POST   | `/roll/event` | Roll 2d6 + Cities & Knights event die                |
| GET    | `/stats`      | Get full session statistics and roll history          |
| POST   | `/reset`      | Clear the current game session                       |

**Example `/roll` response:**
```json
{
  "die1": 3,
  "die2": 5,
  "total": 8,
  "roll_number": 12,
  "sevens": 2,
  "distribution": {"2": 1, "3": 0, "4": 2, ...}
}
```

**Example `/roll/event` response** (adds event die fields):
```json
{
  "die1": 4,
  "die2": 3,
  "total": 7,
  "event_symbol": "barbarian",
  "event_label": "Barbarian Ship",
  "roll_number": 13,
  "sevens": 3,
  "distribution": {"2": 1, "3": 0, ...}
}
```

## Features

- **Animated dice** with Unicode die faces and roll animation
- **Robber alert** — flashing red banner when a 7 is rolled
- **Live statistics** — roll count, seven count, seven rate vs expected 16.7%
- **Distribution chart** — bar chart of actual rolls vs theoretical 2d6 probability curve
- **Cities & Knights event die** — toggle to include barbarian/trade/politics/science results
- **Roll history** — scrollable log of all rolls in the current session
- **Keyboard shortcut** — press Space or Enter to roll
- **Mobile-friendly** — responsive design that works on phones and tablets
- **New Game** button to reset all session data

## Development Notes

- **No tests exist** — there is no test suite or testing framework configured.
- **No requirements.txt** — Flask must be installed manually.
- **No .gitignore** — none has been created yet.
- **Debug mode is on** — `app.run(debug=True)` in `app.py`. Disable for production.
- **Session storage** — Flask's default cookie-based sessions. Session data (roll history, distribution) is stored client-side in a signed cookie. For very long games the cookie may approach browser size limits.

## Code Conventions

- Single-file Flask backend with the app instance at module level (`app.py:5`).
- Route handlers return `jsonify()` responses.
- Standard library imports are separated from third-party imports.
- 4-space indentation (Python standard).
- Frontend is a single self-contained HTML file — no external JS/CSS dependencies.
- CSS uses custom properties (CSS variables) for the Catan-themed color palette.
- JavaScript uses `async/await` with `fetch()` for API calls.

## Key Architecture Decisions

- **Server-side roll generation** — dice use `random.randint(1, 6)` on the server for fairness; the client only displays results.
- **Session-based game state** — all game data (history, distribution, counts) is stored in Flask sessions so each browser gets independent game state with no database required.
- **Cities & Knights event die** — modeled as a weighted list (3 barbarian, 1 trade, 1 politics, 1 science) matching the physical die.
- **No SPA framework** — vanilla JS keeps the stack simple and the page fast to load.
- **Probability reference** — the expected 2d6 distribution is hardcoded in both Python (for `/stats`) and JS (for the chart) to show players how their rolls compare to theory.
