# 🐳 Guía de Dockerización - Blacklist Microservice

## 📋 Cambios Realizados

### Archivos Creados/Modificados:
1. **Dockerfile** - Imagen Docker de la aplicación
2. **.dockerignore** - Optimización del build Docker
3. **buildspec.yml** - Pipeline CodeBuild con Docker + ECR
4. **Dockerrun.aws.json** - Configuración Elastic Beanstalk Docker
5. **docker-compose.yml** - Desarrollo local con Docker
6. **DOCKER_SETUP.md** - Esta guía

---

## 🚀 Configuración AWS (Paso a Paso)

### 1. Crear Repositorio ECR (Elastic Container Registry)

```bash
# Opción A: Desde AWS CLI
aws ecr create-repository \
    --repository-name blacklist-microservice \
    --region us-west-2

# Opción B: El buildspec.yml lo creará automáticamente
```

**En la Consola AWS:**
1. Ve a **Amazon ECR** → **Repositories**
2. Click en **Create repository**
3. Nombre: `blacklist-microservice`
4. Configuración: Por defecto (privado)
5. **Create repository**

### 2. Configurar CodeBuild con Docker

**Actualizar el Proyecto CodeBuild:**

1. Ve a **AWS CodeBuild** → Tu proyecto
2. Click en **Edit** → **Environment**

**Configuración de Environment:**
```yaml
Environment image: Managed image
Operating system: Ubuntu
Runtime: Standard
Image: aws/codebuild/standard:7.0
Image version: Always use latest
Environment type: Linux
Privileged: ✅ ACTIVAR (OBLIGATORIO para Docker)
```

**⚠️ IMPORTANTE:** Debes marcar **"Enable this flag if you want to build Docker images"**

### 3. Configurar Variables de Entorno en CodeBuild

**Opción A: En CodeBuild directamente**
1. Ve a tu proyecto CodeBuild → **Edit** → **Environment**
2. Agrega en **Environment variables**:

```
AWS_DEFAULT_REGION = us-west-2
AWS_ACCOUNT_ID = 123456789012  (tu Account ID)
IMAGE_REPO_NAME = blacklist-microservice
```

**Opción B: En buildspec.yml** (Ya configurado)
```yaml
env:
  variables:
    AWS_DEFAULT_REGION: "us-west-2"
    AWS_ACCOUNT_ID: "123456789012"  # Reemplazar
    IMAGE_REPO_NAME: "blacklist-microservice"
```

### 4. Permisos IAM para CodeBuild

El **Service Role** de CodeBuild necesita estos permisos:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:DescribeRepositories",
        "ecr:CreateRepository"
      ],
      "Resource": "*"
    }
  ]
}
```

**Cómo agregarlo:**
1. Ve a **IAM** → **Roles**
2. Busca el rol de tu CodeBuild (ej: `codebuild-blacklist-service-role`)
3. Click en **Add permissions** → **Create inline policy**
4. Pega la policy de arriba
5. Nombre: `ECR-Docker-Access`
6. **Create policy**

### 5. Configurar Elastic Beanstalk para Docker

**Opción A: Crear nuevo ambiente con Docker**
```bash
eb init -p docker blacklist-microservice --region us-west-2
eb create blacklist-docker-env
```

**Opción B: Actualizar ambiente existente**

1. Ve a **Elastic Beanstalk** → Tu aplicación
2. **Create a new environment**
3. Environment tier: **Web server environment**
4. Platform: **Docker**
5. Platform branch: **Docker running on 64bit Amazon Linux 2023**
6. Application code: Upload `Dockerrun.aws.json`

**Variables de Entorno en EB:**
1. Ve a tu ambiente → **Configuration** → **Software** → **Edit**
2. Agrega:
```
DATABASE_URL = postgresql+psycopg2://user:pass@host:5432/db
JWT_SECRET = tu-secret-jwt
APP_ALLOWED_BEARER = tu-bearer-token
FLASK_ENV = production
```

### 6. Permisos EC2 para ECR (Elastic Beanstalk)

El **Instance Profile** (rol EC2) de Elastic Beanstalk necesita:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "*"
    }
  ]
}
```

**Cómo agregarlo:**
1. Ve a **IAM** → **Roles**
2. Busca `aws-elasticbeanstalk-ec2-role`
3. Si no existe, créalo con la policy de arriba
4. En tu ambiente EB → **Configuration** → **Security** → **IAM instance profile**
5. Selecciona `aws-elasticbeanstalk-ec2-role`

---

## 🔄 Pipeline Completo

### Flujo de Despliegue:

```
┌─────────────┐
│  Git Push   │
│   (GitHub)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CodeBuild  │──── Detecta cambios
│   (Build)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Docker Build│──── Construye imagen
│   + Push    │──── Sube a ECR
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Elastic   │──── Descarga imagen
│  Beanstalk  │──── Despliega container
└─────────────┘
```

### Verificar el buildspec.yml:

El archivo `buildspec.yml` hace esto:
1. **pre_build**: Login a ECR, crear repo si no existe
2. **build**: Construir imagen Docker
3. **post_build**: Push a ECR, generar `Dockerrun.aws.json`
4. **artifacts**: Entregar `Dockerrun.aws.json` a EB

---

## 💻 Desarrollo Local con Docker

### Iniciar la aplicación:
```bash
# Construir y levantar servicios
docker-compose up --build

# En segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f blacklist-app

# Detener
docker-compose down
```

