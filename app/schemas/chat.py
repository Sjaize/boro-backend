from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class ChatRoomListItem(BaseModel):
    chat_room_id: int
    post_id: int
    post_type: str
    post_title: str
    partner_nickname: str
    partner_profile_image_url: Optional[str] = None
    last_message_preview: Optional[str] = None
    last_message_at: Optional[datetime] = None
    unread_count: int

    class Config:
        from_attributes = True


class ChatRoomPostInfo(BaseModel):
    post_id: int
    title: str
    price: int
    rental_period_text: Optional[str] = None
    post_image_url: Optional[str] = None
    post_type: str

    class Config:
        from_attributes = True


class ChatParticipant(BaseModel):
    user_id: int
    nickname: str
    profile_image_url: Optional[str] = None
    role: str

    class Config:
        from_attributes = True


class ChatRoomDetail(BaseModel):
    chat_room_id: int
    post: ChatRoomPostInfo
    participants: List[ChatParticipant]
    last_read_message_id: Optional[int] = None
    unread_count: int
    transaction_completed: bool

    class Config:
        from_attributes = True


class ChatMessageListItem(BaseModel):
    message_id: int
    sender_user_id: int
    message_type: str  # text, image
    content: str
    created_at: datetime
    is_mine: bool

    class Config:
        from_attributes = True


class ChatMessageCreate(BaseModel):
    message_type: str
    content: str


class ChatReadUpdate(BaseModel):
    last_read_message_id: int


class ChatRoomCreateResponse(BaseModel):
    chat_room_id: int
    is_new: bool
