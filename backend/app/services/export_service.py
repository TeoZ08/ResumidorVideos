def montar_markdown_contexto(resumo: dict) -> str:
    """Monta um Markdown estável para reaproveitar o resumo em bases de contexto."""
    video_id = resumo["video_id"]
    titulo = resumo["title"]
    url = resumo.get("url") or f"https://www.youtube.com/watch?v={video_id}"
    data = resumo.get("created_at") or "Não informado"

    return "\n".join(
        [
            "# Resumo de vídeo",
            "",
            "## Fonte",
            f"URL: {url}",
            f"Título: {titulo}",
            f"Data de processamento: {data}",
            "",
            "## Resumo",
            "",
            resumo["summary"],
            "",
            "## Pontos principais",
            "",
            "- A extrair a partir do resumo acima.",
            "",
            "## Conceitos importantes",
            "",
            "- A confirmar conforme o conteúdo do vídeo.",
            "",
            "## Tarefas/ações sugeridas",
            "",
            "- A confirmar conforme o conteúdo do vídeo.",
            "",
            "## Possível destino no teo-contexto",
            "",
            "- A confirmar conforme tema, projeto ou disciplina relacionada.",
            "",
            "## Observações",
            "",
            "- Exportado pelo ResumidorVideos para uso como base de contexto.",
        ]
    )
