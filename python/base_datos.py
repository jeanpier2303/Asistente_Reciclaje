import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), "env/.env"))

def conectar():
    """Crea la conexión a la base de datos."""
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None


def guardar_analisis(clasificacion, color, comando_serial, descripcion, modelo, confianza):
    """
    Inserta un registro en la tabla analisis y en colores_detectados.
    """
    conexion = conectar()
    if not conexion:
        print(" No se pudo establecer conexión con la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        # Insertar en analisis
        sql_analisis = """
            INSERT INTO analisis (clasificacion, comando_serial, modelo, confianza, descripcion)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_analisis, (clasificacion, comando_serial, modelo, confianza, descripcion))
        id_analisis = cursor.lastrowid

        # Insertar en colores_detectados
        sql_color = "INSERT INTO colores_detectados (id_analisis, color) VALUES (%s, %s)"
        cursor.execute(sql_color, (id_analisis, color))

        conexion.commit()
        print(f" Registro guardado correctamente (ID análisis: {id_analisis})")

    except Error as e:
        print(f" Error al guardar los datos: {e}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()