### Probar la API:
```bash
# Health check
curl http://localhost:8000/ping

# Agregar email (requiere token)
curl -X POST http://localhost:8000/blacklists \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-bearer-token" \
  -d '{
    "email": "test@example.com",
    "app_uuid": "f2a1b8c9-7e6d-4d5b-9a8f-3a4b5c6d7e8f",
    "blocked_reason": "test"
  }'

# Consultar email
curl http://localhost:8000/blacklists/test@example.com \
  -H "Authorization: Bearer dev-bearer-token"
```

### Conectar a PostgreSQL local:
```bash
docker exec -it blacklist-postgres psql -U postgres -d blacklist_db
```

---

## 🔧 Comandos Útiles Docker

### Construcción y Testing:
```bash
# Construir imagen manualmente
docker build -t blacklist-microservice:local .

# Ejecutar solo el contenedor
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e JWT_SECRET="secret" \
  -e APP_ALLOWED_BEARER="token" \
  blacklist-microservice:local

# Inspeccionar imagen
docker images blacklist-microservice
docker inspect blacklist-microservice:local

# Ver logs del contenedor
docker logs blacklist-app -f
```

### ECR Manual (Opcional):
```bash
# Obtener Account ID
aws sts get-caller-identity --query Account --output text

# Login a ECR
aws ecr get-login-password --region us-west-2 | \
  docker login --username AWS --password-stdin \
  123456789012.dkr.ecr.us-west-2.amazonaws.com

# Tag y Push manual
docker tag blacklist-microservice:local \
  123456789012.dkr.ecr.us-west-2.amazonaws.com/blacklist-microservice:v1.0

docker push \
  123456789012.dkr.ecr.us-west-2.amazonaws.com/blacklist-microservice:v1.0
```

---

## 📝 Checklist de Configuración

### Antes de hacer push:
- [ ] Actualizar `AWS_ACCOUNT_ID` en `buildspec.yml`
- [ ] Actualizar `Dockerrun.aws.json` con tu ECR URI
- [ ] Verificar región en `buildspec.yml` (us-west-2)

### En AWS CodeBuild:
- [ ] Habilitar **Privileged mode** para Docker
- [ ] Agregar variables de entorno (AWS_ACCOUNT_ID, etc)
- [ ] Verificar permisos IAM del Service Role (ECR access)

### En AWS ECR:
- [ ] Crear repositorio `blacklist-microservice`
- [ ] Verificar región correcta (us-west-2)

### En AWS Elastic Beanstalk:
- [ ] Crear/actualizar ambiente con plataforma **Docker**
- [ ] Configurar variables de entorno (DATABASE_URL, JWT_SECRET, etc)
- [ ] Verificar Instance Profile tiene permisos ECR
- [ ] Cambiar Platform a **Docker running on 64bit Amazon Linux 2023**

### Testing:
- [ ] Probar build local: `docker build -t test .`
- [ ] Probar docker-compose: `docker-compose up`
- [ ] Verificar endpoints funcionan en local
- [ ] Hacer push y verificar CodeBuild logs
- [ ] Verificar imagen en ECR
- [ ] Verificar despliegue en EB

---

## 🐛 Troubleshooting

### Error: "Cannot connect to Docker daemon"
**Solución:** Habilitar **Privileged mode** en CodeBuild

### Error: "denied: User not authorized"
**Solución:** Verificar permisos IAM de ECR en el Service Role de CodeBuild

### Error: "EB health check failed"
**Solución:** 
- Verificar que el contenedor expone puerto 8000
- Verificar variables de entorno en EB
- Ver logs: `eb logs` o en consola EB

### Error: "ECR repository not found"
**Solución:** Crear repositorio manualmente o dejar que buildspec.yml lo cree

### Contenedor no inicia en EB:
```bash
# Ver logs de EB
eb logs

# Conectar por SSH a instancia EC2
eb ssh

# Ver logs de Docker en la instancia
sudo docker logs $(sudo docker ps -aq --latest)
```

---

## 📊 Diferencias con Despliegue Tradicional

| Aspecto | Antes (Tradicional) | Ahora (Docker) |
|---------|---------------------|----------------|
| **Plataforma EB** | Python 3.12 | Docker |
| **Dependencias** | `requirements.txt` en EC2 | Build en Docker image |
| **Build** | CodeBuild instala deps | CodeBuild construye imagen |
| **Despliegue** | Zip con código fuente | Imagen Docker desde ECR |
| **Artifacts** | Todo el código | Solo `Dockerrun.aws.json` |
| **Consistencia** | Depende del ambiente | Idéntico en dev/prod |
| **Rollback** | Versión anterior de código | Versión anterior de imagen |

---

## 🎯 Próximos Pasos

1. **Actualizar buildspec.yml** con tu `AWS_ACCOUNT_ID`
2. **Configurar CodeBuild** con privileged mode
3. **Crear repositorio ECR**
4. **Actualizar/crear ambiente EB** con plataforma Docker
5. **Configurar variables de entorno** en EB
6. **Hacer push** y verificar pipeline

---

## 📚 Referencias

- [AWS Elastic Beanstalk Docker](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/single-container-docker.html)
- [AWS CodeBuild Docker](https://docs.aws.amazon.com/codebuild/latest/userguide/sample-docker.html)
- [Amazon ECR Documentation](https://docs.aws.amazon.com/ecr/latest/userguide/what-is-ecr.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

¿Dudas? Revisa los logs en:
- **CodeBuild**: CloudWatch Logs del build
- **ECR**: Verifica imagen subida
- **Elastic Beanstalk**: Logs de la aplicación y health checks

