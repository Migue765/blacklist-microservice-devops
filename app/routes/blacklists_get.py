from flask import Blueprint, jsonify
from app import db
from app.models import Blacklist
from app.auth import require_bearer_token
from app.utils import setup_logging

# Blueprint para el endpoint GET (pendiente por Nata)
blacklists_get_bp = Blueprint('blacklists_get', __name__)
logger = setup_logging()

@blacklists_get_bp.route('/<email>', methods=['GET'])
@require_bearer_token
def check_blacklist(email):
    """
    Check if an email is in the blacklist

    Path Parameters:
        email: Email address to check

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: Email status with details
        401: Unauthorized
        404: Email not found in blacklist

    Response Shape:
        {
            "email": "user@example.com",
            "is_blacklisted": true/false,
            "reason": "blocked reason or null"
        }

    TODO: Implementar por Nata en rama feature/nata-get-endpoint
    - Validación de formato de email
    - Manejo de errores específicos
    - Pruebas unitarias completas
    - Documentación de API actualizada
    """
    # TODO: Implementar lógica completa
    # Por ahora retorna respuesta mock para evitar errores
    return jsonify({
        'email': email,
        'is_blacklisted': False,
        'reason': None,
        'status': 'pending_implementation'
    }), 200

# TODO: Agregar pruebas unitarias cuando se implemente
# def test_check_blacklist_success():
#     """Test successful blacklist check"""
#     pass
#
# def test_check_blacklist_not_found():
#     """Test blacklist check when email not found"""
#     pass
#
# def test_check_blacklist_unauthorized():
#     """Test blacklist check without proper auth"""
#     pass
