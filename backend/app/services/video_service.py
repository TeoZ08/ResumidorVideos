import re


def extrair_id_video(url: str) -> str | None:
    """Extrai o ID único do vídeo do YouTube."""
    if not url:
        return None

    padroes = [
        r"(?:youtube\.com\/watch\?v=)([0-9A-Za-z_-]{11})",
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
        r"(?:youtube\.com\/shorts\/)([0-9A-Za-z_-]{11})",
        r"(?:youtube\.com\/embed\/)([0-9A-Za-z_-]{11})",
    ]

    for padrao in padroes:
        match = re.search(padrao, url)
        if match:
            return match.group(1)

    return None


def montar_titulo_padrao(video_id: str) -> str:
    return f"Video {video_id}"
