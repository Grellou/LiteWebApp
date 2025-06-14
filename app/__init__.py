from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_smorest import Api
from flask_jwt_extended import JWTManager

SECRET_KEY = "dev118"

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
api = Api()
jwt = JWTManager()

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

    # Api configs
    app.config["API_TITLE"] = "LiteWebApp REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["JWT_SECRET_KEY"] = "dev119"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900 # 15mins

    # Mail configs
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = "haroldasalekna2@gmail.com"
    app.config["MAIL_PASSWORD"] = "hdas hohh vlpm jtpm"
    app.config["MAIL_DEFAULT_SENDER"] = "haroldasalekna2@gmail.com"

    # Debug
    app.config["MAIL_DEBUG"] = True

    # Initializations
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.nagivation_route import bp as NavigationBlueprint
    from app.routes.user_route import bp as UserBlueprint
    from app.routes.api.user_route import bp as UserApiBlueprint
    from app.routes.api.item_route import bp as ItemApiBlueprint


    app.register_blueprint(NavigationBlueprint)
    app.register_blueprint(UserBlueprint)
    api.register_blueprint(UserApiBlueprint)
    api.register_blueprint(ItemApiBlueprint)

    return app
