"""
Tests unitarios para el endpoint GET /blacklists/<email>
Ejecutar con: pytest test_blacklist_get.py -v
"""

import pytest
import json
from datetime import datetime
from app import create_app, db
from app.models import Blacklist


@pytest.fixture
def app():
    """Crear aplicación de prueba"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Headers con autenticación"""
    return {
        'Authorization': 'Bearer dev-bearer-token',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_blacklist_entry(app):
    """Crear entrada de prueba en blacklist"""
    with app.app_context():
        entry = Blacklist(
            email='blacklisted@example.com',
            app_uuid='123e4567-e89b-12d3-a456-426614174000',
            blocked_reason='Spam detected',
            client_ip='127.0.0.1'
        )
        db.session.add(entry)
        db.session.commit()
        return entry.email


class TestGetBlacklistEndpoint:
    """Suite de tests para GET /blacklists/<email>"""
    
    def test_get_blacklisted_email_returns_true(self, client, auth_headers, sample_blacklist_entry):
        """
        TEST 1: Verificar que un email en blacklist retorna is_blacklisted=True
        """
        # Arrange
        email = sample_blacklist_entry
        
        # Act
        response = client.get(
            f'/blacklists/{email}',
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['email'] == email
        assert data['is_blacklisted'] is True
        assert data['blocked_reason'] == 'Spam detected'
    
    
    def test_get_non_blacklisted_email_returns_false(self, client, auth_headers):
        """
        TEST 2: Verificar que un email NO en blacklist retorna is_blacklisted=False
        """
        # Arrange
        email = 'notfound@example.com'
        
        # Act
        response = client.get(
            f'/blacklists/{email}',
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['email'] == email.lower()
        assert data['is_blacklisted'] is False
        assert data['blocked_reason'] is None
    
    
    def test_get_without_authorization_returns_401(self, client):
        """
        TEST 3: Verificar que sin token retorna 401 Unauthorized
        """
        # Arrange
        email = 'test@example.com'
        
        # Act
        response = client.get(f'/blacklists/{email}')
        
        # Assert
        assert response.status_code == 401
        data = json.loads(response.data)
        
        assert data['error'] == 'Unauthorized'
        assert 'message' in data
    
    
    def test_get_with_invalid_token_returns_401(self, client):
        """
        TEST 4: Verificar que con token inválido retorna 401
        """
        # Arrange
        email = 'test@example.com'
        headers = {'Authorization': 'Bearer invalid-token'}
        
        # Act
        response = client.get(
            f'/blacklists/{email}',
            headers=headers
        )
        
        # Assert
        assert response.status_code == 401
        data = json.loads(response.data)
        
        assert data['error'] == 'Unauthorized'
    
    
    def test_get_with_invalid_email_format_returns_400(self, client, auth_headers):
        """
        TEST 5: Verificar que email sin @ retorna 400 Bad Request
        """
        # Arrange
        invalid_email = 'not-an-email'
        
        # Act
        response = client.get(
            f'/blacklists/{invalid_email}',
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert data['error'] == 'Bad Request'
        assert 'Invalid email format' in data['message']
    
    
    def test_get_email_case_insensitive(self, client, auth_headers, sample_blacklist_entry):
        """
        TEST 6: Verificar que la búsqueda es case-insensitive
        """
        # Arrange
        email_uppercase = sample_blacklist_entry.upper()
        
        # Act
        response = client.get(
            f'/blacklists/{email_uppercase}',
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['is_blacklisted'] is True
        assert data['blocked_reason'] == 'Spam detected'
    
    
    def test_get_response_structure(self, client, auth_headers):
        """
        TEST 7: Verificar estructura correcta de la respuesta
        """
        # Arrange
        email = 'structure-test@example.com'
        
        # Act
        response = client.get(
            f'/blacklists/{email}',
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verificar que tiene todos los campos requeridos
        assert 'email' in data
        assert 'is_blacklisted' in data
        assert 'blocked_reason' in data
        
        # Verificar tipos de datos
        assert isinstance(data['email'], str)
        assert isinstance(data['is_blacklisted'], bool)
        assert data['blocked_reason'] is None or isinstance(data['blocked_reason'], str)


class TestGetBlacklistIntegration:
    """Tests de integración para el flujo completo"""
    
    def test_post_then_get_email(self, client, auth_headers):
        """
        TEST 8: Flujo completo - POST y luego GET del mismo email
        """
        # Arrange
        email = f'integration-{datetime.now().strftime("%Y%m%d%H%M%S")}@example.com'
        post_data = {
            'email': email,
            'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'blocked_reason': 'Integration test'
        }
        
        # Act - POST
        post_response = client.post(
            '/blacklists',
            data=json.dumps(post_data),
            headers=auth_headers
        )
        
        # Assert POST
        assert post_response.status_code == 201
        
        # Act - GET
        get_response = client.get(
            f'/blacklists/{email}',
            headers=auth_headers
        )
        
        # Assert GET
        assert get_response.status_code == 200
        data = json.loads(get_response.data)
        
        assert data['email'] == email
        assert data['is_blacklisted'] is True
        assert data['blocked_reason'] == 'Integration test'
    
    
    def test_multiple_emails_in_blacklist(self, client, auth_headers, app):
        """
        TEST 9: Verificar múltiples emails en blacklist
        """
        # Arrange - Agregar múltiples emails
        emails = [
            'user1@example.com',
            'user2@example.com',
            'user3@example.com'
        ]
        
        with app.app_context():
            for email in emails:
                entry = Blacklist(
                    email=email,
                    app_uuid='123e4567-e89b-12d3-a456-426614174000',
                    blocked_reason=f'Reason for {email}',
                    client_ip='127.0.0.1'
                )
                db.session.add(entry)
            db.session.commit()
        
        # Act & Assert - Verificar cada uno
        for email in emails:
            response = client.get(
                f'/blacklists/{email}',
                headers=auth_headers
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert data['email'] == email
            assert data['is_blacklisted'] is True
            assert f'Reason for {email}' in data['blocked_reason']


class TestGetBlacklistEdgeCases:
    """Tests de casos especiales y límites"""
    
    def test_get_with_special_characters_in_email(self, client, auth_headers):
        """
        TEST 10: Email con caracteres especiales
        """
        # Arrange
        email = 'user+test@example.com'
        
        # Act
        response = client.get(
            f'/blacklists/{email}',
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'email' in data
    
    
    def test_get_empty_email_returns_404(self, client, auth_headers):
        """
        TEST 11: Email vacío debe retornar 404
        """
        # Act
        response = client.get(
            '/blacklists/',
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 404
    
    
    def test_get_with_bearer_token_lowercase(self, client, sample_blacklist_entry):
        """
        TEST 12: Bearer token en minúsculas debe funcionar
        """
        # Arrange
        email = sample_blacklist_entry
        headers = {'Authorization': 'bearer dev-bearer-token'}
        
        # Act
        response = client.get(
            f'/blacklists/{email}',
            headers=headers
        )
        
        # Assert
        assert response.status_code == 200


# Configuración de pytest
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])