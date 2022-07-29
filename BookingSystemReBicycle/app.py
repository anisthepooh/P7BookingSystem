from contextlib import nullcontext
from cs50 import SQL
from flask import Flask, request, render_template, redirect


app = Flask(__name__)

db = SQL("sqlite:///Database.db")

@app.route("/")
def start():
    return render_template("/Frontpage.html")
if __name__ == "__main__":
    app.run()

@app.route("/BicycleType.html")
def proces():
    return render_template("/BicycleType.html")

@app.route("/BicycleType.html", methods=["POST", "GET"])
def information():
    bicycletype = request.form.get("bicycletype2")
    reparations = request.form.get("reparations")
    timeslot = request.form.get("timeslot")
    date = request.form.get("date")
    note = request.form.get("note")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    phonenumber = request.form.get("phonenumber")
    email = request.form.get("email")
    db.execute("INSERT INTO users (firstname, lastname, phonenumber, email) VALUES (:firstname, :lastname, :phonenumber, :email)", firstname=firstname, lastname=lastname,  phonenumber=phonenumber, email=email)
    person = db.execute("SELECT personid FROM users ORDER BY personid DESC LIMIT 1")
    personid = person[0]['personid']
    db.execute("INSERT INTO booking (person, timeslot, date, bicycletype, reparations, Note) VALUES (:personid, :timeslot, :date, :bicycletype, :reparations, :note)", personid=personid, timeslot=timeslot, date=date, bicycletype=bicycletype, reparations=reparations, note=note)
    return redirect("/bookingconfirmation.html")

@app.route("/users.html")
def users():
    rows = db.execute("SELECT * FROM users")
    return render_template("/users.html", rows=rows)

@app.route("/booking.html")
def bookings():
    rows = db.execute("SELECT * FROM booking ORDER BY date, timeslot")
    return render_template("/booking.html", rows=rows)

@app.route("/bookingconfirmation.html")
def confirmation():
    persons= db.execute("SELECT * FROM users ORDER BY personid DESC LIMIT 1")
    rows = db.execute("SELECT * FROM booking ORDER BY bookingnumber DESC LIMIT 1")
    reparation1 = db.execute("SELECT reparations FROM booking ORDER BY bookingnumber DESC LIMIT 1")
    reparation = reparation1[0]['reparations']
    if reparation == "Tire repair":
        time = "30 min."
    elif reparation == "Chain repair":
        time = "45 min."
    elif reparation == "Breaks":    
        time = "60 min."
    elif reparation == "Service check":
        time = "90 min."
    elif reparation == "Other":
        time = "Unknown"
    return render_template("/bookingconfirmation.html", rows=rows, persons=persons, time=time)

@app.route("/cancel.html", methods=["POST", "GET"])
def cancel():
    if request.method == "GET":
        return render_template ("/cancel.html")
    else:
        bookingnumber = request.form.get("bookingnumber")
        if bookingnumber != nullcontext:
            book = db.execute("SELECT person FROM booking WHERE bookingnumber = %s ORDER BY bookingnumber", bookingnumber)
            if book == []:
                return render_template("error.html", bookingnumber=bookingnumber)
            else:
                person = book[0]['person']
                db.execute("DELETE FROM booking WHERE bookingnumber= %s;", bookingnumber)
                db.execute("DELETE FROM users WHERE personid= %s;", person)
                return render_template("succes.html", bookingnumber=bookingnumber)
        else:
            return render_template("/cancel.html")