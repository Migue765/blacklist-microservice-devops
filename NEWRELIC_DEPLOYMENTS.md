# Configuración de Eventos de Despliegue en New Relic

Esta guía explica cómo configurar el envío automático de eventos de despliegue a New Relic.

## ✅ Configuración Implementada

1. **Script de notificación**: `scripts/notify_newrelic_deployment.py`
2. **Release phase en Procfile**: Se ejecuta automáticamente después de cada despliegue
3. **Múltiples métodos**: Soporta API key y License key

## 🔑 Obtener API Key de New Relic

Para usar el método recomendado (API REST), necesitas obtener una API key:

1. Ve a [New Relic API Keys](https://one.newrelic.com/admin-portal/api-keys/home)
2. Haz clic en "Create a key"
3. Selecciona "User key" o "Ingest - License" key
4. Copia la API key generada

## 📋 Configuración en Heroku

### Opción 1: Usar API Key (Recomendado)

```bash
heroku config:set NEW_RELIC_API_KEY=tu-api-key-aqui -a blacklist-api
heroku config:set NEW_RELIC_APP_NAME=blacklist-api -a blacklist-api
```

### Opción 2: Usar License Key (Alternativa)

Si no tienes API key, puedes usar la license key:

```bash
heroku config:set NEW_RELIC_LICENSE_KEY=tu-license-key-aqui -a blacklist-api
heroku config:set NEW_RELIC_APP_NAME=blacklist-api -a blacklist-api
```

## 🚀 Cómo Funciona

### Release Phase en Heroku

El `Procfile` ahora incluye una fase `release`:

```
release: python scripts/notify_newrelic_deployment.py
web: gunicorn ...
```

Heroku ejecuta automáticamente el script `release` **antes** de iniciar los dynos web. Esto significa que:

1. Heroku despliega el código
2. Ejecuta el script `release` (notifica a New Relic)
3. Inicia los dynos web

### Información Capturada

El script captura automáticamente:

- **Revision**: Hash del commit (HEROKU_SLUG_COMMIT)
- **Description**: Descripción del slug (HEROKU_SLUG_DESCRIPTION)
- **User**: Usuario que hizo el despliegue (HEROKU_USER)
- **App Name**: Nombre de la aplicación
- **Timestamp**: Fecha y hora del despliegue

## 📊 Ver Despliegues en New Relic

### 1. En el Dashboard de la Aplicación

1. Ve a [New Relic Applications](https://one.newrelic.com/)
2. Selecciona tu aplicación
3. En el timeline, verás marcadores de despliegue (deployment markers)

### 2. Usando NRQL

```sql
SELECT * FROM Deployment SINCE 7 days ago
```

O más específico:

```sql
SELECT * FROM Deployment 
WHERE appName = 'blacklist-api' 
SINCE 7 days ago 
ORDER BY timestamp DESC
```

### 3. Ver Despliegues con Detalles

```sql
SELECT timestamp, revision, user, description 
FROM Deployment 
WHERE appName = 'blacklist-api' 
SINCE 30 days ago 
ORDER BY timestamp DESC
```

## 🔍 Verificar que Funciona

### 1. Hacer un despliegue

```bash
git push heroku main
```

### 2. Ver los logs del release phase

```bash
heroku logs --tail -a blacklist-api | grep -i deployment
```

Deberías ver algo como:

```
✓ Deployment notification sent to New Relic successfully
  App: blacklist-api (ID: 123456)
  Revision: abc123def456...
```

### 3. Verificar en New Relic

1. Espera 1-2 minutos
2. Ve a tu aplicación en New Relic
3. Busca los marcadores de despliegue en el timeline

## 🐛 Troubleshooting

### El script no se ejecuta

**Problema**: No ves el mensaje de deployment en los logs

**Solución**:
1. Verifica que el Procfile tenga la línea `release:`
2. Verifica que el script existe: `ls scripts/notify_newrelic_deployment.py`
3. Verifica los logs completos: `heroku logs --tail -a blacklist-api`

### Error: "Application not found"

**Problema**: El script dice que la aplicación no se encuentra

**Solución**:
1. Verifica que `NEW_RELIC_APP_NAME` coincida exactamente con el nombre en New Relic
2. Verifica que la API key tenga permisos para leer aplicaciones
3. Lista las aplicaciones disponibles en New Relic

### Error: "API key not set"

**Problema**: El script dice que no hay API key

**Solución**:
1. Verifica las variables de entorno: `heroku config -a blacklist-api`
2. Configura la API key: `heroku config:set NEW_RELIC_API_KEY=...`
3. O usa la license key como alternativa

### Los despliegues no aparecen en New Relic

**Problema**: El script se ejecuta pero no ves despliegues en New Relic

**Solución**:
1. Verifica que la API key tenga permisos de escritura
2. Espera 1-2 minutos (puede haber delay)
3. Verifica que estés buscando en la aplicación correcta
4. Usa la consulta NRQL para buscar despliegues

## 📝 Notas Importantes

1. **Release Phase**: Se ejecuta antes de iniciar los dynos, así que si falla, el despliegue puede fallar
2. **No bloqueante**: El script está diseñado para no fallar el despliegue si New Relic no está disponible
3. **Múltiples métodos**: Si la API key falla, intenta usar la license key automáticamente
4. **Información automática**: Heroku proporciona automáticamente las variables de entorno necesarias

## 🔗 Referencias

- [New Relic Deployment API](https://docs.newrelic.com/docs/apis/rest-api-v2/get-started/get-started-rest-api-v2/)
- [Heroku Release Phase](https://devcenter.heroku.com/articles/release-phase)
- [New Relic API Keys](https://docs.newrelic.com/docs/apis/get-started/intro-apis/understand-new-relic-api-keys/)

