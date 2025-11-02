# ✅ CHECKLIST - Configuración AWS para Deploy Automático con Docker

## 🎯 Lo que ya tienes listo:
- ✅ Dockerfile
- ✅ buildspec.yml configurado
- ✅ Dockerrun.aws.json
- ✅ Repositorio ECR creado: `153641554973.dkr.ecr.us-east-1.amazonaws.com/blacklist`
- ✅ CodeBuild conectado a GitHub (hace trigger en push a main)

---

## 🔧 LO QUE FALTA CONFIGURAR (3 pasos):

### 1️⃣ CODEBUILD: Habilitar Docker (Privileged Mode)

**Por qué:** CodeBuild necesita permisos especiales para construir imágenes Docker.

**Cómo hacerlo:**
1. Ve a **AWS CodeBuild** → Tu proyecto
2. Click en **Edit** → **Environment**
3. Busca la sección **Additional configuration**
4. ✅ **Marca el checkbox:** "Enable this flag if you want to build Docker images or want a build to get elevated privileges"
5. **Save**

**Screenshot mental:** Debes ver un checkbox que dice "Privileged"

---

### 2️⃣ CODEBUILD: Permisos IAM para ECR

**Por qué:** CodeBuild necesita permisos para subir imágenes al repositorio ECR.

**Cómo hacerlo:**

**Paso A: Encontrar el rol**
1. Ve a **IAM** → **Roles**
2. Busca: `codebuild-<nombre-de-tu-proyecto>-service-role`
   (Por ejemplo: `codebuild-blacklist-service-role`)

**Paso B: Agregar política**
1. Click en el rol
2. Click en **Add permissions** → **Create inline policy**
3. Click en la pestaña **JSON**
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
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:DescribeRepositories"
      ],
      "Resource": "*"
    }
  ]
}
```

5. Click **Review policy**
6. Nombre: `ECR-Push-Access`
7. Click **Create policy**

---

### 3️⃣ ELASTIC BEANSTALK: Configurar para Docker

#### Opción A: Crear nuevo ambiente (Recomendado si quieres mantener el actual)

1. Ve a **Elastic Beanstalk** → Tu aplicación
2. Click en **Create a new environment**
3. Configuración:
   - **Environment tier:** Web server environment
   - **Environment name:** `blacklist-docker-env` (o el nombre que quieras)
   - **Platform:** Docker
   - **Platform branch:** Docker running on 64bit Amazon Linux 2023
   - **Application code:** Sample application (se actualizará automáticamente)

4. Click **Configure more options**
5. En **Software** → **Edit**
   - Agrega las mismas variables de entorno que tienes en tu ambiente actual:
   ```
   DATABASE_URL = postgresql+psycopg2://...
   JWT_SECRET = ...
   APP_ALLOWED_BEARER = ...
   FLASK_ENV = production
   ```
   - **Save**

6. En **Security** → **Edit**
   - **IAM instance profile:** `aws-elasticbeanstalk-ec2-role` (crear si no existe)
   - **Save**

7. Click **Create environment**

#### Opción B: Actualizar ambiente existente (Más rápido pero con downtime)

1. Ve a tu ambiente actual
2. Click en **Actions** → **Platform update**
3. Cambiar a plataforma: **Docker running on 64bit Amazon Linux 2023**
4. **Update**

---

### 3️⃣.1 ELASTIC BEANSTALK: Permisos IAM para ECR

**Por qué:** Las instancias EC2 de EB necesitan permisos para descargar imágenes de ECR.

**Cómo hacerlo:**

1. Ve a **IAM** → **Roles**
2. Busca: `aws-elasticbeanstalk-ec2-role`
3. Si NO existe, créalo:
   - Click **Create role**
   - **Trusted entity:** AWS service
   - **Use case:** EC2
   - Click **Next**
   - Busca y agrega estas políticas:
     - `AmazonEC2ContainerRegistryReadOnly` ✅
     - `AWSElasticBeanstalkWebTier` ✅
     - `AWSElasticBeanstalkWorkerTier` ✅
   - Nombre: `aws-elasticbeanstalk-ec2-role`
   - **Create role**

4. Si YA existe:
   - Click en el rol
   - **Add permissions** → **Attach policies**
   - Busca: `AmazonEC2ContainerRegistryReadOnly`
   - Marca el checkbox
   - **Attach policy**

5. Asignar el rol a tu ambiente EB:
   - Ve a tu ambiente EB → **Configuration**
   - **Security** → **Edit**
   - **IAM instance profile:** Selecciona `aws-elasticbeanstalk-ec2-role`
   - **Apply**

---

## 🚀 PROBAR EL FLUJO COMPLETO

Después de configurar los 3 pasos anteriores:

```bash
# 1. Verificar que todo esté bien
git status

