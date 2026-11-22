"""Punto de entrada: ejecuta una demostración con operaciones correctas e incorrectas."""
from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reservas import Reserva
from gestor import GestorSoftwareFJ


def ejecutar_demo():
    sistema = GestorSoftwareFJ()
    print("\n=== SOFTWARE FJ | DEMOSTRACIÓN DEL SISTEMA ===")

    # try/except/else: si el registro sale bien, también lo informamos.
    try:
        c1 = Cliente("C001", "Laura Gómez", "laura@email.com", "3001234567")
        sistema.agregar_cliente(c1)
    except Exception as error:
        sistema.registrar_error("registro de cliente válido", error)
        print("No se pudo registrar el primer cliente:", error)
    else:
        print("1. Cliente registrado:", c1.nombre)

    # Datos incorrectos: el programa captura el error y sigue con la demo.
    try:
        Cliente("C002", "Al", "correo-invalido", "abc")
    except Exception as error:
        sistema.registrar_error("registro de cliente inválido", error)
        print("2. Cliente inválido controlado:", error)

    try:
        c2 = Cliente("C003", "Carlos Ruiz", "carlos@email.com", "3105556677")
        sistema.agregar_cliente(c2)
        print("3. Segundo cliente registrado:", c2.nombre)
    except Exception as error:
        sistema.registrar_error("segundo cliente", error)

    # Se crean servicios de tres tipos distintos.
    servicios = [
        ReservaSala("S001", "Sala Ejecutiva", 50000, 12),
        AlquilerEquipo("S002", "Portátiles", 18000, 8),
        Asesoria("S003", "Consultoría Python", 90000, "Desarrollo de software")
    ]
    for numero, servicio in enumerate(servicios, start=4):
        try:
            sistema.agregar_servicio(servicio)
            print(f"{numero}. Servicio creado:", servicio.describir())
        except Exception as error:
            sistema.registrar_error("creación de servicio", error)

    try:
        ReservaSala("S004", "Sala con tarifa errónea", -100, 5)
    except Exception as error:
        sistema.registrar_error("creación de servicio incorrecto", error)
        print("7. Servicio inválido controlado:", error)

    # Reserva exitosa de sala.
    try:
        r1 = Reserva("R001", c1, servicios[0], 2, {"personas": 6})
        sistema.agregar_reserva(r1)
        r1.confirmar()
        total = r1.procesar(descuento=0.05)
        print(f"8. Reserva procesada correctamente. Total: ${total:,.2f}")
    except Exception as error:
        sistema.registrar_error("reserva de sala", error)
        print("No se pudo completar la reserva:", error)

    # Reserva de equipos con una cantidad superior al inventario.
    try:
        r2 = Reserva("R002", c2, servicios[1], 3, {"cantidad": 20})
        sistema.agregar_reserva(r2)
        r2.confirmar()
    except Exception as error:
        sistema.registrar_error("reserva de equipos fallida", error)
        print("9. Reserva de equipos rechazada:", error)

    # Servicio no disponible.
    try:
        servicios[2].disponible = False
        r3 = Reserva("R003", c1, servicios[2], 1, {"modalidad": "virtual"})
        sistema.agregar_reserva(r3)
        r3.confirmar()
    except Exception as error:
        sistema.registrar_error("reserva de asesoría no disponible", error)
        print("10. Servicio no disponible controlado:", error)

    # Estado incorrecto: procesar sin confirmar.
    try:
        r4 = Reserva("R004", c2, servicios[0], 1, {"personas": 4})
        sistema.agregar_reserva(r4)
        r4.procesar()
    except Exception as error:
        sistema.registrar_error("procesamiento sin confirmar", error)
        print("11. Operación no permitida controlada:", error)

    # Parámetro de duración incorrecto.
    try:
        Reserva("R005", c1, servicios[0], 0, {"personas": 2})
    except Exception as error:
        sistema.registrar_error("reserva con duración inválida", error)
        print("12. Duración inválida controlada:", error)

    # Duplicado para comprobar la validación de códigos.
    try:
        sistema.agregar_cliente(Cliente("C001", "Otra Persona", "otra@email.com", "3001112233"))
    except Exception as error:
        sistema.registrar_error("registro duplicado", error)
        print("13. Código duplicado controlado:", error)

    # try/except/finally: el cierre se informa incluso si hubo una excepción.
    try:
        print("\nResumen final:", sistema.resumen())
        print("Reservas registradas:")
        for reserva in sistema.reservas:
            print(" -", reserva.obtener_resumen())
    except Exception as error:
        sistema.registrar_error("resumen final", error)
        print("No fue posible mostrar el resumen.")
    finally:
        print("\nLa demostración terminó. La aplicación se mantuvo activa.")
        print("Revisa logs/software_fj.log para consultar los eventos y errores.")


if __name__ == "__main__":
    ejecutar_demo()
