from .db import Database

# Clase Habitacion que gestiona la información y disponibilidad de las habitaciones del hostal
class Habitacion():
    """
    Clase que maneja las habitaciones del hostal, incluyendo su información básica,
    disponibilidad y costos. Proporciona funcionalidad para gestionar las habitaciones
    y su estado en el sistema.
    """
    
    def __init__(self, numero_habitacion, tipo_habitacion, costo):
        """
        Constructor de la clase Habitacion
        
        Args:
            numero_habitacion (int): Número identificador único de la habitación
            tipo_habitacion (str): Tipo de habitación (individual, doble, suite)
            costo (float): Costo por noche de la habitación
        """
        # Atributos que definen una habitación
        self.numero_habitacion = numero_habitacion  # Identificador único
        self.tipo_habitacion = tipo_habitacion      # Tipo de habitación
        self.costo = costo                          # Costo por noche
        self.db = Database()                        # Conexión a la base de datos

    def guardar(self):
        """
        Guarda una nueva habitación en la base de datos
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        query = """
            INSERT INTO habitaciones (numero_habitacion, tipo_habitacion, costo)
            VALUES (%s, %s, %s)
        """
        return self.db.ejecutar_query(query, (self.numero_habitacion, self.tipo_habitacion, self.costo))

    def actualizar(self):
        """
        Actualiza la información de una habitación existente
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        query = """
            UPDATE habitaciones 
            SET tipo_habitacion = %s, costo = %s
            WHERE numero_habitacion = %s
        """
        return self.db.ejecutar_query(query, (self.tipo_habitacion, self.costo, self.numero_habitacion))

    def eliminar(self):
        """
        Elimina una habitación del sistema
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
        """
        query = "DELETE FROM habitaciones WHERE numero_habitacion = %s"
        return self.db.ejecutar_query(query, (self.numero_habitacion,))

    @staticmethod
    def obtener_todas():
        """
        Obtiene todas las habitaciones registradas en el sistema
        
        Returns:
            list: Lista de todas las habitaciones en la base de datos
        """
        db = Database()
        query = "SELECT * FROM habitaciones"
        return db.obtener_datos(query)

    @staticmethod
    def obtener_por_numero(numero_habitacion):
        """
        Busca una habitación específica por su número
        
        Args:
            numero_habitacion (int): Número de la habitación a buscar
            
        Returns:
            Habitacion: Instancia de Habitacion si se encuentra, None si no existe
        """
        db = Database()
        query = "SELECT * FROM habitaciones WHERE numero_habitacion = %s"
        resultado = db.obtener_datos(query, (numero_habitacion,))
        if resultado:
            return Habitacion(resultado[0][1], resultado[0][2], resultado[0][3])
        return None

"""
Notas sobre la arquitectura del sistema de habitaciones:

1. Gestión de Habitaciones:
   - Sistema centralizado para manejar el inventario de habitaciones
   - Control de tipos y costos de habitaciones
   - Integración con el sistema de reservas

2. Interacción con la Base de Datos:
   - Utiliza la clase Database para persistencia de datos
   - Mantiene la integridad de los datos de habitaciones
   - Implementa operaciones CRUD completas

3. Validaciones y Reglas de Negocio:
   - Verifica la existencia de habitaciones
   - Mantiene consistencia en los tipos de habitación
   - Gestiona los costos asociados

4. Integración con el Sistema:
   - Los métodos de negocio específicos se implementan en main.py
   - Coordina con las clases Reserva y Servicio
   - Mantiene la consistencia de los datos en todo el sistema
"""