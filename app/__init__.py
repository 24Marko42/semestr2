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


def create_app(config_class=Config, config_overrides=None):
    """Create Flask app. Optionally pass a dict `config_overrides` which will be
    applied after the `config_class` to allow tests to override e.g. the database URI.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    if migrate:
        migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'
    login.login_message = 'Please log in to access this page.'

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
