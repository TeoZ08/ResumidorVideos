import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def resumir_transcricao_gemini(texto):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    Você é um assistente especialista em resumos.
    Leia a transcrição abaixo e forneça um resumo conciso em tópicos (bullet points) 
    destacando os pontos principais.
    
    TRANSCRIÇÃO:
    {texto}
    """
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erro ao gerar resumo: {e}"