from flask import Blueprint, render_template

bp = Blueprint("navigation", __name__)

# Home page route
@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template("home.html")
