from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Speichert Antworten (einfach, aber ok für Schulprojekt)
answers = {
    "1": "",
    "2": "",
    "3": ""
}

# -------------------------
# DASHBOARD (Anzeige)
# -------------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# -------------------------
# INPUT SEITE (iPads)
# -------------------------
@app.route("/submit/<ipad>")
def submit(ipad):
    # Schutz: nur 1,2,3 erlaubt
    if ipad not in answers:
        return "Ungültiges iPad", 400

    return render_template("submit.html", ipad=ipad)


# -------------------------
# SPEICHERN DER ANTWORT
# -------------------------
@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data"}), 400

    ipad = str(data.get("ipad", ""))
    text = data.get("text", "")

    if ipad not in answers:
        return jsonify({"success": False, "error": "Invalid ipad"}), 400

    answers[ipad] = text

    return jsonify({"success": True})


# -------------------------
# LIVE DATEN FÜR DASHBOARD
# -------------------------
@app.route("/answers")
def get_answers():
    return jsonify(answers)


# -------------------------
# HEALTH CHECK (wichtig für Render)
# -------------------------
@app.route("/health")
def health():
    return "OK", 200


# -------------------------
# LOCAL RUN (nur zuhause)
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)