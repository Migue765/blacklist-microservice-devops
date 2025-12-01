# Multi-stage build para optimizar el tamaño de la imagen
FROM public.ecr.aws/docker/library/python:3.11-slim AS builder

# Variables de entorno para optimizar Python en contenedores
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias necesarias para compilar psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --user -r requirements.txt

# Etapa final
FROM public.ecr.aws/docker/library/python:3.11-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH

# New Relic environment variables
ENV NEW_RELIC_APP_NAME="blacklist-microservice" \
    NEW_RELIC_LOG=stdout \
    NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true \
    NEW_RELIC_LICENSE_KEY=01591B20C0FFADDA87E9C64F9CDD2B757B123ACD84F77EE29BAF5D3FA06B256A \
    NEW_RELIC_LOG_LEVEL=info

# Instalar solo la librería runtime de PostgreSQL y curl para health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias de la etapa builder al home del usuario appuser
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# Copiar y hacer ejecutable el script de inicio
COPY --chown=appuser:appuser start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Cambiar al usuario no-root
USER appuser

# Exponer puerto (usa variable PORT o 5000 por defecto)
EXPOSE 5000

# Comando para ejecutar la aplicación usando el script de inicio
CMD ["/app/start.sh"]

