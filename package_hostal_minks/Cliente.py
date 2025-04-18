from .db import Database

# Clase base Cliente que maneja la información personal de los usuarios del sistema
class Cliente():
    # Atributos base para almacenar información personal del cliente
    nombre = ""          # Nombre completo del cliente
    RUN = ""            # Número de identificación personal (RUT/DNI)
    metodoPago = ""     # Método de pago preferido
    email = ""          # Correo electrónico de contacto
    numeroContacto = 0  # Número telefónico de contacto

    def __init__(self, nombre, run, metodo_pago, email, numero_contacto):
        """
        Inicializa un nuevo cliente con su información personal
        
        Args:
            nombre (str): Nombre completo del cliente
            run (str): Número de identificación personal
            metodo_pago (str): Método de pago preferido
            email (str): Correo electrónico
            numero_contacto (str): Número de teléfono
        """
        self.nombre = nombre
        self.run = run
        self.metodo_pago = metodo_pago
        self.email = email
        self.numero_contacto = numero_contacto
        self.db = Database()

    def guardar(self):
        query = """
            INSERT INTO usuarios (nombre, run, metodo_pago, email, numero_contacto)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.ejecutar_query(query, (
            self.nombre, self.run, self.metodo_pago, self.email, self.numero_contacto
        ))

    def actualizar(self):
        query = """
            UPDATE usuarios 
            SET nombre = %s, metodo_pago = %s, email = %s, numero_contacto = %s
            WHERE run = %s
        """
        return self.db.ejecutar_query(query, (
            self.nombre, self.metodo_pago, self.email, self.numero_contacto, self.run
        ))

    def eliminar(self):
        query = "DELETE FROM usuarios WHERE run = %s"
        return self.db.ejecutar_query(query, (self.run,))

    @staticmethod
    def obtener_todos():
        db = Database()
        query = "SELECT * FROM usuarios"
        return db.obtener_datos(query)

    @staticmethod
    def obtener_por_run(run):
        db = Database()
        query = "SELECT * FROM usuarios WHERE run = %s"
        resultado = db.obtener_datos(query, (run,))
        if resultado:
            return Cliente(
                resultado[0][5], resultado[0][6], resultado[0][7],
                resultado[0][8], resultado[0][9]
            )
        return None

"""
Notas sobre la arquitectura del sistema:

1. Diseño de la clase Cliente:
   - Clase base que contiene la información personal común a todos los usuarios
   - Implementa operaciones CRUD básicas para gestión de clientes
   - Sirve como superclase para la clase Usuario que añade funcionalidad de autenticación

2. Gestión de datos:
   - Utiliza el patrón DAO para acceso a base de datos
   - Mantiene consistencia en el formato de los datos personales
   - Proporciona métodos estáticos para consultas comunes

3. Consideraciones:
   - Los métodos de negocio específicos se implementan en main.py
   - Esta clase se centra en la gestión de datos personales
   - Proporciona una base sólida para la herencia en Usuario.py
"""
