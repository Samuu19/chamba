import requests
import mysql.connector

def get_products_from_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        products = response.json()

        valid_products = []
        for product in products:
            try:
                valid_products.append({
                    "codigo": product["Codigo"],
                    "name": product["Name"],
                    "brand": product["Brand"],
                    "family": product["Family"],
                    "stock": int(product["Stock"]),
                    "regular_price": product["FinalPrice"],
                    "image": product["Imagen"],
                    "sync": int(product["Sync"])
                })
            except KeyError as e:
                print(f"Falta un campo requerido en el producto: {str(e)}")
            except ValueError as e:
                print(f"Error en la conversión de datos del producto: {str(e)}")

        return valid_products

    except Exception as e:
        print(f"Error al obtener productos del JSON: {str(e)}")
        return []

def insert_products_to_db(products, db_config):
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insertar cada producto en la base de datos
        for product in products:
            cursor.execute("""
                INSERT INTO productos (codigo, name, brand, family, stock, regular_price, image, sync)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                product["codigo"],
                product["name"],
                product["brand"],
                product["family"],
                product["stock"],
                product["regular_price"],
                product["image"],
                product["sync"]
            ))

        # Confirmar la transacción
        connection.commit()
        print("Productos insertados correctamente en la base de datos.")

    except mysql.connector.Error as err:
        print(f"Error al insertar productos en la base de datos: {err}")
    finally:
        # Cerrar la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'divia_db'
}

# URL del JSON
url = "https://serverupagency.com/balitool/apisDivia/diviaApis/prov/dpSicsa/jsonDb.php?userId=3"

# Obtener productos del JSON
products = get_products_from_json(url)

# Insertar productos en la base de datos
if products:
    insert_products_to_db(products, db_config)