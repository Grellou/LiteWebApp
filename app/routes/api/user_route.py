from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app import db
from app.models import UserModel
from app.schemas import UserSchema

bp = Blueprint("user_api", __name__)

@bp.route("/api/user/<int:user_id>")
class User(MethodView):

    # Delete user from database
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
