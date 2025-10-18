from flask import Blueprint, jsonify
from app.utils import setup_logging

health_bp = Blueprint('health', __name__)
logger = setup_logging()

@health_bp.route('/ping', methods=['GET'])
@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for Elastic Beanstalk

    Returns:
        JSON response with status 'ok'
    """
    logger.info("Health check requested")
    return jsonify({"status": "ok"}), 200
