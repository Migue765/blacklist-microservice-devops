from flask import Blueprint, jsonify
from app import db
from app.models import Blacklist
from app.auth import require_bearer_token
from app.utils import setup_logging

# Blueprint para el endpoint GET Pendiente
blacklists_get_bp = Blueprint('blacklists_get', __name__)
logger = setup_logging()

@blacklists_get_bp.route('/<email>', methods=['GET'])
@require_bearer_token
def check_blacklist(email):
    return jsonify({
        'email': email,
        'is_blacklisted': False,
        'reason': None,
        'status': 'pending_implementation'
    }), 200
