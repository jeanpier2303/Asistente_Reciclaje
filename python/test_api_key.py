import os
from google import genai
from google.genai.errors import APIError

def test_gemini_api_key():
    """
    Intenta inicializar el cliente y hacer una solicitud simple para
    verificar si la clave API es válida y está activa.
    """
    # --- 1. Obtener la clave ---
    # La clave se lee de la variable de entorno GEMINI_API_KEY
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ ERROR: La variable de entorno 'GEMINI_API_KEY' no está configurada.")
        print("👉 Solución: Ejecuta el siguiente comando en tu terminal ANTES de este script:")
        print('   $env:GEMINI_API_KEY="TU_NUEVA_CLAVE_AQUI" (en PowerShell)')
        return

    print("🔑 Clave API encontrada. Intentando conectarse a Gemini...")
    print(f"DEBUG: Clave leída (primeros 5 caracteres): {api_key[:5]}...")

    try:
        # --- 2. Inicializar el cliente ---
        # Si la clave es inválida, este paso o el siguiente fallará.
        client = genai.Client(api_key=api_key)

        # --- 3. Hacer una solicitud mínima (listar modelos) ---
        # Esto confirma que la clave es válida y está activa.
        models = client.models.list()
        
        # Opcional: Contar cuántos modelos ve
        num_models = sum(1 for _ in models) 

        # --- 4. Resultado Exitoso ---
        print("\n✅ ¡ÉXITO! La clave API es VÁLIDA y funciona correctamente.")
        print(f"⚙️ Conexión establecida. Modelos disponibles listados: {num_models}")

    except APIError as e:
        # --- 5. Resultado de Error de API ---
        print("\n❌ ERROR DE API: La clave no es válida o está restringida.")
        print(f"🛑 Mensaje del error: {e}")
        if "API key expired" in str(e) or "API_KEY_INVALID" in str(e):
            print("👉 Solución: Asegúrate de que la clave que usas es una NUEVA clave generada recientemente.")
        elif "PERMISSION_DENIED" in str(e):
             print("👉 Solución: El proyecto podría no tener habilitada la API Generative Language.")
        
    except Exception as e:
        # --- 6. Otros Errores ---
        print(f"\n⚠️ ERROR INESPERADO: Ocurrió un problema durante la ejecución: {e}")

if __name__ == "__main__":
    test_gemini_api_key()