# Sistema de Reservas - Hostal Miryks

## Sobre el proyecto
Este es mi proyecto académico de un sistema de reservas hecho con Python y Tkinter. Lo desarrollé pensando en un hostal ficticio llamado Miryks, donde se pueden hacer reservas de habitaciones y gestionar diferentes servicios. Para hacerlo más realista, incluí varios roles de usuario para ver cómo funcionaría en un hostal de verdad.

## Lo que puedes hacer

Si entras como cliente puedes:
- Hacer reservas cuando quieras
- Pedir servicios extra (como desayuno o estacionamiento)
- Ver tus reservas y cómo van
- Revisar a qué hora puedes entrar y salir

Si eres funcionario del hostal:
- Ves quién llega y se va cada día
- Manejas los check-in y check-out
- Organizas los horarios
- Mantienes todo al día

Como administrador:
- Controlas todas las reservas
- Puedes cambiar o cancelar reservas
- Manejas los usuarios
- Supervisas todo

Y si eres el gestor:
- Ves gráficos de ocupación
- Analizas qué servicios se usan más
- Generas informes
- Tienes toda la info para tomar decisiones

## Para hacerlo funcionar necesitas:

En tu PC:
- Python 3.8 o más nuevo
- MySQL 8.0
- Las librerías del requirements.txt
- Un procesador normal (2GHz)
- 4GB de RAM
- 500MB de espacio

## Pasos para instalarlo:

1. Clona o descarga el proyecto

2. Crea un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
```

3. Instala las librerías:
```bash
pip install -r requirements.txt
```

4. Prepara MySQL:
- Crea una base de datos 'hostal_miryks'
- Importa los datos de prueba
- Configura la conexión

5. Y arranca el programa:
```bash
python main.py
```

## Usuarios de prueba

Para probar como administrador:
- Usuario: admin
- Clave: #305Dlab1

Para probar como funcionario:
- Usuario: funcionario
- Clave: #305Dlab2

Para probar como gestor:
- Usuario: gestor
- Clave: #305Dlab3

Para probar como cliente usa cualquiera:
- antonio305 / Antonio1456
- federico24 / Federico245

## Las habitaciones

Tenemos tres tipos:
1. Suite de Lujo
   - 4 personas
   - Baño privado
   - $80,000 por noche

2. Doble
   - 2 personas
   - Baño compartido
   - $40,000 por noche

3. Individual
   - 1 persona
   - Baño privado
   - $30,000 por noche

## Servicios adicionales

- Desayuno continental → $5,000 
  (Con pan, frutas, cereales y bebidas calientes)

- Estacionamiento → $10,000 
  (Con vigilancia 24/7)

- Tour por la ciudad → $15,000 
  (Con un guía que conoce todo)

- Wi-Fi → $3,000 
  (Para Netflix o trabajo remoto)

## ¿Cómo funciona una reserva?

Es simple:
1. El cliente reserva y elige sus servicios
2. El funcionario pone los horarios
3. Cuando llega → check-in
4. Cuando se va → check-out

## Detalles técnicos

- Está hecho con Python y Tkinter
- Usa MySQL para la base de datos
- Tiene sonidos (Pygame) para hacerlo más dinámico
- Gráficos de matplotlib para los informes
- Un calendario fácil de usar
- Diferentes permisos según el usuario
- Todo con validaciones para que no falle

## Nota
Este es un proyecto académico, así que todos los datos y usuarios son de prueba. 