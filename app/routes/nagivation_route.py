from flask import Blueprint, render_template, request
from app.models import ItemModel
from sqlalchemy import or_

bp = Blueprint("navigation", __name__)

# Home page route
@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template("home.html")

# Store page route
@bp.route("/store")
def store_page():
    search_query = request.args.get("query", "") # search query
    sort = request.args.get("sort", "name")
    direction = request.args.get("direction", "asc")

    # Search
    if search_query:
        items = ItemModel.query.filter(or_(ItemModel.name.ilike(f"%{search_query}%"))).all()
    else:
        items = ItemModel.query.all()

    # Sorting   
    sort_column = getattr(ItemModel, sort, ItemModel.name)
    if direction == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()
    items = ItemModel.query.order_by(sort_column).all()

    return render_template("store.html", items=items, sort=sort, direction=direction, search_query=search_query)

