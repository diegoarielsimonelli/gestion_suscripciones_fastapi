import datetime
from sqlmodel import SQLModel, Field

class Servicio(SQLModel, table=True):
    """Mapeo de la tabla de PostgreSQL."""
    id: int|None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    precio_mensual: float
    fecha_vencimiento: datetime.date|None = Field(default=None)

    def esta_activo(self) -> bool:
        if self.fecha_vencimiento is None:
            return True
        return self.fecha_vencimiento >= datetime.date.today()
