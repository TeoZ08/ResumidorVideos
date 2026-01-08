from audio_transcricao import obter_transcricao
from apigemini import resumir_transcricao


def main():
    url = input("URL do vídeo: ").strip()

    if not url:
        print("❌ URL inválida.")
        return

    print("\n🔍 Buscando legendas...")
    transcricao = obter_transcricao(url)

    if not transcricao:
        print("\n❌ Não foi possível obter a transcrição.")
        return

    print(f"✅ Legenda encontrada! ({len(transcricao)} caracteres)")
    print("🧠 Gerando resumo com IA...\n")

    resumo = resumir_transcricao(transcricao)

    print("=" * 40)
    print("RESUMO DO VÍDEO")
    print("=" * 40)
    print(resumo)


if __name__ == "__main__":
    main()
