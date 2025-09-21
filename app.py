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


@app.route("/contact_book/delete_contact/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id: int):
    contact = db.session.get(Contact, contact_id)
    if contact is not None:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for("contact_book"))


@app.route("/contact_book/edit_contact/<int:contact_id>", methods=["POST"])
def edit_contact(contact_id: int):
    contact = db.session.get(Contact, contact_id)
    if not contact:
        return redirect(url_for("index"))
    if request.method == "POST":
        contact.name = request.form["name"].strip()
        contact.email = request.form.get("email", "").strip() or None
        contact.phone = request.form.get("phone", "").strip() or None
        db.session.commit()
        return redirect(url_for("contact_book"))
