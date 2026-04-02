from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatRoomListItem(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "chat_room_id": 55,
                "post_id": 101,
                "post_type": "BORROW",
                "post_title": "보조배터리 구해요",
                "partner_nickname": "배터리왕",
                "partner_profile_image_url": "https://picsum.photos/seed/user3/200",
                "last_message_preview": "보조배터리 필요하시는 글 보고 연락드렸어요",
                "last_message_at": "2026-03-30T09:39:00Z",
                "unread_count": 3,
            }
        },
    )
    chat_room_id: int
    post_id: int
    post_type: str
    post_title: str
    partner_nickname: str
    partner_profile_image_url: Optional[str] = None
    last_message_preview: Optional[str] = None
    last_message_at: Optional[datetime] = None
    unread_count: int


class ChatRoomPostInfo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "post_id": 101,
                "title": "보조배터리 구해요",
                "price": 1100,
                "rental_period_text": "1시간",
                "post_image_url": "https://picsum.photos/seed/post101/400/300",
                "post_type": "BORROW",
            }
        },
    )
    post_id: int
    title: str
    price: int
    rental_period_text: Optional[str] = None
    post_image_url: Optional[str] = None
    post_type: str


class ChatParticipant(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "user_id": 1,
                "nickname": "홍길동",
                "profile_image_url": "https://picsum.photos/seed/user1/200",
                "role": "borrower",
            }
        },
    )
    user_id: int
    nickname: str
    profile_image_url: Optional[str] = None
    role: str


class ChatRoomDetail(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "chat_room_id": 55,
                "post": {
                    "post_id": 101,
                    "title": "보조배터리 구해요",
                    "price": 1100,
                    "rental_period_text": "1시간",
                    "post_image_url": "https://picsum.photos/seed/post101/400/300",
                    "post_type": "BORROW",
                },
                "participants": [
                    {
                        "user_id": 1,
                        "nickname": "홍길동",
                        "profile_image_url": "https://picsum.photos/seed/user1/200",
                        "role": "borrower",
                    },
                    {
                        "user_id": 2,
                        "nickname": "배터리왕",
                        "profile_image_url": "https://picsum.photos/seed/user3/200",
                        "role": "lender",
                    },
                ],
                "last_read_message_id": 203,
                "unread_count": 3,
                "transaction_completed": False,
            }
        },
    )
    chat_room_id: int
    post: ChatRoomPostInfo
    participants: List[ChatParticipant]
    last_read_message_id: Optional[int] = None
    unread_count: int
    transaction_completed: bool


class ChatMessageListItem(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message_id": 201,
                "sender_user_id": 1,
                "message_type": "text",
                "content": "안녕하세요! 보조배터리 아직 필요하신가요?",
                "created_at": "2026-03-30T15:58:00Z",
                "is_mine": True,
            }
        },
    )
    message_id: int
    sender_user_id: int
    message_type: str
    content: str
    created_at: datetime
    is_mine: bool


class ChatMessageCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"message_type": "text", "content": "안녕하세요!"}}
    )
    message_type: str
    content: str


class ChatReadUpdate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"last_read_message_id": 203}})
    last_read_message_id: int


class ChatRoomCreateResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"chat_room_id": 55, "is_new": True}}
    )
    chat_room_id: int
    is_new: bool


class ChatRoomListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "chat_rooms": [
                    {
                        "chat_room_id": 55,
                        "post_id": 101,
                        "post_type": "BORROW",
                        "post_title": "보조배터리 구해요",
                        "partner_nickname": "배터리왕",
                        "partner_profile_image_url": "https://picsum.photos/seed/user3/200",
                        "last_message_preview": "보조배터리 필요하시는 글 보고 연락드렸어요",
                        "last_message_at": "2026-03-30T09:39:00Z",
                        "unread_count": 3,
                    }
                ],
                "page": 1,
                "size": 20,
                "has_next": False,
            }
        }
    )
    chat_rooms: List[ChatRoomListItem]
    page: int
    size: int
    has_next: bool


class MessageListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "messages": [
                    {
                        "message_id": 201,
                        "sender_user_id": 1,
                        "message_type": "text",
                        "content": "안녕하세요! 보조배터리 아직 필요하신가요?",
                        "created_at": "2026-03-30T15:58:00Z",
                        "is_mine": True,
                    },
                    {
                        "message_id": 202,
                        "sender_user_id": 2,
                        "message_type": "text",
                        "content": "네, 오늘 오후에 가능해요!",
                        "created_at": "2026-03-30T15:59:00Z",
                        "is_mine": False,
                    },
                ],
                "next_cursor": None,
                "has_next": False,
            }
        }
    )
    messages: List[ChatMessageListItem]
    next_cursor: Optional[int] = None
    has_next: bool


class ChatMarkReadResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"chat_room_id": 55, "last_read_message_id": 203, "unread_count": 0}
        }
    )
    chat_room_id: int
    last_read_message_id: int
    unread_count: int
