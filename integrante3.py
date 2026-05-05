from integrante2 import servicio
from datetime import datetime

# Esta funcion la usamos para escribir en el archivo errores.txt cada vez que pase algo importante o haya un error
def guardar_registro(mensaje, tipo="ERROR"):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("errores.txt", "a") as archivo:
        archivo.write(f"{fecha} - {tipo} - {mensaje}\n")

# estas son las excepciones personalizadas que creamos para manejar errores especificos de cada servicio
class SalaNoDisponibleError(Exception):
    """se lanza cuando la sala que piden no existe o no tiene capacidad"""
    pass

class EquipoNoDisponibleError(Exception):
    """se lanza cuando el equipo que piden no esta en la lista de disponibles"""
    pass

class AsesoriaInvalidaError(Exception):
    """se lanza cuando el area o el nivel de la asesoria no son validos"""
    pass


# SERVICIO DE SALA
# Esta clase hereda de servicio y se encarga de todo lo relacionado con reservar salas
class ServicioSala(servicio):
    # Aca definimos las salas que existen y cuantas personas caben en cada una
    salas_disponibles = {
        "sala_A": 10,
        "sala_B": 20,
        "sala_C": 50
    }

    # En el constructor recibimos los datos de la sala que quieren reservar
    def __init__(self, nombre, costo_base, sala, horas, personas):
        super().__init__(nombre, costo_base)
        self.sala = sala
        self.horas = horas
        self.personas = personas

    # Aca validamos que la sala exista, que las horas y personas sean correctas y que no se pase de la capacidad
    def validar_parametros(self):
        if self.sala not in self.salas_disponibles:
            raise SalaNoDisponibleError(f"La sala '{self.sala}' no existe. Disponibles: {list(self.salas_disponibles.keys())}")

        if not isinstance(self.horas, (int, float)) or self.horas <= 0:
            raise ValueError("Las horas deben ser un numero mayor a 0")

        if not isinstance(self.personas, int) or self.personas <= 0:
            raise ValueError("La cantidad de personas debe ser un entero mayor a 0")

        capacidad = self.salas_disponibles[self.sala]
        if self.personas > capacidad:
            raise SalaNoDisponibleError(f"La sala '{self.sala}' tiene capacidad para {capacidad} personas, pero se pidieron {self.personas}")

    # Este metodo calcula en cuánto sale reservar la sala
    # Le podemos pasar impuesto y descuento o no, por eso tienen valor por defecto en 0
    def calcular_costo(self, impuesto=0, descuento=0):
        # Primero validamos que los datos esten bien, si no, se registra el error y se lanza la excepcion
        try:
            self.validar_parametros()
        except (SalaNoDisponibleError, ValueError) as e:
            guardar_registro(f"Error validando sala: {e}")
            raise

        # El total es el costo base por la cantidad de horas
        total = self.costo_base * self.horas

        # Aca intentamos aplicar el descuento, si el tipo de dato es incorrecto se encadena la excepcion
        try:
            if descuento < 0 or descuento > 100:
                raise ValueError("El descuento debe estar entre 0 y 100")
            total = total - (total * descuento / 100)
        except TypeError as e:
            raise ValueError("El descuento debe ser un numero") from e
        finally:
            # El finally se ejecuta siempre, haya error o no, y registramos que se proceso el calculo
            guardar_registro(f"Calculo de costo para sala '{self.sala}' procesado", "INFO")

        # Si nos pasaron impuesto lo sumamos al total
        if impuesto > 0:
            total = total + (total * impuesto / 100)
        else:
            # Si no hay impuesto no hacemos nada
            pass

        return round(total, 2)

    # Este metodo retorna un string con la info de la reserva de sala
    def descripcion(self):
        return (f"Reserva de '{self.sala}' para {self.personas} personas "
                f"por {self.horas} horas. Costo base por hora: ${self.costo_base}")


