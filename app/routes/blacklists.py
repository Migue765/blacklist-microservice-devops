from flask import Blueprint, request, jsonify
from app import db
from app.models import Blacklist
from app.schemas import BlacklistSchema, BlacklistResponseSchema, ErrorSchema
from app.auth import require_bearer_token
from app.utils import get_client_ip, setup_logging
from app.db_metrics import db_operation_timer, record_db_metric
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import newrelic.agent
import time

blacklists_bp = Blueprint('blacklists', __name__)
logger = setup_logging()

# Initialize schemas
blacklist_schema = BlacklistSchema()
blacklist_response_schema = BlacklistResponseSchema()
error_schema = ErrorSchema()

@blacklists_bp.route('', methods=['POST'])
@require_bearer_token
@newrelic.agent.function_trace()
def add_to_blacklist():
    """
    Add an email to the global blacklist

    Request Body:
        {
            "email": "user@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spam detected" (optional)
        }

    Headers:
        Authorization: Bearer <token>

    Returns:
        201: Email added successfully
        400: Validation error
        401: Unauthorized
        409: Email already exists
        500: Server error
    """
    # Record custom metric for blacklist addition attempt
    newrelic.agent.record_custom_metric('Custom/Blacklist/AddAttempt', 1)
    
    try:
        # Validate request data
        data = request.get_json()
        if not data:
            newrelic.agent.record_custom_metric('Custom/Blacklist/AddValidationError', 1)
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body must be JSON'
            }), 400

        # Validate using Marshmallow schema
        try:
            validated_data = blacklist_schema.load(data)
        except Exception as e:
            newrelic.agent.record_custom_metric('Custom/Blacklist/AddValidationError', 1)
            return jsonify({
                'error': 'Bad Request',
                'message': 'Validation error',
                'details': str(e)
            }), 400

        # Get client IP
        client_ip = get_client_ip()

        # Create new blacklist entry
        blacklist_entry = Blacklist(
            email=validated_data['email'],
            app_uuid=validated_data['app_uuid'],
            blocked_reason=validated_data.get('blocked_reason'),
            client_ip=client_ip,
            created_at=datetime.utcnow()
        )

        # Save to database with timing
        try:
            start_time = time.time()
            db.session.add(blacklist_entry)
            db.session.commit()
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Record database response time metric
            record_db_metric("insert", elapsed_time, success=True)

            logger.info("Email added to blacklist", 
                       email=validated_data['email'], 
                       client_ip=client_ip,
                       app_uuid=validated_data['app_uuid'],
                       db_time_ms=elapsed_time)

            # Record success metric
            newrelic.agent.record_custom_metric('Custom/Blacklist/AddSuccess', 1)
            newrelic.agent.add_custom_attribute('email', validated_data['email'])
            newrelic.agent.add_custom_attribute('app_uuid', validated_data['app_uuid'])

            return jsonify({
                'message': 'Email agregado exitosamente a la lista negra.',
                'data': blacklist_response_schema.dump(blacklist_entry)
            }), 201

        except IntegrityError as e:
            db.session.rollback()
            # Record database error metric
            record_db_metric("insert", 0, success=False)
            
            if 'unique constraint' in str(e).lower() or 'duplicate key' in str(e).lower():
                # Record duplicate email metric
                newrelic.agent.record_custom_metric('Custom/Blacklist/AddDuplicate', 1)
                newrelic.agent.record_exception()
                return jsonify({
                    'error': 'Conflict',
                    'message': 'Email already exists in blacklist'
                }), 409
            else:
                logger.error("Database integrity error", 
                             error=str(e), 
                             error_type="IntegrityError")
                # Record database error
                newrelic.agent.record_custom_metric('Custom/Blacklist/AddDatabaseError', 1)
                newrelic.agent.record_exception()
                return jsonify({
                    'error': 'Internal Server Error',
                    'message': 'Database error occurred'
                }), 500

    except Exception as e:
        logger.error("Unexpected error in add_to_blacklist", 
                    error=str(e), 
                    error_type=type(e).__name__)
        # Record error metric
        newrelic.agent.record_custom_metric('Custom/Blacklist/AddError', 1)
        newrelic.agent.record_exception()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500

# TODO: GET endpoint movido a blacklists_get.py
