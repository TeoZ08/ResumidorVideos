import argparse
import sys
import re
from audio_transcricao import obter_transcricao
from apigemini import resumir_transcricao
import banco_dados # Importando nosso novo módulo

def extrair_id_video(url: str) -> str:
    """Extrai o ID único do vídeo do YouTube (ex: dqw4w9wgXcQ)"""
    padroes = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
        r"(?:shorts\/)([0-9A-Za-z_-]{11})"
    ]
    for padrao in padroes:
        match = re.search(padrao, url)
        if match:
            return match.group(1)
    return "desconhecido"

def main():
    # 0. Garante que o banco existe
    banco_dados.inicializar_banco()

    parser = argparse.ArgumentParser(description="Resumidor de Vídeos do YouTube com IA")
    parser.add_argument("url", help="URL do vídeo do YouTube")
    parser.add_argument("--salvar", action="store_true", help="Salva o resumo em um arquivo .md")
    parser.add_argument("--forcar", action="store_true", help="Ignora o cache e força nova análise")
    
    args = parser.parse_args()
    video_id = extrair_id_video(args.url)

    print(f"🔍 Processando Vídeo ID: {video_id}")

    # 1. VERIFICAÇÃO DE CACHE (A mágica acontece aqui)
    resumo_existente = banco_dados.buscar_resumo(video_id)

    if resumo_existente and not args.forcar:
        print("⚡ Resumo encontrado no banco de dados! (Pulando transcrição e IA)")
        resumo = resumo_existente
    else:
        # Se não tem no banco, faz o fluxo normal
        if args.forcar:
            print("🔄 Forçando nova análise...")
        
        print("📥 Baixando legendas...")
        texto_transcricao = obter_transcricao(args.url)
        
        if not texto_transcricao:
            print("❌ Encerrando: Não foi possível obter a legenda.")
            sys.exit(1)

        print(f"✅ Legenda extraída. Enviando para IA...")
        
        resumo = resumir_transcricao(texto_transcricao)
        
        # Salva no banco para a próxima vez
        # (Titulo improvisado, se quiser pegar o titulo real precisaria de outra lib, mas o ID serve)
        titulo_fake = f"Video {video_id}" 
        banco_dados.salvar_resumo(video_id, titulo_fake, resumo)

    # 2. Exibição do Resultado
    if args.salvar:
        nome_arquivo = f"Resumo_{video_id}.md"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"# Resumo do Vídeo: {args.url}\n\n")
            f.write(resumo)
        print(f"\n💾 Arquivo criado: {nome_arquivo}")
    else:
        print("\n" + "="*40)
        print("RESUMO DO VÍDEO")
        print("="*40)
        print(resumo)

if __name__ == "__main__":
    main()