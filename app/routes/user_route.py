from flask import Blueprint, flash, redirect, url_for, render_template
from app import db
from forms import RegistrationForm
from models import UserModel

bp = Blueprint("user", __name__)

# User register route
@bp.route("/register", methods=["POST", "GET"])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        # Check if username or email already exists
        existing_username = UserModel.query.filter_by(UserModel.username == form.username.data).first()
        existing_email_address = UserModel.query.filter_by(UserModel.email_address == form.email_address.data).first()
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

    flash("Incorrect data has been entered during registration.", "danger")
    return render_template("register.html", form=form)