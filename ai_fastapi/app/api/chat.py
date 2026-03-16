from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from app.services.rag_service import get_answer_stream

router = APIRouter()

class ChatReq(BaseModel):
    prompt: str

@router.post("/chat-stream/")
async def chat_stream(req: ChatReq):
    # StreamingResponse 会把你的生成器实时推送到前端
    return StreamingResponse(get_answer_stream(req.prompt), media_type="text/event-stream")