#!/bin/bash

# Script de ayuda para dockerización del proyecto Blacklist Microservice
# Uso: ./docker-deploy.sh [comando]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración (ajustar según tu AWS)
AWS_REGION=${AWS_DEFAULT_REGION:-"us-west-2"}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-"153641554973"}
IMAGE_REPO_NAME="blacklist-api"
IMAGE_TAG="latest"

function print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

function print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

function print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

function check_aws_account() {
    if [ -z "$AWS_ACCOUNT_ID" ]; then
        print_info "Obteniendo AWS Account ID..."
        AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        print_info "AWS Account ID: $AWS_ACCOUNT_ID"
    fi
}

function build_local() {
    print_info "Construyendo imagen Docker localmente..."
    docker build -t blacklist-api:latest .
    print_info "✅ Imagen construida exitosamente: blacklist-api:latest"
}

function run_local() {
    print_info "Ejecutando contenedor localmente..."
    docker run -d \
        -p 8000:8000 \
        --name blacklist-app-local \
        -e DATABASE_URL="postgresql+psycopg2://postgres:postgres123@host.docker.internal:5432/blacklist_db" \
        -e JWT_SECRET="dev-jwt-secret" \
        -e APP_ALLOWED_BEARER="dev-bearer-token" \
        -e FLASK_ENV="development" \
        blacklist-api:latest
    
    print_info "✅ Contenedor ejecutándose en http://localhost:8000"
    print_info "Ver logs: docker logs -f blacklist-app-local"
    print_info "Detener: docker stop blacklist-app-local && docker rm blacklist-app-local"
}

function compose_up() {
    print_info "Levantando servicios con Docker Compose..."
    docker-compose up --build -d
    print_info "✅ Servicios levantados"
    print_info "Ver logs: docker-compose logs -f"
    print_info "Detener: docker-compose down"
}

function compose_down() {
    print_info "Deteniendo servicios Docker Compose..."
    docker-compose down
    print_info "✅ Servicios detenidos"
}

function test_health() {
    print_info "Probando health check..."
    sleep 3
    response=$(curl -s http://localhost:8000/ping || echo "error")
    
    if [ "$response" == "pong" ]; then
        print_info "✅ Health check exitoso: $response"
    else
        print_error "❌ Health check falló: $response"
        exit 1
    fi
}

function create_ecr_repo() {
    check_aws_account
    print_info "Creando repositorio ECR: $IMAGE_REPO_NAME"
    
    aws ecr create-repository \
        --repository-name $IMAGE_REPO_NAME \
        --region $AWS_REGION \
        --image-scanning-configuration scanOnPush=true \
        || print_warning "Repositorio ya existe o error al crear"
    
    print_info "✅ Repositorio ECR listo"
}

function ecr_login() {
    check_aws_account
    print_info "Login a Amazon ECR..."
    
    aws ecr get-login-password --region $AWS_REGION | \
        docker login --username AWS --password-stdin \
        $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
    
    print_info "✅ Login exitoso a ECR"
}

function push_to_ecr() {
    check_aws_account
    ecr_login
    
    REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE_REPO_NAME
    
    print_info "Construyendo imagen..."
    docker build -t blacklist-api:latest .
    
    print_info "Taggeando imagen para ECR..."
    docker tag blacklist-api:latest $REPOSITORY_URI:latest
    docker tag blacklist-api:latest $REPOSITORY_URI:$(git rev-parse --short HEAD)
    
    print_info "Pushing a ECR..."
    docker push $REPOSITORY_URI:latest
    docker push $REPOSITORY_URI:$(git rev-parse --short HEAD)
    
    print_info "✅ Imagen subida a ECR: $REPOSITORY_URI:latest"
}

function update_dockerrun() {
    check_aws_account
    REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE_REPO_NAME
    
    print_info "Actualizando Dockerrun.aws.json..."
    
    cat > Dockerrun.aws.json << EOF
{
  "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "$REPOSITORY_URI:$IMAGE_TAG",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": 8000,
      "HostPort": 80
    }
  ],
  "Logging": "/var/log/nginx"
}
EOF
    
    print_info "✅ Dockerrun.aws.json actualizado"
}

function show_help() {
    cat << EOF
🐳 Script de Dockerización - Blacklist Microservice

Uso: ./docker-deploy.sh [comando]

Comandos disponibles:

  Desarrollo Local:
    build              Construir imagen Docker localmente
    run                Ejecutar contenedor localmente
    compose-up         Levantar servicios con docker-compose
    compose-down       Detener servicios docker-compose
    test               Probar health check
    logs               Ver logs de docker-compose

  AWS ECR:
    create-repo        Crear repositorio en Amazon ECR
    login              Login a Amazon ECR
    push               Construir y subir imagen a ECR
    update-dockerrun   Actualizar Dockerrun.aws.json con tu Account ID

  Completo:
    deploy             Build + Push + Update Dockerrun
    setup-aws          Crear repo + Login (primera vez)

  Otros:
    help               Mostrar esta ayuda

Variables de entorno:
  AWS_ACCOUNT_ID       Tu AWS Account ID (se obtiene automáticamente si no está)
  AWS_DEFAULT_REGION   Región AWS (default: us-west-2)

Ejemplos:
  ./docker-deploy.sh build
  ./docker-deploy.sh compose-up
  ./docker-deploy.sh push
  AWS_ACCOUNT_ID=123456789012 ./docker-deploy.sh deploy

EOF
}

function logs() {
    docker-compose logs -f
}

function deploy() {
    build_local
    push_to_ecr
    update_dockerrun
    print_info "✅ Deploy completado. Ahora puedes subir los cambios y CodeBuild desplegará automáticamente."
}

function setup_aws() {
    create_ecr_repo
    ecr_login
    print_info "✅ Setup de AWS completado"
}

# Main script
case "${1:-help}" in
    build)
        build_local
        ;;
    run)
        run_local
        ;;
    compose-up)
        compose_up
        ;;
    compose-down)
        compose_down
        ;;
    test)
        test_health
        ;;
    logs)
        logs
        ;;
    create-repo)
        create_ecr_repo
        ;;
    login)
        ecr_login
        ;;
    push)
        push_to_ecr
        ;;
    update-dockerrun)
        update_dockerrun
        ;;
    deploy)
        deploy
        ;;
    setup-aws)
        setup_aws
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Comando desconocido: $1"
        show_help
        exit 1
        ;;
esac

