from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Load user
@login_manager.user_loader
def load_user(user_id):
    from app.models import UserModel

    return UserModel.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    # Configs
    app.config["SECRET_KEY"] = "dev118"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True

    # Initializations
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints here
    from app.routes.nagivation_route import bp as NavigationBlueprint
    from app.routes.user_route import bp as UserBlueprint

    app.register_blueprint(NavigationBlueprint)
    app.register_blueprint(UserBlueprint)
    return app
