from os import access
from flask_smorest import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from app import db
from app.models import UserModel
from app.schemas import UserSchema, AuthSchema, AuthResponseSchema
from sqlalchemy.exc import SQLAlchemyError
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

bp = Blueprint("user_api", __name__)

@bp.route("/api/auth")
class Auth(MethodView):
    @bp.arguments(AuthSchema)
    @bp.response(200, AuthResponseSchema)
    def post(self, auth_data):
        user = UserModel.query.filter_by(username=auth_data["username"]).first()

        if not user or not user.check_password(auth_data["password"]):
            abort(401, message="Invalid credentials.")

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}

@bp.route("/api/user/<int:user_id>")
class UserId(MethodView):
    # Get single user data
    @bp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    # Update single user data
    @bp.arguments(UserSchema)
    @bp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id)

        # Update fields
        user.username = user_data["username"]
        user.email_address = user_data["email_address"]
        user.verified = user_data["verified"]
        user.set_password(user_data["password"])

        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(500, message=f"An error occurred while updating user: {str(error)}")

        return {"message": "User data updated."}, 200

    # Delete single user from database
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted."}, 200

@bp.route("/api/user")
class User(MethodView):
    # Add single user
    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        # Check if user exists
        if UserModel.query.filter_by(email_address=user_data["email_address"]).first():
            abort(400, message="User with that email address already exists.")

        # User instance
        user = UserModel(username=user_data["username"], email_address=user_data["email_address"], verified=user_data["verified"]) # type: ignore
        # Hash password
        user.set_password(user_data["password"])
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating user.")

        return user

@bp.route("/api/users")
class Users(MethodView):
    # Get list of all users
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    # Delete all users
    def delete(self):
        users = UserModel.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()

        return {"message": "All users deleted."}, 200

