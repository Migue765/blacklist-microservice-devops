from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from app.config import Config
import os

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
    from app.routes.blacklists_get import blacklists_get_bp
    from app.routes.health import health_bp
    from app.routes.ping import ping_bp

    app.register_blueprint(blacklists_bp, url_prefix='/blacklists')
    app.register_blueprint(blacklists_get_bp, url_prefix='/blacklists')
    app.register_blueprint(health_bp)
    app.register_blueprint(ping_bp)

    # Root endpoint for health checks
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint for load balancer health checks"""
        return jsonify({"status": "ok"}), 200

    # Create tables
    with app.app_context():
        db.create_all()

    # Wrap app with New Relic WSGI middleware if enabled
    if os.environ.get('NEW_RELIC_LICENSE_KEY'):
        try:
            import newrelic.agent
            app = newrelic.agent.WSGIApplicationWrapper(app)
        except ImportError:
            pass  # New Relic not installed, continue without it

    return app