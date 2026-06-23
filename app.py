from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

answers = {"1": None, "2": None, "3": None}
answer_order = []
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
    global round_active, answer_order

    data = request.get_json()
    ipad = str(data.get("ipad"))
    answer = data.get("answer")

    if not round_active:
        return jsonify({"success": False, "msg": "Runde beendet"})

    if answers[ipad] is not None:
        return jsonify({"success": False, "msg": "Schon geantwortet"})

    answers[ipad] = {
        "answer": answer,
        "time": time.time()
    }

    answer_order.append(ipad)

    return jsonify({"success": True})


@app.route("/state")
def state():
    return jsonify({
        "answers": answers,
        "order": answer_order,
        "round_active": round_active
    })


@app.route("/reset", methods=["POST"])
def reset():
    global answers, answer_order, round_active
    answers = {"1": None, "2": None, "3": None}
    answer_order = []
    round_active = True
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
