import yt_dlp
import os

# Transformamos em função para receber a URL de fora
def baixar_legenda(url_do_video):
    # Definimos um nome fixo para não termos erro de arquivo não encontrado
    nome_arquivo = "legenda_temporaria"

    # Removemos arquivos antigos para garantir
    if os.path.exists(f"{nome_arquivo}.pt.srt"):
        os.remove(f"{nome_arquivo}.pt.srt")

    ydl_opts = {
        'skip_download': True,      # Não baixa o vídeo nem áudio, SÓ a legenda (fica mais rápido)
        'writesub': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['pt', 'en'],
        'subtitlesformat': 'srt',
        'outtmpl': nome_arquivo,    # Força o nome ser "legenda_temporaria"
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url_do_video, download=True)
            
            # Retorna o nome do arquivo que foi criado
            if os.path.exists(f"{nome_arquivo}.pt.srt"):
                return f"{nome_arquivo}.pt.srt"
            elif os.path.exists(f"{nome_arquivo}.en.srt"):
                return f"{nome_arquivo}.en.srt"
            else:
                return None
    except Exception as e:
        print(f"Erro: {e}")
        return None