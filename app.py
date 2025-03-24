from flask import Flask, render_template
import mysql.connector

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'divia_db'
}

# Ruta principal
@app.route('/')
def index():
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Obtener productos con stock mayor a cero
        cursor.execute("SELECT * FROM productos WHERE stock > 0")
        productos = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        # Renderizar la plantilla HTML con los productos
        return render_template('index.html', productos=productos)

    except mysql.connector.Error as err:
        return f"Error al conectar a la base de datos: {err}"

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)