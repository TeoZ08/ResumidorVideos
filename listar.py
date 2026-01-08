import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("🔍 Listando modelos disponíveis para sua chave (SDK google-genai)...")

try:
    # No novo SDK, list() retorna um iterador de objetos Model
    for model in client.models.list():
        # Vamos imprimir o nome diretamente. Geralmente vem como "models/nome"
        print(f" - {model.name}")
        
except Exception as e:
    print(f"❌ Erro crítico ao listar: {e}")