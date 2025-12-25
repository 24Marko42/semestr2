from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Optional imports (allow tests to run without installing all deps)
try:
    from flask_migrate import Migrate
except Exception:
    Migrate = None
from flask_login import LoginManager
try:
    from flasgger import Swagger
except Exception:
    Swagger = None
import os
from .config import Config


db = SQLAlchemy()
if Migrate:
    migrate = Migrate()
else:
    migrate = None
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    if migrate:
        migrate.init_app(app, db)
    login.init_app(app)

    # Initialize Flasgger with the YAML spec if present and flasgger installed
    if Swagger:
        try:
            swagger_spec = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'swagger.yml')
            Swagger(app, template_file=swagger_spec)
        except Exception:
            Swagger(app)

    from . import models
    from .routes_api import bp as api_bp
    from .routes_web import bp as web_bp
    from .auth import bp as auth_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(web_bp)
    app.register_blueprint(auth_bp)

    return app
