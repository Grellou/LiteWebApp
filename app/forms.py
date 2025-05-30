from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# Form for registration
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=20)])
    email_address = StringField("Email address", validators=[DataRequired(), Email(), Length(max=40)])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(max=40)])
    password2 = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField("Sign up")

# Form for login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=40)])
    submit = SubmitField("Login")
