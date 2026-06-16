import os

from . import database_service
from .video_service import extrair_id_video, montar_titulo_padrao


class SummaryError(Exception):
    message = "Ocorreu um erro inesperado ao processar o vídeo."
    status_code = 500


class InvalidYoutubeUrlError(SummaryError):
    message = "Informe uma URL válida do YouTube."
    status_code = 400


class TranscriptError(SummaryError):
    message = "Não foi possível obter legenda deste vídeo. Tente outro vídeo com legendas disponíveis."
    status_code = 422


class GeminiConfigError(SummaryError):
    message = "A chave GEMINI_API_KEY não foi configurada no servidor."
    status_code = 503


class GeminiRateLimitError(SummaryError):
    message = "Limite temporário da API atingido. Tente novamente mais tarde."
    status_code = 429


class GeminiApiError(SummaryError):
    message = "Ocorreu um erro na API ao gerar o resumo."
    status_code = 502


def _normalizar_resumo_salvo(resumo: dict, from_cache: bool) -> dict:
    return {
        "video_id": resumo["video_id"],
        "title": resumo["title"],
        "summary": resumo["summary"],
        "from_cache": from_cache,
        "created_at": resumo["created_at"],
    }


def _validar_resposta_gemini(resumo: str):
    if not resumo:
        raise GeminiApiError()

    if resumo.startswith("❌ Falha"):
        raise GeminiRateLimitError()

    if resumo.startswith("❌ ERRO: GEMINI_API_KEY"):
        raise GeminiConfigError()

    if resumo.startswith("❌ Erro ao gerar resumo"):
        raise GeminiApiError()


def _carregar_env():
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ModuleNotFoundError:
        pass


def processar_video(url: str, force: bool = False, cookies_file_path: str | None = None) -> dict:
    database_service.inicializar()

    video_id = extrair_id_video(url)
    if not video_id:
        raise InvalidYoutubeUrlError()

    resumo_salvo = database_service.buscar(video_id)
    if resumo_salvo and not force:
        return _normalizar_resumo_salvo(resumo_salvo, from_cache=True)

    _carregar_env()

    if not os.getenv("GEMINI_API_KEY"):
        raise GeminiConfigError()

    from audio_transcricao import obter_transcricao
    from apigemini import resumir_transcricao

    transcricao = obter_transcricao(url, cookies_file_path)
    if not transcricao:
        raise TranscriptError()

    resumo = resumir_transcricao(transcricao)
    _validar_resposta_gemini(resumo)

    titulo = montar_titulo_padrao(video_id)
    database_service.salvar(video_id, titulo, resumo, url)

    resumo_atualizado = database_service.buscar(video_id)
    return _normalizar_resumo_salvo(resumo_atualizado, from_cache=False)
