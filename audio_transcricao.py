import html
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
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
        "pt-BR",
        "a.pt-BR",
        "pt",
        "a.pt",
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


def _cookies_disponivel(cookies_file_path: str | None) -> bool:
    if not cookies_file_path:
        return False

    try:
        return Path(cookies_file_path).is_file() and Path(cookies_file_path).stat().st_size > 0
    except OSError:
        return False


def _selecionar_vtt(vtt_files: list[Path]) -> Path | None:
    if not vtt_files:
        return None

    def nome_normalizado(path: Path) -> str:
        return path.name.lower().replace("_", "-")

    prioridades = ["pt-br", "pt", "en"]
    for idioma in prioridades:
        for path in vtt_files:
            nome = nome_normalizado(path)
            if re.search(rf"[.-]{re.escape(idioma)}(?:-[^.]+)?\.vtt$", nome):
                print(f"✅ Legenda VTT encontrada com yt-dlp: {idioma}")
                return path

    escolhido = sorted(vtt_files)[0]
    print(f"⚠️ Usando legenda VTT alternativa do yt-dlp: {escolhido.name}")
    return escolhido


def _limpar_linha_vtt(linha: str) -> str:
    linha = re.sub(r"<\d{2}:\d{2}:\d{2}\.\d{3}>", "", linha)
    linha = re.sub(r"<[^>]+>", "", linha)
    linha = _limpar_texto(linha)
    linha = re.sub(r"\s+", " ", linha)
    return linha.strip()


def _vtt_para_texto(vtt_content: str) -> str | None:
    partes = []
    vistos = set()
    pulando_note = False

    for linha in vtt_content.splitlines():
        linha = linha.strip("\ufeff ")

        if not linha:
            pulando_note = False
            continue

        upper = linha.upper()
        if upper.startswith("WEBVTT") or upper.startswith("STYLE") or upper.startswith("REGION"):
            continue

        if upper.startswith("NOTE"):
            pulando_note = True
            continue
        if pulando_note:
            continue

        if "-->" in linha:
            continue
        if re.fullmatch(r"\d+", linha):
            continue
        if re.fullmatch(r"[0-9a-fA-F-]{8,}", linha):
            continue
        if re.search(r"\b(?:align|position|line|size|vertical):", linha):
            continue

        texto = _limpar_linha_vtt(linha)
        if not texto:
            continue

        chave = re.sub(r"\W+", " ", texto.lower()).strip()
        if chave in vistos:
            continue

        vistos.add(chave)
        partes.append(texto)

    texto_final = " ".join(partes)
    texto_final = re.sub(r"\s+", " ", texto_final).strip()
    return texto_final or None


def _obter_com_yt_dlp(url_video: str, cookies_file_path: str | None) -> str | None:
    print("⚠️ Tentando fallback com yt-dlp...")

    yt_dlp_bin = shutil.which("yt-dlp")
    if not yt_dlp_bin:
        print("❌ yt-dlp não encontrado. Instale a dependência no ambiente virtual.")
        return None

    with tempfile.TemporaryDirectory(prefix="resumidorvideos-yt-dlp-") as tmpdir:
        cmd = [
            yt_dlp_bin,
            "--skip-download",
            "--ignore-no-formats-error",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            "en,pt,pt-BR",
            "--sub-format",
            "vtt/srv3/ttml/best",
            "-o",
            str(Path(tmpdir) / "%(id)s.%(ext)s"),
        ]

        if _cookies_disponivel(cookies_file_path):
            cmd.extend(["--cookies", str(cookies_file_path)])
            print(f"🔑 Usando arquivo de cookies para yt-dlp: {cookies_file_path}")
        else:
            print(
                "🍪 Arquivo de cookies não configurado, ausente ou vazio; "
                "YouTube pode bloquear IP de VPS."
            )

        cmd.append(url_video)

        try:
            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=180,
            )
        except subprocess.CalledProcessError as erro:
            mensagem = (erro.stderr or erro.stdout or str(erro)).strip()
            if len(mensagem) > 500:
                mensagem = mensagem[:500] + "..."
            print(f"❌ yt-dlp falhou: {mensagem}")
            return None
        except subprocess.TimeoutExpired:
            print("❌ yt-dlp excedeu o tempo limite ao buscar legendas.")
            return None

        vtt_files = list(Path(tmpdir).glob("*.vtt"))
        if not vtt_files:
            print("❌ yt-dlp não baixou nenhum arquivo VTT.")
            return None

        vtt_file_path = _selecionar_vtt(vtt_files)
        if not vtt_file_path:
            return None

        vtt_content = vtt_file_path.read_text(encoding="utf-8", errors="replace")
        return _vtt_para_texto(vtt_content)


def obter_transcricao(url_video: str, cookies_file_path: str | None = None) -> str | None:
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

    try:
        texto = _obter_com_yt_dlp(url_video, cookies_file_path)
        if texto:
            return texto
    except Exception as erro:
        print(f"⚠️ O yt-dlp também falhou: {erro}")

    print("❌ Nenhuma legenda pôde ser obtida.")
    return None
