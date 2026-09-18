from sqlmodel import create_engine, SQLModel, Session

# Ruta de conexión usando las credenciales exactas del docker-compose
DATABASE_URL = "postgresql://admin:secret_password@localhost:5432/gestion_suscripciones"

# El motor de conexión (Engine) maneja la comunicación real con Postgres
engine = create_engine(DATABASE_URL, echo=True)  # echo=True te muestra las consultas SQL reales en la terminal

def init_db():
    """Crea las tablas en la base de datos si no existen."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Generador para manejar sesiones por cada petición de la API (Inyección de Dependencias)."""
    with Session(engine) as session:
        yield session
