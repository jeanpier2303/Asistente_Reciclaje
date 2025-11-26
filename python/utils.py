""" import os
from gemini_api import obtener_comando_desde_imagen
from base_datos import guardar_analisis
from serial_arduino import conectar_serial, enviar_comando

# FLUJO PRINCIPAL
if __name__ == "__main__":
    print("🔹 Iniciando Asistente Inteligente de Reciclaje 🔹")

    # Conectar al Arduino
    arduino = conectar_serial("COM5")

    # Analizar imagen local
    ruta_imagen = "./IMG/fran.jpg"
    if not os.path.exists(ruta_imagen):
        print(f" No se encontró la imagen '{ruta_imagen}'. Colócala en la carpeta del proyecto.")
        exit()

    print(f" Analizando imagen: {ruta_imagen}")
    resultado = obtener_comando_desde_imagen(ruta_imagen)

    if resultado and "clasificacion" in resultado:
        print(" Resultado obtenido del modelo:")
        print(resultado)

        # Guardar en la base de datos
        guardar_analisis(
            clasificacion=resultado.get("clasificacion"),
            color=resultado.get("color"),
            comando_serial=resultado.get("comando_serial"),
            descripcion=resultado.get("descripcion"),
            modelo="Gemini",
            confianza=95.0
        )

        # Enviar comando al Arduino
        comando = resultado.get("comando_serial")
        enviar_comando(arduino, comando)

    else:
        print(" No se obtuvo un resultado válido del modelo.")
 """