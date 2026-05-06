#1007453198#
import uuid
from datetime import datetime
#Pruebas

class Reserva:
    def __init__(self, cliente, servicio, duracion, fecha_hora=None, estado="Pendiente"):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.fecha_hora = fecha_hora if fecha_hora else datetime.now()
        self.estado = estado
        self.id = str(uuid.uuid4())[:8]  # Generación directa del ID
        self.validar_datos()

    def validar_datos(self):
        if not hasattr(self.cliente, "nombre"):
            raise ValueError("El cliente debe tener atributo 'nombre'")
        if not hasattr(self.servicio, "nombre"):
            raise ValueError("El servicio debe tener atributo 'nombre'")
        if not isinstance(self.duracion, (int, float)) or self.duracion <= 0:
            raise ValueError("La duración debe ser un número positivo")
        if self.estado not in ["Pendiente", "Confirmada", "Cancelada", "Completada"]:
            raise ValueError("Estado no válido")

    def confirmar(self):
        if self.estado == "Cancelada":
            raise Exception("No se puede confirmar una reserva cancelada")
        if self.estado == "Completada":
            raise Exception("La reserva ya fue completada")
        self.estado = "Confirmada"
        return f"Reserva {self.id} confirmada para {self.cliente.nombre}"

    def cancelar(self):
        if self.estado == "Completada":
            raise Exception("No se puede cancelar una reserva completada")
        self.estado = "Cancelada"
        return f"Reserva {self.id} cancelada"

    def procesar_reserva(self):
        if self.estado != "Confirmada":
            raise Exception("Solo se pueden procesar reservas confirmadas")
        self.estado = "Completada"
        return f"Reserva {self.id} procesada exitosamente"

    def mostrar_informacion(self):
        return (f"ID: {self.id} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Duración: {self.duracion}h | "
                f"Fecha: {self.fecha_hora.strftime('%Y-%m-%d %H:%M')} | Estado: {self.estado}")


class GestorReservas:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        self.clientes.append(cliente)

    def registrar_servicio(self, servicio):
        self.servicios.append(servicio)

    def crear_reserva(self, cliente, servicio, duracion):
        nueva_reserva = Reserva(cliente, servicio, duracion)
        self.reservas.append(nueva_reserva)
        return nueva_reserva

    def confirmar_reserva(self, id_reserva):
        reserva = self.buscar_reserva(id_reserva)
        return reserva.confirmar()

    def cancelar_reserva(self, id_reserva):
        reserva = self.buscar_reserva(id_reserva)
        return reserva.cancelar()

    def procesar_reserva(self, id_reserva):
        reserva = self.buscar_reserva(id_reserva)
        return reserva.procesar_reserva()

    def buscar_reserva(self, id_reserva):
        for r in self.reservas:
            if r.id == id_reserva:
                return r
        raise ValueError(f"No existe reserva con ID {id_reserva}")

    def mostrar_todas_reservas(self):
        if not self.reservas:
            return "No hay reservas registradas"
        return "\n".join([r.mostrar_informacion() for r in self.reservas])