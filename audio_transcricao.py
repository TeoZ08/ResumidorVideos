import yt_dlp
import os
import glob
import re

def limpar_srt(texto_srt):
    """Remove timestamps do SRT para retornar texto limpo."""
    # Remove linhas de tempo (ex: 00:00:01,000 --> 00:00:04,000)
    texto = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', texto_srt)
    # Remove índices numéricos isolados
    texto = re.sub(r'^\d+$', '', texto, flags=re.MULTILINE)
    # Remove tags de formatação como <font> ou <b>
    texto = re.sub(r'<[^>]+>', '', texto)
    # Remove linhas vazias
    texto = re.sub(r'\n+', '\n', texto).strip()
    return texto

def obter_transcricao(url_video):
    nome_base = "legenda_temp"
    
    # 1. Limpeza prévia de arquivos antigos
    for f in glob.glob(f"{nome_base}*"):
        try: os.remove(f)
        except: pass

    # 2. Verifica se o cookies.txt existe (Segurança)
    cookies_path = 'cookies.txt'
    if not os.path.exists(cookies_path):
        print("ERRO CRÍTICO: 'cookies.txt' não encontrado na pasta!")
        return None

    print(f"Usando cookies de: {os.path.abspath(cookies_path)}")

    # 3. Configuração Blindada do YT-DLP
    ydl_opts = {
        'skip_download': True,
        'writesub': True,
        'writeautomaticsub': True,     # Pega legenda gerada auto se não tiver manual
        'subtitleslangs': ['pt', 'en'], 
        'subtitlesformat': 'srt',
        'outtmpl': nome_base,          # Nome do arquivo de saída
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookies_path,    # <--- O SEGREDO DO SUCESSO
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url_video, download=True)
            
        # 4. Encontra o arquivo gerado (pode ser .pt.srt ou .en.srt)
        arquivos = glob.glob(f"{nome_base}*.srt")
        
        if arquivos:
            arquivo_legenda = arquivos[0]
            with open(arquivo_legenda, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Limpa e retorna o texto puro
            return limpar_srt(conteudo)
        else:
            print("Erro: O yt-dlp finalizou mas nenhuma legenda foi salva.")
            return None

    except Exception as e:
        print(f"Erro no download: {e}")
        return None