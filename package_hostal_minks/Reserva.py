from .db import Database

# Clase Reserva que gestiona las reservaciones de habitaciones y servicios en el hostal
class Reserva():
    """
    Clase que maneja el proceso de reservas, incluyendo habitaciones y servicios adicionales.
    Proporciona funcionalidad para crear, modificar y cancelar reservas, así como
    gestionar los estados de las mismas.
    """
    
    # Atributos que definen una reserva
    id_reserva = 0           # Identificador único de la reserva
    run_cliente = ""         # RUN/DNI del cliente que realiza la reserva
    fecha_ingreso = ""       # Fecha de inicio de la estadía
    fecha_salida = ""        # Fecha de término de la estadía
    estado = ""             # Estado actual de la reserva (confirmada, cancelada, etc.)
    id_habitacion = 0       # Identificador de la habitación reservada
    servicios = []          # Lista de servicios adicionales incluidos en la reserva

    def __init__(self, id_reserva, run_cliente, fecha_ingreso, fecha_salida, estado, id_habitacion, servicios):
        """
        Constructor de la clase Reserva
        
        Args:
            id_reserva (int): Identificador único de la reserva
            run_cliente (str): RUN/DNI del cliente
            fecha_ingreso (str): Fecha de inicio en formato DD/MM/YYYY
            fecha_salida (str): Fecha de término en formato DD/MM/YYYY
            estado (str): Estado actual de la reserva
            id_habitacion (int): ID de la habitación reservada
            servicios (list): Lista de servicios adicionales
        """
        self.id_reserva = id_reserva
        self.run_cliente = run_cliente
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.estado = estado
        self.id_habitacion = id_habitacion
        self.servicios = servicios
        self.db = Database()

    def guardar(self):
        query = """
            INSERT INTO reservas (usuario_id, habitacion_id, servicio_id, fecha_check_in, fecha_check_out, cantidad_personas)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.db.ejecutar_query(query, (
            self.usuario_id, self.habitacion_id, self.servicio_id,
            self.fecha_check_in, self.fecha_check_out, self.cantidad_personas
        ))

    def actualizar(self):
        query = """
            UPDATE reservas 
            SET habitacion_id = %s, servicio_id = %s, fecha_check_in = %s, 
                fecha_check_out = %s, cantidad_personas = %s
            WHERE usuario_id = %s
        """
        return self.db.ejecutar_query(query, (
            self.habitacion_id, self.servicio_id, self.fecha_check_in,
            self.fecha_check_out, self.cantidad_personas, self.usuario_id
        ))

    def eliminar(self):
        query = "DELETE FROM reservas WHERE usuario_id = %s"
        return self.db.ejecutar_query(query, (self.usuario_id,))

    @staticmethod
    def obtener_todas():
        db = Database()
        query = "SELECT * FROM reservas"
        return db.obtener_datos(query)

    @staticmethod
    def obtener_por_usuario(usuario_id):
        db = Database()
        query = "SELECT * FROM reservas WHERE usuario_id = %s"
        resultado = db.obtener_datos(query, (usuario_id,))
        if resultado:
            return Reserva(
                resultado[0][1], resultado[0][2], resultado[0][3],
                resultado[0][4], resultado[0][5], resultado[0][6]
            )
        return None

"""
Notas sobre la arquitectura del sistema de reservas:

1. Gestión de Reservas:
   - Sistema centralizado para manejar reservaciones de habitaciones
   - Integración con el módulo de servicios adicionales
   - Control de estados y validaciones de disponibilidad

2. Interacción con la Base de Datos:
   - Utiliza la clase Database para persistencia de datos
   - Mantiene la integridad referencial con otras entidades
   - Implementa operaciones CRUD completas

3. Validaciones y Reglas de Negocio:
   - Verifica disponibilidad de habitaciones
   - Controla fechas de ingreso y salida
   - Gestiona la asignación de servicios adicionales

4. Integración con el Sistema:
   - Los métodos de negocio específicos se implementan en main.py
   - Coordina con las clases Cliente, Habitacion y Servicio
   - Mantiene la consistencia de los datos en todo el sistema
"""


