from app import mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app import SECRET_KEY

# Set token and it's expiry time
token = URLSafeTimedSerializer(SECRET_KEY)
TOKEN_EXPIRATION = 900 # seconds. 15 mins

# Generate time limited token for user email address
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
            subject="LiteWebApp account verification",
            recipients=[user_email_address],
            body=f"Please verify your account: {verification_url}")
        mail.send(message)
        return True, None
    except Exception as error:
        return False, f"Email sending has failed: {str(error)}"
