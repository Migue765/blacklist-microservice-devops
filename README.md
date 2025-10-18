# 🧩 Blacklist Microservice DevOps

Microservicio en **Python + Flask + PostgreSQL** para gestionar una **lista negra global de correos electrónicos**.
Desarrollado y desplegado manualmente en **AWS Elastic Beanstalk (PaaS)** como parte del curso
**“DevOps: Agilizando el Despliegue Continuo de Aplicaciones” – Universidad de los Andes.**

---

## 🚀 Objetivo

Implementar un microservicio REST que permita:
- Agregar correos a una lista negra global.
- Consultar si un correo se encuentra en la lista negra.
- Realizar el despliegue manual en la nube (sin CI/CD).
- Documentar y probar los endpoints en **Postman**.
- Evaluar diferentes estrategias de despliegue en AWS Beanstalk.

---

## ⚙️ Stack Tecnológico

- **Lenguaje:** Python 3.8+
- **Framework:** Flask 1.1.x
- **Extensiones:**
  - Flask SQLAlchemy (ORM)
  - Flask RESTful (APIs)
  - Flask Marshmallow (serialización/validación)
  - Flask JWT Extended (autenticación Bearer)
  - Werkzeug
- **Base de Datos:** PostgreSQL (AWS RDS)
- **Proveedor Cloud:** AWS (Elastic Beanstalk + RDS)
- **Herramienta de documentación:** Postman

## 🏗️ Estructura del Proyecto

```
blacklist-microservice-devops/
├── app/
│   ├── __init__.py              # Factory pattern y configuración
│   ├── config.py                # Variables de entorno
│   ├── models.py                # Modelo Blacklist
│   ├── schemas.py               # Validación Marshmallow
│   ├── auth.py                  # Middleware Bearer token
│   ├── utils.py                 # Utilidades (IP, logging)
│   ├── wsgi.py                  # Entry point para EB
│   └── routes/
│       ├── __init__.py
│       ├── blacklists.py        # Endpoints principales
│       └── health.py            # Health check
├── requirements.txt
├── Procfile                     # Comando para EB
├── runtime.txt                  # Versión Python
└── .ebextensions/               # Configuración EB
```

---

## 📡 Endpoints del API REST

### `POST /blacklists`
Agrega un email a la lista negra global.
**Body (JSON):**
```json
{
  "email": "usuario@ejemplo.com",
  "app_uuid": "f2a1b8c9-7e6d-4d5b-9a8f-3a4b5c6d7e8f",
  "blocked_reason": "correo sospechoso"
}
````

**Header:**
`Authorization: Bearer <TOKEN>`
**Response:**

```json
{"message": "Email agregado exitosamente a la lista negra."}
```

---

### `GET /blacklists/<email>`

Consulta si un email está en la lista negra.
**Header:**
`Authorization: Bearer <TOKEN>`
**Response:**

```json
{
  "email": "usuario@ejemplo.com",
  "is_blacklisted": true,
  "reason": "correo sospechoso"
}
```

---

## 🚀 Configuración Local

### 1. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
export DATABASE_URL="sqlite:///blacklist.db"  # Para desarrollo local
export JWT_SECRET="dev-secret-key"
export APP_ALLOWED_BEARER="dev-bearer-token"
export FLASK_ENV="development"
```

### 4. Ejecutar aplicación
```bash
# Opción 1: Script de desarrollo (recomendado)
python run_server.py

# Opción 2: Script de inicio rápido
python start_dev.py

# Opción 3: Gunicorn (producción)
gunicorn app.wsgi:app
```

### 5. Probar la aplicación
```bash
# Ejecutar pruebas completas
python test_api.py

# Ejecutar pruebas simples
python test_simple.py
```

---

## 🧪 Pruebas de la API

### Health Check
Verificar que el servidor está funcionando:
```bash
curl http://localhost:5001/ping
```

### Agregar email a la lista negra
```bash
curl -X POST http://localhost:5001/blacklists \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-bearer-token" \
  -d '{
    "email": "test@example.com",
    "app_uuid": "f2a1b8c9-7e6d-4d5b-9a8f-3a4b5c6d7e8f",
    "blocked_reason": "correo de prueba"
  }'
```

### Consultar si un email está en la lista negra
```bash
# TODO: Pendiente implementación por Nata en rama feature/nata-get-endpoint
# curl -X GET http://localhost:5001/blacklists/test@example.com \
#   -H "Authorization: Bearer dev-bearer-token"
```

