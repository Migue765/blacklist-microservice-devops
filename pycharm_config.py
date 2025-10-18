#!/usr/bin/env python3
"""
Configuración específica para PyCharm
Ejecutar este archivo para configurar el entorno local
"""

import os
import sys
from pathlib import Path

def setup_pycharm_environment():
    """Configurar variables de entorno para PyCharm"""

    # Variables de entorno para desarrollo local
    env_vars = {
        'DATABASE_URL': 'sqlite:///blacklist.db',
        'JWT_SECRET': 'dev-secret-key',
        'APP_ALLOWED_BEARER': 'dev-bearer-token',
        'FLASK_ENV': 'development',
        'FLASK_APP': 'app/wsgi.py',
        'PORT': '5000',
        'LOG_LEVEL': 'INFO'
    }

    print("🔧 Configurando entorno para PyCharm...")

    # Establecer variables de entorno
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"✅ {key} = {value}")

    # Agregar el directorio app al path de Python
    app_dir = Path(__file__).parent / 'app'
    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))
        print(f"✅ Agregado al PYTHONPATH: {app_dir}")

    print("\n🚀 Entorno configurado correctamente!")
    print("Ahora puedes ejecutar la aplicación desde PyCharm")

    return True

if __name__ == "__main__":
    setup_pycharm_environment()
