from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# -----------------------------
# SPIEL ZUSTAND
# -----------------------------
answers = {
    "1": None,
    "2": None,
    "3": None
}

scores = {
    "1": 0,
    "2": 0,
    "3": 0
}

correct_answer = None
round_active = True


# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        scores=scores
    )


# -----------------------------
# IPAD SEITE
# -----------------------------
@app.route("/submit/<ipad>")
def submit(ipad):
    if ipad not in answers:
        return "Ungültiges iPad", 400

    return render_template("submit.html", ipad=ipad)


# -----------------------------
# ANTWORT SPEICHERN (BUZZER LOGIK)
# -----------------------------
@app.route("/save", methods=["POST"])
def save():
    global round_active

    data = request.get_json()
    ipad = str(data.get("ipad"))
    answer = data.get("answer")

    if ipad not in answers:
        return jsonify({"success": False, "error": "Invalid iPad"}), 400

    # nur erste Antwort zählt
    if answers[ipad] is not None:
        return jsonify({"success": False, "message": "Already answered"}), 200

    if not round_active:
        return jsonify({"success": False, "message": "Round finished"}), 200

    answers[ipad] = answer

    # wenn richtige Antwort gesetzt ist
    if correct_answer and answer == correct_answer:
        scores[ipad] += 1
        round_active = False  # Runde sofort beenden (schnellste gewinnt)

    return jsonify({"success": True})


# -----------------------------
# NEUE RUNDE STARTEN
# -----------------------------
@app.route("/next_round", methods=["POST"])
def next_round():
    global answers, round_active, correct_answer

    data = request.get_json()
    correct_answer = data.get("correct")

    answers = {"1": None, "2": None, "3": None}
    round_active = True

    return jsonify({"success": True})


# -----------------------------
# DASHBOARD DATEN
# -----------------------------
@app.route("/state")
def state():
    return jsonify({
        "answers": answers,
        "scores": scores,
        "round_active": round_active
    })


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
