import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models.models import Contact

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact_book", methods=["GET", "POST"])
def contact_book():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        if name:
            new_contact = Contact(name=name, email=email, phone=phone)
            db.session.add(new_contact)
            db.session.commit()

    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template("contacts.html", contacts=contacts)


# TODO: add phone field to contacts page
# TODO: Add in feature to edit/delete contacts
