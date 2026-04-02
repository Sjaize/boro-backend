from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_chats_service, get_current_user
from app.schemas.chat import ChatMessageCreate, ChatReadUpdate

router = APIRouter(prefix="/api/chats", tags=["Chats"])


@router.get("")
async def list_chat_rooms(
    type: str = Query("ALL"),
    page: int = Query(1),
    size: int = Query(20),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.list_chat_rooms(current_user["id"], type, page, size)}


@router.get("/{chat_room_id}")
async def get_chat_room(
    chat_room_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.get_chat_room(chat_room_id, current_user["id"])}


@router.get("/{chat_room_id}/messages")
async def list_messages(
    chat_room_id: int,
    cursor: Optional[int] = Query(None),
    size: int = Query(20),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.list_messages(chat_room_id, current_user["id"], cursor, size)}


@router.post("/{chat_room_id}/messages")
async def send_message(
    chat_room_id: int,
    body: ChatMessageCreate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.send_message(chat_room_id, current_user["id"], body.model_dump())}


@router.patch("/{chat_room_id}/read")
async def mark_read(
    chat_room_id: int,
    body: ChatReadUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.mark_read(chat_room_id, current_user["id"], body.last_read_message_id)}
