# Configuración de Logs Heroku → New Relic

Esta guía explica cómo configurar el envío de logs desde Heroku a New Relic.

## ✅ Pasos Completados

1. **Agregar drain de logs a Heroku:**
   ```bash
   heroku drains:add "https://log-api.newrelic.com/log/v1?Api-Key=d3ff7086d2f70298966f131778a86e5aFFFFNRAL&format=heroku" -a blacklist-api
   ```

2. **Verificar que el drain está configurado:**
   ```bash
   heroku drains --app blacklist-api --json
   ```

## 📋 Configuración Implementada

### 1. Sistema de Logging Estructurado

El proyecto ahora usa un sistema de logging estructurado en formato JSON que es compatible con New Relic:

- **Formato JSON**: Los logs se formatean en JSON para facilitar el parsing en New Relic
- **Metadatos enriquecidos**: Cada log incluye timestamp, nivel, módulo, función, línea, etc.
- **Campos personalizados**: Los logs pueden incluir campos adicionales como `email`, `client_ip`, `error_type`, etc.

### 2. Procfile Actualizado

El Procfile ahora está configurado para:
- Usar la variable de entorno `PORT` de Heroku
- Escribir logs a stdout/stderr (capturados automáticamente por Heroku)
- Incluir access logs y error logs

### 3. Logging en las Rutas

Todas las rutas ahora usan logging estructurado con campos adicionales:
- `POST /blacklists`: Incluye `email`, `client_ip`, `app_uuid`
- `GET /blacklists/<email>`: Incluye `email`, `is_blacklisted`
- Errores: Incluyen `error`, `error_type`

## 🔍 Verificar que los Logs se Envían

### 1. Ver logs en Heroku
```bash
heroku logs --tail -a blacklist-api
```

Deberías ver logs en formato JSON cuando la aplicación está en Heroku:
```json
{"timestamp": "2025-12-01T00:00:00Z", "level": "INFO", "message": "Health check requested", "endpoint": "/health", "dyno": "web.1", "source": "heroku"}
```

### 2. Ver logs en New Relic

1. Ve a [New Relic Logs](https://one.newrelic.com/logs)
2. Selecciona tu aplicación: `blacklist-microservice` o `blacklist-api`
3. Deberías ver los logs apareciendo en tiempo real

### 3. Consultar logs en New Relic

Usa la consulta NRQL:
```sql
SELECT * FROM Log WHERE app_name = 'blacklist-api' SINCE 1 hour ago
```

O más específico:
```sql
SELECT * FROM Log 
WHERE message LIKE '%blacklist%' 
SINCE 1 hour ago 
ORDER BY timestamp DESC
```

### 4. Filtrar logs por nivel
```sql
SELECT * FROM Log 
WHERE level = 'ERROR' 
AND app_name = 'blacklist-api' 
SINCE 24 hours ago
```

### 5. Buscar logs con campos específicos
```sql
SELECT * FROM Log 
WHERE email IS NOT NULL 
SINCE 1 hour ago
```

## 🧪 Probar el Sistema

### 1. Hacer una petición a la API
```bash
curl https://blacklist-api.herokuapp.com/health
```

### 2. Verificar en Heroku
```bash
heroku logs --tail -a blacklist-api | grep health
```

### 3. Verificar en New Relic
- Ve a New Relic → Logs
- Busca el log con `message = "Health check requested"`

## 📊 Campos Disponibles en los Logs

Los logs incluyen los siguientes campos:

### Campos Base (siempre presentes)
- `timestamp`: ISO 8601 timestamp
- `level`: INFO, ERROR, WARNING, DEBUG
- `logger`: Nombre del logger
- `message`: Mensaje del log
- `module`: Módulo Python
- `function`: Función donde se generó el log
- `line`: Línea de código

### Campos Condicionales
- `dyno`: Nombre del dyno de Heroku (si está en Heroku)
- `source`: "heroku" (si está en Heroku)
- `app_name`: Nombre de la app en New Relic
- `email`: Email procesado (en logs de blacklist)
- `client_ip`: IP del cliente
- `app_uuid`: UUID de la aplicación
- `is_blacklisted`: Estado de blacklist
- `error`: Mensaje de error
- `error_type`: Tipo de error
- `endpoint`: Endpoint accedido

## 🔧 Troubleshooting

### Los logs no aparecen en New Relic

1. **Verificar que el drain está activo:**
   ```bash
   heroku drains --app blacklist-api
   ```

2. **Verificar que los logs se generan:**
   ```bash
   heroku logs --tail -a blacklist-api
   ```

3. **Verificar la API key de New Relic:**
   - Asegúrate de que la API key es válida
   - Verifica que tiene permisos para escribir logs

4. **Verificar formato de logs:**
   - Los logs deben estar en formato JSON cuando están en Heroku
   - Verifica que `HEROKU_APP_NAME` o `DYNO` estén configurados

### Los logs no tienen formato JSON

Si los logs no están en formato JSON, verifica:
1. Que la variable de entorno `HEROKU_APP_NAME` o `DYNO` esté configurada
2. Que el código esté usando el nuevo `StructuredLogger`

## 📝 Notas Importantes

1. **Heroku captura automáticamente** todo lo que se escribe a stdout/stderr
2. **New Relic parsea automáticamente** los logs en formato JSON
3. **Los campos personalizados** aparecen como atributos en New Relic y pueden usarse en queries
4. **El formato JSON** solo se usa en producción (Heroku), en desarrollo local usa formato simple

## 🔗 Referencias

- [New Relic Logs Documentation](https://docs.newrelic.com/docs/logs/)
- [Heroku Log Drains](https://devcenter.heroku.com/articles/log-drains)
- [New Relic Heroku Integration](https://docs.newrelic.com/docs/logs/logs-context/configure-logs-context-ruby/)

