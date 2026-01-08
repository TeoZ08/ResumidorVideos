import re
from youtube_transcript_api import YouTubeTranscriptApi


def extrair_id_video(url: str) -> str | None:
    padroes = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
        r"(?:shorts\/)([0-9A-Za-z_-]{11})"
    ]

    for padrao in padroes:
        match = re.search(padrao, url)
        if match:
            return match.group(1)

    return None


def obter_transcricao(url_video: str) -> str | None:
    video_id = extrair_id_video(url_video)

    if not video_id:
        print("❌ Não foi possível extrair o ID do vídeo.")
        return None

    print(f"Processando vídeo ID: {video_id}...")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            transcript = transcript_list.find_manually_created_transcript(['pt', 'pt-BR'])
        except:
            try:
                transcript = transcript_list.find_manually_created_transcript(['en', 'en-US'])
            except:
                transcript = transcript_list.find_generated_transcript(['pt', 'pt-BR', 'en'])

        dados = transcript.fetch()
        texto = " ".join(item["text"] for item in dados)

        return texto

    except Exception as e:
        print(f"Erro ao obter transcrição: {e}")
        return None
