from app import db, bcrypt
from flask_login import UserMixin

class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email_address = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(40), nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    login_attempts = db.Column(db.Integer, default=0)
    locked = db.Column(db.Boolean, default=False)

    # Hash password
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
    # Check hashed password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
