from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    url: str = Field(..., min_length=1)
    force: bool = False


class SummaryResponse(BaseModel):
    video_id: str
    title: str
    summary: str
    from_cache: bool = False
    created_at: str | None = None


class HistoryItem(BaseModel):
    video_id: str
    title: str
    created_at: str | None = None


class HistoryDetail(BaseModel):
    video_id: str
    title: str
    summary: str
    created_at: str | None = None
