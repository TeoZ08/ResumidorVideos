import argparse
import sys

from backend.app.services.export_service import montar_markdown_contexto
from backend.app.services.summary_service import SummaryError, processar_video
from backend.app.services.video_service import extrair_id_video

def main():
    parser = argparse.ArgumentParser(description="Resumidor de Vídeos do YouTube com IA")
    parser.add_argument("url", help="URL do vídeo do YouTube")
    parser.add_argument("--salvar", action="store_true", help="Salva o resumo em um arquivo .md")
    parser.add_argument("--forcar", action="store_true", help="Ignora o cache e força nova análise")
    
    args = parser.parse_args()
    video_id = extrair_id_video(args.url)

    print(f"🔍 Processando Vídeo ID: {video_id}")

    try:
        if args.forcar:
            print("🔄 Forçando nova análise...")

        resultado = processar_video(args.url, force=args.forcar)
        resumo = resultado["summary"]

        if resultado["from_cache"]:
            print("⚡ Resumo encontrado no banco de dados! (Pulando transcrição e IA)")
        else:
            print("✅ Resumo gerado e salvo no banco de dados.")
    except SummaryError as erro:
        print(f"❌ {erro.message}")
        sys.exit(1)

    if args.salvar:
        nome_arquivo = f"Resumo_{resultado['video_id']}.md"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(montar_markdown_contexto(resultado))
        print(f"\n💾 Arquivo criado: {nome_arquivo}")
    else:
        print("\n" + "="*40)
        print("RESUMO DO VÍDEO")
        print("="*40)
        print(resumo)

if __name__ == "__main__":
    main()
