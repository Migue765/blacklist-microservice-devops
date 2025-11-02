# ✅ CONFIGURACIÓN ACTUALIZADA A OREGON (us-west-2)

## 📝 Cambios Aplicados

Todos los archivos han sido actualizados para usar:

```
Región: us-west-2 (Oregon)
Account ID: 153641554973
Repositorio ECR: blacklist-api
URI Completo: 153641554973.dkr.ecr.us-west-2.amazonaws.com/blacklist-api
```

### Archivos Actualizados:
- ✅ `buildspec.yml` → Región: us-west-2, Repo: blacklist-api
- ✅ `Dockerrun.aws.json` → URI actualizado
- ✅ `push-to-ecr.sh` → Configuración Oregon
- ✅ `docker-deploy.sh` → Configuración Oregon

---

## 🧪 PROBAR LOCALMENTE (Antes de push)

### Opción 1: Con el script (Recomendado)
```bash
# Build de la imagen
./docker-deploy.sh build

# O ejecutar con docker-compose
./docker-compose up --build -d

# Probar health check
curl http://localhost:8000/ping
```

### Opción 2: Push manual a ECR (Opcional)
```bash
# Usa el script que preparé
./push-to-ecr.sh

# O manualmente:
aws ecr get-login-password --region us-west-2 | \
  docker login --username AWS --password-stdin \
  153641554973.dkr.ecr.us-west-2.amazonaws.com

docker build -t blacklist-api .

docker tag blacklist-api:latest \
  153641554973.dkr.ecr.us-west-2.amazonaws.com/blacklist-api:latest

docker push \
  153641554973.dkr.ecr.us-west-2.amazonaws.com/blacklist-api:latest
```

---

## 🚀 DESPLIEGUE AUTOMÁTICO

Cuando hagas push a `main`, CodeBuild:

1. ✅ Clonará el código de tu rama `main`
2. ✅ Construirá la imagen Docker: `blacklist-api`
3. ✅ Subirá la imagen a: `153641554973.dkr.ecr.us-west-2.amazonaws.com/blacklist-api:latest`
4. ✅ Generará el `Dockerrun.aws.json` con la URI correcta
5. ✅ Elastic Beanstalk descargará y desplegará la imagen

### Comando para desplegar:
```bash
# Verifica los cambios
git status

# Commit
git add .
git commit -m "feat: configure Docker deployment with ECR in us-west-2"

# Push (esto activa CodeBuild automáticamente)
git push origin main
```

---

## ⚙️ CONFIGURACIÓN AWS NECESARIA

**Recuerda completar estos 3 pasos en AWS (del AWS_CONFIG_CHECKLIST.md):**

### 1. CodeBuild - Privileged Mode
- Ve a CodeBuild → Tu proyecto → Edit → Environment
- ✅ Marcar "Privileged" para Docker

### 2. CodeBuild - Permisos ECR
- IAM → Roles → `codebuild-tu-proyecto-service-role`
- Agregar política inline con permisos ECR

### 3. Elastic Beanstalk - Docker Platform
- Crear ambiente con plataforma Docker (us-west-2)
- Instance Profile con permisos `AmazonEC2ContainerRegistryReadOnly`
- Variables de entorno (DATABASE_URL, JWT_SECRET, etc.)

---

## 🔍 VERIFICAR DESPUÉS DEL PUSH

### 1. CodeBuild
```
AWS Console → CodeBuild → Build history
```
Busca en los logs:
- ✅ "Logging in to Amazon ECR..."
- ✅ "Building the Docker image..."
- ✅ "Pushing the Docker images..."

### 2. ECR
```
AWS Console → ECR → Repositories → blacklist-api
```
Deberías ver:
- Imagen con tag `latest`
- Imagen con tag del commit hash

### 3. Elastic Beanstalk
```
AWS Console → Elastic Beanstalk → Tu ambiente
```
En "Recent events" verás el deploy en progreso.

### 4. Probar la API
```bash
# Reemplaza con tu URL de EB
curl http://tu-ambiente.us-west-2.elasticbeanstalk.com/ping

# Debe responder: pong
```

---

## 📊 RESUMEN DE CONFIGURACIÓN

| Componente | Configuración |
|------------|---------------|
| **Región** | us-west-2 (Oregon) ✅ |
| **Account ID** | 153641554973 ✅ |
| **Repositorio ECR** | blacklist-api ✅ |
| **Nombre imagen** | blacklist-api ✅ |
| **URI ECR** | 153641554973.dkr.ecr.us-west-2.amazonaws.com/blacklist-api ✅ |
| **Trigger** | Push a rama `main` ✅ |
| **Build** | CodeBuild con buildspec.yml ✅ |
| **Deploy** | Elastic Beanstalk Docker platform ✅ |

---

## 🎯 PRÓXIMOS PASOS

1. **Probar localmente** (opcional):
   ```bash
   ./docker-deploy.sh build
   ./docker-deploy.sh test
   ```

2. **Configurar AWS** (si aún no lo hiciste):
   - Ver archivo `AWS_CONFIG_CHECKLIST.md`

3. **Hacer push**:
   ```bash
   git add .
   git commit -m "feat: dockerize with ECR us-west-2"
   git push origin main
   ```

4. **Monitorear**:
   - CodeBuild logs
   - ECR images
   - Elastic Beanstalk events

---

**¡Todo listo para deployar con Docker!** 🐳🚀

