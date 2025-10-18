#!/usr/bin/env python3
"""
Script de prueba local para el microservicio de blacklist
Ejecutar: python test_local.py
"""

import os
import sys
import requests
import json
from datetime import datetime

# Configuración local
BASE_URL = "http://localhost:5000"
TOKEN = "dev-bearer-token"

def test_health_check():
    """Probar endpoint de health check"""
    print("🔍 Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/ping")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_add_to_blacklist():
    """Probar agregar email a lista negra"""
    print("\n📧 Probando agregar email a lista negra...")

    test_data = {
        "email": f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "blocked_reason": "Test spam detection"
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{BASE_URL}/blacklists",
                               json=test_data,
                               headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201, test_data["email"]
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

def test_check_blacklist(email):
    """Probar verificar email en lista negra"""
    print(f"\n🔍 Probando verificar email {email}...")

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
        response = requests.get(f"{BASE_URL}/blacklists/{email}",
                              headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_unauthorized():
    """Probar acceso sin token"""
    print("\n🚫 Probando acceso sin token...")

    test_data = {
        "email": "unauthorized@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000"
    }

    try:
        response = requests.post(f"{BASE_URL}/blacklists",
                               json=test_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 401
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🧪 Iniciando pruebas del microservicio de blacklist")
    print("=" * 50)

    # Verificar que el servidor esté corriendo
    if not test_health_check():
        print("\n❌ El servidor no está corriendo. Ejecuta:")
        print("   python -m flask run")
        print("   o")
        print("   gunicorn app.wsgi:app")
        sys.exit(1)

    # Ejecutar pruebas
    tests_passed = 0
    total_tests = 4

    if test_health_check():
        tests_passed += 1
        print("✅ Health check: PASSED")
    else:
        print("❌ Health check: FAILED")

    success, email = test_add_to_blacklist()
    if success:
        tests_passed += 1
        print("✅ Add to blacklist: PASSED")
    else:
        print("❌ Add to blacklist: FAILED")

    if email and test_check_blacklist(email):
        tests_passed += 1
        print("✅ Check blacklist: PASSED")
    else:
        print("❌ Check blacklist: FAILED")

    if test_unauthorized():
        tests_passed += 1
        print("✅ Unauthorized access: PASSED")
    else:
        print("❌ Unauthorized access: FAILED")

    # Resumen
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {tests_passed}/{total_tests} pruebas pasaron")

    if tests_passed == total_tests:
        print("🎉 ¡Todas las pruebas pasaron!")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa la configuración.")

if __name__ == "__main__":
    main()
