from fastapi import APIRouter
from pydantic import BaseModel
from app.core.chat_store import add_message, get_messages, clear_chat

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatMessage(BaseModel):
    device_id: str
    message: str
    sender: str   # "user" | "doctor"


@router.post("/send")
def send_message(data: ChatMessage):
    add_message(
        device_id=data.device_id,
        sender_role=data.sender,
        text=data.message
    )
    return {"status": "sent"}


@router.get("/messages/{device_id}")
def read_messages(device_id: str):
    return get_messages(device_id)


@router.post("/clear/{device_id}")
def clear_session(device_id: str):
    clear_chat(device_id)
    return {"status": "cleared"}
