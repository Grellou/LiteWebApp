from flask import Blueprint, render_template
from app.models import ItemModel

bp = Blueprint("navigation", __name__)

# Home page route
@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template("home.html")

# Store page route
@bp.route("/store")
def store_page():
    items = ItemModel.query.all()
    return render_template("store.html", items=items)

