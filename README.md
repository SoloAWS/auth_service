# Auth Service

Un servicio simple de autorización para validar tokens JWT.

## Descripción

Este servicio proporciona un endpoint `/auth` para validar tokens JWT. Utiliza una base de datos PostgreSQL para almacenar y verificar los tokens.

## Estructura del Proyecto

```
auth_service/
├── main.py              # Punto de entrada principal y endpoints
├── database.py          # Configuración de la base de datos
├── models.py            # Modelos de datos
├── seed_db.py           # Script para poblar la base de datos con tokens de prueba
├── requirements.txt     # Dependencias Python
├── Dockerfile           # Configuración para Docker
├── docker-compose.yml   # Configuración para Docker Compose
└── .env                 # Variables de entorno
```

## Endpoints

### `/auth`

- **Método**: POST
- **Headers**: `Authorization: Bearer <token>`
- **Respuesta**: 
  ```json
  {
    "authorized": true|false,
    "user_id": "string",
    "message": "string"
  }
  ```

### `/health`

- **Método**: GET
- **Respuesta**: `{"status": "ok"}`

## Configuración y Ejecución

### Con Docker Compose

1. Construir y ejecutar los contenedores:
   ```bash
   docker-compose up --build
   ```

2. El servicio estará disponible en `http://localhost:8001`

3. Para poblar la base de datos con tokens de prueba:
   ```bash
   docker-compose exec auth-service python seed_db.py
   ```

### Sin Docker

1. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Configurar una base de datos PostgreSQL y actualizar la variable `DATABASE_URL` en `.env`

3. Ejecutar el servicio:
   ```bash
   uvicorn main:app --reload
   ```

4. Poblar la base de datos con tokens de prueba:
   ```bash
   python seed_db.py
   ```

## Tokens de Prueba

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkRhdGFQYXJ0bmVyIn0.BnLA0KJC3-fQBzpK0KfSO0p4s-KUEHNlpdvUx0Qkzsk
```

Este token corresponde al usuario `partner123`.