# 2. Hacer commit de los cambios
git add .
git commit -m "feat: dockerize application with ECR integration"

# 3. Push a main (esto activará CodeBuild automáticamente)
git push origin main
```

### Monitorear el despliegue:

**1. CodeBuild:**
```
AWS Console → CodeBuild → Build history → Ver el build en progreso
```
Deberías ver:
- ✅ Login a ECR
- ✅ Building Docker image
- ✅ Pushing to ECR
- ✅ Creating Dockerrun.aws.json

**2. ECR:**
```
AWS Console → ECR → Repositories → blacklist
```
Deberías ver la imagen recién subida con tags `latest` y el commit hash.

**3. Elastic Beanstalk:**
```
AWS Console → Elastic Beanstalk → Tu ambiente → Recent events
```
Deberías ver el deploy en progreso.

**4. Probar la API:**
```bash
# Reemplaza con tu URL de EB
curl http://tu-ambiente.elasticbeanstalk.com/ping
```

---

## ⚠️ TROUBLESHOOTING

### Error en CodeBuild: "Cannot connect to the Docker daemon"
**Solución:** No habilitaste Privileged mode en CodeBuild (Paso 1)

### Error en CodeBuild: "denied: User is not authorized"
**Solución:** Falta la política IAM de ECR en CodeBuild (Paso 2)

### Error en EB: "Failed to pull Docker image"
**Solución:** Falta el permiso ECR en el Instance Profile de EB (Paso 3.1)

### EB health check failed
**Solución:** 
- Verifica que las variables de entorno estén configuradas en EB
- Verifica que el puerto 8000 esté expuesto en el Dockerfile (ya está)
- Ve a EB → Logs → Request logs para ver el error específico

---

## 📋 RESUMEN VISUAL

```
┌─────────────────────────────────────┐
│  1. CodeBuild: Privileged Mode ✅   │
│  2. CodeBuild: Permisos ECR ✅      │
│  3. EB: Plataforma Docker ✅        │
│  3.1. EB: Permisos ECR ✅           │
└─────────────────────────────────────┘
                 ↓
      ┌──────────────────┐
      │   git push main  │
      └──────────────────┘
                 ↓
      ┌──────────────────┐
      │   🚀 Deploy      │
      │   Automático     │
      └──────────────────┘
```

---

## 🎯 DESPUÉS DE CONFIGURAR

Cada vez que hagas `git push origin main`:
1. ✅ CodeBuild detecta el push
2. ✅ Clona tu código
3. ✅ Construye la imagen Docker con tu código
4. ✅ Sube la imagen a ECR
5. ✅ Elastic Beanstalk la descarga y despliega
6. ✅ Tu aplicación está actualizada

**¡Sin intervención manual!** 🎉

---

## 📞 ¿Necesitas ayuda?

Si algo falla:
1. Revisa los logs de CodeBuild
2. Verifica que la imagen esté en ECR
3. Revisa los logs de Elastic Beanstalk
4. Compara con este checklist

**Logs útiles:**
```bash
# EB CLI (si lo tienes instalado)
eb logs

# O descarga desde la consola:
EB → Logs → Request Logs → Full Logs
```

