from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# Form for registration
class RegistrationForm(FlaskForm):
    username = StringField("Username", Length(max=20), validators=[DataRequired()])
    email_address = StringField("Email address", Length(max=40), validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", Length(max=40), validators=[DataRequired()])
    password2 = PasswordField("Confirm password", Length(max=40), validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField("Sign up")