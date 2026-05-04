from abc import ABC, abstractmethod

# Clase base abstracta que define la estructura de las entidades en el sistema


class EntidadBase(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def validar_datos(self):
        pass

    @abstractmethod
    def registrar_cliente(self):
        pass

    @abstractmethod
    def mostrar_informacion(self):
        pass


# Clase Cliente
class Cliente(EntidadBase):
    def __init__(self, nombre, documento, correo):
        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo

    # Validacion de los datos del cliente

    def validar_datos(self):
        if not self.__nombre or not self.__documento or not self.__correo:
            raise ValueError("Todos los campos son obligatorios.")
        if "@" not in self.__correo:
            raise ValueError("Correo electrónico no válido.")

        try:
            int(self.__documento) and len(self.__documento) <= 10
        except ValueError:
            raise ValueError("Documento de identidad debe ser numérico.")

    # Validadcion de los datos del cliente

    def registrar_cliente(self):

        self.input_nombre = input("Ingrese el nombre del cliente: ")
        self.input_documento = input("Ingrese el documento de identidad del cliente: ")
        self.input_correo = input("Ingrese el correo electrónico del cliente: ")
        self.__nombre = self.input_nombre
        self.__documento = self.input_documento
        self.__correo = self.input_correo
        return self.input_nombre, self.input_documento, self.input_correo

    # Mostrar la informacion del cliente

    def mostrar_informacion(self):
        return f"Nombre: {self.__nombre}, Documento: {self.__documento}, Correo: {self.__correo}"
