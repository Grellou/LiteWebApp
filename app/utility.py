from app import mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app import SECRET_KEY

# Set token and it's expiry time
token = URLSafeTimedSerializer(SECRET_KEY)
TOKEN_EXPIRATION = 900 # seconds. 15 mins
PASSWORD_TOKEN_EXPIRATION = 1800 # seconds. 30 mins

# ----- ACCOUNT VERIFICATION UTILS -----
# Generate time limited token for user email address confirmation
def generate_token(user_email_address):
    return token.dumps(user_email_address, salt="email-confirmation")

# Confirm token and extract email address if valid
def confirm_token(token_str, expiration=TOKEN_EXPIRATION):
    try:
        email = token.loads(token_str, salt="email-confirmation", max_age=expiration)
        return email
    except SignatureExpired:
        return None, "Confirmation link has expired."
    except BadSignature:
        return None, "Invalid confirmation link."
    except Exception as error:
        return None, f"Token confirmation failed {str(error)}."

# Send email verifacation with secure link
def send_verification_email(user_email_address, verification_url):
    try:
        message = Message(
            subject="LiteWebApp - account verification",
            recipients=[user_email_address],
            body=f"Please verify your account: {verification_url}")
        mail.send(message)
        return True, None
    except Exception as error:
        return False, f"Email sending has failed: {str(error)}"

# ----- PASSWORD RESET UTILS -----
# Generate time limited password reset token
def generate_password_token(user_email_address):
    return token.dumps(user_email_address, salt="password-reset")

# Confirm password token and extract email address if valid
def confirm_password_token(token_str, expiration=TOKEN_EXPIRATION):
    try:
        email = token.loads(token_str, salt="password-reset", max_age=expiration)
        return email
    except SignatureExpired:
        return None, "Password reset link has expired."
    except BadSignature:
        return None, "Invalid password reset link."
    except Exception as error:
        return None, f"Token confirmation failed {str(error)}."

# Send password reset URL to user's email address
def send_password_reset_email(user_email_address, verification_url):
    try:
        message = Message(
            subject="LiteWebApp - password reset",
            recipients=[user_email_address],
            body=f"In order to reset your password go to the following link: {verification_url}")
        mail.send(message)
        return True, None
    except Exception as error:
        return False, f"Email sending has failed: {str(error)}"

# ----- ACCOUNT LOCKED UTILS -----
# Send email about account getting locked
def send_account_locked_email(user_email_address):
    try:
        message = Message(
            subject="LiteWebApp - your account is locked",
            recipients=[user_email_address],
            body="Your account has been locked. In order to restore your access - you must reset your password. Please follow instructions in our website.")
        mail.send(message)
        return True, None
    except Exception as error:
        return False, f"Email sending has failed: {str(error)}"

