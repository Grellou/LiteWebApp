from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    # Configs
    app.config["SECRET_KEY"] = "dev118"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True

    db.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints here
    from app.routes.nagivation_route import bp as NavigationBlueprint
    from app.routes.user_route import bp as UserBlueprint
    app.register_blueprint(NavigationBlueprint)
    app.register_blueprint(UserBlueprint)

    return app