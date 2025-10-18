#!/usr/bin/env python3
"""
Script de inicio para desarrollo en PyCharm
Ejecutar este archivo para iniciar el servidor de desarrollo
"""

import os
import sys
from pathlib import Path

# Configurar variables de entorno
os.environ['DATABASE_URL'] = 'sqlite:///blacklist.db'
os.environ['JWT_SECRET'] = 'dev-secret-key'
os.environ['APP_ALLOWED_BEARER'] = 'dev-bearer-token'
os.environ['FLASK_ENV'] = 'development'
os.environ['PORT'] = '5000'
os.environ['LOG_LEVEL'] = 'INFO'

# Agregar directorio app al path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

# Importar y ejecutar la aplicación
if __name__ == "__main__":
    from app import create_app

    port = int(os.environ.get('PORT', 5000))

    print("🚀 Iniciando Blacklist Microservice...")
    print(f"📍 URL: http://localhost:{port}")
    print(f"🔍 Health Check: http://localhost:{port}/ping")
    print("📧 API Docs: Ver README.md")
    print("🛑 Presiona Ctrl+C para detener")
    print("-" * 50)

    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=True)
