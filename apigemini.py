import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def resumir_transcricao(texto: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "❌ ERRO: GEMINI_API_KEY não encontrada no .env"

    client = genai.Client(api_key=api_key)

    MAX_CARACTERES = 12000
    if len(texto) > MAX_CARACTERES:
        texto = texto[:MAX_CARACTERES]

    prompt = f"""
Você é um assistente especialista em resumos.
Gere um resumo em tópicos (bullet points),
destacando apenas as ideias principais do texto abaixo.

TEXTO:
{texto}
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"❌ Erro ao gerar resumo: {e}"
