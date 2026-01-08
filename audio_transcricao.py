from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

def extrair_id_video(url):
    """
    Extrai o ID do vídeo a partir de URLs comuns do YouTube.
    Suporta: youtube.com/watch?v=ID, youtu.be/ID, shorts/ID
    """
    padroes = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:shorts\/)([0-9A-Za-z_-]{11})'
    ]
    
    for padrao in padroes:
        match = re.search(padrao, url)
        if match:
            return match.group(1)
    return None

def obter_transcricao(url_video):
    video_id = extrair_id_video(url_video)
    
    if not video_id:
        print("Erro: Não foi possível extrair o ID do vídeo. Verifique o link.")
        return None

    print(f"Processando vídeo ID: {video_id}...")

    try:
        # Tenta buscar legendas em Português ou Inglês (prioridade para PT)
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['pt', 'pt-BR', 'en', 'en-US']
        )
        
        # Formata o JSON retornado para texto corrido
        formatter = TextFormatter()
        texto_formatado = formatter.format_transcript(transcript)
        
        return texto_formatado

    except Exception as e:
        # Erros comuns: Vídeo sem legenda ou restrição de criador
        print(f"Erro ao obter transcrição: {e}")
        return None