# SERVICIO DE EQUIPO
# Esta clase hereda de servicio y maneja el alquiler de equipos como portatiles, proyectores, etc
class ServicioEquipo(servicio):
    # Estos son los equipos que se pueden alquilar y el costo extra que tiene cada uno por dia
    equipos_disponibles = {
        "portatil": 15000,
        "proyector": 10000,
        "impresora": 8000,
        "tablet": 12000
    }

    # Recibimos el tipo de equipo, cuantos dias y cuantas unidades quieren
    def __init__(self, nombre, costo_base, tipo_equipo, dias, cantidad):
        super().__init__(nombre, costo_base)
        self.tipo_equipo = tipo_equipo
        self.dias = dias
        self.cantidad = cantidad

    # Validamos que el equipo exista y que los dias y cantidad sean numeros validos
    def validar_parametros(self):
        if self.tipo_equipo not in self.equipos_disponibles:
            raise EquipoNoDisponibleError(f"El equipo '{self.tipo_equipo}' no esta disponible. Disponibles: {list(self.equipos_disponibles.keys())}")

        if not isinstance(self.dias, int) or self.dias <= 0:
            raise ValueError("Los dias deben ser un entero mayor a 0")

        if not isinstance(self.cantidad, int) or self.cantidad <= 0:
            raise ValueError("La cantidad de equipos debe ser un entero mayor a 0")

    # Calcula el costo total del alquiler, con impuesto y descuento opcionales
    def calcular_costo(self, impuesto=0, descuento=0):
        # Validamos los parametros y si falla lo registramos en el log
        try:
            self.validar_parametros()
        except (EquipoNoDisponibleError, ValueError) as e:
            guardar_registro(f"Error validando equipo: {e}")
            raise

        # El total es el costo base mas el costo extra del equipo, multiplicado por dias y cantidad
        costo_adicional = self.equipos_disponibles[self.tipo_equipo]
        total = (self.costo_base + costo_adicional) * self.dias * self.cantidad

        # Aplicamos descuento, si el dato viene mal se encadena la excepcion con from e
        try:
            if descuento < 0 or descuento > 100:
                raise ValueError("El descuento debe estar entre 0 y 100")
            total = total - (total * descuento / 100)
        except TypeError as e:
            raise ValueError("El descuento debe ser un numero") from e
        finally:
            guardar_registro(f"Calculo de costo para equipo '{self.tipo_equipo}' procesado", "INFO")

        # Sumamos el impuesto si viene
        if impuesto > 0:
            total = total + (total * impuesto / 100)

        return round(total, 2)

    # Retorna un string con la info del alquiler
    def descripcion(self):
        return (f"Alquiler de {self.cantidad} '{self.tipo_equipo}' "
                f"por {self.dias} dias. Costo base: ${self.costo_base}")


# SERVICIO DE ASESORIA
# Esta clase hereda de servicio y maneja las asesorias especializadas en diferentes areas
class ServicioAsesoria(servicio):
    # Este array contiene las areas en las que se puede pedir asesoria
    areas_disponibles = ["desarrollo_web", "base_datos", "redes", "seguridad", "inteligencia_artificial"]

    # Recibimos el area, las horas y el nivel (basico, intermedio o avanzado)
    def __init__(self, nombre, costo_base, area, horas, nivel):
        super().__init__(nombre, costo_base)
        self.area = area
        self.horas = horas
        self.nivel = nivel  # basico, intermedio o avanzado

    # Validamos que el area exista, que las horas sean correctas y que el nivel sea uno de los permitidos
    def validar_parametros(self):
        if self.area not in self.areas_disponibles:
            raise AsesoriaInvalidaError(f"El area '{self.area}' no esta disponible. Areas: {self.areas_disponibles}")

        if not isinstance(self.horas, (int, float)) or self.horas <= 0:
            raise ValueError("Las horas deben ser un numero mayor a 0")

        niveles_validos = ["basico", "intermedio", "avanzado"]
        if self.nivel not in niveles_validos:
            raise AsesoriaInvalidaError(f"El nivel '{self.nivel}' no es valido. Usar: {niveles_validos}")

    # Calcula el costo de la asesoria, el nivel afecta el precio porque tiene un multiplicador distinto
    def calcular_costo(self, impuesto=0, descuento=0):
        # Validamos y si hay error lo registramos
        try:
            self.validar_parametros()
        except (AsesoriaInvalidaError, ValueError) as e:
            guardar_registro(f"Error validando asesoria: {e}")
            raise

        # Dependiendo del nivel se multiplica el costo, avanzado sale el doble que basico
        multiplicadores = {
            "basico": 1.0,
            "intermedio": 1.5,
            "avanzado": 2.0
        }

        multiplicador = multiplicadores[self.nivel]
        total = self.costo_base * self.horas * multiplicador

        # Aplicamos descuento, usamos encadenamiento de excepciones (raise from) por si el dato viene mal
        try:
            if descuento < 0 or descuento > 100:
                raise ValueError("El descuento debe estar entre 0 y 100")
            total = total - (total * descuento / 100)
        except TypeError as e:
            raise ValueError("El descuento debe ser un numero") from e
        finally:
            guardar_registro(f"Calculo de costo para asesoria '{self.area}' procesado", "INFO")

        # Aca usamos try/except/else, si no hay error con el impuesto entra al else y registra que salio bien
        try:
            if impuesto > 0:
                total = total + (total * impuesto / 100)
        except TypeError:
            guardar_registro("El impuesto debe ser un numero")
            raise ValueError("El impuesto debe ser numerico")
        else:
            guardar_registro(f"Impuesto aplicado correctamente para asesoria '{self.area}'", "INFO")

        return round(total, 2)

    # Retorna un string con la info de la asesoria
    def descripcion(self):
        return (f"Asesoria en '{self.area}' nivel {self.nivel} "
                f"por {self.horas} horas. Costo base por hora: ${self.costo_base}")
