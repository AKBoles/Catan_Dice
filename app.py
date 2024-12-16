from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/roll', methods=['GET'])
def roll_dice():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    total = die1 + die2
    return jsonify({
        "Die 1": die1,
        "Die 2": die2,
        "Total": total
    })

if __name__ == '__main__':
    app.run(debug=True)

