from flask import Blueprint, jsonify
from app import db
from app.models import Blacklist
from app.auth import require_bearer_token
from app.utils import setup_logging

blacklists_get_bp = Blueprint('blacklists_get', __name__)
logger = setup_logging()

@blacklists_get_bp.route('/<string:email>', methods=['GET'])
@require_bearer_token
def check_blacklist(email):
    """
    Check if an email is in the global blacklist
    
    Args:
        email (str): Email address to check
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Email status with blacklist information
        {
            "email": "user@example.com",
            "is_blacklisted": true,
            "blocked_reason": "Spam detected"
        }
        
        or if not blacklisted:
        {
            "email": "user@example.com", 
            "is_blacklisted": false,
            "blocked_reason": null
        }
    """
    try:
        # Validate email format (basic validation)
        if not email or '@' not in email:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid email format'
            }), 400
        
        # Query database for email
        blacklist_entry = Blacklist.query.filter_by(email=email.lower()).first()
        
        if blacklist_entry:
            logger.info(f"Email {email} found in blacklist")
            return jsonify({
                'email': blacklist_entry.email,
                'is_blacklisted': True,
                'blocked_reason': blacklist_entry.blocked_reason
            }), 200
        else:
            logger.info(f"Email {email} not found in blacklist")
            return jsonify({
                'email': email.lower(),
                'is_blacklisted': False,
                'blocked_reason': None
            }), 200
            
    except Exception as e:
        logger.error(f"Error checking blacklist for {email}: {str(e)}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500