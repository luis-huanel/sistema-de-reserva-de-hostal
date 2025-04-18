# SISTEMA DE RESERVA DE HABITACIONES Y SERVICIOS HOSTAL (EMPRESA MIRYKS)
# Este sistema permite la gestión de un hostal, incluyendo reservas de habitaciones,
# servicios adicionales, gestión de usuarios y generación de informes.

# IMPORTACIÓN DE MÓDULOS NECESARIOS
# Importamos las clases principales del sistema desde el paquete package_hostal_minks
from package_hostal_minks.Usuario import Usuario
from package_hostal_minks.Servicio import Servicio
from package_hostal_minks.Habitacion import Habitacion
from package_hostal_minks.Reserva import Reserva
from package_hostal_minks.db import Database

# Importamos las bibliotecas necesarias para la interfaz gráfica y efectos de sonido
import tkinter
from tkinter import messagebox
from tkinter import PhotoImage
from pygame import mixer
from tkcalendar import Calendar
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# INICIALIZACIÓN DE LA BASE DE DATOS
# Creamos una instancia de la clase Database para manejar todas las operaciones de base de datos
db = Database()

# FUNCIONES DE EFECTOS DE SONIDO
# Estas funciones manejan la reproducción de efectos de sonido para mejorar la experiencia del usuario
def sonido_apertura():
    """
    Reproduce el sonido de apertura cuando se inicia una ventana o acción importante.
    Utiliza la biblioteca pygame.mixer para la reproducción de audio.
    """
    mixer.init()
    mixer.music.load(r"recursos/sonidos/sonido_apertura.wav")
    mixer.music.play()

def sonido_cierre():
    """
    Reproduce el sonido de cierre cuando se finaliza una ventana o acción.
    Utiliza la biblioteca pygame.mixer para la reproducción de audio.
    """
    mixer.init()
    mixer.music.load(r"recursos/sonidos/sonido_cierre.wav")
    mixer.music.play()

def sonido_boton():
    """
    Reproduce el sonido de interacción con botones.
    Utiliza la biblioteca pygame.mixer para la reproducción de audio.
    """
    mixer.init()
    mixer.music.load(r"recursos/sonidos/sonido_boton.wav")
    mixer.music.play()

# CREDENCIALES DE USUARIOS DEL SISTEMA
# A continuación se detallan las credenciales de acceso para los diferentes tipos de usuarios

# Cliente 1
# USUARIO: antonio305
# CONTRASEÑA: Antonio1456

# Cliente 2
# USUARIO: federico24
# CONTRASEÑA: Federico245

# Administrador
# USUARIO: admin
# CONTRASEÑA: #305Dlab1

# Funcionario
# USUARIO: funcionario
# CONTRASEÑA: #305Dlab2

# Gestor de Informes
# USUARIO: gestor
# CONTRASEÑA: #305Dlab3

# FUNCIONES DE INICIALIZACIÓN DE DATOS
def crear_usuarios_iniciales():
    """
    Crea los usuarios iniciales del sistema con sus respectivos roles y permisos.
    Incluye un administrador, un funcionario, un gestor de informes y dos clientes.
    Cada usuario se crea con sus datos personales y credenciales de acceso.
    """
    # Administrador - Usuario con acceso total al sistema
    admin = Usuario(
        nombre_usuario="admin",
    contraseña="#305Dlab1",
    perfil="administrador",
        estado="activo",
        nombre="Carlos Mendoza",
        run="21356555-4",
        metodo_pago="Banco Estado",
        email="carlos.mendoza@minks.cl",
        numero_contacto="973736248"
    )
    admin.guardar()

    # Funcionario - Usuario con acceso a operaciones diarias
    funcionario = Usuario(
        nombre_usuario="funcionario",
    contraseña="#305Dlab2",
    perfil="funcionario",
        estado="activo",
        nombre="María González",
        run="21306545-9",
        metodo_pago="Banco Estado",
        email="maria.gonzalez@minks.cl",
        numero_contacto="938716211"
    )
    funcionario.guardar()

    # Gestor de Informes - Usuario especializado en reportes
    gestor = Usuario(
        nombre_usuario="gestor",
    contraseña="#305Dlab3",
    perfil="gestor de informes",
        estado="activo",
        nombre="Roberto Silva",
        run="31356548-3",
        metodo_pago="Banco Estado",
        email="roberto.silva@minks.cl",
        numero_contacto="953746899"
    )
    gestor.guardar()
    
    # Cliente 1 - Usuario con acceso a reservas y servicios
    cliente1 = Usuario(
        nombre_usuario="antonio305",
    contraseña="Antonio1456",
    perfil="cliente",
        estado="activo",
        nombre="Diego Ramírez",
        run="18765432-1",
        metodo_pago="Banco Estado",
        email="diego.ramirez@email.com",
        numero_contacto="912345678"
    )
    cliente1.guardar()
    
    # Cliente 2 - Usuario con acceso a reservas y servicios
    cliente2 = Usuario(
        nombre_usuario="federico24",
    contraseña="Federico245",
    perfil="cliente",
        estado="activo",
        nombre="Laura Torres",
        run="19876543-2",
        metodo_pago="Banco Estado",
        email="laura.torres@email.com",
        numero_contacto="923456789"
    )
    cliente2.guardar()

def crear_servicios_iniciales():
    """
    Crea los servicios iniciales disponibles en el hostal.
    Cada servicio incluye su nombre, tipo, descripción y costo por persona.
    """
    try:
        # Crear la tabla si no existe
        db.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS servicios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_servicio VARCHAR(100) UNIQUE,
                tipo_servicio VARCHAR(50),
                descripcion TEXT,
                costo_persona DECIMAL(10,2)
            )
        """)
        
        # Definimos los servicios iniciales
        servicios = [
            Servicio(
                nombre_servicio="Desayuno Continental",
                tipo_servicio="Alimentación",
                descripcion="Ofrecemos un delicioso desayuno continental que incluye una variedad de panes frescos, frutas de temporada, cereales, y bebidas calientes para comenzar tu día con energía.",
                costo_persona=5000
            ),
            Servicio(
                nombre_servicio="Estacionamiento Privado",
                tipo_servicio="Comodidad",
                descripcion="Brindamos la conveniencia de un estacionamiento privado para que puedas aparcar tu vehículo de manera segura y accesible.",
                costo_persona=10000
            ),
            Servicio(
                nombre_servicio="Tour Guiado por la Ciudad",
                tipo_servicio="Turismo",
                descripcion="Descubre los encantos locales con nuestros tours guiados por la ciudad. Conoce los lugares más emblemáticos con un guía experto.",
                costo_persona=15000
            ),
            Servicio(
                nombre_servicio="Wi-Fi de Alta Velocidad",
                tipo_servicio="Conectividad",
                descripcion="Mantente conectado en todo momento con nuestra conexión Wi-Fi de alta velocidad. Ideal para trabajo remoto o entretenimiento.",
                costo_persona=3000
            )
        ]
        
        # Guardamos cada servicio si no existe
        for servicio in servicios:
            try:
                # Verificar si el servicio ya existe
                query_check = "SELECT COUNT(*) FROM servicios WHERE nombre_servicio = %s"
                resultado = db.obtener_datos(query_check, (servicio.nombre_servicio,))
                if resultado[0][0] == 0:
                    servicio.guardar()
            except Exception as e:
                print(f"Error al guardar servicio {servicio.nombre_servicio}: {str(e)}")
                
    except Exception as e:
        print(f"Error al crear servicios iniciales: {str(e)}")

def crear_habitaciones_iniciales():
    """
    Crea las habitaciones iniciales del hostal.
    Cada habitación se configura con su número, tipo, capacidad y costo por noche.
    """
    habitaciones = [
        Habitacion(
            numero_habitacion=1,
            tipo_habitacion="Suite de Lujo con Baño Privado (4 Personas)",
            costo=80000
        ),
        Habitacion(
            numero_habitacion=2,
            tipo_habitacion="Habitación Doble Estándar con Baño Compartido (2 personas)",
            costo=40000
        ),
        Habitacion(
            numero_habitacion=3,
            tipo_habitacion="Habitación Individual con Baño Privado (1 persona)",
            costo=30000
        )
    ]
    for habitacion in habitaciones:
        habitacion.guardar()

def inicializar_datos():
    """
    Función principal de inicialización que crea todos los datos necesarios
    para el funcionamiento inicial del sistema solo si no existen.
    """
    # Crear tabla de reserva_servicios si no existe
    db.ejecutar_query("""
        CREATE TABLE IF NOT EXISTS reserva_servicios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_reserva INT,
            id_servicio INT,
            FOREIGN KEY (id_reserva) REFERENCES reservas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_servicio) REFERENCES servicios(id)
        )
    """)
    
    # Crear tabla de reservas si no existe
    db.ejecutar_query("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT,
            id_habitacion INT,
            fecha_entrada DATE,
            fecha_salida DATE,
            num_personas INT,
            estado VARCHAR(20) DEFAULT 'pendiente',
            hora_check_in TIME DEFAULT NULL,
            hora_check_out TIME DEFAULT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
            FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id)
        )
    """)

    # Verificar si ya existen usuarios
    query_check_usuarios = "SELECT COUNT(*) FROM usuarios"
    resultado = db.obtener_datos(query_check_usuarios)
    if resultado[0][0] == 0:
        crear_usuarios_iniciales()

    # Verificar si ya existen servicios
    query_check_servicios = "SELECT COUNT(*) FROM servicios"
    resultado = db.obtener_datos(query_check_servicios)
    if resultado[0][0] == 0:
        crear_servicios_iniciales()

    # Verificar si ya existen habitaciones
    query_check_habitaciones = "SELECT COUNT(*) FROM habitaciones"
    resultado = db.obtener_datos(query_check_habitaciones)
    if resultado[0][0] == 0:
        crear_habitaciones_iniciales()

# CONFIGURACIÓN DE LA INTERFAZ GRÁFICA
# Configuración inicial de la ventana principal
ventana = tkinter.Tk()
ventana.geometry("1920x1080")
ventana.title("Hostal Miryks")

# Configuración del icono de la aplicación
icono = tkinter.PhotoImage(file=f"recursos/imagenes/hostal_miryks_logo.png")
ventana.iconphoto(True, icono)

# Carga y configuración de la imagen principal
ruta_imagen_1 = "recursos/imagenes/imagen1.png"
imagen_1 = PhotoImage(file=ruta_imagen_1)
label_imagen = tkinter.Label(ventana, image=imagen_1)
label_imagen.pack()

# Reproducción del sonido de apertura
sonido_apertura()

# Configuración de la fuente para los campos de entrada
fuente_campos = ("Helvetica", 12)

# CREACIÓN DE ELEMENTOS DE LA INTERFAZ
# Etiquetas y campos para el inicio de sesión
etiqueta_usuario = tkinter.Label(ventana, text="Usuario:", font=fuente_campos)
etiqueta_usuario.place(relx=0.5, rely=0.50, anchor="center")
txt_usuario = tkinter.Entry(ventana, font=fuente_campos)
txt_usuario.place(relx=0.5, rely=0.53, anchor="center")

etiqueta_contraseña = tkinter.Label(ventana, text="Contraseña:", font=fuente_campos)
etiqueta_contraseña.place(relx=0.5, rely=0.57, anchor="center")
txt_contraseña = tkinter.Entry(ventana, show="*", font=fuente_campos)
txt_contraseña.place(relx=0.5, rely=0.6, anchor="center")

def verificar_credenciales():
    """
    Verifica las credenciales ingresadas por el usuario contra la base de datos.
    Si las credenciales son correctas, abre la página principal correspondiente.
    """
    usuario = txt_usuario.get()
    contraseña = txt_contraseña.get()

    # Verificar credenciales usando el método estático de Usuario
    usuario_autenticado = Usuario.verificar_credenciales(usuario, contraseña)
    
    if usuario_autenticado:
        abrir_pagina_principal(usuario_autenticado)
    else:
        messagebox.showerror("Inicio de Sesión", "Credenciales incorrectas")

