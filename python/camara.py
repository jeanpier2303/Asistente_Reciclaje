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

        # Capturar un nuevo frame
        ret, frame_actual = cam.read()
        if not ret:
            continue  # si algo falla, saltar este frame

        # se supone que esto Calcular diferencia entre el frame anterior y el actual
        diff = cv2.absdiff(frame_anterior, frame_actual)

        #esto Convertir a escala de grises no se que hace como tal lo recomendo la IA
        gris = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        #se aplica un desenfoque para eliminar ruido y suavizar la imagen
        blur = cv2.GaussianBlur(gris, (5, 5), 0)

        # Binarizar la imagen: áreas con cambios → blanco (255) "Lo recomendo la IA"
        _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)

        # esto Cuenta cuántos píxeles blancos hay → representa cantidad de movimiento "lo recomendo la IA"
        movimiento = cv2.countNonZero(thresh)

        #  video en tiempo real
        cv2.imshow("Asistente de Reciclaje - Camara", frame_actual)

        # 
        if movimiento > 50000:
            print("Movimiento detectado. Capturando imagen...")

            # Crear nombre único para la imagen
            nombre = f"{carpeta_salida}/captura_{int(time.time())}.jpg"

            # Guardar la imagen
            cv2.imwrite(nombre, frame_actual)
            print(f"Imagen capturada: {nombre}")

            # envia la imagen para ser analizada
            procesar_imagen(nombre, arduino)

            # una Pausa para evitar capturas excesivas
            time.sleep(3)

        # Actualizar frame_anterior para el siguiente ciclo
        frame_anterior = frame_actual.copy()

        # Permite salir con rsa tecla
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
