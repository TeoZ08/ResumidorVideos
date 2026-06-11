import argparse
import sys

from audio_transcricao import obter_transcricao
from backend.app.services.export_service import montar_markdown_contexto
from backend.app.services.summary_service import SummaryError, processar_video
from backend.app.services.video_service import extrair_id_video


def salvar_transcricao(url: str, video_id: str) -> None:
    """Obtém e salva somente a transcrição, sem chamar o Gemini."""
    transcricao = obter_transcricao(url)

    if not transcricao:
        print(
            "❌ Não foi possível obter legenda deste vídeo. "
            "Tente outro vídeo com legendas disponíveis."
        )
        sys.exit(1)

    nome_arquivo = f"Transcricao_{video_id}.txt"

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(transcricao.strip() + "\n")

    print(f"\n💾 Transcrição salva em: {nome_arquivo}")
    print("✅ O Gemini não foi chamado.")


def main():
    parser = argparse.ArgumentParser(
        description="Resumidor e extrator de transcrições de vídeos do YouTube"
    )
    parser.add_argument("url", help="URL do vídeo do YouTube")
    parser.add_argument(
        "--salvar",
        action="store_true",
        help="Salva o resumo em um arquivo .md",
    )
    parser.add_argument(
        "--forcar",
        action="store_true",
        help="Ignora o cache e força uma nova análise",
    )
    parser.add_argument(
        "--transcricao",
        "--somente-transcricao",
        dest="somente_transcricao",
        action="store_true",
        help=(
            "Salva somente a transcrição em .txt e não envia conteúdo ao Gemini"
        ),
    )

    args = parser.parse_args()
    video_id = extrair_id_video(args.url)

    if not video_id:
        print("❌ Informe uma URL válida do YouTube.")
        sys.exit(1)

    print(f"🔍 Processando Vídeo ID: {video_id}")

    if args.somente_transcricao:
        salvar_transcricao(args.url, video_id)
        return

    try:
        if args.forcar:
            print("🔄 Forçando nova análise...")

        resultado = processar_video(args.url, force=args.forcar)
        resumo = resultado["summary"]

        if resultado["from_cache"]:
            print(
                "⚡ Resumo encontrado no banco de dados! "
                "(Pulando transcrição e IA)"
            )
        else:
            print("✅ Resumo gerado e salvo no banco de dados.")
    except SummaryError as erro:
        print(f"❌ {erro.message}")
        sys.exit(1)

    if args.salvar:
        nome_arquivo = f"Resumo_{resultado['video_id']}.md"

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(montar_markdown_contexto(resultado))

        print(f"\n💾 Arquivo criado: {nome_arquivo}")
    else:
        print("\n" + "=" * 40)
        print("RESUMO DO VÍDEO")
        print("=" * 40)
        print(resumo)


if __name__ == "__main__":
    main()
