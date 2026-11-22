import re
from entidades import Entidad
from excepciones import DatoInvalidoError


class Cliente(Entidad):
    def __init__(self, codigo, nombre, correo, telefono):
        super().__init__(codigo)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip().title()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor.strip()):
            raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        limpio = re.sub(r"[\s+\-()]", "", str(valor))
        if not limpio.isdigit() or not 7 <= len(limpio) <= 15:
            raise DatoInvalidoError("El teléfono debe contener entre 7 y 15 dígitos.")
        self.__telefono = str(valor).strip()

    def obtener_resumen(self):
        return f"{self.codigo} | {self.nombre} | {self.correo} | {self.telefono}"

    def __str__(self):
        return self.obtener_resumen()
