from base_datos import conectar_bd

def guardar_analisis(clasificacion, comando_serial, modelo, confianza, descripcion, colores):
    """Guarda un análisis con sus colores detectados."""
    conexion = conectar_bd()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()

        # Insertar en la tabla analisis
        sql_analisis = """
        INSERT INTO analisis (clasificacion, comando_serial, modelo, confianza, descripcion)
        VALUES (%s, %s, %s, %s, %s)
        """
        datos_analisis = (clasificacion, comando_serial, modelo, confianza, descripcion)
        cursor.execute(sql_analisis, datos_analisis)
        id_analisis = cursor.lastrowid

        # Insertar colores relacionados
        sql_color = "INSERT INTO colores_detectados (id_analisis, color) VALUES (%s, %s)"
        for color in colores:
            cursor.execute(sql_color, (id_analisis, color))

        conexion.commit()
        print(f"💾 Análisis guardado correctamente con ID {id_analisis}.")
        return True
    except Exception as e:
        print(f"⚠️ Error al guardar datos: {e}")
        conexion.rollback()
        return False
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
