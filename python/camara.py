import cv2
import time
import os
from gemini_api import obtener_comando_desde_imagen
from serial_arduino import enviar_comando
from base_datos import guardar_analisis


def iniciar_camara(arduino, carpeta_salida="./IMG"):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return

    print("Camara iniciada. Esperando objeto...")

    ret, frame_anterior = cam.read()
    time.sleep(0.5)

    while True:
        ret, frame_actual = cam.read()
        if not ret:
            continue

        diff = cv2.absdiff(frame_anterior, frame_actual)
        gris = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gris, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
        movimiento = cv2.countNonZero(thresh)

        cv2.imshow("Asistente de Reciclaje - Camara", frame_actual)

        if movimiento > 50000:
            print("Movimiento detectado. Capturando imagen...")
            nombre = f"{carpeta_salida}/captura_{int(time.time())}.jpg"
            cv2.imwrite(nombre, frame_actual)

            print(f"Imagen capturada: {nombre}")
            procesar_imagen(nombre, arduino)

            time.sleep(3)

        frame_anterior = frame_actual.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def procesar_imagen(ruta_imagen, arduino):
    print(f"Analizando imagen capturada: {ruta_imagen}")

    resultado = obtener_comando_desde_imagen(ruta_imagen)

    if not resultado or "comando_serial" not in resultado:
        print("El modelo no devolvió un resultado válido.")
        return

    print("Resultado del modelo:")
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
