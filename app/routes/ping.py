from flask import Blueprint, jsonify
from app.utils import setup_logging

ping_bp = Blueprint('ping', __name__)
logger = setup_logging()

@ping_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok v2"}), 200