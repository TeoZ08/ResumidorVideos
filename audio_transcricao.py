from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

def extrair_id_video(url):
    """
    Extrai o ID do vídeo a partir de URLs comuns do YouTube.
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
        # --- CORREÇÃO PARA VERSÃO 1.2.3+ ---
        # 1. Instancia a classe (agora obrigatório)
        ytt = YouTubeTranscriptApi()
        
        # 2. Lista todas as legendas disponíveis para o vídeo
        transcript_list = ytt.list(video_id)
        
        # 3. Encontra a melhor legenda (Prioridade: PT > PT-BR > EN > EN-US)
        transcript = transcript_list.find_transcript(['pt', 'pt-BR', 'en', 'en-US'])
        
        # 4. Baixa o conteúdo (retorna objeto FetchedTranscript)
        fetched_obj = transcript.fetch()
        
        # 5. Converte para dados brutos (lista de dicts) que o formatador entende
        if hasattr(fetched_obj, 'to_raw_data'):
            transcript_data = fetched_obj.to_raw_data()
        else:
            transcript_data = fetched_obj
            
        # 6. Formata para texto corrido
        formatter = TextFormatter()
        return formatter.format_transcript(transcript_data)

    except Exception as e:
        # Tenta pegar erros específicos como "NoTranscriptFound"
        print(f"Erro ao obter transcrição: {e}")
        return None