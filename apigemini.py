import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

def resumir_transcricao(texto: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "❌ ERRO: GEMINI_API_KEY não encontrada no .env"

    client = genai.Client(api_key=api_key)

    # O Gemini Flash 1.5 suporta ~1 milhão de tokens.
    # 100k caracteres é seguro e dá folga.
    MAX_CARACTERES = 100000 
    if len(texto) > MAX_CARACTERES:
        texto = texto[:MAX_CARACTERES]

    prompt = f"""
Você é um assistente especialista em resumos.
Gere um resumo em tópicos (bullet points),
destacando apenas as ideias principais do texto abaixo.

TEXTO:
{texto}
"""
    
    # MUDANÇA 1: Usar 'gemini-flash-latest' (Geralmente é o 1.5 Flash)
    # Ele tem limites gratuitos muito mais generosos que o 2.0 experimental.
    model_name = "gemini-flash-latest" 
    
    print(f"🤖 Enviando para o Gemini ({model_name})...")

    # MUDANÇA 2: Retry Logic (Tentar de novo se der erro 429)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text

        except Exception as e:
            erro_str = str(e)
            # Se for erro de cota (429), espera e tenta de novo
            if "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
                print(f"⏳ Cota atingida. Tentativa {attempt+1}/{max_retries}. Aguardando 30s...")
                time.sleep(30)
            else:
                # Se for outro erro (ex: chave inválida), retorna logo
                return f"❌ Erro ao gerar resumo: {e}"

    return "❌ Falha: O serviço está congestionado. Tente novamente mais tarde."