import sqlite3
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/customers")
def customers():
    with sqlite3.connect("database/bank.db") as con:
        cur = con.cursor()
        customers = cur.execute("SELECT * FROM customers")
        return render_template("customers.html", customers=customers)

@app.route("/transfers")
def transfers():
    with sqlite3.connect("database/bank.db") as con:
        cur = con.cursor()
        transfers = cur.execute("SELECT * FROM Transfers")
        return render_template("transfers.html", transfers=transfers)

@app.route("/transfer", methods=['POST'])
def transfer():
    sender = request.form['sender-email']
    receiver = request.form['receiver-email']
    amount = request.form['amount']
    if not sender or not receiver:
        return 'Sender or receiver can not be empty'
    
    with sqlite3.connect("database/bank.db") as con:
        cur = con.cursor()
        senderDB = cur.execute("SELECT * FROM customers WHERE email = ?;", (sender,)).fetchall()
        receiverDB = cur.execute(f"SELECT * FROM customers WHERE email = ?;", (receiver,)).fetchall()

        senderBal = cur.execute("SELECT balance FROM customers WHERE email = ?;", (sender,)).fetchall()[0][0]
        receiverBal = cur.execute("SELECT balance FROM customers WHERE email = ?;", (receiver,)).fetchall()[0][0]

        senderBal -= int(amount)
        receiverBal += int(amount)

        cur.execute("UPDATE Customers SET balance = ? WHERE email = ?", (senderBal, sender))
        cur.execute("UPDATE Customers SET balance = ? WHERE email = ?", (receiverBal, receiver))

        time = datetime.now().strftime("%B %d, %Y %I:%M%p")
        cur.execute("INSERT INTO Transfers(sender_id, sender_email, receiver_id, receiver_email, amount, trans_date) VALUES(?, ?, ?, ?, ?, ?)", (senderDB[0][0], senderDB[0][2], receiverDB[0][0], receiverDB[0][2], amount, time))

        return redirect(url_for('customers'))