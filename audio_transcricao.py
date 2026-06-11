import html
import xml.etree.ElementTree as ET

from pytubefix import YouTube
from youtube_transcript_api import (
    NoTranscriptFound,
    YouTubeTranscriptApi,
    YouTubeTranscriptApiException,
)

from backend.app.services.video_service import extrair_id_video


IDIOMAS_PREFERIDOS = ["pt-BR", "pt", "en"]


def _limpar_texto(texto: str) -> str:
    return html.unescape(texto.replace("\n", " ").strip())


def _obter_com_transcript_api(video_id: str) -> str | None:
    api = YouTubeTranscriptApi()
    transcricoes = api.list(video_id)

    try:
        transcricao = transcricoes.find_transcript(IDIOMAS_PREFERIDOS)
    except NoTranscriptFound:
        transcricao = next(iter(transcricoes), None)

    if transcricao is None:
        return None

    dados = transcricao.fetch()
    partes = [
        _limpar_texto(item.text)
        for item in dados
        if item.text and item.text.strip()
    ]

    texto = " ".join(partes).strip()

    if texto:
        tipo = "automática" if transcricao.is_generated else "manual"
        print(
            f"✅ Legenda {tipo} encontrada: "
            f"{transcricao.language_code}"
        )

    return texto or None


def _obter_com_pytubefix(url_video: str) -> str | None:
    yt = YouTube(url_video)
    captions = yt.captions

    prioridades = [
        "pt",
        "a.pt",
        "pt-BR",
        "a.pt-BR",
        "en",
        "a.en",
    ]

    legenda_escolhida = None

    for idioma in prioridades:
        if idioma in captions:
            legenda_escolhida = captions[idioma]
            print(f"✅ Legenda encontrada pelo pytubefix: {idioma}")
            break

    if legenda_escolhida is None and len(captions) > 0:
        legenda_escolhida = list(captions.values())[0]
        print(
            "⚠️ Usando legenda alternativa do pytubefix: "
            f"{legenda_escolhida.code}"
        )

    if legenda_escolhida is None:
        return None

    root = ET.fromstring(legenda_escolhida.xml_captions)
    partes = []

    for elemento in root:
        texto = "".join(elemento.itertext())

        if texto.strip():
            partes.append(_limpar_texto(texto))

    return " ".join(partes).strip() or None


def obter_transcricao(url_video: str) -> str | None:
    print(f"Processando: {url_video}...")

    video_id = extrair_id_video(url_video)

    if not video_id:
        print("❌ URL do YouTube inválida.")
        return None

    try:
        texto = _obter_com_transcript_api(video_id)

        if texto:
            return texto
    except YouTubeTranscriptApiException as erro:
        print(f"⚠️ Transcript API não conseguiu obter a legenda: {erro}")
    except Exception as erro:
        print(f"⚠️ Erro inesperado na Transcript API: {erro}")

    print("⚠️ Tentando método alternativo com pytubefix...")

    try:
        texto = _obter_com_pytubefix(url_video)

        if texto:
            return texto
    except Exception as erro:
        print(f"⚠️ O pytubefix também falhou: {erro}")

    print("❌ Nenhuma legenda pôde ser obtida.")
    return None