**Respuesta esperada (cuando esté implementado):**
```json
{
  "email": "test@example.com",
  "is_blacklisted": true,
  "reason": "correo de prueba"
}
```

**Estado actual:** ❌ GET endpoint temporalmente deshabilitado - Pendiente por Nata

---

## 🚧 Estado de Desarrollo

### ✅ Endpoints Implementados
- **POST /blacklists** - Agregar email a lista negra (Juan)
- **GET /ping** - Health check

### ⏳ Pendientes por Implementar
- **GET /blacklists/<email>** - Consultar email en lista negra (Nata)
  - Archivo: `app/routes/blacklists_get.py` (esqueleto creado)
  - Rama: `feature/nata-get-endpoint`
  - Requisitos: Auth Bearer, response shape { email, is_blacklisted, reason }, códigos 200/401/404

---

## 🧪 Pruebas con Postman

1. Crear una **colección Postman** con los dos endpoints.
2. Incluir variables globales (`base_url`, `token`).
3. Generar escenarios de prueba (exitoso y fallido).
4. Publicar la documentación y anexar la URL en el documento de entrega.

---

## ☁️ Despliegue en AWS Elastic Beanstalk

### 1. Preparación

* Crear entorno en **Elastic Beanstalk** (Python 3.8).
* Configurar **variables de entorno** (DB_URI, JWT_SECRET, etc.).
* Asociar una base de datos **PostgreSQL (AWS RDS)**.

### 2. Configurar Variables de Entorno en EB

En la consola de EB, ir a Configuration > Software:
- `DATABASE_URL`: `postgresql+psycopg2://user:pass@host:port/db`
- `JWT_SECRET`: Token secreto para JWT
- `APP_ALLOWED_BEARER`: Token estático para autenticación
- `FLASK_ENV`: `production`
- `LOG_LEVEL`: `INFO`

### 3. Despliegue

```bash
# Crear archivo ZIP (excluir venv y archivos innecesarios)
zip -r blacklist-microservice.zip . -x "venv/*" "*.pyc" "__pycache__/*" ".git/*"
```

* Subir archivo ZIP a Beanstalk
* Validar health checks en la consola
* Probar endpoints desde Postman

### 4. Health Check

El endpoint `/ping` está configurado para health checks automáticos de Beanstalk.

---

## 🔁 Estrategias de Despliegue

Documentar al menos **cuatro estrategias** distintas en Beanstalk (3–6 instancias):

* All-at-once
* Rolling
* Rolling with additional batch
* Immutable / Traffic Splitting

Para cada una incluir:

* # de instancias
* Tiempo total del despliegue
* Validación y capturas
* Hallazgos y observaciones

---

## 📄 Documento de la Entrega

**Nombre:** `Proyecto 1 Entrega 1 – Documento.pdf`
Debe incluir:

* Capturas paso a paso (RDS, Beanstalk, health checks).
* Estrategias de despliegue y análisis.
* URL de Postman Docs y GitHub Repo.

---

## 🎥 Video de Sustentación

Duración máxima: **10 minutos.**
Debe mostrar:

* API funcional en AWS
* Pruebas desde Postman
* Consola de Beanstalk y RDS
* Explicación técnica breve del código y despliegue

---

## 👥 Autores

| Integrante | Correo | GitHub |
|------------|--------|--------|
| Angie Natalia Arandio Niño | a.arandio@uniandes.edu.co | [@nataliaarandio](https://github.com/nataliaarandio) |
| Jazmin Natalia Cordoba Puerto | jn.cordobap1@uniandes.edu.co | [@JazminCorAndes](https://github.com/JazminCorAndes) |
| Juan Esteban Mejia Isaza | je.mejiai1@uniandes.edu.co | [@JUANES545](https://github.com/JUANES545) |
| Miguel Alejandro Gomez Alarcon | ma.gomeza1@uniandes.edu.co | [@Migue765](https://github.com/Migue765) |

---

## 📚 Referencias

* AWS Elastic Beanstalk Documentation
* Flask Official Documentation
* [DevOps: A Software Architect’s Perspective – Addison-Wesley, 2015]
* [AWS Whitepaper – Deployment Strategies](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/aeb-deployment-strategies.html)


¿Quieres que te genere una versión editable (en `.md` lista para GitHub`) con secciones vacías para que tu equipo solo complete nombres, capturas y URLs?
```
