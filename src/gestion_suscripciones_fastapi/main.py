from contextlib import asynccontextmanager
from fastapi import FastAPI
from gestion_suscripciones_fastapi.database import init_db
from gestion_suscripciones_fastapi.routes import router as servicios_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Inicializando base de datos en PostgreSQL...")
    init_db()
    yield
    print("🛑 Apagando el servidor...")

app = FastAPI(
    title="Sistema de Gestión de Suscripciones API Modular",
    version="2.0.0",
    lifespan=lifespan
)

# Inyectamos el módulo de rutas completo a la aplicación principal
app.include_router(servicios_router)
