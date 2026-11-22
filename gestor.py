import logging
from pathlib import Path
from excepciones import RegistroDuplicadoError, NoEncontradoError


class GestorSoftwareFJ:
    def __init__(self, ruta_log="logs/software_fj.log"):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        ruta = Path(ruta_log)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        self.log = logging.getLogger("SoftwareFJ")
        self.log.setLevel(logging.INFO)
        self.log.propagate = False
        if not self.log.handlers:
            manejador = logging.FileHandler(ruta, encoding="utf-8")
            manejador.setFormatter(logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            ))
            self.log.addHandler(manejador)

    def _registrar(self, lista, objeto, tipo):
        if any(x.codigo == objeto.codigo for x in lista):
            raise RegistroDuplicadoError(f"Ya existe {tipo} con código {objeto.codigo}.")
        lista.append(objeto)
        self.log.info("%s registrado: %s", tipo, objeto.codigo)
        return objeto

    def agregar_cliente(self, cliente):
        return self._registrar(self.clientes, cliente, "Cliente")

    def agregar_servicio(self, servicio):
        return self._registrar(self.servicios, servicio, "Servicio")

    def agregar_reserva(self, reserva):
        return self._registrar(self.reservas, reserva, "Reserva")

    def buscar_cliente(self, codigo):
        for cliente in self.clientes:
            if cliente.codigo == codigo.upper():
                return cliente
        raise NoEncontradoError(f"No existe el cliente {codigo}.")

    def buscar_servicio(self, codigo):
        for servicio in self.servicios:
            if servicio.codigo == codigo.upper():
                return servicio
        raise NoEncontradoError(f"No existe el servicio {codigo}.")

    def registrar_error(self, operacion, error):
        self.log.exception("Error en %s: %s", operacion, error)

    def resumen(self):
        return {
            "clientes": len(self.clientes),
            "servicios": len(self.servicios),
            "reservas": len(self.reservas)
        }
