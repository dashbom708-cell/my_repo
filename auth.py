from flask import Blueprint, render_template, redirect, request, flash, url_for
import re
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError


auth = Blueprint("auth", __name__)

@auth.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        data = request.form
        if not all(data.values()):
            flash("All the fields are required!", "error")
        elif len(data.get("full_name")) < 3:
            flash("full name must be at least 3 characters!", "error")
        elif not re.match(r"\w+@\w+\.\w+", data.get("email")):
            flash("The entered email is invalid!", "error")
        elif len(data.get("password")) < 8:
            flash("Weak password, value must be greater than or equal to 8!", "error")
        elif data.get("password") != data.get("confirm"):
            flash("Passwords do not match!", "error")
        else:
            # database
            hashed = generate_password_hash(data["password"], )
            try:
                user = User(full_name=data["full_name"], email=data["email"], password=hashed)
                db.session.add(user)
                db.session.commit()
                flash("Account created!", "success")
                # session
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            except IntegrityError:
                flash("Email already taken!", "error")
    return render_template("sign_in.html", n="1", css_filename="auth.css")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        if not all(data.values()):
            flash("All the fields are required!", "error")
        else:
            user = User.query.filter_by(email=data["email"]).first()
            if not user or not check_password_hash(user.password, data["password"]):
                flash("Invalid Email or password!", "error")
            else:
                login_user(user, remember=True)
                flash("Logged in successfully!", "success")
                return redirect(url_for("views.home"))
    return render_template("login.html", n="1", css_filename="auth.css")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out", "success")
    return redirect(url_for("auth.login"))