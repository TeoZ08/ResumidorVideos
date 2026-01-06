from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
import os # Importante para verificar se o arquivo existe

def extrair_id_video(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def obter_transcricao(url_video):
    video_id = extrair_id_video(url_video)
    if not video_id:
        print("Erro: ID do vídeo não encontrado na URL.")
        return None

    # Verifica se o arquivo de cookies existe na pasta
    arquivo_cookies = 'cookies.txt'
    if not os.path.exists(arquivo_cookies):
        # Se não tiver cookies, tenta sem (mas avisa)
        print("Aviso: 'cookies.txt' não encontrado. Tentando sem autenticação...")
        arquivo_cookies = None

    try:
        # Passamos o parâmetro cookies (se ele existir)
        transcript_list = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['pt', 'pt-BR', 'en', 'en-US'],
            cookies=arquivo_cookies
        )
        
        formatter = TextFormatter()
        texto_limpo = formatter.format_transcript(transcript_list)
        return texto_limpo

    except Exception as e:
        print(f"Erro ao obter transcrição: {e}")
        return None