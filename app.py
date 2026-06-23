from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

answers = {"1": None, "2": None, "3": None}
round_active = True


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/submit/<ipad>")
def submit(ipad):
    if ipad not in answers:
        return "Ungültiges iPad", 400
    return render_template("submit.html", ipad=ipad)


@app.route("/save", methods=["POST"])
def save():
    global round_active

    data = request.get_json()
    ipad = str(data.get("ipad"))
    answer = data.get("answer")

    if not round_active:
        return jsonify({"success": False, "msg": "Round over"})

    if answers[ipad] is not None:
        return jsonify({"success": False, "msg": "Already answered"})

    answers[ipad] = answer
    return jsonify({"success": True})


@app.route("/state")
def state():
    return jsonify({
        "answers": answers,
        "round_active": round_active
    })


@app.route("/reset", methods=["POST"])
def reset():
    global answers, round_active
    answers = {"1": None, "2": None, "3": None}
    round_active = True
    return jsonify({"success": True})


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
