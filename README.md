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
  - Flask SQLAlchemy  
  - Flask RESTful  
  - Flask Marshmallow  
  - Flask JWT Extended  
  - Werkzeug  
- **Base de Datos:** PostgreSQL (AWS RDS)
- **Proveedor Cloud:** AWS (Elastic Beanstalk + RDS)
- **Herramienta de documentación:** Postman

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

### 2. Despliegue

* Comprimir el proyecto (`zip`) y cargarlo manualmente a Beanstalk.
* Validar health checks en la consola.
* Probar endpoints desde Postman.

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

* *Nombre del estudiante 1*
* *Nombre del estudiante 2*
* *Nombre del estudiante 3*
* *Nombre del estudiante 4*

Universidad de los Andes – Maestría en Ingeniería de Software
Curso: *DevOps: Agilizando el Despliegue Continuo de Aplicaciones*
Profesor: *Mario José Villamizar Cano*

---

## 📚 Referencias

* AWS Elastic Beanstalk Documentation
* Flask Official Documentation
* [DevOps: A Software Architect’s Perspective – Addison-Wesley, 2015]
* [AWS Whitepaper – Deployment Strategies](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/aeb-deployment-strategies.html)


¿Quieres que te genere una versión editable (en `.md` lista para GitHub`) con secciones vacías para que tu equipo solo complete nombres, capturas y URLs?
```
