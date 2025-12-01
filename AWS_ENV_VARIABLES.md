# 📋 Guía: Actualizar Variables de Entorno en AWS

Esta guía explica cómo actualizar variables de entorno en AWS dependiendo del servicio que estés usando.

## 🎯 Para AWS ECS (Tu caso actual)

Estás usando **ECS Fargate** con CodeDeploy. Hay dos formas de actualizar variables de entorno:

### Opción 1: Actualizar `taskdef.json` (Recomendado para CI/CD)

Edita el archivo `taskdef.json` y agrega/modifica las variables en la sección `environment`:

```json
{
  "containerDefinitions": [
    {
      "name": "blacklist-app",
      "environment": [
        {
          "name": "NEW_RELIC_API_KEY",
          "value": "A3465C7DC1CE06540CC4C37DAD454DC3DE81C6E97F7F196BB1429FE5C3542036"
        },
        {
          "name": "NEW_RELIC_APP_NAME",
          "value": "blacklist-microservice"
        }
      ]
    }
  ]
}
```

Luego haz commit y push. El pipeline actualizará automáticamente el task definition.

### Opción 2: Consola de AWS (Método manual)

1. **Ve a ECS Console:**
   - https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/cluster-entrega-3/task-definitions

2. **Selecciona tu task definition:**
   - Busca `tarea-entrega-3`
   - Haz clic en la versión más reciente

3. **Crea nueva revisión:**
   - Haz clic en "Create new revision"
   - En "Container definitions", expande `blacklist-app`
   - Ve a la sección "Environment variables"
   - Agrega o edita variables:
     - `NEW_RELIC_API_KEY` = `tu-api-key-aqui`
     - `NEW_RELIC_APP_NAME` = `blacklist-microservice`
   - Haz clic en "Create"

4. **Actualiza el servicio:**
   - Ve a tu servicio: `tarea-entrega-3-service-codedeploy`
   - Haz clic en "Update"
   - Selecciona la nueva revisión del task definition
   - Haz clic en "Update"

### Opción 3: AWS CLI (Para automatización)

```bash
# Registrar nueva revisión del task definition
aws ecs register-task-definition \
  --cli-input-json file://taskdef.json \
  --region us-west-2

# Actualizar el servicio
aws ecs update-service \
  --cluster cluster-entrega-3 \
  --service tarea-entrega-3-service-codedeploy \
  --task-definition tarea-entrega-3 \
  --region us-west-2
```

## 🔧 Variables de New Relic para agregar

Agrega estas variables al `taskdef.json`:

```json
{
  "name": "NEW_RELIC_API_KEY",
  "value": "tu-api-key-de-new-relic"
},
{
  "name": "NEW_RELIC_APP_NAME",
  "value": "blacklist-microservice"
}
```

## 📝 Actualizar taskdef.json

El archivo `taskdef.json` ya incluye un placeholder para `NEW_RELIC_API_KEY`. Solo necesitas:

1. **Editar `taskdef.json`** y reemplazar el valor vacío:
   ```json
   {
     "name": "NEW_RELIC_API_KEY",
     "value": "tu-api-key-real-aqui"
   }
   ```

2. **Hacer commit y push** - El pipeline actualizará automáticamente

## 🔍 Verificar Variables Actuales

### Desde AWS CLI:

```bash
# Ver task definition actual
aws ecs describe-task-definition \
  --task-definition tarea-entrega-3 \
  --region us-west-2 \
  --query 'taskDefinition.containerDefinitions[0].environment'
```

### Desde la Consola:

1. Ve a: https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/cluster-entrega-3/task-definitions
2. Selecciona `tarea-entrega-3`
3. Ve a la última revisión
4. Expande "Container definitions" → `blacklist-app`
5. Ve a "Environment variables"

## 📚 Para Otros Servicios AWS

### AWS Elastic Beanstalk

1. **Consola:**
   - Ve a: https://us-west-2.console.aws.amazon.com/elasticbeanstalk/
   - Selecciona tu entorno
   - Ve a "Configuration" → "Software"
   - Haz clic en "Edit"
   - Agrega variables en "Environment properties"
   - Guarda y aplica

2. **CLI:**
   ```bash
   aws elasticbeanstalk update-environment \
     --environment-name tu-entorno \
     --option-settings \
       Namespace=aws:elasticbeanstalk:application:environment,OptionName=NEW_RELIC_API_KEY,Value=tu-key \
     --region us-west-2
   ```

3. **Archivo `.ebextensions`:**
   Crea `/.ebextensions/environment.config`:
   ```yaml
   option_settings:
     aws:elasticbeanstalk:application:environment:
       NEW_RELIC_API_KEY: tu-api-key
       NEW_RELIC_APP_NAME: blacklist-microservice
   ```

### AWS Lambda

1. **Consola:**
   - Ve a tu función Lambda
   - Ve a "Configuration" → "Environment variables"
   - Agrega/edita variables

2. **CLI:**
   ```bash
   aws lambda update-function-configuration \
     --function-name tu-funcion \
     --environment Variables="{NEW_RELIC_API_KEY=tu-key}" \
     --region us-west-2
   ```

## ⚠️ Mejores Prácticas

1. **No commitees secrets en el código:**
   - Usa AWS Secrets Manager o Parameter Store
   - O actualiza manualmente en la consola

2. **Usa AWS Secrets Manager (Recomendado):**
   ```json
   {
     "secrets": [
       {
         "name": "NEW_RELIC_API_KEY",
         "valueFrom": "arn:aws:secretsmanager:us-west-2:153641554973:secret:newrelic-api-key"
       }
     ]
   }
   ```

3. **Para producción:**
   - Actualiza en la consola manualmente
   - O usa CI/CD con variables secretas

## 🔐 Usar AWS Secrets Manager (Opcional pero Recomendado)

Para mayor seguridad, puedes usar Secrets Manager:

1. **Crear secret:**
   ```bash
   aws secretsmanager create-secret \
     --name newrelic-api-key \
     --secret-string "tu-api-key-aqui" \
     --region us-west-2
   ```

2. **Actualizar task definition para usar el secret:**
   ```json
   {
     "secrets": [
       {
         "name": "NEW_RELIC_API_KEY",
         "valueFrom": "arn:aws:secretsmanager:us-west-2:153641554973:secret:newrelic-api-key"
       }
     ]
   }
   ```

3. **Asegúrate de que el execution role tenga permisos:**
   ```json
   {
     "Effect": "Allow",
     "Action": [
       "secretsmanager:GetSecretValue"
     ],
     "Resource": "arn:aws:secretsmanager:us-west-2:153641554973:secret:newrelic-api-key*"
   }
   ```

## 📋 Resumen Rápido

**Para tu caso (ECS):**

1. **Edita `taskdef.json`** → Agrega/modifica variables en `environment`
2. **Commit y push** → El pipeline actualiza automáticamente
3. **O manualmente en consola:**
   - ECS → Task Definitions → `tarea-entrega-3` → Create new revision
   - Agrega variables → Create
   - Service → Update → Selecciona nueva revisión → Update

