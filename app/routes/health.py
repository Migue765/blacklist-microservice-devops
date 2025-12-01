from flask import Blueprint, jsonify
from app.utils import setup_logging

health_bp = Blueprint('health', __name__)
logger = setup_logging()

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for Elastic Beanstalk

    Returns:
        JSON response with status 'ok'
    """
    try:
        # Try to record health check metric if New Relic is available
        import newrelic.agent
        newrelic.agent.record_custom_metric('Custom/Health/Check', 1)
    except (ImportError, AttributeError):
        # New Relic not available, continue without it
        pass
    
    logger.info("Health check requested")
    return jsonify({"status": "ok"}), 200
