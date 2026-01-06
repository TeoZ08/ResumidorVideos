from audio_transcricao import obter_transcricao
from apigemini import resumir_transcricao_gemini

# 1. Pede a URL
link = input("URL do vídeo: ")

# 2. Chama a função que já retorna o texto pronto da memória
print("Baixando transcrição...")
texto_legenda = obter_transcricao(link)

if texto_legenda:
    # 3. Manda pro Gemini
    print("Gerando resumo...")
    resumo = resumir_transcricao_gemini(texto_legenda)
    
    print("\nRESUMO:\n")
    print(resumo)
else:
    print("Não foi possível gerar o resumo.")