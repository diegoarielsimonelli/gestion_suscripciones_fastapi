class SuscripcionBaseError(Exception):
    """Excepción raíz del sistema."""
    pass

class ErrorDeLogicaNegocio(SuscripcionBaseError):
    """Errores que violan las reglas de la aplicación."""
    def __str__(self):
        return f"⚠️ [REGLA DE NEGOCIO VIOLADA] -> {self.args[0]}"
