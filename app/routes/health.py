from flask import Blueprint, jsonify
from app.utils import setup_logging
import newrelic.agent

health_bp = Blueprint('health', __name__)
logger = setup_logging()

@health_bp.route('/health', methods=['GET'])
@newrelic.agent.function_trace()
def health_check():
    """
    Health check endpoint for Elastic Beanstalk

    Returns:
        JSON response with status 'ok'
    """
    # Record health check metric
    newrelic.agent.record_custom_metric('Custom/Health/Check', 1)
    logger.info("Health check requested")
    return jsonify({"status": "ok"}), 200
