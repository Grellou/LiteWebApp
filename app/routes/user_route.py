from flask import Blueprint, flash, redirect, url_for, render_template
from app import db
from app.forms import RegistrationForm, LoginForm, PasswordResetForm, PasswordChangeForm
from app.models import UserModel
from app.utility import generate_token, send_verification_email, confirm_token, generate_password_token, send_password_reset_email, confirm_password_token
from flask_login import login_user, login_required, logout_user

bp = Blueprint("user", __name__)

# User register route
@bp.route("/register", methods=["POST", "GET"])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        # Check if username or email already exists
        username = UserModel.query.filter_by(username=form.username.data).first()
        email_address = UserModel.query.filter_by(email_address=form.email_address.data).first()
        if username:
            flash("Username is already taken.", "danger")
            return redirect(url_for("user.register_page"))
        if email_address:
            flash("Email address is already taken.", "danger")

        # Proceed with creating account
        user = UserModel(username = form.username.data, email_address = form.email_address.data) # type: ignore
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()

        # Generate and send verification email
        token = generate_token(user.email_address)
        verify_url = url_for("user.verify_account_page", token=token, _external=True)
        success, error = send_verification_email(user.email_address, verify_url)
        if not success:
            flash(f"Verification email failed to send: {error}", "danger")
        else:
            flash("Please check your email for verification link.", "warning")
        return redirect(url_for("user.login_page"))

    return render_template("register.html", form=form)

# User login route
@bp.route("/login", methods=["POST", "GET"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()

        # Check if user found and password matches
        if user and user.check_password(form.password.data):
            if not user.verified: # Check if account is verified
                flash("Please verify your account before logging in.", "warning")
                return redirect(url_for("user.login_page"))
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

# Account verification route
@bp.route("/verify/<string:token>")
def verify_account_page(token):
    email = confirm_token(token)
    
    # Invalid token
    if not email:
        flash("Expired or invalid verification token.", "danger")
        return redirect(url_for("user.login_page"))
    
    user = UserModel.query.filter_by(email_address=email).first()
    
    # User not found
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("user.login_page"))
    
    # Return  according to current verification of user account
    if user.verified:
        flash("User is already verified.", "info")
    else:
        user.verified = True
        db.session.commit()
        flash("Your account has been verified! You can login.", "success")
    
    return redirect(url_for("user.login_page"))
    
# Password reset route
@bp.route("/password_reset", methods=["POST", "GET"])
def password_reset_page():
    form = PasswordResetForm()
    if form.validate_on_submit():
        # Get user by it's email address
        user = UserModel.query.filter_by(email_address=form.email_address.data).first()

        if not user:
            flash("User with such email address was not found.", "danger")
            return redirect(url_for("password_reset_page"))
        
        # Generate password reset URL and send email
        token = generate_password_token(user.email_address)
        verify_url = url_for("user.change_password_page", token=token, _external=True)
        success, error = send_password_reset_email(user.email_address, verify_url)
        if not success:
            flash(f"Password reset email failed to send: {error}", "danger")
        else:
            flash("Please check your email for password reset link.", "success")
        return redirect(url_for("user.password_reset_page"))

    return render_template("password_reset.html", form=form)

# Change password route
@bp.route("/password_reset/<string:token>", methods=["POST", "GET"])
def change_password_page(token):
    form = PasswordChangeForm()
    if form.validate_on_submit():
        # Get user's email address from token
        email = confirm_password_token(token)
    
        # Invalid token
        if not email:
            flash("Expired or invalid password reset URL.", "danger")
            return redirect(url_for("user.password_reset_page"))

        # Get user by it's email address
        user = UserModel.query.filter_by(email_address=email).first()
        if user:
            user.set_password(form.password1.data)
            db.session.commit()
            flash("Password has been changed successfully!", "success")
            return redirect(url_for("user.login_page"))

    return render_template("password_change.html")

