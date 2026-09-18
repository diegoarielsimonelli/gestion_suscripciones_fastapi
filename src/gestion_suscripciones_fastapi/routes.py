import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from gestion_suscripciones_fastapi.database import get_session
from gestion_suscripciones_fastapi.modelos import Servicio

# Creamos el router modular
router = APIRouter(prefix="/servicios", tags=["Servicios de Suscripción"])

@router.post(
    "/", 
    response_model=Servicio, 
    status_code=status.HTTP_201_CREATED,
    summary="Contratar / Registrar un nuevo servicio"
)
def crear_servicio(servicio: Servicio, session: Session = Depends(get_session)):
    """
    Registra un nuevo servicio en el sistema.
    
    Valida automáticamente que el nombre no esté duplicado en PostgreSQL.
    """
    # Verificamos si ya existe un servicio con ese mismo nombre
    statement = select(Servicio).where(Servicio.nombre == servicio.nombre)
    servicio_existente = session.exec(statement).first()
    
    if servicio_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El servicio '{servicio.nombre}' ya se encuentra registrado."
        )
        
    if servicio.precio_mensual <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El precio mensual debe ser mayor a cero."
        )

    # Si pasa las validaciones, lo guardamos mediante el ORM
    session.add(servicio)
    session.commit()
    session.refresh(servicio)  # Recupera el ID autogenerado por Postgres
    return servicio


@router.get(
    "/", 
    response_model=List[Servicio],
    summary="Listar todos los servicios registrados"
)
def listar_servicios(session: Session = Depends(get_session)):
    """
    Trae el listado completo de servicios almacenados en la base de datos PostgreSQL.
    """
    statement = select(Servicio)
    servicios = session.exec(statement).all()
    return servicios
@router.get(
    "/activos", 
    response_model=List[Servicio],
    summary="Listar únicamente los servicios que no están vencidos"
)
def listar_servicios_activos(session: Session = Depends(get_session)):
    """
    Realiza una consulta a PostgreSQL filtrando de manera eficiente.
    
    Trae los servicios cuya fecha de vencimiento sea hoy, posterior, o nula (sin vencimiento).
    """
    hoy = datetime.date.today()
    
    # Expresamos la consulta SQL usando SQLModel
    # Filtra: fecha_vencimiento >= hoy O fecha_vencimiento es NULL
    statement = select(Servicio).where(
        (Servicio.fecha_vencimiento >= hoy) | (Servicio.fecha_vencimiento == None)
    )
    
    servicios_activos = session.exec(statement).all()
    return servicios_activos


@router.get(
    "/total",
    summary="Calcular el costo total de los servicios activos con cupones"
)
def calcular_total_suscripciones(
    cupon: str|None = None, 
    session: Session = Depends(get_session)
):
    """
    Calcula el subtotal acumulado de todas las suscripciones activas y aplica
    un cupón de descuento opcional por parámetro (BIENVENIDA o PROMO50).
    """
    # 1. Obtenemos solo los servicios activos de la base de datos
    hoy = datetime.date.today()
    statement = select(Servicio).where(
        (Servicio.fecha_vencimiento >= hoy) | (Servicio.fecha_vencimiento == None)
    )
    servicios = session.exec(statement).all()
    
    # 2. Sumamos sus precios mensuales
    subtotal = sum(s.precio_mensual for s in servicios)
    
    # 3. Aplicamos las reglas comerciales del cupón
    total = subtotal
    if cupon == "BIENVENIDA":
        total = subtotal * 0.90  # 10% descuento
    elif cupon == "PROMO50":
        total = subtotal * 0.50  # 50% descuento
        
    return {
        "cantidad_servicios_activos": len(servicios),
        "subtotal_base": round(subtotal, 2),
        "cupon_aplicado": cupon if cupon in ["BIENVENIDA", "PROMO50"] else "Ninguno",
        "total_final": round(total, 2)
    }