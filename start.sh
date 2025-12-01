#!/bin/bash
set -e

# Configurar puerto
PORT=${PORT:-5000}

# Verificar si New Relic está disponible y configurado
if command -v newrelic-admin >/dev/null 2>&1 && [ -n "$NEW_RELIC_LICENSE_KEY" ]; then
    echo "Starting application with New Relic monitoring..."
    exec newrelic-admin run-program gunicorn \
        --bind "0.0.0.0:${PORT}" \
        --workers 3 \
        --timeout 60 \
        --access-logfile - \
        --error-logfile - \
        application:application
else
    echo "Warning: New Relic not available, starting without monitoring..."
    exec gunicorn \
        --bind "0.0.0.0:${PORT}" \
        --workers 3 \
        --timeout 60 \
        --access-logfile - \
        --error-logfile - \
        application:application
fi

