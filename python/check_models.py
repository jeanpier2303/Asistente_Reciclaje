import cv2
import time
import os


def probar_camara(carpeta_salida="./TEST_IMG"):
    # Crear carpeta si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("❌ Error: No se pudo acceder a la cámara.")
        return

    print("✅ Cámara iniciada. Probando detección de movimiento...")

    # Tomar primer frame como referencia
    ret, frame_anterior = cam.read()
    time.sleep(0.3)

    while True:
        # Capturar frame actual
        ret, frame_actual = cam.read()
        if not ret:
            print("⚠ Error leyendo frame, continuando…")
            continue

        # Detectar movimiento
        diff = cv2.absdiff(frame_anterior, frame_actual)
        gris = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gris, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
        movimiento = cv2.countNonZero(thresh)

        print(f"Movimiento detectado: {movimiento}")

        cv2.imshow("TEST - Camara", frame_actual)

        # Si hay mucho movimiento → capturar imagen
        if movimiento > 50000:
            nombre = f"{carpeta_salida}/test_{int(time.time())}.jpg"
            cv2.imwrite(nombre, frame_actual)
            print(f"📸 Imagen guardada: {nombre}")
            time.sleep(2)

        # Actualizar frame anterior
        frame_anterior = frame_actual.copy()

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    probar_camara()
