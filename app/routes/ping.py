from flask import Blueprint, jsonify
from app.utils import setup_logging
import newrelic.agent

ping_bp = Blueprint('ping', __name__)
logger = setup_logging()

@ping_bp.route('/ping', methods=['GET'])
@newrelic.agent.function_trace()
def ping():
    # Record ping metric
    newrelic.agent.record_custom_metric('Custom/Ping/Request', 1)
    return jsonify({"status": "ok v2"}), 200