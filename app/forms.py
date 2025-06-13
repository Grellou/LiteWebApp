from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
import re

# Form for registration
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=20)])
    email_address = StringField("Email address", validators=[DataRequired(), Email(), Length(max=40)])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=40)])
    password2 = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField("Sign up")
    
    # Password must contain uppercase, lowercase, digit and one special character
    def validate_password1(self, field):
        password = field.data
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError("Password must contain at least one special.")

# Form for login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=40)])
    submit = SubmitField("Login")

# Form for password reset
class PasswordResetForm(FlaskForm):
    email_address = StringField("Email address", validators=[DataRequired(), Email(), Length(max=40)])
    submit = SubmitField("Send password reset email")

# Form to change password after reset request
class PasswordChangeForm(FlaskForm):
    password1 = PasswordField("New password", validators=[DataRequired(), Length(min=8, max=40)])
    password2 = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField("Confirm")

    # Password must contain uppercase, lowercase, digit and one special character
    def validate_password1(self, field):
        password = field.data
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError("Password must contain at least one special.")

# Form to request email change
class EmailChangeRequestForm(FlaskForm):
    email_address = StringField("Your current email address", validators=[DataRequired(), Email(), Length(max=40)])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=40)])
    password2 = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField("Submit")

# Form to change email address
class EmailChangeForm(FlaskForm):
    email_address = StringField("New email address", validators=[DataRequired(), Email(), Length(max=40)])
    submit = SubmitField("Confirm")
