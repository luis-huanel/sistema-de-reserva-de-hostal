# Clase Usuario que hereda de Cliente
# Implementa la gestión de usuarios del sistema con diferentes perfiles (admin, funcionario, gestor, cliente)
from package_hostal_minks.Cliente import Cliente
from .db import Database

class Usuario(Cliente):
    def __init__(self, nombre_usuario, contraseña, perfil, estado, nombre, run, metodo_pago, email, numero_contacto):
        # Inicializa la clase padre Cliente con los datos personales
        super().__init__(nombre, run, metodo_pago, email, numero_contacto)
        # Atributos específicos de Usuario para la autenticación y control de acceso
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.perfil = perfil  # Puede ser: admin, funcionario, gestor, cliente
        self.estado = estado  # Puede ser: activo, inactivo
        # Datos heredados de Cliente
        self.nombre = nombre
        self.run = run
        self.metodo_pago = metodo_pago
        self.email = email
        self.numero_contacto = numero_contacto
        self.id = None  # ID único en la base de datos
        self.db = Database()
        
        # Intenta obtener el ID si el usuario ya existe en la base de datos
        self._obtener_id()

    def _obtener_id(self):
        """Obtiene el ID del usuario de la base de datos si existe"""
        query = "SELECT id FROM usuarios WHERE nombre_usuario = %s"
        resultado = self.db.obtener_datos(query, (self.nombre_usuario,))
        if resultado:
            self.id = resultado[0][0]

    def guardar(self):
        """Guarda el usuario en la base de datos"""
        query = """
            INSERT INTO usuarios (nombre_usuario, contraseña, perfil, estado, nombre, run, metodo_pago, email, numero_contacto)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        if self.db.ejecutar_query(query, (
            self.nombre_usuario, self.contraseña, self.perfil, self.estado,
            self.nombre, self.run, self.metodo_pago, self.email, self.numero_contacto
        )):
            self._obtener_id()  # Actualizamos el ID después de guardar
            return True
        return False

    def actualizar(self):
        """Actualiza los datos del usuario en la base de datos"""
        query = """
            UPDATE usuarios 
            SET contraseña = %s, perfil = %s, estado = %s, nombre = %s,
                run = %s, metodo_pago = %s, email = %s, numero_contacto = %s
            WHERE nombre_usuario = %s
        """
        return self.db.ejecutar_query(query, (
            self.contraseña, self.perfil, self.estado, self.nombre,
            self.run, self.metodo_pago, self.email, self.numero_contacto,
            self.nombre_usuario
        ))

    def eliminar(self):
        """Elimina el usuario de la base de datos"""
        query = "DELETE FROM usuarios WHERE nombre_usuario = %s"
        return self.db.ejecutar_query(query, (self.nombre_usuario,))

    @staticmethod
    def obtener_todos():
        """Obtiene todos los usuarios de la base de datos"""
        db = Database()
        query = "SELECT * FROM usuarios"
        return db.obtener_datos(query)

    @staticmethod
    def obtener_por_nombre_usuario(nombre_usuario):
        """
        Obtiene un usuario por su nombre de usuario
        Retorna una instancia de Usuario si existe, None si no existe
        """
        db = Database()
        query = "SELECT * FROM usuarios WHERE nombre_usuario = %s"
        resultado = db.obtener_datos(query, (nombre_usuario,))
        if resultado:
            usuario = Usuario(
                nombre_usuario=resultado[0][1],
                contraseña=resultado[0][2],
                perfil=resultado[0][3],
                estado=resultado[0][4],
                nombre=resultado[0][5],
                run=resultado[0][6],
                metodo_pago=resultado[0][7],
                email=resultado[0][8],
                numero_contacto=resultado[0][9]
            )
            usuario.id = resultado[0][0]  # Asignamos el ID directamente
            return usuario
        return None

    @staticmethod
    def verificar_credenciales(nombre_usuario, contraseña):
        """
        Verifica las credenciales del usuario contra la base de datos
        
        Args:
            nombre_usuario (str): Nombre de usuario a verificar
            contraseña (str): Contraseña asociada al usuario
            
        Returns:
            Usuario: Instancia de Usuario si las credenciales son correctas
            None: Si las credenciales son incorrectas
        """
        db = Database()
        query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
        resultado = db.obtener_datos(query, (nombre_usuario, contraseña))
        if resultado:
            usuario = Usuario(
                nombre_usuario=resultado[0][1],
                contraseña=resultado[0][2],
                perfil=resultado[0][3],
                estado=resultado[0][4],
                nombre=resultado[0][5],
                run=resultado[0][6],
                metodo_pago=resultado[0][7],
                email=resultado[0][8],
                numero_contacto=resultado[0][9]
            )
            usuario.id = resultado[0][0]  # Asignamos el ID directamente
            return usuario
        return None

"""
Notas sobre la arquitectura del sistema:

1. Estructura del código:
   - Esta clase Usuario hereda de Cliente para mantener la jerarquía del sistema
   - Gestiona la autenticación y autorización de usuarios
   - Implementa el patrón DAO para acceso a datos

2. Decisiones de diseño:
   - Los métodos CRUD están en esta clase para mantener la encapsulación
   - Se usa una base de datos MySQL para persistencia
   - La contraseña se maneja como texto plano (en un sistema real debería estar hasheada)

3. Integración con main.py:
   - Los métodos de negocio complejos están en main.py para evitar dependencias circulares
   - Esta clase se centra en operaciones básicas CRUD y autenticación
"""












