from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_chats_service, get_current_user
from app.schemas.chat import (
    ChatMarkReadResponse,
    ChatMessageCreate,
    ChatMessageListItem,
    ChatReadUpdate,
    ChatRoomDetail,
    ChatRoomListResponse,
    MessageListResponse,
)
from app.schemas.common import DataResponse

router = APIRouter(prefix="/api/chats", tags=["Chats"])


@router.get("", response_model=DataResponse[ChatRoomListResponse])
async def list_chat_rooms(
    type: str = Query("ALL"),
    page: int = Query(1),
    size: int = Query(20),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.list_chat_rooms(current_user["id"], type, page, size)}


@router.get("/{chat_room_id}", response_model=DataResponse[ChatRoomDetail])
async def get_chat_room(
    chat_room_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.get_chat_room(chat_room_id, current_user["id"])}


@router.get("/{chat_room_id}/messages", response_model=DataResponse[MessageListResponse])
async def list_messages(
    chat_room_id: int,
    cursor: Optional[int] = Query(None),
    size: int = Query(20),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.list_messages(chat_room_id, current_user["id"], cursor, size)}


@router.post("/{chat_room_id}/messages", response_model=DataResponse[ChatMessageListItem])
async def send_message(
    chat_room_id: int,
    body: ChatMessageCreate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.send_message(chat_room_id, current_user["id"], body.model_dump())}


@router.patch("/{chat_room_id}/read", response_model=DataResponse[ChatMarkReadResponse])
async def mark_read(
    chat_room_id: int,
    body: ChatReadUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.mark_read(chat_room_id, current_user["id"], body.last_read_message_id)}
