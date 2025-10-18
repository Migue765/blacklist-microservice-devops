from flask import request, jsonify
from functools import wraps
from app.config import Config

def require_bearer_token(f):
    """Decorator to require Bearer token authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authorization header is required'
            }), 401

        try:
            auth_type, token = auth_header.split(' ', 1)
            if auth_type.lower() != 'bearer':
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Authorization type must be Bearer'
                }), 401
        except ValueError:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid Authorization header format'
            }), 401

        if token != Config.APP_ALLOWED_BEARER:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid token'
            }), 401

        return f(*args, **kwargs)

    return decorated_function
