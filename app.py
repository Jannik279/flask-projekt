from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

answers = {"1": None, "2": None, "3": None}
answer_order = []
round_id = 0  # 👈 NEU


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
    global answer_order

    data = request.get_json()
    ipad = str(data.get("ipad"))
    answer = data.get("answer")

    if answers[ipad] is not None:
        return jsonify({"success": False})

    answers[ipad] = answer
    answer_order.append(ipad)

    return jsonify({"success": True})


@app.route("/state")
def state():
    return jsonify({
        "answers": answers,
        "order": answer_order,
        "round_id": round_id   # 👈 WICHTIG
    })


@app.route("/reset", methods=["POST"])
def reset():
    global answers, answer_order, round_id

    answers = {"1": None, "2": None, "3": None}
    answer_order = []
    round_id += 1   # 👈 neue Runde!

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
