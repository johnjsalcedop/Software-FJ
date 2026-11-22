from abc import abstractmethod
from entidades import Entidad
from excepciones import DatoInvalidoError, ServicioNoDisponibleError


class Servicio(Entidad):
    def __init__(self, codigo, nombre, tarifa, disponible=True):
        super().__init__(codigo)
        self.nombre = nombre
        self.tarifa = tarifa
        self.disponible = disponible

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")
        self.__nombre = valor.strip()

    @property
    def tarifa(self):
        return self.__tarifa

    @tarifa.setter
    def tarifa(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            raise DatoInvalidoError("La tarifa debe ser un número mayor que cero.")
        self.__tarifa = float(valor)

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise DatoInvalidoError("La disponibilidad debe ser verdadera o falsa.")
        self.__disponible = valor

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio {self.nombre} no está disponible.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):
        """Permite calcular el costo base, con impuesto y/o con descuento."""
        self.validar_disponibilidad()
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duración debe ser un número mayor que cero.")
        if not 0 <= impuesto <= 1:
            raise DatoInvalidoError("El impuesto debe estar entre 0 y 1.")
        if not 0 <= descuento <= 1:
            raise DatoInvalidoError("El descuento debe estar entre 0 y 1.")

        subtotal = self.calcular_subtotal(float(duracion))
        total = subtotal * (1 - descuento) * (1 + impuesto)
        if total < 0 or total != total:
            raise ArithmeticError("El cálculo produjo un valor inconsistente.")
        return round(total, 2)

    def calcular_costo_simple(self, duracion):
        """Variante corta: aplica los valores predeterminados."""
        return self.calcular_costo(duracion)

    @abstractmethod
    def calcular_subtotal(self, duracion):
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, **kwargs):
        raise NotImplementedError

    def obtener_resumen(self):
        return f"{self.codigo} | {self.nombre} | ${self.tarifa:,.2f}"


class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, tarifa, capacidad, disponible=True):
        super().__init__(codigo, nombre, tarifa, disponible)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad < 1:
            raise DatoInvalidoError("La capacidad debe ser un entero positivo.")
        self.capacidad = capacidad

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0, personas=1):
        self.validar_parametros(personas=personas)
        return super().calcular_costo(duracion, impuesto, descuento)

    def validar_parametros(self, **kwargs):
        personas = kwargs.get("personas")
        if isinstance(personas, bool) or not isinstance(personas, int) or personas < 1:
            raise DatoInvalidoError("Indica una cantidad válida de personas.")
        if personas > self.capacidad:
            raise DatoInvalidoError("La cantidad de personas supera la capacidad de la sala.")

    def calcular_subtotal(self, duracion):
        return self.tarifa * duracion

    def describir(self):
        return f"Sala: {self.nombre}. Capacidad máxima: {self.capacidad} personas."


class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, tarifa, unidades, disponible=True):
        super().__init__(codigo, nombre, tarifa, disponible)
        if isinstance(unidades, bool) or not isinstance(unidades, int) or unidades < 1:
            raise DatoInvalidoError("Las unidades deben ser un entero positivo.")
        self.unidades = unidades

    def validar_parametros(self, **kwargs):
        cantidad = kwargs.get("cantidad")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 1:
            raise DatoInvalidoError("La cantidad de equipos debe ser un entero positivo.")
        if cantidad > self.unidades:
            raise ServicioNoDisponibleError("No hay suficientes equipos disponibles.")

    def calcular_subtotal(self, duracion):
        return self.tarifa * duracion

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0, cantidad=1):
        self.validar_parametros(cantidad=cantidad)
        return super().calcular_costo(duracion, impuesto, descuento) * cantidad

    def describir(self):
        return f"Alquiler de equipos: {self.nombre}. Unidades disponibles: {self.unidades}."


class Asesoria(Servicio):
    def __init__(self, codigo, nombre, tarifa, especialidad, disponible=True):
        super().__init__(codigo, nombre, tarifa, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError("La especialidad es obligatoria.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, **kwargs):
        modalidad = kwargs.get("modalidad", "virtual")
        if modalidad not in ("virtual", "presencial"):
            raise DatoInvalidoError("La modalidad debe ser virtual o presencial.")

    def calcular_subtotal(self, duracion):
        return self.tarifa * duracion

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0, modalidad="virtual"):
        self.validar_parametros(modalidad=modalidad)
        extra = 0.10 if modalidad == "presencial" else 0
        return super().calcular_costo(duracion, impuesto, descuento) * (1 + extra)

    def describir(self):
        return f"Asesoría especializada en {self.especialidad}: {self.nombre}."
