from app import db
from app.models import ItemModel
from app.schemas import ItemSchema, ItemsSchema
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
        # Check if item with such name exists
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

@bp.route("/api/item/<int:item_id>")
class ItemId(MethodView):
    # Update single user's data
    @jwt_required()
    @bp.arguments(ItemSchema)
    @bp.response(200, ItemSchema)
    @bp.doc(description="Update single user's data.")
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)

        try:
            for field, value in item_data.items():
                if hasattr(item, field):
                    setattr(item, field, value)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(500, message=f"An error occurred while updating item: {str(error)}")

        return item

    # Get single item's data
    @jwt_required()
    @bp.response(200, ItemSchema)
    @bp.doc(description="Get single item's data.")
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    # Delete single item
    @jwt_required()
    @bp.response(200, description="Item deleted.")
    @bp.doc(description="Delete single item.")
    def delete(self, item_id):
        # Check if item exists with such ID
        item = ItemModel.query.get_or_404(item_id)

        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(500, message=f"An error occurred while deleting item: {str(error)}")

        return {"message": "Item deleted."}, 200

@bp.route("/api/items")
class Items(MethodView):
    # Get list of all items
    @jwt_required()
    @bp.response(200, ItemSchema(many=True))
    @bp.doc(description="Get list of all items.")
    def get(self):
        return ItemModel.query.all()
    
    # Create multiple items from single request
    @jwt_required()
    @bp.arguments(ItemsSchema)
    @bp.response(201, ItemsSchema)
    @bp.doc(description="Create multiple items from single request")
    def post(self, items_data):
        items = []
        try:
            for item_data in items_data["items"]:

                # Check for duplicate item names
                if ItemModel.query.filter_by(name=item_data["name"], language=item_data["language"]).first():
                    db.session.rollback()
                    abort(400, message="Item already exists.")
                # Add items   
                item = ItemModel(**item_data)
                db.session.add(item)
                db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(500, message=f"An error occurred while adding items: {str(error)}")

        return items
    
    # Delete all items
    @jwt_required()
    @bp.response(200, description="All items deleted.")
    @bp.doc(description="Delete all items.")
    def delete(self):
        items = ItemModel.query.all()
        for item in items:
            db.session.delete(item)
        db.session.commit()
        
        return {"message": "All items deleted."}, 200
