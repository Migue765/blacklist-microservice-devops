#!/bin/bash

# Script para hacer push manual de la imagen Docker a ECR
# Basado en las instrucciones de AWS ECR

set -e

# Configuración de tu repositorio ECR
AWS_REGION="us-west-2"
AWS_ACCOUNT_ID="153641554973"
ECR_REPO="blacklist-api"
REPOSITORY_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

echo "🐳 Push Manual a ECR - Blacklist Microservice"
echo "=============================================="
echo ""
echo "Repositorio: ${REPOSITORY_URI}"
echo "Región: ${AWS_REGION}"
echo ""

# Paso 1: Login a ECR
echo "📝 Paso 1: Autenticando en Amazon ECR..."
aws ecr get-login-password --region ${AWS_REGION} | \
    docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

if [ $? -eq 0 ]; then
    echo "✅ Login exitoso a ECR"
else
    echo "❌ Error en login a ECR"
    exit 1
fi

echo ""

# Paso 2: Build de la imagen
echo "🔨 Paso 2: Construyendo imagen Docker..."
docker build -t blacklist-api .

if [ $? -eq 0 ]; then
    echo "✅ Imagen construida exitosamente"
else
    echo "❌ Error al construir la imagen"
    exit 1
fi

echo ""

# Paso 3: Etiquetar la imagen
echo "🏷️  Paso 3: Etiquetando imagen..."
docker tag blacklist-api:latest ${REPOSITORY_URI}:latest

# Crear tag con git commit hash si existe
if git rev-parse --short HEAD > /dev/null 2>&1; then
    COMMIT_HASH=$(git rev-parse --short HEAD)
    docker tag blacklist-api:latest ${REPOSITORY_URI}:${COMMIT_HASH}
    echo "✅ Imagen etiquetada como: latest y ${COMMIT_HASH}"
else
    echo "✅ Imagen etiquetada como: latest"
fi

echo ""

# Paso 4: Push a ECR
echo "📤 Paso 4: Enviando imagen a ECR..."
docker push ${REPOSITORY_URI}:latest

if [ $? -eq 0 ]; then
    echo "✅ Imagen enviada exitosamente a ECR"
else
    echo "❌ Error al enviar la imagen"
    exit 1
fi

# Push del tag con commit hash si existe
if [ ! -z "$COMMIT_HASH" ]; then
    echo "📤 Enviando también tag con commit hash..."
    docker push ${REPOSITORY_URI}:${COMMIT_HASH}
fi

echo ""
echo "🎉 ¡Proceso completado exitosamente!"
echo ""
echo "📋 Imagen disponible en:"
echo "   ${REPOSITORY_URI}:latest"
if [ ! -z "$COMMIT_HASH" ]; then
    echo "   ${REPOSITORY_URI}:${COMMIT_HASH}"
fi
echo ""
echo "🔍 Verificar en AWS Console:"
echo "   https://console.aws.amazon.com/ecr/repositories/private/${AWS_ACCOUNT_ID}/${ECR_REPO}?region=${AWS_REGION}"
echo ""
echo "📦 Siguiente paso: Desplegar en Elastic Beanstalk"
echo "   - Asegúrate de que tu ambiente EB esté configurado con plataforma Docker"
echo "   - Verifica que el Instance Profile tenga permisos de ECR"
echo "   - Haz push de tu código y CodeBuild desplegará automáticamente"
echo ""

