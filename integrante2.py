from abc import ABC, abstractmethod  
#cambio 
# Clase abstracta "servicio"
# Sirve como plantilla para otros servicios que hereden de esta
class servicio(ABC):      

    # Constructor de la clase
    # Inicializa los atributos nombre y costo_base
    def __init__(self, nombre, costo_base):        
        self.nombre = nombre        
        self.costo_base = costo_base  

    # Getter del atributo nombre
    @property 
    def nombre(self):    
        return self.__nombre  

    # Setter del atributo nombre con validación
    @nombre.setter 
    def nombre(self, valor):        
        # Verifica que sea un string y no esté vacío
        if not isinstance(valor, str) or valor.strip() == "":            
            raise ValueError("El nombre del servicio no puede estar vacío.")        
        self.__nombre = valor  

    # Getter del atributo costo_base
    @property 
    def costo_base(self):    
        return self.__costo_base  

    # Setter del atributo costo_base con validaciones
    @costo_base.setter 
    def costo_base(self, valor):        
        # Verifica que sea numérico (int o float)
        if not isinstance(valor, (int, float)):            
            raise TypeError("El costo base debe ser numérico.")  

        # Verifica que sea mayor que cero
        if valor <= 0:            
            raise ValueError("El costo base debe ser mayor que cero.")  

        self.__costo_base = valor  

    # Método abstracto para calcular el costo
    # Debe ser implementado en las clases hijas
    @abstractmethod 
    def calcular_costo(self, args, kwargs):    
        pass  

    # Método abstracto para describir el servicio
    @abstractmethod 
    def descripcion(self):    
        pass  

    # Método abstracto para validar parámetros específicos
    @abstractmethod 
    def validar_parametros(self):    
        pass  