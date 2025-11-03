# 🐳 Docker Commands - Blacklist Microservice

## Variables de entorno
```bash
export AWS_ACCOUNT_ID="153641554973"
export AWS_REGION="us-west-2"
export ECR_REPOSITORY="blacklist-api"
export ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY"
```

## 1. Autenticación con ECR
```bash
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 153641554973.dkr.ecr.us-west-2.amazonaws.com
```

## 2. Construir la imagen
```bash
docker build -t blacklist-api .
```

## 3. Etiquetar la imagen
```bash
docker tag blacklist-api:latest 153641554973.dkr.ecr.us-west-2.amazonaws.com/blacklist-api:latest
```

## 4. Push a ECR
```bash
docker push 153641554973.dkr.ecr.us-west-2.amazonaws.com/blacklist-api:latest
```

## 5. Ejecutar localmente (testing)
```bash
# Con variables de entorno desde archivo .env
docker run -p 8000:8000 --env-file .env blacklist-api:latest

# O directamente
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e BEARER_TOKEN="dev-bearer-token" \
  -e JWT_SECRET_KEY="your-secret-key" \
  blacklist-api:latest
```

## 6. Verificar salud del contenedor
```bash
curl http://localhost:8000/health
curl http://localhost:8000/ping
```

## 7. Ver logs
```bash
docker logs <container-id> -f
```

## 8. Comandos útiles

### Listar imágenes
```bash
docker images | grep blacklist-api
```

### Limpiar imágenes antiguas
```bash
docker image prune -a
```

### Inspeccionar imagen
```bash
docker inspect blacklist-api:latest
```

### Ver contenedores corriendo
```bash
docker ps
```

### Detener contenedor
```bash
docker stop <container-id>
```

## 🚀 Pipeline Automático

El pipeline en CodeBuild hace todo esto automáticamente:
1. ✅ Ejecuta tests unitarios
2. 🔐 Se autentica con ECR
3. 🏗️ Construye la imagen Docker
4. 🏷️ Etiqueta con `latest` y commit hash
5. ⬆️ Sube a ECR
6. 📦 Genera `imagedefinitions.json` para deploy

## 📝 Notas
- La imagen usa Python 3.11 slim para optimizar tamaño
- Multi-stage build para reducir capas
- Usuario no-root para seguridad
- Health check integrado
- Logs a stdout/stderr para CloudWatch

