from flask import Blueprint, request, jsonify
from app import db
from app.models import Blacklist
from app.schemas import BlacklistSchema, BlacklistResponseSchema, ErrorSchema
from app.auth import require_bearer_token
from app.utils import get_client_ip, setup_logging
from datetime import datetime
from sqlalchemy.exc import IntegrityError

blacklists_bp = Blueprint('blacklists', __name__)
logger = setup_logging()

# Initialize schemas
blacklist_schema = BlacklistSchema()
blacklist_response_schema = BlacklistResponseSchema()
error_schema = ErrorSchema()

@blacklists_bp.route('', methods=['POST'])
@require_bearer_token
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
    try:
        # Validate request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body must be JSON'
            }), 400

        # Validate using Marshmallow schema
        try:
            validated_data = blacklist_schema.load(data)
        except Exception as e:
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

        # Save to database
        try:
            db.session.add(blacklist_entry)
            db.session.commit()

            logger.info(f"Email {validated_data['email']} added to blacklist by IP {client_ip}")

            return jsonify({
                'message': 'Email agregado exitosamente a la lista negra.',
                'data': blacklist_response_schema.dump(blacklist_entry)
            }), 201

        except IntegrityError as e:
            db.session.rollback()
            if 'unique constraint' in str(e).lower() or 'duplicate key' in str(e).lower():
                return jsonify({
                    'error': 'Conflict',
                    'message': 'Email already exists in blacklist'
                }), 409
            else:
                logger.error(f"Database integrity error: {str(e)}")
                return jsonify({
                    'error': 'Internal Server Error',
                    'message': 'Database error occurred'
                }), 500

    except Exception as e:
        logger.error(f"Unexpected error in add_to_blacklist: {str(e)}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500

# TODO: GET endpoint movido a blacklists_get.py
# Pendiente implementación por Nata en rama feature/nata-get-endpoint
# @blacklists_bp.route('/<email>', methods=['GET'])
# def check_blacklist(email):
#     # Lógica movida a app/routes/blacklists_get.py
