import re
from audio_transcricao import baixar_legenda
from apigemini import resumir_transcricao_gemini

def limpar_srt(texto_srt):
    """Remove timestamps e numeração do formato SRT, deixando apenas o texto."""
    # Remove linhas de tempo (ex: 00:00:01,000 --> 00:00:04,000)
    texto = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', texto_srt)
    # Remove índices numéricos das legendas (ex: 1, 2, 3...) em linhas isoladas
    texto = re.sub(r'^\d+$', '', texto, flags=re.MULTILINE)
    # Remove linhas vazias excessivas
    texto = re.sub(r'\n+', '\n', texto).strip()
    return texto

# 1. Pede a URL
link = input("URL do vídeo: ")

# 2. Chama a função de download
print("Baixando legenda...")
arquivo = baixar_legenda(link)

if arquivo:
    # 3. Lê o arquivo
    with open(arquivo, 'r', encoding='utf-8') as f:
        texto_da_legenda = f.read()

    # LIMPEZA DO TEXTO ANTES DE ENVIAR PARA A IA
    texto_limpo = limpar_srt(texto_da_legenda)
    
    # 4. Manda pro Gemini
    print("Gerando resumo...")
    resumo = resumir_transcricao_gemini(texto_limpo)
    
    print("\nRESUMO:\n")
    print(resumo)
else:
    print("Não consegui baixar a legenda.")