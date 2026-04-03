from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.common import UTCDatetime


class NotificationListItem(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "type": "urgent_post",
                "title": "근처에 긴급 게시글이 올라왔어요",
                "body": "보조배터리 급하게 빌려드려요",
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
    created_at: UTCDatetime


class NotificationListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notifications": [
                    {
                        "id": 1,
                        "type": "urgent_post",
                        "title": "근처에 긴급 게시글이 올라왔어요",
                        "body": "보조배터리 급하게 빌려드려요",
                        "related_post_id": 101,
                        "related_chat_room_id": None,
                        "is_read": False,
                        "created_at": "2026-03-30T09:39:00Z",
                    }
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


class DeviceTokenRegisterRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "device_token": "fcm-device-token-value",
                "platform": "android",
            }
        }
    )

    device_token: str
    platform: Literal["android", "ios", "web"]


class DeviceTokenDeleteRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"device_token": "fcm-device-token-value"}}
    )

    device_token: str


class DeviceTokenResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "device_token": "fcm-device-token-value",
                "platform": "android",
                "is_active": True,
            }
        },
    )

    device_token: str
    platform: str
    is_active: bool


class DeviceTokenDeleteResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"device_token": "fcm-device-token-value", "deleted": True}}
    )

    device_token: str
    deleted: bool
