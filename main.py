from audio_transcricao import obter_transcricao
from apigemini import resumir_transcricao_gemini

def main():
    # 1. Pede a URL
    link = input("URL do vídeo: ").strip()
    
    if not link:
        print("URL inválida.")
        return

    # 2. Obtém a transcrição (agora via API, sem download de vídeo)
    print("\n🔍 Buscando legendas...")
    texto_legenda = obter_transcricao(link)

    if texto_legenda:
        print("✅ Legenda encontrada! Tamanho do texto:", len(texto_legenda), "caracteres.")
        
        # 3. Manda pro Gemini
        print("🧠 Gerando resumo com IA...")
        resumo = resumir_transcricao_gemini(texto_legenda)
        
        print("\n" + "="*40)
        print("RESUMO DO VÍDEO")
        print("="*40 + "\n")
        print(resumo)
    else:
        print("\n❌ Não foi possível obter o resumo deste vídeo.")

if __name__ == "__main__":
    main()