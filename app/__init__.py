import os

from dotenv import load_dotenv
from flask import Flask

from app.config import LocalConfig, ProductionConfig
from app.extensions import db, migrate, login_manager
from .blueprints.main import bp as main_bp
from .blueprints.admin import bp as admin_bp


def create_app():
    env = os.getenv('ENV', 'local')
    if env == 'local':
        load_dotenv('.env')

    app = Flask(__name__)

    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(LocalConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app import models

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    return app

