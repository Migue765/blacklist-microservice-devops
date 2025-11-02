# 🚀 QUICK START - Dockerización del Proyecto

## ✅ Archivos Creados (Ya listos en el repo)

- ✅ `Dockerfile` - Configuración de la imagen Docker
- ✅ `.dockerignore` - Optimización del build
- ✅ `docker-compose.yml` - Desarrollo local con PostgreSQL
- ✅ `Dockerrun.aws.json` - Config para Elastic Beanstalk
- ✅ `buildspec.yml` - Pipeline actualizado para Docker
- ✅ `docker-deploy.sh` - Script de ayuda
- ✅ `DOCKER_SETUP.md` - Guía completa paso a paso
- ✅ `env.example` - Variables de entorno actualizadas

---

## 🎯 LO QUE DEBES HACER EN AWS (ANTES DE HACER PUSH)

### 1️⃣ ACTUALIZAR buildspec.yml

Edita el archivo `buildspec.yml` línea 7:

```yaml
AWS_ACCOUNT_ID: "YOUR_AWS_ACCOUNT_ID"  # ⚠️ Reemplazar con tu Account ID
```

**Cómo obtener tu Account ID:**
```bash
aws sts get-caller-identity --query Account --output text
```

O ejecuta:
```bash
./docker-deploy.sh update-dockerrun
```

---

### 2️⃣ CREAR REPOSITORIO EN ECR

**Opción A: Automático con el script**
```bash
./docker-deploy.sh create-repo
```

**Opción B: Manual en AWS Console**
1. Ve a **Amazon ECR** → **Repositories**
2. Click **Create repository**
3. Nombre: `blacklist-microservice`
4. Región: `us-west-2`
5. **Create**

**Opción C: AWS CLI**
```bash
aws ecr create-repository \
  --repository-name blacklist-microservice \
  --region us-west-2
```

---

### 3️⃣ CONFIGURAR CODEBUILD

1. Ve a **AWS CodeBuild** → Tu proyecto
2. Click **Edit** → **Environment**

**IMPORTANTE - Configurar:**
```
Environment image: Managed image
Operating system: Ubuntu
Runtime: Standard
Image: aws/codebuild/standard:7.0
Environment type: Linux
Privileged: ✅ ACTIVAR (OBLIGATORIO)
```

**✅ Marca:** "Enable this flag if you want to build Docker images"

**Variables de entorno (opcional, ya están en buildspec.yml):**
```
AWS_DEFAULT_REGION = us-west-2
AWS_ACCOUNT_ID = <tu-account-id>
IMAGE_REPO_NAME = blacklist-microservice
```

---

### 4️⃣ PERMISOS IAM - CODEBUILD

**Agregar política al Service Role de CodeBuild:**

1. Ve a **IAM** → **Roles**
2. Busca el rol: `codebuild-<nombre-proyecto>-service-role`
3. Click **Add permissions** → **Create inline policy**
4. Pega esto:

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

5. Nombre: `ECR-Docker-Access`
6. **Create policy**

---

### 5️⃣ CONFIGURAR ELASTIC BEANSTALK

**Si ya tienes un ambiente:**

1. Ve a **Elastic Beanstalk** → Tu aplicación
2. **Create new environment**
3. Environment name: `blacklist-docker-env`
4. Platform: **Docker**
5. Platform branch: **Docker running on 64bit Amazon Linux 2023**
6. Application code: **Sample application** (se actualizará con CodeBuild)

**Variables de entorno:**
1. Configuration → Software → Edit
2. Agrega:
```
DATABASE_URL = postgresql+psycopg2://user:pass@rds-host:5432/db
JWT_SECRET = <tu-secret>
APP_ALLOWED_BEARER = <tu-token>
FLASK_ENV = production
```

---

### 6️⃣ PERMISOS IAM - ELASTIC BEANSTALK

**Agregar política al Instance Profile de EB:**

1. Ve a **IAM** → **Roles**
2. Busca: `aws-elasticbeanstalk-ec2-role`
3. Click **Add permissions** → **Attach policies**
4. Busca y marca: `AmazonEC2ContainerRegistryReadOnly`
5. **Attach policy**

Si el rol no existe, créalo con la política `AmazonEC2ContainerRegistryReadOnly`.

