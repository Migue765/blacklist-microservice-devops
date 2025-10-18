#!/usr/bin/env python3
"""
Script simple para probar la aplicación localmente
"""

import os
import sys
from app import create_app

# Configurar variables de entorno
os.environ['DATABASE_URL'] = 'sqlite:///blacklist.db'
os.environ['APP_ALLOWED_BEARER'] = 'dev-bearer-token'
os.environ['FLASK_ENV'] = 'development'

def test_app():
    """Probar que la aplicación se crea correctamente"""
    try:
        app = create_app()
        print("✅ Aplicación creada correctamente")

        # Probar health check
        with app.test_client() as client:
            response = client.get('/ping')
            print(f"🔍 Health Check Status: {response.status_code}")
            print(f"📄 Response: {response.get_json()}")

            if response.status_code == 200:
                print("✅ Health check funcionando correctamente")
            else:
                print("❌ Health check falló")

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Probando aplicación...")
    success = test_app()

    if success:
        print("\n🎉 ¡Aplicación funcionando correctamente!")
        print("📍 Para ejecutar el servidor:")
        print("   python start_dev.py")
    else:
        print("\n❌ Error en la aplicación")
        sys.exit(1)
