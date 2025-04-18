import mysql.connector
from mysql.connector import Error

# Clase Database que gestiona la conexión y operaciones con la base de datos MySQL
class Database:
    """
    Clase que maneja todas las operaciones de base de datos del sistema.
    Proporciona métodos para ejecutar consultas SQL y gestionar la conexión
    con el servidor MySQL.
    """
    
    def __init__(self):
        """
        Constructor que inicializa la conexión a la base de datos.
        Crea la base de datos y las tablas si no existen.
        """
        try:
            # Establece la conexión inicial con el servidor MySQL
            self.conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password=''
            )
            self.cursor = self.conexion.cursor()
            
            # Crea la base de datos si no existe y la selecciona para uso
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS hostal_minks")
            self.cursor.execute("USE hostal_minks")
            
            # Inicializa la estructura de la base de datos
            self.crear_tablas()
            print("Conexión exitosa a la base de datos")
            
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self.conexion = None
            self.cursor = None

    def crear_tablas(self):
        """
        Crea las tablas necesarias en la base de datos si no existen.
        Define la estructura de datos para usuarios, habitaciones, servicios y reservas.
        """
        if not self.cursor:
            return

        # Tabla de usuarios: almacena información de clientes y funcionarios
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(50) UNIQUE,
                contraseña VARCHAR(100),
                perfil VARCHAR(20),
                estado VARCHAR(20),
                nombre VARCHAR(100),
                run VARCHAR(20),
                metodo_pago VARCHAR(50),
                email VARCHAR(100),
                numero_contacto VARCHAR(20)
            )
        """)

        # Tabla de habitaciones: gestiona el inventario de habitaciones
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitaciones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                numero_habitacion INT UNIQUE,
                tipo_habitacion VARCHAR(50),
                costo DECIMAL(10,2)
            )
        """)

        # Tabla de servicios: almacena los servicios adicionales disponibles
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_servicio VARCHAR(100) UNIQUE,
                tipo_servicio VARCHAR(50),
                descripcion TEXT,
                costo_persona DECIMAL(10,2)
            )
        """)

        # Tabla de reservas: gestiona las reservaciones de habitaciones
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT,
                id_habitacion INT,
                fecha_entrada DATE,
                fecha_salida DATE,
                num_personas INT,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
                FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id),
                INDEX idx_usuario_fecha (id_usuario, fecha_entrada)
            )
        """)

        # Tabla de relación reserva_servicios: gestiona los servicios incluidos en cada reserva
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reserva_servicios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_reserva INT,
                id_servicio INT,
                FOREIGN KEY (id_reserva) REFERENCES reservas(id),
                FOREIGN KEY (id_servicio) REFERENCES servicios(id)
            )
        """)
        self.conexion.commit()

    def ejecutar_query(self, query, params=None):
        """
        Ejecuta una consulta SQL en la base de datos
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta preparada
            
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return False
            
        try:
            self.cursor.execute(query, params or ())
            self.conexion.commit()
            return True
        except Error as e:
            print(f"Error al ejecutar query: {e}")
            return False

    def obtener_datos(self, query, params=None):
        """
        Ejecuta una consulta SELECT y retorna los resultados
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta preparada
            
        Returns:
            list: Lista de resultados de la consulta
        """
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return []
            
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al obtener datos: {e}")
            return []

    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos de manera segura
        """
        if self.conexion and self.conexion.is_connected():
            self.cursor.close()
            self.conexion.close()
            print("Conexión cerrada")

"""
Notas sobre la arquitectura de la base de datos:

1. Estructura de Datos:
   - Diseño relacional con tablas interconectadas
   - Uso de claves foráneas para mantener integridad referencial
   - Índices optimizados para consultas frecuentes

2. Gestión de Conexiones:
   - Conexión única por instancia de Database
   - Manejo de errores robusto
   - Cierre seguro de conexiones

3. Operaciones de Base de Datos:
   - Consultas preparadas para prevenir SQL injection
   - Transacciones automáticas para operaciones CRUD
   - Métodos genéricos para consultas comunes

4. Consideraciones de Seguridad:
   - Credenciales de base de datos en el código (deberían estar en un archivo de configuración)
   - No se implementa pooling de conexiones
   - Las contraseñas se almacenan en texto plano (deberían estar hasheadas)
""" 