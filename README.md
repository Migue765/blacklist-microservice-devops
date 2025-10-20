# 🧩 Blacklist Microservice DevOps

Microservicio **Python + Flask** para gestionar lista negra global de correos electrónicos. Desplegado en **AWS Elastic Beanstalk** como parte del curso "DevOps: Agilizando el Despliegue Continuo de Aplicaciones" – Universidad de los Andes.

## 🚀 Objetivo

Implementar microservicio REST que permita:
- Agregar correos a lista negra global
- Consultar si un correo está en la lista negra
- Despliegue manual en AWS (sin CI/CD)
- Documentación y pruebas en Postman

## ⚙️ Stack Tecnológico

- **Backend:** Python 3.11+, Flask 1.1.x
- **Base de Datos:** PostgreSQL (AWS RDS)
- **Cloud:** AWS Elastic Beanstalk
- **Herramientas:** Flask-SQLAlchemy, Flask-RESTful, Flask-Marshmallow, JWT


## Entregable 1
[VIDEO ENTREGA 1](https://photos.app.goo.gl/FhiarQ4Qq1mkV1eo6)

[DOCUMENTO ENTREGA 1](https://github.com/user-attachments/files/23013214/Entrega1_DevOps_Uniandes.Ultimo.pdf)

[URL health](http://blacklist-v2-env.eba-9bsigk76.us-west-2.elasticbeanstalk.com/health)

url base: http://blacklist-v2-env.eba-9bsigk76.us-west-2.elasticbeanstalk.com

## 🏗️ Estructura del Proyecto

```
blacklist-microservice-devops/
├── app/
│   ├── __init__.py              # Factory pattern
│   ├── config.py                # Configuración
│   ├── models.py                # Modelo Blacklist
│   ├── schemas.py               # Validación Marshmallow
│   ├── auth.py                  # Autenticación Bearer
│   ├── utils.py                 # Utilidades
│   ├── wsgi.py                  # Entry point EB
│   └── routes/
│       ├── blacklists.py        # POST endpoint
│       ├── blacklists_get.py    # GET endpoint
│       └── health.py            # Health check
├── requirements.txt             # Dependencias
├── run_server.py                # Script desarrollo
├── test_api.py                  # Pruebas API
├── api_tests.http               # Pruebas HTTP
├── postman_collection.json      # Colección Postman
└── .ebextensions/               # Configuración EB
```

## 📡 API Endpoints

### POST /blacklists
Agrega email a lista negra.

**Request:**
```json
{
  "email": "usuario@ejemplo.com",
  "app_uuid": "f2a1b8c9-7e6d-4d5b-9a8f-3a4b5c6d7e8f",
  "blocked_reason": "correo sospechoso"
}
```

**Headers:** `Authorization: Bearer <TOKEN>`

**Response:**
```json
{"message": "Email agregado exitosamente a la lista negra."}
```

### GET /blacklists/<email>
Consulta si email está en lista negra.

**Headers:** `Authorization: Bearer <TOKEN>`

**Response:**
```json
{
  "email": "usuario@ejemplo.com",
  "is_blacklisted": true,
  "reason": "correo sospechoso"
}
```

## 🚀 Configuración Local

### 1. Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar
```bash
python run_server.py
```

### 4. Probar
```bash
python test_api.py
```

## 🧪 Pruebas API

### Health Check
```bash
curl http://localhost:5001/ping
```

### Agregar Email
```bash
curl -X POST http://localhost:5001/blacklists \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-bearer-token" \
  -d '{"email": "test@example.com", "app_uuid": "f2a1b8c9-7e6d-4d5b-9a8f-3a4b5c6d7e8f", "blocked_reason": "test"}'
```

### Consultar Email
```bash
curl -X GET http://localhost:5001/blacklists/test@example.com \
  -H "Authorization: Bearer dev-bearer-token"
```

**Respuesta esperada:**
```json
{
  "email": "test@example.com",
  "is_blacklisted": true,
  "blocked_reason": "correo de prueba"
}
```

## 📋 Colección Postman

### Endpoints Incluidos:
1. Health Check
2. Add Email to Blacklist
3. Check Blacklisted Email
4. Check Non-Blacklisted Email
5. Duplicate Email (409 Conflict)
6. Unauthorized POST Request
7. Unauthorized GET Request
8. Invalid Email Format

### Uso Rápido:
1. Importa el archivo local `postman_collection.json` o a traves de [Postman](https://app.getpostman.com/join-team?invite_code=741d3059f192ebdf7aa5756f276743db1c2aa0c0475f5634a30de66dd3525e86&target_code=5e2e990ea07442725fa97d4f20a61a62).
2. Configura las variables de entorno:
   - `base_url`: `http://localhost:5001`
   - `token`: `dev-bearer-token`
3. Ejecuta las pruebas individuales o toda la colección

## 🚧 Estado de Desarrollo

### ✅ Implementado
- **POST /blacklists** - Agregar email a lista negra
- **GET /blacklists/<email>** - Consultar email en lista negra
- **GET /ping** - Health check

## ☁️ Despliegue AWS

### Variables de Entorno EB
- `DATABASE_URL`: `postgresql+psycopg2://user:pass@host:port/db`
- `JWT_SECRET`: Token secreto JWT
- `APP_ALLOWED_BEARER`: Token autenticación
- `FLASK_ENV`: `production`

### Despliegue
```bash
zip -r blacklist-microservice.zip . -x "venv/*" "*.pyc" "__pycache__/*" ".git/*"
```

## 🔁 Estrategias de Despliegue

Documentar 4 estrategias en Beanstalk (3-6 instancias):
- All-at-once
- Rolling
- Rolling with additional batch
- Immutable / Traffic Splitting

## 📄 Entregables

- **Documento PDF:** Capturas RDS, Beanstalk, health checks, estrategias de despliegue
- **Postman Docs:** URL de documentación API
- **GitHub Repo:** Código fuente
- **Video:** 10 min máximo mostrando API funcional, pruebas Postman, consola AWS

## 👥 Autores

| Integrante | Correo | GitHub |
|------------|--------|--------|
| Angie Natalia Arandio Niño | a.arandio@uniandes.edu.co | [@nataliaarandio](https://github.com/nataliaarandio) |
| Jazmin Natalia Cordoba Puerto | jn.cordobap1@uniandes.edu.co | [@JazminCorAndes](https://github.com/JazminCorAndes) |
| Juan Esteban Mejia Isaza | je.mejiai1@uniandes.edu.co | [@JUANES545](https://github.com/JUANES545) |
| Miguel Alejandro Gomez Alarcon | ma.gomeza1@uniandes.edu.co | [@Migue765](https://github.com/Migue765) |

## 📚 Referencias

- [AWS Elastic Beanstalk Documentation](https://docs.aws.amazon.com/elasticbeanstalk/)
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [AWS Deployment Strategies](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/aeb-deployment-strategies.html)
