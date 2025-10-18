#!/bin/bash

# Script de instalación de dependencias para Blacklist Microservice
# Soluciona problemas de conectividad con PyPI

echo "🚀 Instalando dependencias del Blacklist Microservice..."

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar conectividad con PyPI
echo "🌐 Verificando conectividad con PyPI..."
if curl -s --connect-timeout 10 https://pypi.org/simple/ > /dev/null; then
    echo "✅ Conectividad con PyPI OK"
    PYPI_URL="https://pypi.org/simple/"
else
    echo "⚠️  Problemas de conectividad con PyPI, usando configuración alternativa"
    PYPI_URL="https://pypi.org/simple/"
fi

# Instalar dependencias con diferentes estrategias
echo "📥 Instalando dependencias..."

# Estrategia 1: Instalación normal
if pip install --index-url $PYPI_URL --timeout 60 --retries 3 -r requirements.txt; then
    echo "✅ Instalación exitosa con PyPI oficial"
else
    echo "⚠️  Falló instalación normal, intentando estrategia alternativa..."

    # Estrategia 2: Instalación individual
    echo "📦 Instalando dependencias individualmente..."

    packages=(
        "Flask==1.1.4"
        "Flask-SQLAlchemy==2.5.1"
        "Flask-Marshmallow==0.14.0"
        "Flask-JWT-Extended==3.25.1"
        "Flask-RESTful==0.3.9"
        "marshmallow==3.13.0"
        "psycopg2-binary==2.9.3"
        "gunicorn==20.1.0"
        "python-dotenv==0.19.2"
        "Werkzeug==1.0.1"
    )

    for package in "${packages[@]}"; do
        echo "Instalando $package..."
        if ! pip install --index-url $PYPI_URL --timeout 60 --retries 3 "$package"; then
            echo "❌ Error instalando $package"
            echo "🔄 Intentando sin versión específica..."
            package_name=$(echo $package | cut -d'=' -f1)
            pip install --index-url $PYPI_URL --timeout 60 --retries 3 "$package_name"
        fi
    done
fi

# Verificar instalación
echo "🔍 Verificando instalación..."
python -c "import flask; print('✅ Flask instalado correctamente')" 2>/dev/null || echo "❌ Error con Flask"
python -c "import flask_sqlalchemy; print('✅ Flask-SQLAlchemy instalado correctamente')" 2>/dev/null || echo "❌ Error con Flask-SQLAlchemy"

echo "🎉 Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. source venv/bin/activate"
echo "2. export DATABASE_URL='sqlite:///blacklist.db'"
echo "3. export APP_ALLOWED_BEARER='dev-bearer-token'"
echo "4. python start_dev.py"
echo ""
echo "🧪 Para probar:"
echo "python test_local.py"
