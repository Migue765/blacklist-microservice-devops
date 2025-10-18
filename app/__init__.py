from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.blacklists import blacklists_bp
    from app.routes.health import health_bp

    app.register_blueprint(blacklists_bp, url_prefix='/blacklists')
    app.register_blueprint(health_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
