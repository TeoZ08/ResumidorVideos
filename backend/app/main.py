from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from .schemas import HistoryDetail, HistoryItem, SummarizeRequest, SummaryResponse
from .services import database_service
from .services.summary_service import SummaryError, processar_video


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    database_service.inicializar()
    yield


app = FastAPI(title="Resumidor de Videos API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/summarize", response_model=SummaryResponse)
def summarize(payload: SummarizeRequest):
    try:
        return processar_video(payload.url, payload.force)
    except SummaryError as erro:
        print(f"Erro controlado ao processar video: {erro.__class__.__name__}")
        raise HTTPException(status_code=erro.status_code, detail=erro.message) from erro
    except Exception as erro:
        print(f"Erro inesperado ao processar video: {erro}")
        raise HTTPException(
            status_code=500,
            detail="Ocorreu um erro inesperado ao processar o vídeo.",
        ) from erro


@app.get("/api/history", response_model=list[HistoryItem])
def history():
    itens = database_service.listar()
    return [
        {
            "video_id": item["video_id"],
            "title": item["title"],
            "created_at": item["created_at"],
        }
        for item in itens
    ]


@app.get("/api/history/{video_id}", response_model=HistoryDetail)
def history_detail(video_id: str):
    item = database_service.buscar(video_id)
    if not item:
        raise HTTPException(status_code=404, detail="Resumo não encontrado.")

    return {
        "video_id": item["video_id"],
        "title": item["title"],
        "summary": item["summary"],
        "created_at": item["created_at"],
    }


@app.get("/api/export/{video_id}")
def export_summary(video_id: str):
    item = database_service.buscar(video_id)
    if not item:
        raise HTTPException(status_code=404, detail="Resumo não encontrado.")

    conteudo = "\n".join(
        [
            f"# Resumo do Vídeo: {item['title']}",
            "",
            f"**ID do vídeo:** {item['video_id']}",
            f"**Data de processamento:** {item['created_at'] or 'Não informado'}",
            "",
            "---",
            "",
            item["summary"],
        ]
    )

    return Response(
        content=conteudo,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename=Resumo_{video_id}.md"},
    )


if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")


@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    index_file = FRONTEND_DIST / "index.html"
    requested_file = FRONTEND_DIST / full_path

    if requested_file.is_file():
        return FileResponse(requested_file)

    if index_file.exists():
        return FileResponse(index_file)

    raise HTTPException(status_code=404, detail="Frontend ainda não foi gerado.")
