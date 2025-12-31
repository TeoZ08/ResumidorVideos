import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

def resumir_transcricao_gemini(texto):
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Você é um assistente especialista em resumos.
    Leia a transcrição abaixo e forneça um resumo conciso em tópicos (bullet points) 
    destacando os pontos principais.
    
    TRANSCRIÇÃO:
    {texto}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar resumo: {e}"