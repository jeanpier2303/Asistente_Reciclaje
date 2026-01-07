import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 🔍 DIAGNÓSTICO
print("=" * 50)
print("🔍 DIAGNÓSTICO DE API KEY")
print("=" * 50)
print(f"📁 Directorio actual: {os.getcwd()}")
print(f"📄 Archivo .env existe: {os.path.exists('.env')}")

if api_key:
    print(f"✅ API Key encontrada: {api_key[:15]}...{api_key[-4:]}")
    print(f"📏 Longitud de la clave: {len(api_key)} caracteres")
else:
    print("❌ NO se encontró GEMINI_API_KEY en .env")
    print("\n⚠️  Verifica que tu archivo .env contenga:")
    print("   GEMINI_API_KEY=tu_clave_aquí")
    exit()

print("=" * 50)

# Configurar y probar
try:
    genai.configure(api_key=api_key)
    print("🔧 Configurando modelo gemini-1.5-flash...")
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Di solo 'funciona' si puedes leerme")
    
    print("✅ ¡CONEXIÓN EXITOSA!")
    print(f"📨 Respuesta del modelo: {response.text}")
    
except Exception as e:
    print("❌ ERROR AL CONECTAR:")
    print(f"   {e}")
    print("\n💡 Posibles causas:")
    print("   1. API Key expirada o inválida")
    print("   2. Cuota excedida (límite gratuito agotado)")
    print("   3. API Key no habilitada para Gemini")
    print("\n🔗 Genera una nueva clave en:")
    print("   https://aistudio.google.com/app/apikey")