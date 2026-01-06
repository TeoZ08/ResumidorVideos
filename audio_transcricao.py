from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

def extrair_id_video(url):
    """Extrai o ID de 11 caracteres de URLs comuns do YouTube."""
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

    try:
        # Tenta buscar legendas em Português, depois Inglês (e variantes)
        transcript_list = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['pt', 'pt-BR', 'en', 'en-US']
        )
        
        # O formatter já junta o texto e remove os timestamps automaticamente
        formatter = TextFormatter()
        texto_limpo = formatter.format_transcript(transcript_list)
        
        return texto_limpo

    except Exception as e:
        # A lib lança exceções claras se não houver legenda ou se for bloqueado
        print(f"Erro ao obter transcrição: {e}")
        return None