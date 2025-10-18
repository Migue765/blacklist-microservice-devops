#!/usr/bin/env python3
"""
Script completo para probar la API del microservicio
"""

import os
import sys
import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5001"
TOKEN = "dev-bearer-token"

def test_health_check():
    """Probar health check"""
    print("🔍 Probando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/ping", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_add_to_blacklist():
    """Probar agregar email a lista negra"""
    print("\n📧 Probando Agregar a Lista Negra...")

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
                               headers=headers,
                               timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 201, test_data["email"]
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def test_check_blacklist(email):
    """Probar verificar email en lista negra"""
    print(f"\n🔍 Probando Verificar Email: {email}")

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
        response = requests.get(f"{BASE_URL}/blacklists/{email}",
                              headers=headers,
                              timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_unauthorized():
    """Probar acceso sin token"""
    print("\n🚫 Probando Acceso Sin Token...")

    test_data = {
        "email": "unauthorized@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000"
    }

    try:
        response = requests.post(f"{BASE_URL}/blacklists",
                               json=test_data,
                               timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 401
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Blacklist Microservice - Pruebas de API")
    print("=" * 50)

    # Verificar que el servidor esté corriendo
    print("🔍 Verificando servidor...")
    try:
        response = requests.get(f"{BASE_URL}/ping", timeout=2)
        if response.status_code != 200:
            print("❌ El servidor no está respondiendo correctamente")
            print("💡 Ejecuta: python run_server.py")
            sys.exit(1)
    except Exception as e:
        print("❌ No se puede conectar al servidor")
        print("💡 Ejecuta: python run_server.py")
        sys.exit(1)

    print("✅ Servidor funcionando correctamente")

    # Ejecutar pruebas
    tests_passed = 0
    total_tests = 4

    if test_health_check():
        tests_passed += 1
        print("✅ Health Check: PASSED")
    else:
        print("❌ Health Check: FAILED")

    success, email = test_add_to_blacklist()
    if success:
        tests_passed += 1
        print("✅ Add to Blacklist: PASSED")
    else:
        print("❌ Add to Blacklist: FAILED")

    if email and test_check_blacklist(email):
        tests_passed += 1
        print("✅ Check Blacklist: PASSED")
    else:
        print("❌ Check Blacklist: FAILED")

    if test_unauthorized():
        tests_passed += 1
        print("✅ Unauthorized Access: PASSED")
    else:
        print("❌ Unauthorized Access: FAILED")

    # Resumen
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {tests_passed}/{total_tests} pruebas pasaron")

    if tests_passed == total_tests:
        print("🎉 ¡Todas las pruebas pasaron!")
        print("✅ El microservicio está funcionando correctamente")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("🔍 Revisa los logs del servidor para más detalles")

if __name__ == "__main__":
    main()
