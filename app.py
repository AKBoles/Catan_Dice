from flask import Flask, render_template, jsonify, send_from_directory

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/index")
@app.route("/index.html")
def index_alt():
    return render_template("index.html")

@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name": "Catan Roller",
        "short_name": "Catan",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1a0f0a",
        "theme_color": "#2c1810",
        "description": "Dice roller & stats tracker for Settlers of Catan",
        "icons": [
            {"src": "/static/icon.svg", "sizes": "192x192", "type": "image/svg+xml"},
            {"src": "/static/icon.svg", "sizes": "512x512", "type": "image/svg+xml"}
        ]
    })

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "app": "Catan Roller"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