Luego:
1. Ve a tu ambiente EB → **Configuration** → **Security**
2. **IAM instance profile**: `aws-elasticbeanstalk-ec2-role`
3. **Apply**

---

## 🧪 PROBAR LOCALMENTE (Antes de desplegar)

### Opción 1: Docker Compose (Recomendado)
```bash
# Levantar todo (app + PostgreSQL)
docker-compose up --build

# Probar
curl http://localhost:8000/ping
```

### Opción 2: Solo Docker
```bash
# Build
docker build -t blacklist-microservice .

# Run
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e JWT_SECRET="secret" \
  -e APP_ALLOWED_BEARER="token" \
  blacklist-microservice
```

### Opción 3: Script de ayuda
```bash
./docker-deploy.sh build
./docker-deploy.sh compose-up
./docker-deploy.sh test
```

---

## 🚀 DESPLIEGUE

Una vez configurado todo en AWS:

```bash
# 1. Verifica que todo esté ok
./docker-deploy.sh test

# 2. Commit y push
git add .
git commit -m "Dockerized application"
git push origin main

# 3. CodeBuild se activará automáticamente y:
#    - Construirá la imagen Docker
#    - La subirá a ECR
#    - Generará Dockerrun.aws.json
#    - Elastic Beanstalk desplegará la imagen
```

---

## 📊 VERIFICAR DESPLIEGUE

### 1. Revisar CodeBuild
```bash
# En AWS Console
CodeBuild → Build history → Ver logs
```

### 2. Revisar ECR
```bash
# En AWS Console
ECR → Repositories → blacklist-microservice → Ver imágenes

# O con CLI
aws ecr list-images \
  --repository-name blacklist-microservice \
  --region us-west-2
```

### 3. Revisar Elastic Beanstalk
```bash
# En AWS Console
Elastic Beanstalk → Tu ambiente → Recent events

# O con EB CLI
eb logs

# Ver health
curl http://tu-ambiente.elasticbeanstalk.com/ping
```

---

## ⚠️ TROUBLESHOOTING RÁPIDO

| Error | Solución |
|-------|----------|
| "Cannot connect to Docker daemon" | Habilitar **Privileged mode** en CodeBuild |
| "denied: User not authorized" | Verificar permisos ECR en IAM del Service Role |
| "EB health check failed" | Verificar variables de entorno en EB |
| "Repository not found" | Crear repositorio ECR |
| "Build failed" | Ver logs en CodeBuild → Verificar `AWS_ACCOUNT_ID` |

**Ver logs detallados:**
```bash
# CodeBuild
AWS Console → CodeBuild → Build history → View logs

# Elastic Beanstalk
eb logs
# O en consola: Environment → Logs → Request logs
```

---

## 📚 DOCUMENTACIÓN COMPLETA

- **Guía paso a paso:** [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **README principal:** [README.md](README.md)
- **Variables de entorno:** [env.example](env.example)
- **Script de ayuda:** `./docker-deploy.sh help`

---

## 🎓 DIFERENCIAS CLAVE

| Antes | Ahora |
|-------|-------|
| Plataforma: Python 3.12 | Plataforma: Docker |
| Build: instala requirements | Build: construye imagen |
| Deploy: código fuente | Deploy: imagen Docker |
| Artifacts: todo el código | Artifacts: Dockerrun.aws.json |
| Consistencia: varía por ambiente | Consistencia: idéntica |

---

## ✅ CHECKLIST FINAL

### Antes de hacer push:
- [ ] Actualizar `AWS_ACCOUNT_ID` en `buildspec.yml`
- [ ] Crear repositorio ECR
- [ ] Configurar CodeBuild con Privileged mode
- [ ] Agregar permisos ECR al Service Role de CodeBuild
- [ ] Crear/actualizar ambiente EB con plataforma Docker
- [ ] Agregar permisos ECR al Instance Profile de EB
- [ ] Configurar variables de entorno en EB
- [ ] Probar build local: `docker build -t test .`
- [ ] Probar docker-compose: `docker-compose up`

### Después del push:
- [ ] Verificar build exitoso en CodeBuild
- [ ] Verificar imagen en ECR
- [ ] Verificar health check de EB
- [ ] Probar endpoints de la API

---

**¿Listo?** 🚀

```bash
git add .
git commit -m "feat: dockerize application with ECR and EB integration"
git push origin main
```

¡Y CodeBuild hará el resto! 🎉

