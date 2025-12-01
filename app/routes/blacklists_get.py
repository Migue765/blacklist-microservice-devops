from flask import Blueprint, jsonify
from app import db
from app.models import Blacklist
from app.auth import require_bearer_token
from app.utils import setup_logging
from app.db_metrics import record_db_metric
import newrelic.agent
import time

blacklists_get_bp = Blueprint('blacklists_get', __name__)
logger = setup_logging()

@blacklists_get_bp.route('/<string:email>', methods=['GET'])
@require_bearer_token
@newrelic.agent.function_trace()
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
    # Record custom metric for blacklist query attempt
    newrelic.agent.record_custom_metric('Custom/Blacklist/QueryAttempt', 1)
    
    try:
        # Validate email format (basic validation)
        if not email or '@' not in email:
            newrelic.agent.record_custom_metric('Custom/Blacklist/QueryValidationError', 1)
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid email format'
            }), 400
        
        # Query database for email with timing
        start_time = time.time()
        blacklist_entry = Blacklist.query.filter_by(email=email.lower()).first()
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Record database response time metric
        record_db_metric("query", elapsed_time, success=True)
        
        if blacklist_entry:
            logger.info("Email found in blacklist", 
                       email=email, 
                       is_blacklisted=True,
                       db_time_ms=elapsed_time)
            # Record found metric
            newrelic.agent.record_custom_metric('Custom/Blacklist/QueryFound', 1)
            newrelic.agent.add_custom_attribute('email', email.lower())
            newrelic.agent.add_custom_attribute('is_blacklisted', True)
            return jsonify({
                'email': blacklist_entry.email,
                'is_blacklisted': True,
                'blocked_reason': blacklist_entry.blocked_reason
            }), 200
        else:
            logger.info("Email not found in blacklist", 
                       email=email, 
                       is_blacklisted=False,
                       db_time_ms=elapsed_time)
            # Record not found metric
            newrelic.agent.record_custom_metric('Custom/Blacklist/QueryNotFound', 1)
            newrelic.agent.add_custom_attribute('email', email.lower())
            newrelic.agent.add_custom_attribute('is_blacklisted', False)
            return jsonify({
                'email': email.lower(),
                'is_blacklisted': False,
                'blocked_reason': None
            }), 200
            
    except Exception as e:
        # Record database error metric if it's a DB error
        if 'database' in str(e).lower() or 'sql' in str(e).lower():
            record_db_metric("query", 0, success=False)
        
        logger.error("Error checking blacklist", 
                    email=email, 
                    error=str(e), 
                    error_type=type(e).__name__)
        # Record error metric
        newrelic.agent.record_custom_metric('Custom/Blacklist/QueryError', 1)
        newrelic.agent.record_exception()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500