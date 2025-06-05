from flask.views import MethodView
from flask_smorest import Blueprint
from app import db
from app.models import UserModel

bp = Blueprint("user_api", __name__)

@bp.route("/api/user/<int:user_id>")
class UserId(MethodView):
    # Get user data
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    # Delete user from database
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
