# Software FJ – Sistema Integral de Gestión

La aplicación está desarrollada en Python, sin bases de datos. Gestiona clientes, servicios y reservas utilizando objetos y listas en memoria.

## Ejecución
Desde la carpeta del proyecto:

```bash
python main.py
```

El programa realizará una demostración de algunas operaciones válidas e inválidas. Los eventos y errores quedan registrados en `logs/software_fj.log`.

- `entidades.py`: clase abstracta base `Entidad`.
- `clientes.py`: cliente con atributos encapsulados y validaciones.
- `servicios.py`: clase abstracta `Servicio` y tres servicios concretos.
- `reservas.py`: ciclo de vida de las reservas.
- `excepciones.py`: excepciones propias del sistema.
- `gestor.py`: listas internas, búsquedas y registro de eventos.
- `main.py`: demostración de 13 operaciones.

## Principios POO
- **Abstracción:** `Entidad` y `Servicio` son clases abstractas.
- **Herencia:** `Cliente`, `ReservaSala`, `AlquilerEquipo` y `Asesoria` heredan de sus clases base.
- **Polimorfismo:** cada servicio implementa sus propias reglas, descripción y cálculo.
- **Encapsulación:** los datos personales del cliente y el estado interno de la reserva se protegen mediante atributos privados y propiedades.
- **Sobrecarga simulada:** Python no ofrece sobrecarga tradicional por firma; se aprovechan parámetros opcionales y métodos especializados para admitir distintas variantes de cálculo.

## Manejo de errores
Ene l código utilizo excepciones personalizadas como lo dice el proyecto, bloques `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from exc`. Los errores se almacenarán en el archivo de log.

## 
Los clientes, servicios y reservas viven en memoria y se reinician al cerrar el programa. El único archivo que se utiliza es el log de eventos y errores, tal como pide el ejercicio.
