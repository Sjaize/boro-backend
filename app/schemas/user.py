from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.common import UTCDatetime


class UserMeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nickname": "민수",
                "profile_image_url": "https://picsum.photos/seed/user1/200",
                "region_name": "역삼동",
                "trust_score": 4.8,
                "borrow_count": 3,
                "lend_count": 5,
                "like_count": 12,
                "nearby_urgent_alerts_enabled": False,
            }
        },
    )

    id: int
    nickname: str
    profile_image_url: Optional[str] = None
    region_name: Optional[str] = None
    trust_score: float
    borrow_count: int
    lend_count: int
    like_count: int
    nearby_urgent_alerts_enabled: bool


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nickname": "민수",
                "profile_image_url": "https://picsum.photos/seed/user1/200",
            }
        }
    )

    nickname: Optional[str] = None
    profile_image_url: Optional[str] = None


class LocationUpdate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"lat": 37.5006, "lng": 127.0364}})

    lat: float
    lng: float


class LocationResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "region_name": "강남구",
                "full_address": "서울특별시 강남구 역삼동",
                "lat": 37.5006,
                "lng": 127.0364,
            }
        }
    )

    region_name: str
    full_address: str
    lat: float
    lng: float


class UserSettingsUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notification_radius_m": 1500,
                "interest_keywords": ["전자기기", "캠핑"],
                "nearby_urgent_alerts_enabled": True,
            }
        }
    )

    notification_radius_m: Optional[int] = None
    interest_keywords: Optional[list[str]] = None
    nearby_urgent_alerts_enabled: Optional[bool] = None


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 2,
                "nickname": "지연",
                "profile_image_url": "https://picsum.photos/seed/user2/200",
                "region_name": "선릉동",
                "completed_transaction_count": 10,
                "trust_score": 4.7,
                "review_count": 8,
            }
        },
    )

    id: int
    nickname: str
    profile_image_url: Optional[str] = None
    region_name: Optional[str] = None
    completed_transaction_count: int
    trust_score: float
    review_count: int


class ReviewListItem(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "review_id": 1,
                "rating": 5,
                "comment": "시간 약속을 잘 지켜주셨어요.",
                "created_at": "2026-03-30T12:34:56Z",
            }
        },
    )

    review_id: int
    rating: int
    comment: Optional[str] = None
    created_at: UTCDatetime


class ReviewListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "reviews": [
                    {
                        "review_id": 1,
                        "rating": 5,
                        "comment": "시간 약속을 잘 지켜주셨어요.",
                        "created_at": "2026-03-30T12:34:56Z",
                    },
                    {
                        "review_id": 2,
                        "rating": 4,
                        "comment": "물건 상태가 설명과 일치했어요.",
                        "created_at": "2026-03-28T09:00:00Z",
                    },
                ],
                "page": 1,
                "size": 10,
                "has_next": False,
            }
        }
    )

    reviews: List[ReviewListItem]
    page: int
    size: int
    has_next: bool


class UserUpdateResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "nickname": "민수",
                "profile_image_url": "https://picsum.photos/seed/user1/200",
            }
        }
    )

    id: int
    nickname: str
    profile_image_url: Optional[str] = None


class UserSettingsResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notification_radius_m": 1500,
                "interest_keywords": ["전자기기", "캠핑"],
                "nearby_urgent_alerts_enabled": True,
            }
        }
    )

    notification_radius_m: Optional[int] = None
    interest_keywords: Optional[list[str]] = None
    nearby_urgent_alerts_enabled: bool
