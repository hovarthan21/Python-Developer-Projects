from flask import Flask, render_template, request, redirect, url_for, session
import requests, csv, os
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "supersecretkey" 

LOG_FILE = "logs/conversions.csv"

def get_symbols():
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url).json()
    if "rates" not in response:
        return {"USD": "US Dollar"}
    return {code: code for code in response["rates"].keys()}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["country"] = request.form["country"]
        session["age"] = request.form["age"]
        return redirect(url_for("converter"))
    return render_template("login.html")

@app.route("/converter", methods=["GET", "POST"])
def converter():
    if "name" not in session:
        return redirect(url_for("login"))

    symbols = get_symbols()
    result = None
    if request.method == "POST":
        amount = float(request.form["amount"])
        from_curr = request.form["from"]
        to_curr = request.form["to"]

        url = f"https://open.er-api.com/v6/latest/{from_curr}"
        data = requests.get(url).json()

        if "rates" in data:
            rate = data["rates"].get(to_curr, None)
            if rate:
                result = amount * rate

                os.makedirs("logs", exist_ok=True)
                with open(LOG_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        session["name"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        amount, from_curr, to_curr, result
                    ])

    return render_template("converter.html", symbols=symbols, result=result, username=session["name"])

@app.route("/analysis")
def analysis():
    if "name" not in session:
        return redirect(url_for("login"))

    history = []
    totals = defaultdict(float)
    cutoff = datetime.now() - timedelta(days=7)

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 6:
                    continue
                user, dt_str, amt, from_curr, to_curr, result = row
                if user == session["name"]:
                    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                    if dt >= cutoff:
                        history.append(row)
                        totals[to_curr] += float(result)

    return render_template("analysis.html", history=history, totals=totals, username=session["name"])

if __name__ == "__main__":
    app.run(debug=True)
