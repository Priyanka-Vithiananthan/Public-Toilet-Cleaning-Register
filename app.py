from flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime

app = Flask(__name__)

CSV_FILE = "toilet_data.csv"


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/complaint")
def complaint():
    return render_template("complaint.html")


@app.route("/submit_complaint", methods=["POST"])
def submit_complaint():

    df = pd.read_csv(CSV_FILE)

    new_id = len(df) + 1

    new_record = {
        "record_id": new_id,
        "block_id": "B" + str(new_id).zfill(3),
        "location": request.form["location"],
        "cleaning_date": datetime.now().strftime("%d-%m-%Y"),
        "cleaner": "Not Assigned",
        "complaint_text": request.form["complaint_text"],
        "complaint_date": datetime.now().strftime("%d-%m-%Y"),
        "status": "Pending",
        "needs_attention": "Yes"
    }

    df.loc[len(df)] = new_record

    try:
        df.to_csv(CSV_FILE, index=False)
    except PermissionError:
        return """
        <h2 style='color:red;text-align:center'>
        Close toilet_data.csv and try again.
        </h2>
        """

    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():

    df = pd.read_csv(CSV_FILE)

    total = len(df)

    cleaned = len(df[df["status"] == "Clean"])

    pending = len(df[df["status"] == "Pending"])

    progress = len(df[df["status"] == "In Progress"])

    attention = len(df[df["needs_attention"] == "Yes"])

    return render_template(
        "dashboard.html",
        data=df.to_dict(orient="records"),
        total=total,
        cleaned=cleaned,
        pending=pending,
        progress=progress,
        attention=attention
    )


if __name__ == "__main__":
    app.run(debug=True)