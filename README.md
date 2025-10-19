# 🧩 Blacklist Microservice DevOps

Microservicio **Python + Flask** para gestionar lista negra global de correos electrónicos. Desplegado en **AWS Elastic Beanstalk** como parte del curso "DevOps: Agilizando el Despliegue Continuo de Aplicaciones" – Universidad de los Andes.

## 🚀 Objetivo

Implementar microservicio REST que permita:
- Agregar correos a lista negra global
- Consultar si un correo está en la lista negra
- Despliegue manual en AWS (sin CI/CD)
- Documentación y pruebas en Postman

## ⚙️ Stack Tecnológico

- **Backend:** Python 3.8+, Flask 1.1.x
- **Base de Datos:** PostgreSQL (AWS RDS)
- **Cloud:** AWS Elastic Beanstalk
- **Herramientas:** Flask-SQLAlchemy, Flask-RESTful, Flask-Marshmallow, JWT

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
│       ├── blacklists_get.py    # GET endpoint (pendiente)
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
# TODO: Pendiente...
# curl -X GET http://localhost:5001/blacklists/test@example.com \
#   -H "Authorization: Bearer dev-bearer-token"
```

## 🚧 Estado de Desarrollo

### ✅ Implementado
- **POST /blacklists** - Agregar email (Juan)
- **GET /ping** - Health check

### ⏳ Pendiente
- **GET /blacklists/<email>**

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
