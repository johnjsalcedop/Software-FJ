from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Base común para los objetos principales del sistema."""

    def __init__(self, codigo):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código de la entidad es obligatorio.")
        self._codigo = codigo.strip().upper()
        self._creado = datetime.now()

    @property
    def codigo(self):
        return self._codigo

    @property
    def creado(self):
        return self._creado

    @abstractmethod
    def obtener_resumen(self):
        """Cada entidad define cómo mostrar su información básica."""
        raise NotImplementedError
