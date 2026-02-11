from flask import Flask, jsonify, render_template, session
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Theoretical probability distribution for 2d6 (as percentages)
EXPECTED_DISTRIBUTION = {
    2: 2.78, 3: 5.56, 4: 8.33, 5: 11.11, 6: 13.89,
    7: 16.67, 8: 13.89, 9: 11.11, 10: 8.33, 11: 5.56, 12: 2.78,
}

CITIES_KNIGHTS_EVENTS = [
    {"symbol": "barbarian", "label": "Barbarian Ship"},
    {"symbol": "barbarian", "label": "Barbarian Ship"},
    {"symbol": "barbarian", "label": "Barbarian Ship"},
    {"symbol": "trade", "label": "Trade"},
    {"symbol": "politics", "label": "Politics"},
    {"symbol": "science", "label": "Science"},
]


def _init_session():
    """Initialize game session data if not present."""
    if "history" not in session:
        session["history"] = []
        session["distribution"] = {str(k): 0 for k in range(2, 13)}
        session["sevens"] = 0
        session["roll_count"] = 0


@app.route("/")
def index():
    _init_session()
    return render_template("index.html")


@app.route("/roll", methods=["POST"])
def roll_dice():
    _init_session()
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    total = die1 + die2

    session["roll_count"] += 1
    session["distribution"][str(total)] += 1
    if total == 7:
        session["sevens"] += 1

    roll_entry = {
        "roll_number": session["roll_count"],
        "die1": die1,
        "die2": die2,
        "total": total,
    }
    session["history"].append(roll_entry)
    session.modified = True

    return jsonify({
        "die1": die1,
        "die2": die2,
        "total": total,
        "roll_number": session["roll_count"],
        "sevens": session["sevens"],
        "distribution": session["distribution"],
    })


@app.route("/roll/event", methods=["POST"])
def roll_with_event():
    """Roll 2d6 plus the Cities & Knights event die."""
    _init_session()
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    total = die1 + die2

    event = random.choice(CITIES_KNIGHTS_EVENTS)

    session["roll_count"] += 1
    session["distribution"][str(total)] += 1
    if total == 7:
        session["sevens"] += 1

    roll_entry = {
        "roll_number": session["roll_count"],
        "die1": die1,
        "die2": die2,
        "total": total,
        "event": event["label"],
    }
    session["history"].append(roll_entry)
    session.modified = True

    return jsonify({
        "die1": die1,
        "die2": die2,
        "total": total,
        "event_symbol": event["symbol"],
        "event_label": event["label"],
        "roll_number": session["roll_count"],
        "sevens": session["sevens"],
        "distribution": session["distribution"],
    })


@app.route("/stats", methods=["GET"])
def stats():
    """Return current game session statistics."""
    _init_session()
    dist = session["distribution"]
    roll_count = session["roll_count"]
    actual_pct = {}
    for k, v in dist.items():
        actual_pct[k] = round((v / roll_count) * 100, 2) if roll_count > 0 else 0

    return jsonify({
        "roll_count": roll_count,
        "sevens": session["sevens"],
        "distribution": dist,
        "actual_percentages": actual_pct,
        "expected_percentages": {str(k): v for k, v in EXPECTED_DISTRIBUTION.items()},
        "history": session["history"],
    })


@app.route("/reset", methods=["POST"])
def reset():
    """Reset the current game session."""
    session.clear()
    _init_session()
    return jsonify({"status": "ok", "message": "Game reset"})


if __name__ == "__main__":
    app.run(debug=True)
