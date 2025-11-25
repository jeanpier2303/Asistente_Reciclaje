import serial
import time

# CONFIGURACIÓN DEL PUERTO SERIAL
def conectar_serial(puerto="COM5", baudrate=9600, timeout=2):
    """
    Intenta conectar con el Arduino.
    """
    try:
        arduino = serial.Serial(port=puerto, baudrate=baudrate, timeout=timeout)
        time.sleep(2)  # Esperar a que Arduino se reinicie
        print(f"🔌 Conectado exitosamente al Arduino en {puerto}")
        return arduino
    except Exception as e:
        print(f" Error al conectar con Arduino: {e}")
        return None


# FUNCIÓN PARA ENVIAR COMANDO
def enviar_comando(arduino, comando):
    """
    Envía una letra ('B', 'V', 'N', 'R') al Arduino.
    """
    if arduino and arduino.is_open:
        try:
            arduino.write(comando.encode())  # Enviar carácter
            print(f" Comando '{comando}' enviado correctamente.")
        except Exception as e:
            print(f"Error al enviar el comando: {e}")
    else:
        print(" No hay conexión activa con el Arduino.")
