#!/usr/bin/env python3
"""
Test para verificar que el GET endpoint está deshabilitado
"""

import requests

def test_get_disabled():
    """Verificar que GET /blacklists/<email> retorna 404"""
    print("🔍 Probando que GET está deshabilitado...")

    headers = {
        "Authorization": "Bearer dev-bearer-token"
    }

    try:
        response = requests.get("http://localhost:5001/blacklists/test@example.com",
                              headers=headers,
                              timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")

        # Debería retornar 404 (Not Found) porque la ruta no existe
        if response.status_code == 404:
            print("✅ GET endpoint correctamente deshabilitado")
            return True
        else:
            print("❌ GET endpoint aún está activo (no debería estar)")
            return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Verificando que GET está deshabilitado...")
    print("=" * 50)

    success = test_get_disabled()

    if success:
        print("\n🎉 GET endpoint correctamente deshabilitado")
    else:
        print("\n❌ GET endpoint aún está activo")
