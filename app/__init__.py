from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.routes.nagivation_route import bp as NavigationBlueprint

def create_app():
    app = Flask(__name__)

    # Configs
    app.config["SECRET_KEY"] = "dev118"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True

    bcrypt = Bcrypt(app)
    db = SQLAlchemy(app)


    # Register blueprints here
    app.register_blueprint(NavigationBlueprint)

    return app