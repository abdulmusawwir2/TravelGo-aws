

from flask import Flask, render_template, request, redirect, session, flash
from services.dynamodb_service import create_user, get_user, create_booking, get_user_bookings
from services.sns_service import send_booking_email
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "travelgo_secret"


@app.route("/")
def home():
    return redirect("/login")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]

        create_user(email, name, password)

        flash("Account created successfully! Please login.", "success")
        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user(email)

        if user and user["password"] == password:
            session["user"] = email
            flash(f"Welcome back, {email}!", "success")
            return redirect("/dashboard")

        else:
            flash("Invalid email or password.", "error")

    return render_template("login.html")


# DASHBOARD
from services.dynamodb_service import get_user_bookings


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    email = session["user"]

    bookings = get_user_bookings(email)

    total_trips = len(bookings)
    total_saved = sum(float(b["price"]) for b in bookings)

    cities = set()
    for b in bookings:
        cities.add(b["destination"])

    cities_visited = len(cities)

    reward_points = total_trips * 10

    return render_template(
        "dashboard.html",
        email=email,
        total_trips=total_trips,
        cities=cities_visited,
        reward_points=reward_points,
        total_saved=total_saved,
        bookings=bookings
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user", None)

    flash("You have been logged out.", "info")

    return redirect("/login")


# BOOKING
@app.route("/booking", methods=["GET", "POST"])
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
            email,
            type,
            source,
            destination,
            date,
            seat,
            price
        )

        message = f"""
Booking Confirmed!

Booking ID: {booking_id}
Type: {type}
From: {source}
To: {destination}
Date: {date}
Seat: {seat}
Price: ${price}
"""

        print("Sending SNS email...")
        send_booking_email(message)
        print("SNS email sent")

        flash(
            f"Booking Successful! {type} from {source} to {destination}. Booking ID: {booking_id}",
            "success"
        )

        return redirect("/dashboard")

    return render_template("booking.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
