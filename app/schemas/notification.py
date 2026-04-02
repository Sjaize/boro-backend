from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class NotificationListItem(BaseModel):
    id: int
    type: str  # urgent_post, chat_message, interest_post
    title: str
    body: str
    related_post_id: Optional[int] = None
    related_chat_room_id: Optional[int] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    notifications: List[NotificationListItem]
    page: int
    size: int
    has_next: bool


class NotificationReadResponse(BaseModel):
    id: int
    is_read: bool

    class Config:
        from_attributes = True
