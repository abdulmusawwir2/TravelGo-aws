from flask import Flask, render_template, request, redirect, session
from services.dynamodb_service import create_user, get_user

from services.sns_service import send_booking_email
from services.dynamodb_service import create_booking

app = Flask(__name__)
app.secret_key = "travelgo_secret"

# Temporary user storage (later we will use DynamoDB)
users = {}

@app.route("/")
def home():
    return redirect("/login")


# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]

        create_user(email, name, password)

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user(email)

        if user and user["password"] == password:

            session["user"] = email
            return redirect("/dashboard")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    email = session["user"]

    return render_template("dashboard.html", email=email)


# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")



@app.route("/booking", methods=["GET","POST"])
def booking():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        email = session["user"]
        type = request.form["type"]
        source = request.form["source"]
        destination = request.form["destination"]
        date = request.form["date"]
        seat = request.form["seat"]
        price = request.form["price"]

        booking_id = create_booking(
            email, type, source, destination, date, seat, price
        )

        message = f"""
Booking Confirmed!

Booking ID: {booking_id}
Type: {type}
From: {source}
To: {destination}
Date: {date}
Seat: {seat}
Price: {price}
"""

        print("Sending SNS email...")
        send_booking_email(message)
        print("SNS email sent")

        return "Booking Successful!"

    return render_template("booking.html")


if __name__ == "__main__":
    app.run(debug=True)