# Sistema de Gestión de Suscripciones API REST

Una API REST moderna, eficiente y completamente modularizada desarrollada con **FastAPI** y **SQLModel**. El sistema administra el registro de suscripciones, realiza consultas optimizadas con lógica temporal y calcula costos totales integrando cupones comerciales, persistiendo toda la información de manera segura en un motor relacional **PostgreSQL**.

Este repositorio representa el hito evolutivo de nivel **Semi-Senior**, donde se deja atrás el almacenamiento en memoria volátil para interactuar con infraestructura de producción mediante contenedores virtuales.

---

## 🛠️ Stack Tecnológico

- **[Python 3.12+]**: Uso de tipado estricto y la librería nativa `typing` (`Optional`, `List`) para asegurar contratos de datos limpios.
- **[FastAPI]**: Framework web asíncrono de alto rendimiento utilizado para la exposición de endpoints y la generación automática de documentación.
- **[SQLModel]**: Un ORM híbrido moderno (basado en SQLAlchemy y Pydantic) que unifica la definición de esquemas de bases de datos y la validación de peticiones HTTP en una sola clase de Python.
- **[PostgreSQL 16]**: Motor de base de datos relacional robusto utilizado como capa de persistencia definitiva.
- **[Docker & Docker Compose]**: Utilizado para empaquetar, aislar y levantar la infraestructura local con un solo comando.
- **[uv]**: Gestor de paquetes y entornos virtuales ultrarrápido utilizado para administrar el ciclo de vida del proyecto.

---

## 📐 Arquitectura del Software y Modularización

El proyecto implementa una separación estricta de responsabilidades (SoC), distribuyendo el código en componentes independientes para garantizar la mantenibilidad:

```text
gestion_suscripciones_fastapi/
│
├── src/
│   └── gestion_suscripciones_fastapi/
│       ├── __init__.py
│       ├── database.py      # Configuración del Engine del ORM y generador de sesiones por inyección
│       ├── excepciones.py   # Tipificación de errores personalizados de lógica de negocio
│       ├── modelos.py       # Definición de tablas relacionales con SQLModel e indexación estricta
│       ├── routes.py        # Módulo independiente de endpoints implementando APIRouter
│       └── main.py          # Inicialización limpia de FastAPI y ciclo de vida de la aplicación (lifespan)
│
├── docker-compose.yml       # Orquestación del contenedor local de PostgreSQL
├── pyproject.toml           # Metadatos del proyecto y dependencias manejadas por uv
└── README.md
```

### Patrones de diseño implementados:

1.  **Inyección de Dependencias (`Depends`)**: Se utiliza para inyectar de manera segura la sesión de la base de datos (`get_session`) en cada petición HTTP, garantizando la apertura y cierre automático de conexiones y previniendo fugas en el servidor.
2.  **Modularización mediante `APIRouter`**: Los endpoints están completamente desacoplados de la instancia global de la aplicación web, agrupados bajo prefijos limpios (`/servicios`) y tags organizacionales.
3.  **Ciclo de Vida Moderno (`lifespan`)**: FastAPI se encarga de disparar la comunicación con el ORM e inicializar las tablas de la base de datos automáticamente en el contenedor Docker justo antes de comenzar a escuchar peticiones.

---

## 🏁 Endpoints Disponibles (API Contract)

La API autogenera documentación interactiva bajo el estándar OpenAPI (Swagger UI). Los contratos principales expuestos son:

- `POST /servicios/` - Registra y contrata un nuevo servicio validando unicidad de nombre y precios mayores a cero (Devuelve HTTP 201).
- `GET /servicios/` - Retorna el listado histórico de todas las suscripciones en la base de datos.
- `GET /servicios/activos` - Realiza un filtrado eficiente directamente en PostgreSQL trayendo únicamente servicios cuya fecha de vencimiento sea igual, posterior al día de hoy, o nula.
- `GET /servicios/total` - Calcula la sumatoria de gastos activos y procesa la inyección de cupones comerciales opcionales (`BIENVENIDA`, `PROMO50`).

---

## 🚀 Instalación y Despliegue Local

Sigue estos pasos para clonar el proyecto, inicializar la base de datos distribuida y correr el servidor en tu entorno local:

1.  **Levantar la Base de Datos (Requiere Docker Desktop activo):**
    En la raíz del proyecto, ejecuta el comando para encender el contenedor de PostgreSQL en segundo plano:
    ```bash
    docker compose up -d
    ```
2.  **Instalar dependencias con `uv`:**
    ```bash
    uv add fastapi sqlmodel psycopg2-binary uvicorn
    ```
3.  **Encender el servidor de desarrollo:**
    ```bash
    uv run uvicorn gestion_suscripciones_fastapi.main:app --reload
    ```
4.  **Acceder a la documentación interactiva:**
    Abre tu navegador e ingresa a: [http://127.0.0](http://127.0.0)
