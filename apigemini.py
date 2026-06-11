import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

MAX_CARACTERES = 60_000
TIMEOUT_MS = 90_000
MAX_RETRIES = 3


def resumir_transcricao(texto: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "❌ ERRO: GEMINI_API_KEY não encontrada no .env"

    model_name = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

    if len(texto) > MAX_CARACTERES:
        print(
            f"⚠️ Transcrição muito extensa: {len(texto)} caracteres. "
            f"Limitando para {MAX_CARACTERES}."
        )
        texto = texto[:MAX_CARACTERES]

    prompt = f"""
Você é um assistente especialista em resumos de conteúdos educacionais.

Produza um resumo estruturado em português contendo:

1. Tema central
2. Principais ideias
3. Conceitos importantes
4. Exemplos mencionados
5. Conclusão
6. Tarefas ou ações sugeridas, quando existirem

Seja objetivo, mas preserve informações relevantes.

TRANSCRIÇÃO:

{texto}
"""

    for tentativa in range(1, MAX_RETRIES + 1):
        try:
            print(
                f"🤖 Enviando para o Gemini ({model_name}) — "
                f"tentativa {tentativa}/{MAX_RETRIES}..."
            )

            inicio = time.time()

            with genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(timeout=TIMEOUT_MS),
            ) as client:
                resposta = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=2_500,
                    ),
                )

            tempo = time.time() - inicio
            print(f"✅ Resposta recebida em {tempo:.1f} segundos.")

            if not resposta.text:
                return "❌ Erro ao gerar resumo: resposta vazia do Gemini."

            return resposta.text

        except Exception as erro:
            erro_str = str(erro)

            print(
                f"⚠️ Falha na tentativa {tentativa}: "
                f"{type(erro).__name__}: {erro}"
            )

            if tentativa >= MAX_RETRIES:
                return f"❌ Erro ao gerar resumo: {erro}"

            if "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
                espera = 30 * tentativa
            else:
                espera = 5 * tentativa

            print(f"⏳ Nova tentativa em {espera} segundos...")
            time.sleep(espera)

    return "❌ Falha: não foi possível gerar o resumo."
