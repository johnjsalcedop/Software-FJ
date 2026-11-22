class ErrorSistema(Exception):
    """Error general del sistema Software FJ."""


class DatoInvalidoError(ErrorSistema):
    """Se usa cuando un dato no cumple las reglas esperadas."""


class RegistroDuplicadoError(ErrorSistema):
    """Se intenta registrar un elemento que ya existe."""


class NoEncontradoError(ErrorSistema):
    """No se encuentra el elemento solicitado."""


class ServicioNoDisponibleError(ErrorSistema):
    """El servicio no está disponible para la operación."""


class EstadoReservaError(ErrorSistema):
    """La operación no está permitida por el estado de la reserva."""
