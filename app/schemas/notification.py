from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class NotificationListItem(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "type": "urgent_post",
                "title": "주변에 물건이 필요한 사람이 있어요!",
                "body": "보조배터리 필요해요",
                "related_post_id": 101,
                "related_chat_room_id": None,
                "is_read": False,
                "created_at": "2026-03-30T09:39:00Z",
            }
        },
    )
    id: int
    type: str
    title: str
    body: str
    related_post_id: Optional[int] = None
    related_chat_room_id: Optional[int] = None
    is_read: bool
    created_at: datetime


class NotificationListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notifications": [
                    {
                        "id": 1,
                        "type": "urgent_post",
                        "title": "주변에 물건이 필요한 사람이 있어요!",
                        "body": "보조배터리 필요해요",
                        "related_post_id": 101,
                        "related_chat_room_id": None,
                        "is_read": False,
                        "created_at": "2026-03-30T09:39:00Z",
                    },
                    {
                        "id": 3,
                        "type": "chat_message",
                        "title": "새로운 채팅 메시지가 도착했어요!",
                        "body": "오늘 6시에 거래 가능하신가요?",
                        "related_post_id": 101,
                        "related_chat_room_id": 55,
                        "is_read": True,
                        "created_at": "2026-03-30T09:20:00Z",
                    },
                ],
                "page": 1,
                "size": 20,
                "has_next": False,
            }
        }
    )
    notifications: List[NotificationListItem]
    page: int
    size: int
    has_next: bool


class NotificationReadResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "is_read": True}},
    )
    id: int
    is_read: bool
