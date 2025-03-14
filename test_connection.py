import mysql.connector

def test_db_connection(db_config):
    try:
        # Intentar conectar a la base de datos
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("✅ ¡Conexión a la base de datos exitosa!")
        
        # Cerrar la conexión
        connection.close()
        print("Conexión cerrada.")
    
    except mysql.connector.Error as err:
        print(f"❌ Error al conectar a la base de datos: {err}")

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',       # Usuario de MySQL (por defecto es "root" en XAMPP)
    'password': '',       # Contraseña de MySQL (por defecto está vacía en XAMPP)
    'database': 'divia_db'  # Nombre de la base de datos
}

# Probar la conexión
test_db_connection(db_config)