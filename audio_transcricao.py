import yt_dlp
import os
import traceback # Importante para ver o erro real

# Transformamos em função para receber a URL de fora
def baixar_legenda(url_do_video):
    # Definimos um nome fixo para não termos erro de arquivo não encontrado
    nome_arquivo = "legenda_temporaria"


    # Remove arquivos antigos
    if os.path.exists(f"{nome_arquivo}.pt.srt"):
        os.remove(f"{nome_arquivo}.pt.srt")
    if os.path.exists(f"{nome_arquivo}.en.srt"):
        os.remove(f"{nome_arquivo}.en.srt")

    ydl_opts = {
        'skip_download': True,      # Não baixa o vídeo nem áudio, SÓ a legenda (fica mais rápido)
        'writesub': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['pt', 'en'],
        'subtitlesformat': 'srt',
        'outtmpl': nome_arquivo,    # Força o nome ser "legenda_temporaria"
        'quiet': True,
        'verbose': True,
        # --- ESTRATÉGIA ANTI-BLOQUEIO NATIVA ---
        # 1. Força IPv4: O Google costuma bloquear faixas de IPv6 (erro 429), mas confia mais no IPv4.
        'force_ipv4': True,
        
        # 2. Cabeçalho manual: Diz ao YouTube que somos um navegador Chrome comum.
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

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
    except Exception:
        # Imprime o erro completo na tela
        traceback.print_exc()
        return None