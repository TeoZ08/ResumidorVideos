from audio_transcricao import baixar_legenda
from apigemini import resumir_transcricao_gemini

# 1. Pede a URL
link = input("URL do vídeo: ")

# 2. Chama a função do seu arquivo de download
print("Baixando legenda...")
arquivo = baixar_legenda(link)

if arquivo:
    # 3. Lê o arquivo de texto (simples, sem regex por enquanto)
    with open(arquivo, 'r', encoding='utf-8') as f:
        texto_da_legenda = f.read()

    # 4. Manda pro Gemini (usando seu arquivo apigemini.py)
    print("Gerando resumo...")
    resumo = resumir_transcricao_gemini(texto_da_legenda)
    
    print("\nRESUMO:\n")
    print(resumo)
else:
    print("Não consegui baixar a legenda.")