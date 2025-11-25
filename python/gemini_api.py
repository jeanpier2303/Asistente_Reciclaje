import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from base_datos import guardar_analisis


# CARGAR CLAVE DESDE .ENV
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(" No se encontró la clave GEMINI_API_KEY en el archivo .env")

# Configurar el cliente
genai.configure(api_key=api_key)

# FUNCIÓN: ENVIAR IMAGEN Y OBTENER JSON
def obtener_comando_desde_imagen(ruta_imagen: str) -> dict:
    """
    Envía una imagen al modelo Gemini gratuito y obtiene un JSON con la instrucción.
    """
    try:
        # Abrir imagen correctamente con PIL (no como _io.BufferedReader)
        imagen = Image.open(ruta_imagen)

        prompt = ( """
        Eres un asistente inteligente de reciclaje. Analiza cuidadosamente la imagen que te envío y determina de qué tipo de residuo se trata.

        Tu respuesta **debe estar en formato JSON válido** (sin texto adicional, sin explicaciones, sin etiquetas Markdown, ni comentarios).

        La clasificación de residuos debe basarse en el siguiente criterio:

        - **Blanco (Aprovechable):** plástico, papel, cartón, vidrio, metal, tetra pak, botellas PET, latas, etc.
        - **Verde (Orgánico):** restos de comida, cáscaras de frutas o verduras, residuos biodegradables.
        - **Negro (No Aprovechable):** residuos sanitarios, servilletas sucias, papel higiénico, colillas, desechos contaminados, etc.

        Si no puedes identificar claramente el residuo, considera la clasificación como una **falla (Rojo)**.

        La salida JSON debe tener exactamente los siguientes campos:

        {
        "clasificacion": "EXITO" o "FALLA",
        "color": "BLANCO" o "VERDE" o "NEGRO" o "ROJO",
        "comando_serial": "B" o "V" o "N" o "R",
        "descripcion": "Explicación breve (por qué se clasificó así)"
        }

        Donde:
        - `clasificacion` es "EXITO" si la IA pudo identificar con claridad el tipo de residuo, o "FALLA" si no.
        - `color` corresponde al contenedor según el tipo.
        - `comando_serial` es la letra que debe enviarse al Arduino:
        - 'B' = contenedor blanco (aprovechable)
        - 'V' = contenedor verde (orgánico)
        - 'N' = contenedor negro (no aprovechable)
        - 'R' = falla (no se pudo identificar)
        - `descripcion` explica brevemente la decisión.

        Ejemplo de respuesta esperada:
        {
        "clasificacion": "EXITO",
        "color": "VERDE",
        "comando_serial": "V",
        "descripcion": "Se observa una cáscara de plátano, un residuo orgánico."
        }
        """
        )

        #  Modelo gratuito y actualizado
        model = genai.GenerativeModel("gemini-flash-latest")

        # Enviar la solicitud
        response = model.generate_content([prompt, imagen])
        texto = response.text.strip()
        print(f" Respuesta cruda del modelo:\n{texto}\n")

        # Intentar extraer JSON de la respuesta
        inicio = texto.find("{")
        fin = texto.rfind("}") + 1
        if inicio != -1 and fin != -1:
            datos = json.loads(texto[inicio:fin])
            return datos
        else:
            return {"error": "No se encontró JSON válido en la respuesta"}

    except Exception as e:
        print(f" Error procesando la imagen: {e}")
        return {}

# PRUEBA LOCAL 
if __name__ == "__main__":
    resultado = obtener_comando_desde_imagen("banana.jpg")
    print("Resultado final:", resultado)
