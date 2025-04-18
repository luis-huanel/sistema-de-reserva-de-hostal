from .db import Database

# Clase Servicio que gestiona los servicios adicionales ofrecidos por el hostal
class Servicio():
    """
    Clase que maneja los servicios adicionales del hostal, como desayuno, estacionamiento,
    tours y Wi-Fi. Proporciona funcionalidad para gestionar estos servicios y sus costos
    asociados.
    """
    
    # Atributos que definen un servicio
    nombreServicio = ""    # Nombre identificador del servicio
    tipoServicio = ""      # Categoría del servicio (alimentación, transporte, etc.)
    descripcion = ""       # Descripción detallada del servicio
    costoPersona = 0       # Costo por persona del servicio

    def __init__(self, nombre_servicio, tipo_servicio, descripcion, costo_persona):
        """
        Constructor de la clase Servicio
        
        Args:
            nombre_servicio (str): Nombre identificador del servicio
            tipo_servicio (str): Categoría del servicio
            descripcion (str): Descripción detallada
            costo_persona (float): Costo por persona
        """
        # Inicialización de atributos de la instancia
        self.nombre_servicio = nombre_servicio
        self.tipo_servicio = tipo_servicio
        self.descripcion = descripcion
        self.costo_persona = costo_persona
        self.db = Database()

    def guardar(self):
        """
        Guarda un nuevo servicio en la base de datos
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        query = """
            INSERT INTO servicios (nombre_servicio, tipo_servicio, descripcion, costo_persona)
            VALUES (%s, %s, %s, %s)
        """
        return self.db.ejecutar_query(query, (self.nombre_servicio, self.tipo_servicio, self.descripcion, self.costo_persona))

    def actualizar(self):
        """
        Actualiza la información de un servicio existente
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        query = """
            UPDATE servicios 
            SET tipo_servicio = %s, descripcion = %s, costo_persona = %s
            WHERE nombre_servicio = %s
        """
        return self.db.ejecutar_query(query, (self.tipo_servicio, self.descripcion, self.costo_persona, self.nombre_servicio))

    def eliminar(self):
        """
        Elimina un servicio del sistema
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
        """
        query = "DELETE FROM servicios WHERE nombre_servicio = %s"
        return self.db.ejecutar_query(query, (self.nombre_servicio,))

    @staticmethod
    def obtener_todos():
        """
        Obtiene todos los servicios registrados en el sistema
        
        Returns:
            list: Lista de todos los servicios en la base de datos
        """
        db = Database()
        query = "SELECT * FROM servicios"
        return db.obtener_datos(query)

    @staticmethod
    def obtener_por_nombre(nombre_servicio):
        """
        Busca un servicio específico por su nombre
        
        Args:
            nombre_servicio (str): Nombre del servicio a buscar
            
        Returns:
            Servicio: Instancia de Servicio si se encuentra, None si no existe
        """
        db = Database()
        query = "SELECT * FROM servicios WHERE nombre_servicio = %s"
        resultado = db.obtener_datos(query, (nombre_servicio,))
        if resultado:
            return Servicio(resultado[0][1], resultado[0][2], resultado[0][3], resultado[0][4])
        return None

"""
Notas sobre la arquitectura del sistema de servicios:

1. Gestión de Servicios:
   - Sistema centralizado para manejar servicios adicionales
   - Control de tipos y costos de servicios
   - Integración con el sistema de reservas

2. Interacción con la Base de Datos:
   - Utiliza la clase Database para persistencia de datos
   - Mantiene la integridad de los datos de servicios
   - Implementa operaciones CRUD completas

3. Validaciones y Reglas de Negocio:
   - Verifica la existencia de servicios
   - Mantiene consistencia en los tipos de servicio
   - Gestiona los costos asociados

4. Integración con el Sistema:
   - Los métodos de negocio específicos se implementan en main.py
   - Coordina con las clases Reserva y Habitacion
   - Mantiene la consistencia de los datos en todo el sistema
"""
