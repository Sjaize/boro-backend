from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse

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
TEST_CHAT_PAGE = Path(__file__).resolve().parents[3] / "test_chat.html"


@router.get("/test-page", include_in_schema=False)
async def chat_test_page():
    return FileResponse(TEST_CHAT_PAGE)


@router.get(
    "",
    response_model=DataResponse[ChatRoomListResponse],
    summary="채팅방 목록 조회",
    description=(
        "내 채팅방 목록을 조회합니다.\n\n"
        "**type 파라미터:**\n"
        "- `ALL`: 전체\n"
        "- `LEND`: 빌려드려요 관련\n"
        "- `BORROW`: 구해요 관련"
    ),
)
async def list_chat_rooms(
    type: str = Query("ALL"),
    page: int = Query(1),
    size: int = Query(20),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.list_chat_rooms(current_user["id"], type, page, size)}


@router.get(
    "/{chat_room_id}",
    response_model=DataResponse[ChatRoomDetail],
    summary="채팅방 상세 조회",
    description="채팅방 정보, 참여자, 연결된 게시글 정보를 조회합니다.",
)
async def get_chat_room(
    chat_room_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.get_chat_room(chat_room_id, current_user["id"])}


@router.get(
    "/{chat_room_id}/messages",
    response_model=DataResponse[MessageListResponse],
    summary="메시지 목록 조회",
    description=(
        "채팅방 메시지 목록을 커서 기반으로 조회합니다.\n\n"
        "- `cursor`: 마지막으로 받은 `message_id` (첫 요청 시 생략)\n"
        "- 최신 메시지부터 내려옵니다."
    ),
)
async def list_messages(
    chat_room_id: int,
    cursor: Optional[int] = Query(None),
    size: int = Query(20),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": service.list_messages(chat_room_id, current_user["id"], cursor, size)}


@router.post(
    "/{chat_room_id}/messages",
    response_model=DataResponse[ChatMessageListItem],
    summary="메시지 전송",
    description="채팅방에 메시지를 전송합니다. `message_type`: `text` / `image`",
)
async def send_message(
    chat_room_id: int,
    body: ChatMessageCreate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": await service.send_message(chat_room_id, current_user["id"], body.model_dump())}


@router.patch(
    "/{chat_room_id}/read",
    response_model=DataResponse[ChatMarkReadResponse],
    summary="메시지 읽음 처리",
    description="마지막으로 읽은 메시지 ID를 업데이트하여 읽음 처리합니다.",
)
async def mark_read(
    chat_room_id: int,
    body: ChatReadUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_chats_service),
):
    return {"data": await service.mark_read(chat_room_id, current_user["id"], body.last_read_message_id)}
