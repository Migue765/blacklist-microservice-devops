#!/usr/bin/env python3
"""
Script para ejecutar el servidor de desarrollo
"""

import os
import sys
from app import create_app

def main():
    """Función principal para ejecutar el servidor"""

    # Configurar variables de entorno
    os.environ['DATABASE_URL'] = 'sqlite:///blacklist.db'
    os.environ['APP_ALLOWED_BEARER'] = 'dev-bearer-token'
    os.environ['FLASK_ENV'] = 'development'

    # Crear aplicación
    app = create_app()

    print("🚀 Blacklist Microservice - Servidor de Desarrollo")
    print("=" * 50)
    print("📍 URL: http://localhost:5001")
    print("🔍 Health Check: http://localhost:5001/ping")
    print("📧 API Base: http://localhost:5001/blacklists")
    print("🔑 Token: dev-bearer-token")
    print("=" * 50)
    print("🛑 Presiona Ctrl+C para detener")
    print()

    try:
        # Ejecutar servidor
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=True,
            use_reloader=False  # Evitar problemas con el reloader
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido correctamente")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
