from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

answers = {
    "1": "",
    "2": "",
    "3": ""
}

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/submit/<ipad>")
def submit(ipad):
    return render_template("submit.html", ipad=ipad)

@app.route("/save", methods=["POST"])
def save():

    data = request.get_json()

    ipad = data["ipad"]
    text = data["text"]

    answers[ipad] = text

    return jsonify({"success": True})

@app.route("/answers")
def get_answers():
    return jsonify(answers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)