def abrir_pagina_principal(usuario):
    """
    Abre la página principal del sistema según el perfil del usuario.
    Configura la interfaz y los botones disponibles según los permisos del usuario.
    
    Args:
        usuario: Objeto Usuario con los datos del usuario que inició sesión
    """
    global ventana
    ventana.iconify()

    # Configuración de la ventana principal
    pagina_principal = tkinter.Toplevel()
    pagina_principal.geometry("1920x1080")
    pagina_principal.title(f"Bienvenido, {usuario.nombre}")

    # Configuración del icono
    icono = tkinter.PhotoImage(file=f"recursos/imagenes/hostal_miryks_logo.png")
    ventana.iconphoto(True, icono)

    # Carga de la imagen de fondo
    ruta_imagen_2 = "recursos/imagenes/imagen2.png"
    imagen_2 = PhotoImage(file=ruta_imagen_2)
    label_imagen_2 = tkinter.Label(ventana, image=imagen_2)
    label_imagen_2.pack()

    def mostrar_detalles_cuenta():
        """
        Muestra un cuadro de diálogo con los detalles de la cuenta del usuario.
        """
        messagebox.showinfo("Detalles de la Cuenta", 
            f"Nombre: {usuario.nombre}\n"
            f"Nombre de Usuario: {usuario.nombre_usuario}\n"
            f"RUN: {usuario.run}\n"
                                                     f"Perfil: {usuario.perfil}\n"
                                                     f"Email: {usuario.email}\n"
            f"Número de Contacto: {usuario.numero_contacto}\n"
                                                     f"Estado: {usuario.estado}\n"
            f"Método de Pago: {usuario.metodo_pago}\n")

    sonido_apertura()

    # Configuración de botones según el perfil del usuario
    if usuario.perfil == "administrador":
        # Botones específicos para administrador
        btn_detalles_cuenta = tkinter.Button(pagina_principal, text="VER DETALLES DE CUENTA", 
            command=mostrar_detalles_cuenta, font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_detalles_cuenta.pack(pady=10)

        btn_eliminar_reservas = tkinter.Button(pagina_principal, text="ELIMINAR RESERVAS DE CLIENTES",
            command=lambda: eliminar_reservas_clientes(usuario), font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_eliminar_reservas.pack(pady=10)

        btn_modificar_reservas = tkinter.Button(pagina_principal, text="MODIFICAR RESERVAS DE CLIENTES",
            command=lambda: modificar_reservas_clientes(usuario), font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_modificar_reservas.pack(pady=10)

    elif usuario.perfil == "funcionario":
        # Botones específicos para funcionario
        btn_detalles_cuenta = tkinter.Button(pagina_principal, text="VER DETALLES DE CUENTA",
            command=mostrar_detalles_cuenta, font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_detalles_cuenta.pack(pady=10)

        btn_agendar = tkinter.Button(pagina_principal, text="AGENDAR HORAS",
            command=lambda: agendar_horas(usuario), font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_agendar.pack(pady=10)

        btn_visualizar = tkinter.Button(pagina_principal, text="VISUALIZAR RESERVAS",
            command=lambda: visualizar_reservas(usuario), font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_visualizar.pack(pady=10)

    elif usuario.perfil == "gestor de informes":
        # Botones específicos para gestor
        btn_detalles_cuenta = tkinter.Button(pagina_principal, text="VER DETALLES DE CUENTA",
            command=mostrar_detalles_cuenta, font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_detalles_cuenta.pack(pady=10)

        btn_informe_ocupacion = tkinter.Button(pagina_principal, text="INFORME DE OCUPACIÓN",
            command=generar_informe_ocupacion_grafico, font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_informe_ocupacion.pack(pady=10)

        btn_informe_servicios = tkinter.Button(pagina_principal, text="INFORME DE SERVICIOS",
            command=generar_informe_servicios_grafico, font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_informe_servicios.pack(pady=10)

    elif usuario.perfil == "cliente":
        # Botones específicos para cliente
        btn_detalles_cuenta = tkinter.Button(pagina_principal, text="VER DETALLES DE CUENTA",
            command=mostrar_detalles_cuenta, font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_detalles_cuenta.pack(pady=10)

        btn_reservar = tkinter.Button(pagina_principal, text="HACER RESERVA",
            command=lambda: hacer_reserva(usuario), font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_reservar.pack(pady=10)

        btn_ver_reservas = tkinter.Button(pagina_principal, text="VER MIS RESERVAS",
            command=lambda: ver_mis_reservas(usuario), font=('Helvetica', 16), fg="white", bg="#457fee")
        btn_ver_reservas.pack(pady=10)



    # Botón de cerrar sesión común para todos los perfiles
    btn_cerrar_sesion = tkinter.Button(pagina_principal, text="CERRAR SESIÓN",
        command=lambda: cerrar_sesion(pagina_principal), font=('Helvetica', 16), fg="white", bg="#457fee")
    btn_cerrar_sesion.pack(pady=10)

    # Carga de la imagen de fondo
    ruta_imagen_2 = "recursos/imagenes/imagen2.png"
    imagen_2 = PhotoImage(file=ruta_imagen_2)
    label_imagen_2 = tkinter.Label(pagina_principal, image=imagen_2)
    label_imagen_2.pack()

    pagina_principal.mainloop()

def cerrar_sesion(ventana):
    """
    Cierra la sesión actual y reproduce el sonido de cierre.
    
    Args:
        ventana: Ventana actual que se cerrará
    """
    sonido_cierre()
    ventana.destroy()

# BOTÓN DE INICIO DE SESIÓN
btn_iniciar_sesion = tkinter.Button(ventana, text="Iniciar Sesión", 
    command=verificar_credenciales, font=fuente_campos, bg="#457fee", fg="white")
btn_iniciar_sesion.place(relx=0.5, rely=0.7, anchor="center") 

# INFORMACIÓN DE USUARIOS DE PRUEBA
# Crear un frame para contener la información de usuarios
frame_usuarios = tkinter.Frame(ventana, bg="#457fee")
frame_usuarios.place(relx=0.5, rely=0.8, anchor="center")

# Título de la sección
titulo_usuarios = tkinter.Label(frame_usuarios, 
    text="Usuarios de Prueba Disponibles:", 
    font=("Helvetica", 12, "bold"),
    fg="white",
    bg="#457fee")
titulo_usuarios.pack(pady=5)

# Función para crear etiquetas de usuario
def crear_etiqueta_usuario(texto):
    return tkinter.Label(frame_usuarios, 
        text=texto,
        font=("Helvetica", 10),
        fg="white",
        bg="#457fee")

# Administrador
crear_etiqueta_usuario("Administrador - Usuario: admin, Contraseña: #305Dlab1").pack(pady=2)

# Funcionario
crear_etiqueta_usuario("Funcionario - Usuario: funcionario, Contraseña: #305Dlab2").pack(pady=2)

# Gestor de Informes
crear_etiqueta_usuario("Gestor de Informes - Usuario: gestor, Contraseña: #305Dlab3").pack(pady=2)

# Clientes
crear_etiqueta_usuario("Cliente 1 - Usuario: antonio305, Contraseña: Antonio1456").pack(pady=2)
crear_etiqueta_usuario("Cliente 2 - Usuario: federico24, Contraseña: Federico245").pack(pady=2)

#------------------------------------------------------------------------------------------------


# FUNCIONES PARA GESTIÓN DE RESERVAS (CLIENTE)
def hacer_reserva(usuario):
    """
    Permite a un cliente realizar una nueva reserva de manera sencilla.
    """
    # Crear ventana de reserva con estilo mejorado
    ventana_reserva = tkinter.Toplevel()
    ventana_reserva.geometry("1000x900")
    ventana_reserva.title("Nueva Reserva - Hostal Miryks")
    ventana_reserva.configure(bg="#f0f0f0")

    # Frame principal con padding y mejor organización
    frame_principal = tkinter.Frame(ventana_reserva, bg="#f0f0f0")
    frame_principal.pack(padx=40, pady=30, fill="both", expand=True)

    # Título principal con mejor diseño
    titulo = tkinter.Label(frame_principal, 
        text="Nueva Reserva",
        font=("Helvetica", 24, "bold"),
        fg="#2c3e50",
        bg="#f0f0f0")
    titulo.pack(pady=(0,30))

    # Frame para contenido en dos columnas
    frame_contenido = tkinter.Frame(frame_principal, bg="#f0f0f0")
    frame_contenido.pack(fill="both", expand=True)

    # Columna izquierda
    frame_izquierda = tkinter.Frame(frame_contenido, bg="#f0f0f0")
    frame_izquierda.pack(side="left", padx=20, fill="both", expand=True)

    # Sección de habitaciones con marco
    frame_habitaciones = tkinter.LabelFrame(frame_izquierda, 
        text="Selección de Habitación",
        font=("Helvetica", 12, "bold"),
        fg="#2c3e50",
        bg="#f0f0f0",
        padx=15,
        pady=10)
    frame_habitaciones.pack(fill="x", pady=(0,20))

    # Obtener habitaciones de la base de datos
    query_habitaciones = "SELECT id, numero_habitacion, tipo_habitacion, costo FROM habitaciones"
    habitaciones = db.obtener_datos(query_habitaciones)
    
    # Variable para la habitación seleccionada
    habitacion_seleccionada = tkinter.StringVar()
    
    # Lista de habitaciones con mejor formato
    habitaciones_info = {}  # Diccionario para almacenar info de habitaciones
    for habitacion in habitaciones:
        # Extraer el número de personas de la descripción
        tipo_hab = habitacion[2]
        if "4 Personas" in tipo_hab:
            max_personas = 4
        elif "2 p" in tipo_hab:
            max_personas = 2
        elif "1 persona" in tipo_hab:
            max_personas = 1
        else:
            max_personas = 1  # valor por defecto
            
        habitaciones_info[str(habitacion[0])] = max_personas
        
        texto = f"Habitación {habitacion[1]} - {habitacion[2]}\nPrecio: ${habitacion[3]:,} CLP"
        radio = tkinter.Radiobutton(frame_habitaciones,
            text=texto,
            variable=habitacion_seleccionada,
            value=str(habitacion[0]),
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f0f0f0",
            justify="left",
            wraplength=400)
        radio.pack(pady=5, anchor="w")

    # Frame para fechas con mejor organización
    frame_fechas = tkinter.LabelFrame(frame_izquierda,
        text="Selección de Fechas",
        font=("Helvetica", 12, "bold"),
        fg="#2c3e50",
        bg="#f0f0f0",
        padx=15,
        pady=10)
    frame_fechas.pack(fill="x", pady=(0,20))

    # Variables para almacenar las fechas seleccionadas
    fecha_entrada = tkinter.StringVar()
    fecha_salida = tkinter.StringVar()

    # Función para actualizar la fecha de entrada
    def seleccionar_fecha_entrada(event=None):
        fecha = cal_entrada.selection_get()
        fecha_entrada.set(fecha.strftime("%d/%m/%Y"))
        # Actualizar fecha mínima de salida
        fecha_min_salida = fecha + timedelta(days=1)
        cal_salida.selection_set(fecha_min_salida)
        cal_salida.config(mindate=fecha_min_salida)
        fecha_salida.set(fecha_min_salida.strftime("%d/%m/%Y"))

    # Función para actualizar la fecha de salida
    def seleccionar_fecha_salida(event=None):
        fecha = cal_salida.selection_get()
        fecha_salida.set(fecha.strftime("%d/%m/%Y"))

    # Calendarios en contenedores separados
    frame_cal_entrada = tkinter.Frame(frame_fechas, bg="#f0f0f0")
    frame_cal_entrada.pack(side="left", padx=10)

    tkinter.Label(frame_cal_entrada,
        text="Fecha de entrada:",
        font=("Helvetica", 11),
        fg="#2c3e50",
        bg="#f0f0f0").pack()

    # Configurar fecha actual y mínima para entrada
    fecha_actual = datetime.now()
    cal_entrada = Calendar(frame_cal_entrada,
        selectmode='day',
        year=fecha_actual.year,
        month=fecha_actual.month,
        day=fecha_actual.day,
        mindate=fecha_actual,
        locale='es_ES',
        background="#ffffff",
        foreground="#2c3e50",
        selectbackground="#3498db",
        selectforeground="#ffffff")
    cal_entrada.pack(pady=5)
    
    # Establecer fecha inicial y vincular evento
    fecha_entrada.set(fecha_actual.strftime("%d/%m/%Y"))
    cal_entrada.bind("<<CalendarSelected>>", seleccionar_fecha_entrada)

    frame_cal_salida = tkinter.Frame(frame_fechas, bg="#f0f0f0")
    frame_cal_salida.pack(side="left", padx=10)

    tkinter.Label(frame_cal_salida,
        text="Fecha de salida:",
        font=("Helvetica", 11),
        fg="#2c3e50",
        bg="#f0f0f0").pack()

    # Configurar fecha inicial de salida (día siguiente)
    fecha_inicial_salida = fecha_actual + timedelta(days=1)
    cal_salida = Calendar(frame_cal_salida,
        selectmode='day',
        year=fecha_inicial_salida.year,
        month=fecha_inicial_salida.month,
        day=fecha_inicial_salida.day,
        mindate=fecha_inicial_salida,
        locale='es_ES',
        background="#ffffff",
        foreground="#2c3e50",
        selectbackground="#3498db",
        selectforeground="#ffffff")
    cal_salida.pack(pady=5)
    
    # Establecer fecha inicial de salida y vincular evento
    fecha_salida.set(fecha_inicial_salida.strftime("%d/%m/%Y"))
    cal_salida.bind("<<CalendarSelected>>", seleccionar_fecha_salida)

    # Columna derecha
    frame_derecha = tkinter.Frame(frame_contenido, bg="#f0f0f0")
    frame_derecha.pack(side="right", padx=20, fill="both", expand=True)

    # Número de personas con mejor diseño
    frame_personas = tkinter.LabelFrame(frame_derecha,
        text="Número de Personas",
        font=("Helvetica", 12, "bold"),
        fg="#2c3e50",
        bg="#f0f0f0",
        padx=15,
        pady=10)
    frame_personas.pack(fill="x", pady=(0,20))
    
    entrada_personas = tkinter.Entry(frame_personas,
        font=("Helvetica", 11),
        width=10)
    entrada_personas.pack(pady=10)

    # Servicios adicionales con mejor organización
    frame_servicios = tkinter.LabelFrame(frame_derecha,
        text="Servicios Adicionales",
        font=("Helvetica", 12, "bold"),
        fg="#2c3e50",
        bg="#f0f0f0",
        padx=15,
        pady=10)
    frame_servicios.pack(fill="both", expand=True)

    # Canvas y scrollbar para servicios
    canvas_servicios = tkinter.Canvas(frame_servicios, bg="#f0f0f0")
    scrollbar = tkinter.Scrollbar(frame_servicios, orient="vertical", command=canvas_servicios.yview)
    frame_scroll = tkinter.Frame(canvas_servicios, bg="#f0f0f0")

    canvas_servicios.configure(yscrollcommand=scrollbar.set)
    
    # Configurar el scroll
    def configurar_scroll(event):
        canvas_servicios.configure(scrollregion=canvas_servicios.bbox("all"), width=400)
    
    frame_scroll.bind("<Configure>", configurar_scroll)
    canvas_servicios.create_window((0,0), window=frame_scroll, anchor="nw")
    
    canvas_servicios.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Obtener servicios de la base de datos (sin duplicados)
    query_servicios = """
        SELECT DISTINCT id, nombre_servicio, costo_persona, tipo_servicio 
        FROM servicios 
        ORDER BY tipo_servicio, nombre_servicio
    """
    servicios = db.obtener_datos(query_servicios)
    
    # Variables para servicios seleccionados
    servicios_seleccionados = {}
    current_tipo = None

    for servicio in servicios:
        # Si cambia el tipo de servicio, crear nuevo encabezado
        if servicio[3] != current_tipo:
            current_tipo = servicio[3]
            tkinter.Label(frame_scroll,
                text=f"\n{current_tipo}",
                font=("Helvetica", 11, "bold"),
                fg="#2c3e50",
                bg="#f0f0f0").pack(anchor="w", pady=(10,5))

        var = tkinter.BooleanVar()
        servicios_seleccionados[servicio[0]] = var
        
        frame_servicio = tkinter.Frame(frame_scroll, bg="#f0f0f0")
        frame_servicio.pack(fill="x", pady=2)
        
        check = tkinter.Checkbutton(frame_servicio,
            text=f"{servicio[1]}",
            variable=var,
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f0f0f0")
        check.pack(side="left")
        
        precio = tkinter.Label(frame_servicio,
            text=f"${servicio[2]:,} CLP p/persona",
            font=("Helvetica", 10),
            fg="#7f8c8d",
            bg="#f0f0f0")
        precio.pack(side="right")

    def guardar_reserva():
        try:
            if not habitacion_seleccionada.get():
                messagebox.showerror("Error", "Por favor seleccione una habitación")
                return

            # Obtener datos
            id_habitacion = habitacion_seleccionada.get()
            fecha_entrada_valor = fecha_entrada.get()
            fecha_salida_valor = fecha_salida.get()
            
            # Validar fechas
            if not fecha_entrada_valor or not fecha_salida_valor:
                messagebox.showerror("Error", "Por favor seleccione las fechas de entrada y salida")
                return
                
            try:
                # Convertir fechas para validación
                fecha_entrada_dt = datetime.strptime(fecha_entrada_valor, "%d/%m/%Y")
                fecha_salida_dt = datetime.strptime(fecha_salida_valor, "%d/%m/%Y")
                
                if fecha_entrada_dt >= fecha_salida_dt:
                    messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de entrada")
                    return
                    
                if fecha_entrada_dt.date() < datetime.now().date():
                    messagebox.showerror("Error", "La fecha de entrada no puede ser anterior a hoy")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido")
                return
            
            try:
                num_personas = int(entrada_personas.get())
                if num_personas <= 0:
                    raise ValueError("El número de personas debe ser mayor a 0")
                    
                # Validar número máximo de personas para la habitación seleccionada
                max_personas = habitaciones_info[id_habitacion]
                if num_personas > max_personas:
                    messagebox.showerror("Error", 
                        f"La habitación seleccionada tiene un máximo de {max_personas} personas.\n"
                        f"Por favor seleccione otra habitación o reduzca el número de personas.")
                    return
                    
            except ValueError as e:
                messagebox.showerror("Error", str(e) if "mayor a 0" in str(e) else "Por favor ingrese un número válido de personas")
                return

            # Verificar que el usuario tenga ID
            if not hasattr(usuario, 'id') or usuario.id is None:
                messagebox.showerror("Error", "Error de sesión. Por favor, vuelva a iniciar sesión.")
                return

            # Verificar disponibilidad de la habitación para las fechas seleccionadas
            query_disponibilidad = """
                SELECT COUNT(*) FROM reservas 
                WHERE id_habitacion = %s 
                AND ((fecha_entrada BETWEEN %s AND %s) 
                OR (fecha_salida BETWEEN %s AND %s)
                OR (fecha_entrada <= %s AND fecha_salida >= %s))
            """
            resultado = db.obtener_datos(query_disponibilidad, (
                int(id_habitacion),
                fecha_entrada_dt.strftime("%Y-%m-%d"),
                fecha_salida_dt.strftime("%Y-%m-%d"),
                fecha_entrada_dt.strftime("%Y-%m-%d"),
                fecha_salida_dt.strftime("%Y-%m-%d"),
                fecha_entrada_dt.strftime("%Y-%m-%d"),
                fecha_salida_dt.strftime("%Y-%m-%d")
            ))

            if resultado[0][0] > 0:
                messagebox.showerror("Error", 
                    "La habitación no está disponible para las fechas seleccionadas.\n"
                    "Por favor, seleccione otras fechas o una habitación diferente.")
                return

            # Insertar reserva con estado inicial 'pendiente'
            query_reserva = """
                INSERT INTO reservas (
                    id_usuario, 
                    id_habitacion, 
                    fecha_entrada, 
                    fecha_salida, 
                    num_personas,
                    estado,
                    hora_check_in,
                    hora_check_out
                ) VALUES (%s, %s, %s, %s, %s, 'pendiente', NULL, NULL)
            """
            if not db.ejecutar_query(query_reserva, (
                usuario.id,
                int(id_habitacion),
                fecha_entrada_dt.strftime("%Y-%m-%d"),
                fecha_salida_dt.strftime("%Y-%m-%d"),
                num_personas
            )):
                messagebox.showerror("Error", "No se pudo crear la reserva. Por favor, intente nuevamente.")
                return
            
            # Obtener ID de la reserva
            id_reserva = db.obtener_datos("SELECT LAST_INSERT_ID()")[0][0]
            
            # Insertar servicios seleccionados
            servicios_agregados = False
            for id_servicio, var in servicios_seleccionados.items():
                if var.get():
                    query_servicio = """
                        INSERT INTO reserva_servicios (id_reserva, id_servicio)
                        VALUES (%s, %s)
                    """
                    if not db.ejecutar_query(query_servicio, (id_reserva, id_servicio)):
                        print(f"Error al agregar servicio {id_servicio}")
                    else:
                        servicios_agregados = True
            
            mensaje = "Reserva creada correctamente"
            if servicios_agregados:
                mensaje += " con servicios adicionales"
            messagebox.showinfo("Éxito", mensaje)
            ventana_reserva.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la reserva: {str(e)}")
            print(f"Error detallado: {str(e)}")  # Para debugging

    # Frame para botones con mejor diseño
    frame_botones = tkinter.Frame(frame_principal, bg="#f0f0f0")
    frame_botones.pack(pady=30)

    # Botones con mejor estilo
    btn_cancelar = tkinter.Button(frame_botones,
        text="Cancelar",
        command=ventana_reserva.destroy,
        font=("Helvetica", 12),
        fg="#ffffff",
        bg="#e74c3c",
        width=15,
        padx=10,
        pady=5)
    btn_cancelar.pack(side="left", padx=10)

    btn_guardar = tkinter.Button(frame_botones,
        text="Confirmar Reserva",
        command=guardar_reserva,
        font=("Helvetica", 12),
        fg="#ffffff",
        bg="#2ecc71",
        width=15,
        padx=10,
        pady=5)
    btn_guardar.pack(side="left", padx=10)

    # Centrar la ventana en la pantalla
    ventana_reserva.update_idletasks()
    width = ventana_reserva.winfo_width()
    height = ventana_reserva.winfo_height()
    x = (ventana_reserva.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana_reserva.winfo_screenheight() // 2) - (height // 2)
    ventana_reserva.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def ver_mis_reservas(usuario):
    """
    Muestra todas las reservas del cliente en una lista desplazable.
    """
    # Crear ventana
    ventana_reservas = tkinter.Toplevel()
    ventana_reservas.geometry("900x700")
    ventana_reservas.title("Mis Reservas - Hostal Miryks")
    ventana_reservas.configure(bg="#f5f6fa")

    # Frame principal
    frame_principal = tkinter.Frame(ventana_reservas, bg="#f5f6fa")
    frame_principal.pack(padx=40, pady=30, fill="both", expand=True)

    # Título
    titulo = tkinter.Label(frame_principal, 
        text="Mis Reservas",
        font=("Helvetica", 24, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    titulo.pack(pady=(0,30))

    # Frame con scroll para las reservas
    frame_contenedor = tkinter.Frame(frame_principal, bg="#f5f6fa")
    frame_contenedor.pack(fill="both", expand=True)

    # Canvas y scrollbar
    canvas = tkinter.Canvas(frame_contenedor, bg="#f5f6fa", highlightthickness=0)
    scrollbar = tkinter.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
    frame_reservas = tkinter.Frame(canvas, bg="#f5f6fa")

    # Configurar el scroll
    def configurar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_reservas.bind("<Configure>", configurar_scroll)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear ventana en el canvas
    canvas.create_window((0,0), window=frame_reservas, anchor="nw", width=800)
    
    # Empaquetar canvas y scrollbar
    canvas.pack(side="left", fill="both", expand=True, padx=(0,10))
    scrollbar.pack(side="right", fill="y")

    # Configurar el scroll con el mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Primero, obtener todas las reservas sin servicios
    query_reservas_base = """
        SELECT 
            r.id,
            h.numero_habitacion,
            h.tipo_habitacion,
            h.costo,
            r.fecha_entrada,
            r.fecha_salida,
            r.num_personas,
            r.estado,
            r.hora_check_in,
            r.hora_check_out
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id
        WHERE r.id_usuario = %s
        ORDER BY r.fecha_entrada DESC
    """
    
    print(f"Buscando reservas para el usuario ID: {usuario.id}")
    reservas = db.obtener_datos(query_reservas_base, (usuario.id,))
    print(f"Número de reservas encontradas: {len(reservas)}")

    if not reservas:
        mensaje_vacio = tkinter.Label(frame_reservas,
            text="No tienes reservas activas",
            font=("Helvetica", 14),
            fg="#7f8c8d",
            bg="#f5f6fa")
        mensaje_vacio.pack(pady=20)
        print("No se encontraron reservas para este usuario")
    else:
        print(f"Mostrando {len(reservas)} reservas")
        for idx, reserva in enumerate(reservas, 1):
            print(f"Procesando reserva {idx} de {len(reservas)} - ID: {reserva[0]}")
            
            # Frame para cada reserva
            frame_reserva = tkinter.Frame(frame_reservas, 
                bg="white",
                relief="raised",
                borderwidth=1)
            frame_reserva.pack(pady=10, padx=20, fill="x")

            # Frame para el contenido
            frame_contenido = tkinter.Frame(frame_reserva, bg="white")
            frame_contenido.pack(padx=20, pady=15, fill="x")

            # Título y número de habitación
            frame_titulo = tkinter.Frame(frame_contenido, bg="white")
            frame_titulo.pack(fill="x")

            tkinter.Label(frame_titulo,
                text=f"Habitación {reserva[1]}",
                font=("Helvetica", 16, "bold"),
                fg="#2c3e50",
                bg="white").pack(side="left")

            tkinter.Label(frame_titulo,
                text=f"${reserva[3]:,} CLP",
                font=("Helvetica", 14),
                fg="#27ae60",
                bg="white").pack(side="right")

            # Tipo de habitación
            tkinter.Label(frame_contenido,
                text=f"{reserva[2]}",
                font=("Helvetica", 12),
                fg="#7f8c8d",
                bg="white").pack(anchor="w", pady=(5,10))

            # Frame para fechas
            frame_fechas = tkinter.Frame(frame_contenido, bg="white")
            frame_fechas.pack(fill="x")

            # Fecha de entrada
            frame_entrada = tkinter.Frame(frame_fechas, bg="white")
            frame_entrada.pack(side="left", padx=(0,20))

            tkinter.Label(frame_entrada,
                text="Entrada",
                font=("Helvetica", 11, "bold"),
                fg="#7f8c8d",
                bg="white").pack(anchor="w")

            fecha_entrada = datetime.strptime(str(reserva[4]), "%Y-%m-%d").strftime("%d/%m/%Y")
            tkinter.Label(frame_entrada,
                text=fecha_entrada,
                font=("Helvetica", 11),
                fg="#2c3e50",
                bg="white").pack(anchor="w")

            # Fecha de salida
            frame_salida = tkinter.Frame(frame_fechas, bg="white")
            frame_salida.pack(side="left")

            tkinter.Label(frame_salida,
                text="Salida",
                font=("Helvetica", 11, "bold"),
                fg="#7f8c8d",
                bg="white").pack(anchor="w")

            fecha_salida = datetime.strptime(str(reserva[5]), "%Y-%m-%d").strftime("%d/%m/%Y")
            tkinter.Label(frame_salida,
                text=fecha_salida,
                font=("Helvetica", 11),
                fg="#2c3e50",
                bg="white").pack(anchor="w")

            # Número de personas
            tkinter.Label(frame_contenido,
                text=f"Personas: {reserva[6]}",
                font=("Helvetica", 11),
                fg="#2c3e50",
                bg="white").pack(anchor="w", pady=(10,5))

            # Estado con color y texto descriptivo
            estado_actual = reserva[7] or "pendiente"
            colores_estado = {
                "pendiente": "#f1c40f",  # Amarillo
                "agendado": "#3498db",   # Azul
                "check_in": "#2ecc71",   # Verde
                "check_out": "#e74c3c"   # Rojo
            }
            texto_estado = {
                "pendiente": "Pendiente",
                "agendado": "Horas Agendadas",
                "check_in": "Check-in realizado",
                "check_out": "Check-out completado"
            }

            frame_estado = tkinter.Frame(frame_contenido, bg="white")
            frame_estado.pack(fill="x", pady=(10,0))

            tkinter.Label(frame_estado,
                text=texto_estado.get(estado_actual, "Pendiente"),
                font=("Helvetica", 11, "bold"),
                fg="white",
                bg=colores_estado.get(estado_actual, "#f1c40f"),
                padx=10,
                pady=5).pack(side="left")

            # Mostrar horas agendadas si existen
            if reserva[8] or reserva[9]:  # Si hay hora de check-in o check-out
                frame_horas = tkinter.Frame(frame_estado, bg="white")
                frame_horas.pack(side="right")

                if reserva[8]:  # Hora check-in
                    tkinter.Label(frame_horas,
                        text=f"Check-in: {reserva[8].strftime('%H:%M')}",
                        font=("Helvetica", 11),
                        fg="#2c3e50",
                        bg="white").pack(side="left", padx=10)

                if reserva[9]:  # Hora check-out
                    tkinter.Label(frame_horas,
                        text=f"Check-out: {reserva[9].strftime('%H:%M')}",
                        font=("Helvetica", 11),
                        fg="#2c3e50",
                        bg="white").pack(side="left", padx=10)

            # Obtener servicios para esta reserva específica
            query_servicios = """
                SELECT 
                    s.nombre_servicio,
                    s.costo_persona
                FROM reserva_servicios rs
                JOIN servicios s ON rs.id_servicio = s.id
                WHERE rs.id_reserva = %s
            """
            servicios = db.obtener_datos(query_servicios, (reserva[0],))
            
            if servicios:
                frame_servicios = tkinter.Frame(frame_contenido, bg="white")
                frame_servicios.pack(fill="x", pady=(10,0))

                tkinter.Label(frame_servicios,
                    text="Servicios adicionales:",
                    font=("Helvetica", 11, "bold"),
                    fg="#7f8c8d",
                    bg="white").pack(anchor="w")

                for servicio in servicios:
                    frame_servicio = tkinter.Frame(frame_servicios, bg="white")
                    frame_servicio.pack(fill="x", pady=2)

                    tkinter.Label(frame_servicio,
                        text=f"• {servicio[0]}",
                        font=("Helvetica", 11),
                        fg="#2c3e50",
                        bg="white").pack(side="left")

                    tkinter.Label(frame_servicio,
                        text=f"${int(servicio[1]):,} CLP p/persona",
                        font=("Helvetica", 11),
                        fg="#7f8c8d",
                        bg="white").pack(side="right")

    # Botón para cerrar
    btn_cerrar = tkinter.Button(frame_principal,
        text="Cerrar",
        command=ventana_reservas.destroy,
        font=("Helvetica", 12),
        fg="white",
        bg="#e74c3c",
        width=15,
        padx=10,
        pady=5)
    btn_cerrar.pack(pady=20)

    # Centrar la ventana en la pantalla
    ventana_reservas.update_idletasks()
    width = ventana_reservas.winfo_width()
    height = ventana_reservas.winfo_height()
    x = (ventana_reservas.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana_reservas.winfo_screenheight() // 2) - (height // 2)
    ventana_reservas.geometry('{}x{}+{}+{}'.format(width, height, x, y))

#------------------------------------------------------------------------------------------------




# GESTOR DE INFORMES (GENERAR INFORME GRÁFICO DE OCUPACIÓN DE HABITACIONES) (GESTOR)
def generar_informe_ocupacion_grafico():
    """
    Genera un informe gráfico de ocupación de habitaciones usando matplotlib.
    """
    ventana_informe = tkinter.Toplevel()
    ventana_informe.geometry("1200x800")
    ventana_informe.title("Informe Gráfico de Ocupación - Hostal Miryks")
    ventana_informe.configure(bg="#f5f6fa")

    # Frame principal
    frame_principal = tkinter.Frame(ventana_informe, bg="#f5f6fa")
    frame_principal.pack(padx=40, pady=30, fill="both", expand=True)

    # Título
    titulo = tkinter.Label(frame_principal, 
        text="Informe Gráfico de Ocupación de Habitaciones",
        font=("Helvetica", 24, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    titulo.pack(pady=(0,30))

    # Frame para filtros
    frame_filtros = tkinter.LabelFrame(frame_principal,
        text="Filtros",
        font=("Helvetica", 12, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa",
        padx=15,
        pady=10)
    frame_filtros.pack(fill="x", pady=(0,20))

    # Fechas
    frame_fechas = tkinter.Frame(frame_filtros, bg="#f5f6fa")
    frame_fechas.pack(fill="x", pady=10)

    # Fecha inicial
    frame_fecha_inicio = tkinter.Frame(frame_fechas, bg="#f5f6fa")
    frame_fecha_inicio.pack(side="left", padx=20)

    tkinter.Label(frame_fecha_inicio,
        text="Fecha inicial:",
        font=("Helvetica", 11),
        fg="#2c3e50",
        bg="#f5f6fa").pack()

    cal_inicio = Calendar(frame_fecha_inicio,
        selectmode='day',
        year=datetime.now().year,
        month=datetime.now().month,
        day=1,
        locale='es_ES')
    cal_inicio.pack(pady=5)

    # Fecha final
    frame_fecha_fin = tkinter.Frame(frame_fechas, bg="#f5f6fa")
    frame_fecha_fin.pack(side="left", padx=20)

    tkinter.Label(frame_fecha_fin,
        text="Fecha final:",
        font=("Helvetica", 11),
        fg="#2c3e50",
        bg="#f5f6fa").pack()

    cal_fin = Calendar(frame_fecha_fin,
        selectmode='day',
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day,
        locale='es_ES')
    cal_fin.pack(pady=5)

    # Frame para gráficos
    frame_graficos = tkinter.Frame(frame_principal, bg="#f5f6fa")
    frame_graficos.pack(fill="both", expand=True, pady=20)

    def generar_reporte():
        # Limpiar gráficos anteriores
        for widget in frame_graficos.winfo_children():
            widget.destroy()

        fecha_inicio = cal_inicio.selection_get()
        fecha_fin = cal_fin.selection_get()

        # Consulta para obtener estadísticas de ocupación
        query_ocupacion = """
            SELECT 
                h.numero_habitacion,
                h.tipo_habitacion,
                COUNT(r.id) as total_reservas,
                SUM(DATEDIFF(r.fecha_salida, r.fecha_entrada)) as dias_ocupados,
                SUM(r.num_personas) as total_personas,
                SUM(h.costo * DATEDIFF(r.fecha_salida, r.fecha_entrada)) as ingresos_totales
            FROM habitaciones h
            LEFT JOIN reservas r ON h.id = r.id_habitacion
            AND r.fecha_entrada BETWEEN %s AND %s
            GROUP BY h.id, h.numero_habitacion, h.tipo_habitacion
            ORDER BY h.numero_habitacion
        """
        
        resultados = db.obtener_datos(query_ocupacion, (fecha_inicio, fecha_fin))

        # Crear figura con subplots
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_facecolor('#f5f6fa')

        # Gráfico de barras para reservas y días ocupados
        ax1 = plt.subplot(221)
        habitaciones = [f"Hab {r[0]}" for r in resultados]
        reservas = [r[2] for r in resultados]
        dias = [r[3] if r[3] else 0 for r in resultados]

        x = np.arange(len(habitaciones))
        width = 0.35

        ax1.bar(x - width/2, reservas, width, label='Reservas', color='#3498db')
        ax1.bar(x + width/2, dias, width, label='Días ocupados', color='#2ecc71')
        ax1.set_xticks(x)
        ax1.set_xticklabels(habitaciones)
        ax1.set_title('Reservas y Días de Ocupación')
        ax1.legend()

        # Gráfico de barras para personas totales
        ax2 = plt.subplot(222)
        personas = [r[4] if r[4] else 0 for r in resultados]
        ax2.bar(habitaciones, personas, color='#e74c3c')
        ax2.set_title('Total de Personas por Habitación')

        # Gráfico de torta para ingresos
        ax3 = plt.subplot(212)
        ingresos = [r[5] if r[5] else 0 for r in resultados]
        ax3.pie(ingresos, labels=habitaciones, autopct='%1.1f%%', colors=['#3498db', '#2ecc71', '#e74c3c'])
        ax3.set_title('Distribución de Ingresos por Habitación')

        plt.tight_layout()

        # Mostrar gráfico en la ventana
        canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Botón para generar reporte
    btn_generar = tkinter.Button(frame_filtros,
        text="Generar Reporte",
        command=generar_reporte,
        font=("Helvetica", 12),
        fg="white",
        bg="#2ecc71",
        width=15,
        padx=10,
        pady=5)
    btn_generar.pack(pady=10)

    # Botón para cerrar
    btn_cerrar = tkinter.Button(frame_principal,
        text="Cerrar",
        command=ventana_informe.destroy,
        font=("Helvetica", 12),
        fg="white",
        bg="#e74c3c",
        width=15,
        padx=10,
        pady=5)
    btn_cerrar.pack(pady=20)

    # Centrar la ventana
    ventana_informe.update_idletasks()
    width = ventana_informe.winfo_width()
    height = ventana_informe.winfo_height()
    x = (ventana_informe.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana_informe.winfo_screenheight() // 2) - (height // 2)
    ventana_informe.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def generar_informe_servicios_grafico():
    """
    Genera un informe gráfico de uso de servicios adicionales usando matplotlib.
    """
    ventana_informe = tkinter.Toplevel()
    ventana_informe.geometry("1200x800")
    ventana_informe.title("Informe Gráfico de Servicios - Hostal Miryks")
    ventana_informe.configure(bg="#f5f6fa")

    # Frame principal
    frame_principal = tkinter.Frame(ventana_informe, bg="#f5f6fa")
    frame_principal.pack(padx=40, pady=30, fill="both", expand=True)

    # Título
    titulo = tkinter.Label(frame_principal, 
        text="Informe Gráfico de Servicios Adicionales",
        font=("Helvetica", 24, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    titulo.pack(pady=(0,30))

    # Frame para filtros
    frame_filtros = tkinter.LabelFrame(frame_principal,
        text="Filtros",
        font=("Helvetica", 12, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa",
        padx=15,
        pady=10)
    frame_filtros.pack(fill="x", pady=(0,20))

    # Fechas
    frame_fechas = tkinter.Frame(frame_filtros, bg="#f5f6fa")
    frame_fechas.pack(fill="x", pady=10)

    # Fecha inicial
    frame_fecha_inicio = tkinter.Frame(frame_fechas, bg="#f5f6fa")
    frame_fecha_inicio.pack(side="left", padx=20)

    tkinter.Label(frame_fecha_inicio,
        text="Fecha inicial:",
        font=("Helvetica", 11),
        fg="#2c3e50",
        bg="#f5f6fa").pack()

    cal_inicio = Calendar(frame_fecha_inicio,
        selectmode='day',
        year=datetime.now().year,
        month=datetime.now().month,
        day=1,
        locale='es_ES')
    cal_inicio.pack(pady=5)

    # Fecha final
    frame_fecha_fin = tkinter.Frame(frame_fechas, bg="#f5f6fa")
    frame_fecha_fin.pack(side="left", padx=20)

    tkinter.Label(frame_fecha_fin,
        text="Fecha final:",
        font=("Helvetica", 11),
        fg="#2c3e50",
        bg="#f5f6fa").pack()

    cal_fin = Calendar(frame_fecha_fin,
        selectmode='day',
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day,
        locale='es_ES')
    cal_fin.pack(pady=5)

    # Frame para gráficos
    frame_graficos = tkinter.Frame(frame_principal, bg="#f5f6fa")
    frame_graficos.pack(fill="both", expand=True, pady=20)

    def generar_reporte():
        # Limpiar gráficos anteriores
        for widget in frame_graficos.winfo_children():
            widget.destroy()

        fecha_inicio = cal_inicio.selection_get()
        fecha_fin = cal_fin.selection_get()

        # Consulta para obtener estadísticas de servicios
        query_servicios = """
            SELECT 
                s.nombre_servicio,
                s.tipo_servicio,
                COUNT(rs.id) as veces_contratado,
                SUM(s.costo_persona * r.num_personas) as ingresos_totales
            FROM servicios s
            LEFT JOIN reserva_servicios rs ON s.id = rs.id_servicio
            LEFT JOIN reservas r ON rs.id_reserva = r.id
            AND r.fecha_entrada BETWEEN %s AND %s
            GROUP BY s.id, s.nombre_servicio, s.tipo_servicio
            ORDER BY veces_contratado DESC
        """
        
        resultados = db.obtener_datos(query_servicios, (fecha_inicio, fecha_fin))

        # Crear figura con subplots
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_facecolor('#f5f6fa')

        # Gráfico de barras para veces contratado
        ax1 = plt.subplot(221)
        servicios = [r[0] for r in resultados]
        contrataciones = [r[2] if r[2] else 0 for r in resultados]

        ax1.bar(servicios, contrataciones, color='#3498db')
        plt.xticks(rotation=45, ha='right')
        ax1.set_title('Frecuencia de Contratación de Servicios')

        # Gráfico de torta para distribución por tipo
        ax2 = plt.subplot(222)
        tipos = {}
        for r in resultados:
            if r[1] not in tipos:
                tipos[r[1]] = 0
            tipos[r[1]] += r[2] if r[2] else 0

        ax2.pie(tipos.values(), labels=tipos.keys(), autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c', '#f1c40f', '#9b59b6'])
        ax2.set_title('Distribución por Tipo de Servicio')

        # Gráfico de barras para ingresos
        ax3 = plt.subplot(212)
        ingresos = [r[3] if r[3] else 0 for r in resultados]
        
        ax3.bar(servicios, ingresos, color='#e74c3c')
        plt.xticks(rotation=45, ha='right')
        ax3.set_title('Ingresos por Servicio')

        plt.tight_layout()

        # Mostrar gráfico en la ventana
        canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Botón para generar reporte
    btn_generar = tkinter.Button(frame_filtros,
        text="Generar Reporte",
        command=generar_reporte,
        font=("Helvetica", 12),
        fg="white",
        bg="#2ecc71",
        width=15,
        padx=10,
        pady=5)
    btn_generar.pack(pady=10)

    # Botón para cerrar
    btn_cerrar = tkinter.Button(frame_principal,
        text="Cerrar",
        command=ventana_informe.destroy,
        font=("Helvetica", 12),
        fg="white",
        bg="#e74c3c",
        width=15,
        padx=10,
        pady=5)
    btn_cerrar.pack(pady=20)

    # Centrar la ventana
    ventana_informe.update_idletasks()
    width = ventana_informe.winfo_width()
    height = ventana_informe.winfo_height()
    x = (ventana_informe.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana_informe.winfo_screenheight() // 2) - (height // 2)
    ventana_informe.geometry('{}x{}+{}+{}'.format(width, height, x, y))

#------------------------------------------------------------------------------------------------

# FUNCIONES DE ADMINISTRADOR
def eliminar_reservas_clientes(usuario):
    """
    Permite al administrador eliminar las reservas de los clientes.
    Muestra una interfaz con todas las reservas y permite su eliminación.
    """
    # Crear ventana para eliminar reservas
    ventana_eliminar = tkinter.Toplevel()
    ventana_eliminar.geometry("1000x700")
    ventana_eliminar.title("Eliminar Reservas - Administrador")
    ventana_eliminar.configure(bg="#f5f6fa")

    # Frame principal
    frame_principal = tkinter.Frame(ventana_eliminar, bg="#f5f6fa")
    frame_principal.pack(padx=40, pady=30, fill="both", expand=True)

    # Título
    titulo = tkinter.Label(frame_principal, 
        text="Eliminar Reservas de Clientes",
        font=("Helvetica", 24, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    titulo.pack(pady=(0,30))

    # Frame con scroll para las reservas
    frame_contenedor = tkinter.Frame(frame_principal, bg="#f5f6fa")
    frame_contenedor.pack(fill="both", expand=True)

    # Canvas y scrollbar
    canvas = tkinter.Canvas(frame_contenedor, bg="#f5f6fa")
    scrollbar = tkinter.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
    frame_reservas = tkinter.Frame(canvas, bg="#f5f6fa")

    # Configurar el scroll
    def configurar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_reservas.bind("<Configure>", configurar_scroll)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0,0), window=frame_reservas, anchor="nw", width=900)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Obtener todas las reservas con información del cliente
    query_reservas = """
        SELECT 
            r.id,
            u.nombre,
            h.numero_habitacion,
            h.tipo_habitacion,
            r.fecha_entrada,
            r.fecha_salida,
            r.num_personas
        FROM reservas r
        JOIN usuarios u ON r.id_usuario = u.id
        JOIN habitaciones h ON r.id_habitacion = h.id
        ORDER BY r.fecha_entrada DESC
    """
    
    reservas = db.obtener_datos(query_reservas)

    def eliminar_reserva(id_reserva):
        """Función para eliminar una reserva específica"""
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta reserva?"):
            # Primero eliminar los servicios asociados
            db.ejecutar_query("DELETE FROM reserva_servicios WHERE id_reserva = %s", (id_reserva,))
            # Luego eliminar la reserva
            if db.ejecutar_query("DELETE FROM reservas WHERE id = %s", (id_reserva,)):
                messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
                ventana_eliminar.destroy()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la reserva")

    if not reservas:
        mensaje_vacio = tkinter.Label(frame_reservas,
            text="No hay reservas registradas",
            font=("Helvetica", 14),
            fg="#7f8c8d",
            bg="#f5f6fa")
        mensaje_vacio.pack(pady=20)
    else:
        for reserva in reservas:
            # Frame para cada reserva
            frame_reserva = tkinter.Frame(frame_reservas, 
                bg="white",
                relief="raised",
                borderwidth=1)
            frame_reserva.pack(pady=10, fill="x")

            # Contenido de la reserva
            frame_contenido = tkinter.Frame(frame_reserva, bg="white")
            frame_contenido.pack(padx=20, pady=15, fill="x")

            # Información del cliente y habitación
            tkinter.Label(frame_contenido,
                text=f"Cliente: {reserva[1]}",
                font=("Helvetica", 12, "bold"),
                fg="#2c3e50",
                bg="white").pack(anchor="w")

            tkinter.Label(frame_contenido,
                text=f"Habitación {reserva[2]} - {reserva[3]}",
                font=("Helvetica", 11),
                fg="#2c3e50",
                bg="white").pack(anchor="w")

            # Fechas y personas
            fecha_entrada = datetime.strptime(str(reserva[4]), "%Y-%m-%d").strftime("%d/%m/%Y")
            fecha_salida = datetime.strptime(str(reserva[5]), "%Y-%m-%d").strftime("%d/%m/%Y")
            
            tkinter.Label(frame_contenido,
                text=f"Entrada: {fecha_entrada} - Salida: {fecha_salida}",
                font=("Helvetica", 11),
                fg="#7f8c8d",
                bg="white").pack(anchor="w")

            tkinter.Label(frame_contenido,
                text=f"Personas: {reserva[6]}",
                font=("Helvetica", 11),
                fg="#7f8c8d",
                bg="white").pack(anchor="w")

            # Botón de eliminar
            btn_eliminar = tkinter.Button(frame_contenido,
                text="Eliminar Reserva",
                command=lambda id=reserva[0]: eliminar_reserva(id),
                font=("Helvetica", 11),
                fg="white",
                bg="#e74c3c")
            btn_eliminar.pack(pady=(10,0))

    # Botón para cerrar
    btn_cerrar = tkinter.Button(frame_principal,
        text="Cerrar",
        command=ventana_eliminar.destroy,
        font=("Helvetica", 12),
        fg="white",
        bg="#3498db",
        width=15,
        padx=10,
        pady=5)
    btn_cerrar.pack(pady=20)

def modificar_reservas_clientes(usuario):
    """
    Permite al administrador modificar las reservas de los clientes.
    Muestra una interfaz con todas las reservas y permite su modificación.
    """
    # Crear ventana para modificar reservas
    ventana_modificar = tkinter.Toplevel()
    ventana_modificar.geometry("1000x700")
    ventana_modificar.title("Modificar Reservas - Administrador")
    ventana_modificar.configure(bg="#f5f6fa")

    # Frame principal
    frame_principal = tkinter.Frame(ventana_modificar, bg="#f5f6fa")
    frame_principal.pack(padx=40, pady=30, fill="both", expand=True)

    # Título
    titulo = tkinter.Label(frame_principal, 
        text="Modificar Reservas de Clientes",
        font=("Helvetica", 24, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    titulo.pack(pady=(0,30))

    # Frame con scroll para las reservas
    frame_contenedor = tkinter.Frame(frame_principal, bg="#f5f6fa")
    frame_contenedor.pack(fill="both", expand=True)

    # Canvas y scrollbar
    canvas = tkinter.Canvas(frame_contenedor, bg="#f5f6fa", highlightthickness=0)
    scrollbar = tkinter.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
    frame_reservas = tkinter.Frame(canvas, bg="#f5f6fa")

    # Configurar el scroll
    def configurar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_reservas.bind("<Configure>", configurar_scroll)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0,0), window=frame_reservas, anchor="nw", width=900)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Configurar el scroll con el mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Obtener todas las reservas con información del cliente
    query_reservas = """
        SELECT 
            r.id,
            u.nombre,
            h.id as id_habitacion,
            h.numero_habitacion,
            h.tipo_habitacion,
            r.fecha_entrada,
            r.fecha_salida,
            r.num_personas
        FROM reservas r
        JOIN usuarios u ON r.id_usuario = u.id
        JOIN habitaciones h ON r.id_habitacion = h.id
        ORDER BY r.fecha_entrada DESC
    """
    
    reservas = db.obtener_datos(query_reservas)

    def abrir_ventana_modificacion(reserva):
        """Abre una nueva ventana para modificar los detalles de la reserva"""
        ventana_edicion = tkinter.Toplevel()
        ventana_edicion.geometry("800x800")  # Aumentado el alto para asegurar que todo sea visible
        ventana_edicion.title(f"Modificar Reserva - Cliente: {reserva[1]}")
        ventana_edicion.configure(bg="#f5f6fa")
        ventana_edicion.transient(ventana_modificar)
        ventana_edicion.grab_set()

        # Frame principal con scroll
        canvas_principal = tkinter.Canvas(ventana_edicion, bg="#f5f6fa")
        scrollbar = tkinter.Scrollbar(ventana_edicion, orient="vertical", command=canvas_principal.yview)
        frame_edicion = tkinter.Frame(canvas_principal, bg="#f5f6fa")

        # Configurar scroll
        def configurar_scroll(event):
            canvas_principal.configure(scrollregion=canvas_principal.bbox("all"))
        
        frame_edicion.bind("<Configure>", configurar_scroll)
        canvas_principal.configure(yscrollcommand=scrollbar.set)
        canvas_principal.create_window((0,0), window=frame_edicion, anchor="nw", width=750)
        
        # Empaquetar canvas y scrollbar
        canvas_principal.pack(side="left", fill="both", expand=True, padx=(20,0))
        scrollbar.pack(side="right", fill="y")

        # Título de la ventana
        titulo = tkinter.Label(frame_edicion,
            text="Modificar Reserva",
            font=("Helvetica", 20, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa")
        titulo.pack(pady=(20,30))

        # Información del cliente
        frame_cliente = tkinter.LabelFrame(frame_edicion,
            text="Información del Cliente",
            font=("Helvetica", 12, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa")
        frame_cliente.pack(fill="x", padx=20, pady=10)

        tkinter.Label(frame_cliente,
            text=f"Cliente: {reserva[1]}",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=10)

        # Frame para selección de habitación
        frame_habitacion = tkinter.LabelFrame(frame_edicion,
            text="Seleccionar Habitación",
            font=("Helvetica", 12, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa")
        frame_habitacion.pack(fill="x", padx=20, pady=10)

        # Obtener habitaciones disponibles
        query_habitaciones = "SELECT id, numero_habitacion, tipo_habitacion FROM habitaciones"
        habitaciones = db.obtener_datos(query_habitaciones)
        
        # Variable para la habitación seleccionada
        habitacion_seleccionada = tkinter.StringVar(value=str(reserva[2]))

        for hab in habitaciones:
            radio = tkinter.Radiobutton(frame_habitacion,
                text=f"Habitación {hab[1]} - {hab[2]}",
                variable=habitacion_seleccionada,
                value=str(hab[0]),
                font=("Helvetica", 11),
                bg="#f5f6fa",
                activebackground="#e0e6ed",
                cursor="hand2")
            radio.pack(anchor="w", pady=5)

        # Frame para fechas
        frame_fechas = tkinter.LabelFrame(frame_edicion,
            text="Seleccionar Fechas",
            font=("Helvetica", 12, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa")
        frame_fechas.pack(fill="x", padx=20, pady=10)

        # Contenedor para los calendarios
        frame_calendarios = tkinter.Frame(frame_fechas, bg="#f5f6fa")
        frame_calendarios.pack(pady=10)

        # Frame para fecha de entrada
        frame_entrada = tkinter.Frame(frame_calendarios, bg="#f5f6fa")
        frame_entrada.pack(side="left", padx=10)

        tkinter.Label(frame_entrada,
            text="Fecha de entrada:",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=5)

        fecha_entrada_actual = datetime.strptime(str(reserva[5]), "%Y-%m-%d")
        cal_entrada = Calendar(frame_entrada,
            selectmode='day',
            year=fecha_entrada_actual.year,
            month=fecha_entrada_actual.month,
            day=fecha_entrada_actual.day,
            locale='es_ES',
            cursor="hand2")
        cal_entrada.pack()

        # Frame para fecha de salida
        frame_salida = tkinter.Frame(frame_calendarios, bg="#f5f6fa")
        frame_salida.pack(side="left", padx=10)

        tkinter.Label(frame_salida,
            text="Fecha de salida:",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=5)

        fecha_salida_actual = datetime.strptime(str(reserva[6]), "%Y-%m-%d")
        cal_salida = Calendar(frame_salida,
            selectmode='day',
            year=fecha_salida_actual.year,
            month=fecha_salida_actual.month,
            day=fecha_salida_actual.day,
            locale='es_ES',
            cursor="hand2")
        cal_salida.pack()

        # Frame para número de personas
        frame_personas = tkinter.LabelFrame(frame_edicion,
            text="Número de Personas",
            font=("Helvetica", 12, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa")
        frame_personas.pack(fill="x", padx=20, pady=10)

        entrada_personas = tkinter.Entry(frame_personas,
            font=("Helvetica", 11),
            width=10,
            justify="center")
        entrada_personas.insert(0, str(reserva[7]))
        entrada_personas.pack(pady=10)

        def guardar_cambios():
            try:
                # Validar fechas
                fecha_entrada = cal_entrada.selection_get()
                fecha_salida = cal_salida.selection_get()
                
                if fecha_entrada >= fecha_salida:
                    messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de entrada")
                    return

                # Validar número de personas
                try:
                    num_personas = int(entrada_personas.get())
                    if num_personas <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido de personas")
                    return

                # Verificar disponibilidad de la habitación
                query_disponibilidad = """
                    SELECT COUNT(*) FROM reservas 
                    WHERE id_habitacion = %s 
                    AND id != %s
                    AND ((fecha_entrada BETWEEN %s AND %s) 
                    OR (fecha_salida BETWEEN %s AND %s)
                    OR (fecha_entrada <= %s AND fecha_salida >= %s))
                """
                resultado = db.obtener_datos(query_disponibilidad, (
                    int(habitacion_seleccionada.get()),
                    reserva[0],
                    fecha_entrada,
                    fecha_salida,
                    fecha_entrada,
                    fecha_salida,
                    fecha_entrada,
                    fecha_salida
                ))

                if resultado[0][0] > 0:
                    messagebox.showerror("Error", "La habitación no está disponible para las fechas seleccionadas")
                    return

                # Actualizar la reserva
                query_actualizar = """
                    UPDATE reservas 
                    SET id_habitacion = %s, fecha_entrada = %s, fecha_salida = %s, num_personas = %s
                    WHERE id = %s
                """
                if db.ejecutar_query(query_actualizar, (
                    int(habitacion_seleccionada.get()),
                    fecha_entrada,
                    fecha_salida,
                    num_personas,
                    reserva[0]
                )):
                    messagebox.showinfo("Éxito", "Reserva modificada correctamente")
                    ventana_edicion.destroy()
                    ventana_modificar.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo modificar la reserva")

            except Exception as e:
                messagebox.showerror("Error", f"Error al modificar la reserva: {str(e)}")

        # Frame para botones fijo en la parte inferior
        frame_botones = tkinter.Frame(frame_edicion, bg="#f5f6fa")
        frame_botones.pack(pady=30)

        # Botón Cancelar
        btn_cancelar = tkinter.Button(frame_botones,
            text="Cancelar",
            command=ventana_edicion.destroy,
            font=("Helvetica", 12),
            fg="white",
            bg="#e74c3c",
            activebackground="#c0392b",
            cursor="hand2",
            width=15)
        btn_cancelar.pack(side="left", padx=10)

        # Botón Guardar Cambios
        btn_guardar = tkinter.Button(frame_botones,
            text="Guardar Cambios",
            command=guardar_cambios,
            font=("Helvetica", 12),
            fg="white",
            bg="#2ecc71",
            activebackground="#27ae60",
            cursor="hand2",
            width=15)
        btn_guardar.pack(side="left", padx=10)

        # Configurar el scroll con el mouse
        def _on_mousewheel(event):
            canvas_principal.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas_principal.bind_all("<MouseWheel>", _on_mousewheel)

        # Centrar la ventana
        ventana_edicion.update_idletasks()
        width = ventana_edicion.winfo_width()
        height = ventana_edicion.winfo_height()
        x = (ventana_edicion.winfo_screenwidth() // 2) - (width // 2)
        y = (ventana_edicion.winfo_screenheight() // 2) - (height // 2)
        ventana_edicion.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    if not reservas:
        mensaje_vacio = tkinter.Label(frame_reservas,
            text="No hay reservas registradas",
            font=("Helvetica", 14),
            fg="#7f8c8d",
            bg="#f5f6fa")
        mensaje_vacio.pack(pady=20)
    else:
        for reserva in reservas:
            # Frame para cada reserva
            frame_reserva = tkinter.Frame(frame_reservas, 
                bg="white",
                relief="raised",
                borderwidth=1)
            frame_reserva.pack(pady=10, fill="x")

            # Contenido de la reserva
            frame_contenido = tkinter.Frame(frame_reserva, bg="white")
            frame_contenido.pack(padx=20, pady=15, fill="x")

            # Información del cliente y habitación
            tkinter.Label(frame_contenido,
                text=f"Cliente: {reserva[1]}",
                font=("Helvetica", 12, "bold"),
                fg="#2c3e50",
                bg="white").pack(anchor="w")

            tkinter.Label(frame_contenido,
                text=f"Habitación {reserva[3]} - {reserva[4]}",
                font=("Helvetica", 11),
                fg="#2c3e50",
                bg="white").pack(anchor="w")

            # Fechas y personas
            fecha_entrada = datetime.strptime(str(reserva[5]), "%Y-%m-%d").strftime("%d/%m/%Y")
            fecha_salida = datetime.strptime(str(reserva[6]), "%Y-%m-%d").strftime("%d/%m/%Y")
            
            tkinter.Label(frame_contenido,
                text=f"Entrada: {fecha_entrada} - Salida: {fecha_salida}",
                font=("Helvetica", 11),
                fg="#7f8c8d",
                bg="white").pack(anchor="w")

            tkinter.Label(frame_contenido,
                text=f"Personas: {reserva[7]}",
                font=("Helvetica", 11),
                fg="#7f8c8d",
                bg="white").pack(anchor="w")

            # Botón de modificar
            btn_modificar = tkinter.Button(frame_contenido,
                text="Modificar Reserva",
                command=lambda r=reserva: abrir_ventana_modificacion(r),
                font=("Helvetica", 11),
                fg="white",
                bg="#3498db",
                activebackground="#2980b9",
                cursor="hand2")
            btn_modificar.pack(pady=(10,0))

    # Botón para cerrar
    btn_cerrar = tkinter.Button(frame_principal,
        text="Cerrar",
        command=ventana_modificar.destroy,
        font=("Helvetica", 12),
        fg="white",
        bg="#3498db",
        activebackground="#2980b9",
        cursor="hand2",
        width=15,
        padx=10,
        pady=5)
    btn_cerrar.pack(pady=20)

    # Centrar la ventana principal
    ventana_modificar.update_idletasks()
    width = ventana_modificar.winfo_width()
    height = ventana_modificar.winfo_height()
    x = (ventana_modificar.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana_modificar.winfo_screenheight() // 2) - (height // 2)
    ventana_modificar.geometry('{}x{}+{}+{}'.format(width, height, x, y))

#------------------------------------------------------------------------------------------------

# FUNCIONES DE FUNCIONARIO
def visualizar_reservas(usuario):
    """
    Permite al funcionario visualizar todas las reservas activas y próximas,
    con opciones para gestionar check-in y check-out.
    """
    ventana_visualizar = tkinter.Toplevel()
    ventana_visualizar.geometry("1200x800")
    ventana_visualizar.title("Visualizar Reservas - Funcionario")
    ventana_visualizar.configure(bg="#f5f6fa")

    # Frame principal
    frame_principal = tkinter.Frame(ventana_visualizar, bg="#f5f6fa")
    frame_principal.pack(padx=40, pady=30, fill="both", expand=True)

    # Título
    titulo = tkinter.Label(frame_principal, 
        text="Gestión de Reservas",
        font=("Helvetica", 24, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    titulo.pack(pady=(0,20))

    # Frame para filtros
    frame_filtros = tkinter.LabelFrame(frame_principal,
        text="Filtros de Búsqueda",
        font=("Helvetica", 12, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    frame_filtros.pack(fill="x", pady=(0,20))

    # Frame para los controles de filtro
    frame_controles = tkinter.Frame(frame_filtros, bg="#f5f6fa")
    frame_controles.pack(padx=20, pady=10, fill="x")

    # Filtro por estado
    tkinter.Label(frame_controles,
        text="Estado:",
        font=("Helvetica", 11),
        fg="#2c3e50",
        bg="#f5f6fa").pack(side="left", padx=(0,10))

    estado_seleccionado = tkinter.StringVar(value="todos")
    estados = [
        ("Todos", "todos"),
        ("Pendientes", "pendiente"),
        ("Check-in", "check_in"),
        ("Check-out", "check_out")
    ]

    for texto, valor in estados:
        tkinter.Radiobutton(frame_controles,
            text=texto,
            variable=estado_seleccionado,
            value=valor,
            font=("Helvetica", 11),
            bg="#f5f6fa",
            command=lambda: actualizar_lista()).pack(side="left", padx=10)

    # Frame para la lista de reservas con scroll
    frame_contenedor = tkinter.Frame(frame_principal, bg="#f5f6fa")
    frame_contenedor.pack(fill="both", expand=True)

    # Canvas y scrollbar
    canvas = tkinter.Canvas(frame_contenedor, bg="#f5f6fa")
    scrollbar = tkinter.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
    frame_reservas = tkinter.Frame(canvas, bg="#f5f6fa")

    def configurar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_reservas.bind("<Configure>", configurar_scroll)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0,0), window=frame_reservas, anchor="nw", width=1100)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def actualizar_lista():
        # Limpiar lista actual
        for widget in frame_reservas.winfo_children():
            widget.destroy()

        # Consulta base para todas las reservas
        query_base = """
            SELECT 
                r.id,
                u.nombre,
                h.numero_habitacion,
                h.tipo_habitacion,
                r.fecha_entrada,
                r.fecha_salida,
                r.num_personas,
                r.estado,
                r.hora_check_in,
                r.hora_check_out
            FROM reservas r
            JOIN usuarios u ON r.id_usuario = u.id
            JOIN habitaciones h ON r.id_habitacion = h.id
            WHERE 1=1
        """

        # Modificar consulta según el filtro seleccionado
        estado = estado_seleccionado.get()
        params = []
        if estado != "todos":
            query_base += " AND r.estado = %s"
            params.append(estado)

        query_base += " ORDER BY r.fecha_entrada ASC"
        
        reservas = db.obtener_datos(query_base, tuple(params) if params else None)

        if not reservas:
            mensaje_vacio = tkinter.Label(frame_reservas,
                text="No hay reservas que coincidan con los filtros seleccionados",
                font=("Helvetica", 14),
                fg="#7f8c8d",
                bg="#f5f6fa")
            mensaje_vacio.pack(pady=20)
            return

        for reserva in reservas:
            # Frame para cada reserva
            frame_reserva = tkinter.Frame(frame_reservas, 
                bg="white",
                relief="raised",
                borderwidth=1)
            frame_reserva.pack(pady=10, fill="x", padx=20)

            # Frame para el contenido
            frame_contenido = tkinter.Frame(frame_reserva, bg="white")
            frame_contenido.pack(padx=20, pady=15, fill="x")

            # Frame para información principal
            frame_info = tkinter.Frame(frame_contenido, bg="white")
            frame_info.pack(fill="x")

            # Columna izquierda
            frame_izq = tkinter.Frame(frame_info, bg="white")
            frame_izq.pack(side="left", fill="x", expand=True)

            tkinter.Label(frame_izq,
                text=f"Cliente: {reserva[1]}",
                font=("Helvetica", 12, "bold"),
                fg="#2c3e50",
                bg="white").pack(anchor="w")

            tkinter.Label(frame_izq,
                text=f"Habitación {reserva[2]} - {reserva[3]}",
                font=("Helvetica", 11),
                fg="#2c3e50",
                bg="white").pack(anchor="w")

            # Columna derecha
            frame_der = tkinter.Frame(frame_info, bg="white")
            frame_der.pack(side="right")

            # Estado con color
            colores_estado = {
                "pendiente": "#f1c40f",
                "check_in": "#2ecc71",
                "check_out": "#e74c3c"
            }
            texto_estado = {
                "pendiente": "Pendiente",
                "check_in": "Check-in realizado",
                "check_out": "Check-out realizado"
            }
            
            estado_actual = reserva[7] or "pendiente"
            tkinter.Label(frame_der,
                text=texto_estado.get(estado_actual, "Pendiente"),
                font=("Helvetica", 11, "bold"),
                fg="white",
                bg=colores_estado.get(estado_actual, "#f1c40f"),
                padx=10,
                pady=5).pack(anchor="e")

            # Fechas y personas
            fecha_entrada = datetime.strptime(str(reserva[4]), "%Y-%m-%d").strftime("%d/%m/%Y")
            fecha_salida = datetime.strptime(str(reserva[5]), "%Y-%m-%d").strftime("%d/%m/%Y")
            
            frame_detalles = tkinter.Frame(frame_contenido, bg="white")
            frame_detalles.pack(fill="x", pady=(10,0))

            tkinter.Label(frame_detalles,
                text=f"Entrada: {fecha_entrada}",
                font=("Helvetica", 11),
                fg="#7f8c8d",
                bg="white").pack(side="left")

            tkinter.Label(frame_detalles,
                text=f"Salida: {fecha_salida}",
                font=("Helvetica", 11),
                fg="#7f8c8d",
                bg="white").pack(side="left", padx=20)

            tkinter.Label(frame_detalles,
                text=f"Personas: {reserva[6]}",
                font=("Helvetica", 11),
                fg="#7f8c8d",
                bg="white").pack(side="left")

            # Frame para botones
            frame_botones = tkinter.Frame(frame_contenido, bg="white")
            frame_botones.pack(pady=(10,0))

            def realizar_check_in(id_reserva):
                if messagebox.askyesno("Confirmar Check-in", 
                    "¿Desea realizar el check-in para esta reserva?"):
                    if db.ejecutar_query(
                        "UPDATE reservas SET estado = 'check_in' WHERE id = %s",
                        (id_reserva,)):
                        messagebox.showinfo("Éxito", "Check-in realizado correctamente")
                        actualizar_lista()
                    else:
                        messagebox.showerror("Error", "No se pudo realizar el check-in")

            def realizar_check_out(id_reserva):
                if messagebox.askyesno("Confirmar Check-out", 
                    "¿Desea realizar el check-out para esta reserva?"):
                    if db.ejecutar_query(
                        "UPDATE reservas SET estado = 'check_out' WHERE id = %s",
                        (id_reserva,)):
                        messagebox.showinfo("Éxito", "Check-out realizado correctamente")
                        actualizar_lista()
                    else:
                        messagebox.showerror("Error", "No se pudo realizar el check-out")

            # Mostrar botones según el estado
            if estado_actual == "pendiente":
                btn_check_in = tkinter.Button(frame_botones,
                    text="Realizar Check-in",
                    command=lambda id=reserva[0]: realizar_check_in(id),
                    font=("Helvetica", 11),
                    fg="white",
                    bg="#2ecc71",
                    activebackground="#27ae60",
                    cursor="hand2")
                btn_check_in.pack(side="left", padx=5)

            elif estado_actual == "check_in":
                btn_check_out = tkinter.Button(frame_botones,
                    text="Realizar Check-out",
                    command=lambda id=reserva[0]: realizar_check_out(id),
                    font=("Helvetica", 11),
                    fg="white",
                    bg="#e74c3c",
                    activebackground="#c0392b",
                    cursor="hand2")
                btn_check_out.pack(side="left", padx=5)

            # Botón para ver detalles
            btn_detalles = tkinter.Button(frame_botones,
                text="Ver Detalles",
                command=lambda r=reserva: mostrar_detalles_reserva(r),
                font=("Helvetica", 11),
                fg="white",
                bg="#3498db",
                activebackground="#2980b9",
                cursor="hand2")
            btn_detalles.pack(side="left", padx=5)

    def mostrar_detalles_reserva(reserva):
        """Muestra una ventana con los detalles completos de la reserva"""
        ventana_detalles = tkinter.Toplevel()
        ventana_detalles.geometry("600x500")
        ventana_detalles.title(f"Detalles de Reserva - {reserva[1]}")
        ventana_detalles.configure(bg="#f5f6fa")

        # Frame principal
        frame_detalles = tkinter.Frame(ventana_detalles, bg="#f5f6fa")
        frame_detalles.pack(padx=40, pady=30, fill="both", expand=True)

        # Título
        tkinter.Label(frame_detalles,
            text="Detalles de la Reserva",
            font=("Helvetica", 20, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=(0,20))

        # Información del cliente
        frame_cliente = tkinter.LabelFrame(frame_detalles,
            text="Información del Cliente",
            font=("Helvetica", 12, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa")
        frame_cliente.pack(fill="x", pady=10)

        tkinter.Label(frame_cliente,
            text=f"Nombre: {reserva[1]}",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=5)

        # Información de la habitación
        frame_habitacion = tkinter.LabelFrame(frame_detalles,
            text="Información de la Habitación",
            font=("Helvetica", 12, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa")
        frame_habitacion.pack(fill="x", pady=10)

        tkinter.Label(frame_habitacion,
            text=f"Número: {reserva[2]}",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=5)

        tkinter.Label(frame_habitacion,
            text=f"Tipo: {reserva[3]}",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=5)

        # Información de la reserva
        frame_info_reserva = tkinter.LabelFrame(frame_detalles,
            text="Información de la Reserva",
            font=("Helvetica", 12, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa")
        frame_info_reserva.pack(fill="x", pady=10)

        fecha_entrada = datetime.strptime(str(reserva[4]), "%Y-%m-%d").strftime("%d/%m/%Y")
        fecha_salida = datetime.strptime(str(reserva[5]), "%Y-%m-%d").strftime("%d/%m/%Y")

        tkinter.Label(frame_info_reserva,
            text=f"Fecha de entrada: {fecha_entrada}",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=5)

        tkinter.Label(frame_info_reserva,
            text=f"Fecha de salida: {fecha_salida}",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=5)

        tkinter.Label(frame_info_reserva,
            text=f"Número de personas: {reserva[6]}",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=5)

        estado_actual = reserva[7] or "pendiente"
        tkinter.Label(frame_info_reserva,
            text=f"Estado: {texto_estado.get(estado_actual, 'Pendiente')}",
            font=("Helvetica", 11),
            fg="#2c3e50",
            bg="#f5f6fa").pack(pady=5)

        # Obtener servicios de la reserva
        query_servicios = """
            SELECT s.nombre_servicio, s.tipo_servicio, s.costo_persona
            FROM reserva_servicios rs
            JOIN servicios s ON rs.id_servicio = s.id
            WHERE rs.id_reserva = %s
        """
        servicios = db.obtener_datos(query_servicios, (reserva[0],))

        if servicios:
            frame_servicios = tkinter.LabelFrame(frame_detalles,
                text="Servicios Adicionales",
                font=("Helvetica", 12, "bold"),
                fg="#2c3e50",
                bg="#f5f6fa")
            frame_servicios.pack(fill="x", pady=10)

            for servicio in servicios:
                tkinter.Label(frame_servicios,
                    text=f"• {servicio[0]} ({servicio[1]}) - ${servicio[2]:,} CLP p/persona",
                    font=("Helvetica", 11),
                    fg="#2c3e50",
                    bg="#f5f6fa").pack(pady=2)

        # Botón para cerrar
        tkinter.Button(frame_detalles,
            text="Cerrar",
            command=ventana_detalles.destroy,
            font=("Helvetica", 12),
            fg="white",
            bg="#3498db",
            activebackground="#2980b9",
            cursor="hand2").pack(pady=20)

    # Iniciar con la lista completa
    actualizar_lista()

    # Botón para cerrar
    btn_cerrar = tkinter.Button(frame_principal,
        text="Cerrar",
        command=ventana_visualizar.destroy,
        font=("Helvetica", 12),
        fg="white",
        bg="#3498db",
        activebackground="#2980b9",
        cursor="hand2",
        width=15)
    btn_cerrar.pack(pady=20)

def agendar_horas(usuario):
    """
    Permite al funcionario agendar y gestionar horas para check-in y check-out de las reservas.
    """
    ventana_agendar = tkinter.Toplevel()
    ventana_agendar.geometry("1200x800")
    ventana_agendar.title("Agendar Horas - Funcionario")
    ventana_agendar.configure(bg="#f5f6fa")

    # Frame principal
    frame_principal = tkinter.Frame(ventana_agendar, bg="#f5f6fa")
    frame_principal.pack(padx=40, pady=30, fill="both", expand=True)

    # Título
    titulo = tkinter.Label(frame_principal, 
        text="Gestión de Horarios Check-in/Check-out",
        font=("Helvetica", 24, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    titulo.pack(pady=(0,20))

    # Frame superior para calendario y filtros
    frame_superior = tkinter.Frame(frame_principal, bg="#f5f6fa")
    frame_superior.pack(fill="x", pady=(0,20))

    # Frame izquierdo para el calendario
    frame_calendario = tkinter.LabelFrame(frame_superior,
        text="Seleccionar Fecha",
        font=("Helvetica", 12, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    frame_calendario.pack(side="left", padx=20, fill="both")

    # Calendario
    cal = Calendar(frame_calendario,
        selectmode='day',
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day,
        locale='es_ES',
        cursor="hand2")
    cal.pack(pady=10)

    # Frame derecho para filtros
    frame_filtros = tkinter.LabelFrame(frame_superior,
        text="Filtros",
        font=("Helvetica", 12, "bold"),
        fg="#2c3e50",
        bg="#f5f6fa")
    frame_filtros.pack(side="left", padx=20, fill="both", expand=True)

    # Variables para filtros
    filtro_tipo = tkinter.StringVar(value="todos")
    filtro_estado = tkinter.StringVar(value="todos")

    # Frame para tipo de check
    frame_tipo = tkinter.Frame(frame_filtros, bg="#f5f6fa")
    frame_tipo.pack(fill="x", pady=5)

    tkinter.Label(frame_tipo,
        text="Tipo:",
        font=("Helvetica", 11),
        fg="#2c3e50",
        bg="#f5f6fa").pack(side="left", padx=(0,10))

    tipos = [
        ("Todos", "todos"),
        ("Check-in", "check_in"),
        ("Check-out", "check_out")
    ]

    for texto, valor in tipos:
        tkinter.Radiobutton(frame_tipo,
            text=texto,
            variable=filtro_tipo,
            value=valor,
            font=("Helvetica", 11),
            bg="#f5f6fa",
            command=lambda: actualizar_horarios()).pack(side="left", padx=10)

    # Frame para estado
    frame_estado = tkinter.Frame(frame_filtros, bg="#f5f6fa")
    frame_estado.pack(fill="x", pady=5)

    tkinter.Label(frame_estado,
        text="Estado:",
        font=("Helvetica", 11),
        fg="#2c3e50",
        bg="#f5f6fa").pack(side="left", padx=(0,10))

    estados = [
        ("Todos", "todos"),
        ("Pendientes", "pendiente"),
        ("Agendados", "agendado")
    ]

    for texto, valor in estados:
        tkinter.Radiobutton(frame_estado,
            text=texto,
            variable=filtro_estado,
            value=valor,
            font=("Helvetica", 11),
            bg="#f5f6fa",
            command=lambda: actualizar_horarios()).pack(side="left", padx=10)

    # Frame para la lista de horarios con scroll
    frame_contenedor = tkinter.Frame(frame_principal, bg="#f5f6fa")
    frame_contenedor.pack(fill="both", expand=True)

    # Canvas y scrollbar
    canvas = tkinter.Canvas(frame_contenedor, bg="#f5f6fa")
    scrollbar = tkinter.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
    frame_horarios = tkinter.Frame(canvas, bg="#f5f6fa")

    def configurar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_horarios.bind("<Configure>", configurar_scroll)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0,0), window=frame_horarios, anchor="nw", width=1100)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def validar_hora(hora):
        """Valida el formato de hora HH:MM"""
        try:
            datetime.strptime(hora, "%H:%M")
            return True
        except ValueError:
            return False

    def guardar_hora(id_reserva, tipo, hora_var, frame_reserva):
        """Guarda la hora de check-in o check-out"""
        hora = hora_var.get()
        if not validar_hora(hora):
            messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM")
            return

        campo = "hora_check_in" if tipo == "check_in" else "hora_check_out"
        hora_dt = datetime.strptime(hora, "%H:%M").time()

        if db.ejecutar_query(f"UPDATE reservas SET {campo} = %s WHERE id = %s",
            (hora_dt, id_reserva)):
            # Cambiar el estado del frame a agendado
            for widget in frame_reserva.winfo_children():
                widget.configure(bg="#e8f5e9")
            frame_reserva.configure(bg="#e8f5e9")
            messagebox.showinfo("Éxito", f"Hora de {tipo.replace('_', '-')} guardada correctamente")
        else:
            messagebox.showerror("Error", f"No se pudo guardar la hora de {tipo.replace('_', '-')}")

    def actualizar_horarios(event=None):
        # Limpiar lista actual
        for widget in frame_horarios.winfo_children():
            widget.destroy()

        fecha_seleccionada = cal.selection_get()
        
        # Construir la consulta según los filtros
        query_base = """
            SELECT 
                r.id,
                u.nombre,
                h.numero_habitacion,
                h.tipo_habitacion,
                r.fecha_entrada,
                r.fecha_salida,
                r.num_personas,
                r.hora_check_in,
                r.hora_check_out,
                r.estado
            FROM reservas r
            JOIN usuarios u ON r.id_usuario = u.id
            JOIN habitaciones h ON r.id_habitacion = h.id
            WHERE (DATE(r.fecha_entrada) = %s OR DATE(r.fecha_salida) = %s)
        """
        params = [fecha_seleccionada, fecha_seleccionada]

        # Aplicar filtro de tipo
        tipo = filtro_tipo.get()
        if tipo == "check_in":
            query_base += " AND DATE(r.fecha_entrada) = %s"
            params.append(fecha_seleccionada)
        elif tipo == "check_out":
            query_base += " AND DATE(r.fecha_salida) = %s"
            params.append(fecha_seleccionada)

        # Aplicar filtro de estado
        estado = filtro_estado.get()
        if estado == "pendiente":
            query_base += " AND (r.hora_check_in IS NULL OR r.hora_check_out IS NULL)"
        elif estado == "agendado":
            query_base += " AND (r.hora_check_in IS NOT NULL OR r.hora_check_out IS NOT NULL)"

        query_base += " ORDER BY COALESCE(r.hora_check_in, '23:59:59'), COALESCE(r.hora_check_out, '23:59:59')"
        
        reservas = db.obtener_datos(query_base, tuple(params))

        if not reservas:
            tkinter.Label(frame_horarios,
                text="No hay reservas para esta fecha con los filtros seleccionados",
                font=("Helvetica", 14),
                fg="#7f8c8d",
                bg="#f5f6fa").pack(pady=20)
            return

        for reserva in reservas:
            # Frame para cada reserva
            frame_reserva = tkinter.Frame(frame_horarios,
                bg="#ffffff",
                relief="raised",
                borderwidth=1)
            frame_reserva.pack(fill="x", pady=5, padx=20)

            # Si tiene horas agendadas, cambiar el color de fondo
            if reserva[7] or reserva[8]:  # hora_check_in o hora_check_out
                frame_reserva.configure(bg="#e8f5e9")

            # Frame para la información
            frame_info = tkinter.Frame(frame_reserva, bg=frame_reserva.cget("bg"))
            frame_info.pack(padx=20, pady=10, fill="x")

            # Columna izquierda: Información del cliente y habitación
            frame_izq = tkinter.Frame(frame_info, bg=frame_reserva.cget("bg"))
            frame_izq.pack(side="left", fill="x", expand=True)

            # Información básica
            tkinter.Label(frame_izq,
                text=f"Cliente: {reserva[1]}",
                font=("Helvetica", 12, "bold"),
                fg="#2c3e50",
                bg=frame_reserva.cget("bg")).pack(anchor="w")

            tkinter.Label(frame_izq,
                text=f"Habitación {reserva[2]} - {reserva[3]}",
                font=("Helvetica", 11),
                fg="#2c3e50",
                bg=frame_reserva.cget("bg")).pack(anchor="w")

            # Fechas
            fecha_entrada = datetime.strptime(str(reserva[4]), "%Y-%m-%d").strftime("%d/%m/%Y")
            fecha_salida = datetime.strptime(str(reserva[5]), "%Y-%m-%d").strftime("%d/%m/%Y")
            
            tkinter.Label(frame_izq,
                text=f"Entrada: {fecha_entrada} - Salida: {fecha_salida}",
                font=("Helvetica", 11),
                fg="#7f8c8d",
                bg=frame_reserva.cget("bg")).pack(anchor="w")

            # Columna derecha: Gestión de horas
            frame_der = tkinter.Frame(frame_info, bg=frame_reserva.cget("bg"))
            frame_der.pack(side="right", padx=(20,0))

            # Si es fecha de entrada, mostrar gestión de check-in
            if fecha_seleccionada == reserva[4].date():
                frame_check_in = tkinter.Frame(frame_der, bg=frame_reserva.cget("bg"))
                frame_check_in.pack(side="left", padx=10)

                tkinter.Label(frame_check_in,
                    text="Hora Check-in:",
                    font=("Helvetica", 11),
                    fg="#2c3e50",
                    bg=frame_reserva.cget("bg")).pack(side="left", padx=(0,10))

                hora_check_in = tkinter.StringVar(value=reserva[7].strftime("%H:%M") if reserva[7] else "")
                entrada_check_in = tkinter.Entry(frame_check_in,
                    textvariable=hora_check_in,
                    font=("Helvetica", 11),
                    width=10)
                entrada_check_in.pack(side="left")

                tkinter.Button(frame_check_in,
                    text="Guardar",
                    command=lambda: guardar_hora(reserva[0], "check_in", hora_check_in, frame_reserva),
                    font=("Helvetica", 11),
                    fg="white",
                    bg="#2ecc71",
                    activebackground="#27ae60",
                    cursor="hand2").pack(side="left", padx=10)

            # Si es fecha de salida, mostrar gestión de check-out
            if fecha_seleccionada == reserva[5].date():
                frame_check_out = tkinter.Frame(frame_der, bg=frame_reserva.cget("bg"))
                frame_check_out.pack(side="left", padx=10)

                tkinter.Label(frame_check_out,
                    text="Hora Check-out:",
                    font=("Helvetica", 11),
                    fg="#2c3e50",
                    bg=frame_reserva.cget("bg")).pack(side="left", padx=(0,10))

                hora_check_out = tkinter.StringVar(value=reserva[8].strftime("%H:%M") if reserva[8] else "")
                entrada_check_out = tkinter.Entry(frame_check_out,
                    textvariable=hora_check_out,
                    font=("Helvetica", 11),
                    width=10)
                entrada_check_out.pack(side="left")

                tkinter.Button(frame_check_out,
                    text="Guardar",
                    command=lambda: guardar_hora(reserva[0], "check_out", hora_check_out, frame_reserva),
                    font=("Helvetica", 11),
                    fg="white",
                    bg="#2ecc71",
                    activebackground="#27ae60",
                    cursor="hand2").pack(side="left", padx=10)

    # Vincular la actualización al cambio de fecha
    cal.bind("<<CalendarSelected>>", actualizar_horarios)

    # Mostrar horarios iniciales
    actualizar_horarios()

    # Botón para cerrar
    btn_cerrar = tkinter.Button(frame_principal,
        text="Cerrar",
        command=ventana_agendar.destroy,
        font=("Helvetica", 12),
        fg="white",
        bg="#3498db",
        activebackground="#2980b9",
        cursor="hand2",
        width=15)
    btn_cerrar.pack(pady=20)

    # Centrar la ventana
    ventana_agendar.update_idletasks()
    width = ventana_agendar.winfo_width()
    height = ventana_agendar.winfo_height()
    x = (ventana_agendar.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana_agendar.winfo_screenheight() // 2) - (height // 2)
    ventana_agendar.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# INICIALIZACIÓN DE DATOS Y EJECUCIÓN DEL PROGRAMA
inicializar_datos()
ventana.mainloop()

