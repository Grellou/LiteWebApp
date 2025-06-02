from flask import Blueprint, flash, redirect, url_for, render_template
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import UserModel
from flask_login import login_user, login_required, logout_user

bp = Blueprint("user", __name__)

# User register route
@bp.route("/register", methods=["POST", "GET"])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        # Check if username or email already exists
        existing_username = UserModel.query.filter_by(username=form.username.data).first()
        existing_email_address = UserModel.query.filter_by(email_address=form.email_address.data).first()
        if existing_username:
            flash("Username is already taken.", "danger")
            return redirect(url_for("user.register_page"))
        if existing_email_address:
            flash("Email address is already taken.", "danger")

        # Proceed with creating account
        user = UserModel(username = form.username.data, email_address = form.email_address.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! You can login.", "success")
        return redirect(url_for("navigation.home_page"))

    return render_template("register.html", form=form)

# User login route
@bp.route("/login", methods=["POST", "GET"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()

        # Check if user found and password matches
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("navigation.home_page"))
        else:
            flash("Incorrect username or password.", "danger")
            return redirect(url_for("user.login_page"))

    return render_template("login.html", form=form)

# User logout route
@bp.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("You've logged out.", "success")
    return redirect(url_for("navigation.home_page"))
