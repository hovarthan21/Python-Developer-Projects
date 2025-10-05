from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

game_state = {
    "number": random.randint(1, 100),
    "attempts": 0,
    "mode": "single" 
}

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/check_guess', methods=['POST'])
def check_guess():
    data = request.json
    user_guess = int(data['guess'])
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    user_guess = int(data["guess"])
    game_state["attempts"] += 1

    if user_guess == game_state["number"]:
        message = "🎉 Correct! You guessed the number."
        status = "win"
    elif user_guess < game_state["number"]:
        message = "⬆️ Try higher!"
        status = "low"
    else:
        message = "⬇️ Try lower!"
        status = "high"

    return jsonify({
        "message": message,
        "status": status,
        "attempts": game_state["attempts"]
    })

@app.route("/restart", methods=["POST"])
def restart():
    if game_state["mode"] == "single":
        game_state["number"] = random.randint(1, 100)
    else:
        game_state["number"] = None
    game_state["attempts"] = 0
    return jsonify({"message": "Game restarted!"})

@app.route("/set_number", methods=["POST"])
def set_number():
    data = request.get_json()
    game_state["number"] = int(data["number"])
    game_state["attempts"] = 0
    game_state["mode"] = "two-player"
    return jsonify({"message": "Number set for two-player mode!"})

@app.route("/mode", methods=["POST"])
def mode():
    data = request.get_json()
    if data["mode"] == "single":
        game_state["mode"] = "single"
        game_state["number"] = random.randint(1, 100)
        game_state["attempts"] = 0
    else:
        game_state["mode"] = "two-player"
        game_state["number"] = None
        game_state["attempts"] = 0
    return jsonify({"message": f"Mode set to {game_state['mode']}"})

if __name__ == "__main__":
    app.run(debug=True)
