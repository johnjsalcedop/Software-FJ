from datetime import datetime
from entidades import Entidad
from excepciones import DatoInvalidoError, EstadoReservaError


class Reserva(Entidad):
    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, codigo, cliente, servicio, duracion, parametros=None):
        super().__init__(codigo)
        from clientes import Cliente
        from servicios import Servicio
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva necesita un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva necesita un servicio válido.")
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duración debe ser mayor que cero.")
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = float(duracion)
        self.__parametros = parametros or {}
        self.__estado = "PENDIENTE"
        self.__total = None
        self.__fecha_proceso = None

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def estado(self):
        return self.__estado

    @property
    def total(self):
        return self.__total

    def confirmar(self):
        if self.__estado != "PENDIENTE":
            raise EstadoReservaError("Solo se pueden confirmar reservas pendientes.")
        self.__servicio.validar_disponibilidad()
        self.__servicio.validar_parametros(**self.__parametros)
        self.__estado = "CONFIRMADA"
        return True

    def cancelar(self):
        if self.__estado in ("CANCELADA", "PROCESADA"):
            raise EstadoReservaError("No se puede cancelar una reserva cancelada o procesada.")
        self.__estado = "CANCELADA"

    def procesar(self, impuesto=0.19, descuento=0):
        if self.__estado != "CONFIRMADA":
            raise EstadoReservaError("La reserva debe estar confirmada antes de procesarse.")
        try:
            self.__total = self.__servicio.calcular_costo(
                self.__duracion, impuesto, descuento, **self.__parametros
            )
        except TypeError as exc:
            raise DatoInvalidoError("Los parámetros de cálculo no coinciden con el servicio.") from exc
        if not isinstance(self.__total, (int, float)) or self.__total <= 0:
            raise ArithmeticError("El total de la reserva no es válido.")
        self.__estado = "PROCESADA"
        self.__fecha_proceso = datetime.now()
        return self.__total

    def obtener_resumen(self):
        total = f"${self.__total:,.2f}" if self.__total is not None else "Pendiente"
        return (f"{self.codigo} | {self.__cliente.nombre} | "
                f"{self.__servicio.nombre} | {self.__estado} | {total}")
