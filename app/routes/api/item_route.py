from app import db
from app.models import ItemModel
from app.schemas import ItemSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

bp = Blueprint("item_api", __name__)

@bp.route("/api/item")
class Item(MethodView):
    # Add single item
    @jwt_required()
    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    @bp.doc(description="Add single item.")
    def post(self, item_data):
        # Check if item with such ID exists
        if ItemModel.query.filter_by(name=item_data["name"]).first():
            abort(400, message="Item already exists.")

        try:
            item = ItemModel(**item_data)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(500, message=f"An error occurred while adding item: {str(error)}")

        return item

