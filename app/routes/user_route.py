from flask import Blueprint, flash, redirect, url_for, render_template
from app import db
from app.forms import RegistrationForm, LoginForm, PasswordResetForm, PasswordChangeForm, EmailChangeForm, EmailChangeRequestForm
from app.models import UserModel
from app.utility import generate_token, send_verification_email, confirm_token, generate_password_token, send_password_reset_email, confirm_password_token 
from app.utility import send_account_locked_email, generate_email_change_token, confirm_email_change_token, send_email_change_email
from flask_login import current_user, login_user, login_required, logout_user

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

        # Validate if user exists in db
        if not user:
            flash("Account with such username not found.", "danger")
            return redirect(url_for("user.login_page"))
        
        # Check if password is correct
        if not user.check_password(form.password.data):
            user.login_attempts += 1 # increase login attempts value
            db.session.commit()
            flash("Incorrect username or password.", "danger")
            return redirect(url_for("user.login_page"))

        # Check if login attempts should lock user account
        if user.login_attempts >= 3:
            user.locked = True # Lock account
            db.session.commit()
            send_account_locked_email(user.email_address)
            flash("Your account has been locked due to too many invalid login attemps.", "danger")

        # Check if account is verified
        if not user.verified:
            flash("Your account is not verified. Please check your email.", "danger")
            return redirect(url_for("user.login_page"))

        # Check if account is not locked
        if user.locked:
            flash("Your account has been locked.", "danger")
            return redirect(url_for("user.login_page"))

        # Login user if all validations passed
        login_user(user)
        user.login_attempts = 0 # reset login attempts
        db.session.commit()
        flash("Login successful!", "success")
        return redirect(url_for("navigationa.home_page"))

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
            user.login_attempts = 0
            user.locked = False
            db.session.commit()
            flash("Password has been changed successfully!", "success")
            return redirect(url_for("user.login_page"))

    return render_template("password_change.html", form=form)

# My profile
@bp.route("/profile", methods=["POST", "GET"])
@login_required
def profile_page():
    form = EmailChangeRequestForm()
    return render_template("profile.html", form=form)

# Change email request route
@bp.route("/change_email", methods=["GET", "POST"])
@login_required
def change_email_request_page():
    form = EmailChangeRequestForm()
    if form.validate_on_submit():
        # Get user by it's email address
        user = UserModel.query.filter_by(email_address=form.email_address.data).first()

        if not user:
            flash("User with such email address was not found.", "danger")
            return redirect(url_for("user.profile_page"))
        
        # Check entered password in form
        if current_user.check_password(form.password1.data):
            # Generate password reset URL and send email
            token = generate_email_change_token(user.email_address)
            verify_url = url_for("user.change_email_page", token=token, _external=True)
            success, error = send_email_change_email(user.email_address, verify_url)
            if not success:
                flash(f"Email change request failed to send: {error}", "danger")
            else:
                flash("Please check your email for instructions of how change your email address.", "success")
        else:
            flash("Invalid password", "danger")
    return redirect(url_for("navigation.profile_page"))

# Change email
@bp.route("/change_email/<string:token>", methods=["POST", "GET"])
@login_required
def change_email_page(token):
    # Verify token
    email = confirm_password_token(token)
    
    # Invalid token
    if not email:
        flash("Expired or invalid email change request.", "danger")
        return redirect(url_for("user.profile_page"))

    return redirect(url_for("user.profile_page"))
