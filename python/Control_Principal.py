import os
from gemini_api import obtener_comando_desde_imagen
from base_datos import guardar_analisis
from serial_arduino import conectar_serial, enviar_comando
from camara import iniciar_camara


if __name__ == "__main__":
    print("Iniciando Asistente Inteligente de Reciclaje")

    arduino = conectar_serial("COM5")

    print("Selecciona modo:")
    print("1. Camara (automático)")
    print("2. Imagen manual (archivo)")

    opcion = input("Opción: ")

    if opcion == "1":
        iniciar_camara(arduino)

    elif opcion == "2":
        ruta_imagen = "./IMG/maria2.png"

        if not os.path.exists(ruta_imagen):
            print(f"No se encontró la imagen '{ruta_imagen}'.")
            exit()

        print(f"Analizando imagen: {ruta_imagen}")
        resultado = obtener_comando_desde_imagen(ruta_imagen)

        if resultado and "clasificacion" in resultado:
            print("Resultado obtenido del modelo:")
            print(resultado)

            guardar_analisis(
                clasificacion=resultado.get("clasificacion"),
                color=resultado.get("color"),
                comando_serial=resultado.get("comando_serial"),
                descripcion=resultado.get("descripcion"),
                modelo="Gemini",
                confianza=95.0
            )

            comando = resultado.get("comando_serial")
            enviar_comando(arduino, comando)

        else:
            print("No se obtuvo un resultado válido del modelo.")
