from typing import Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime


class UserMeResponse(BaseModel):
    id: int
    nickname: str
    profile_image_url: Optional[str] = None
    region_name: Optional[str] = None
    trust_score: float
    borrow_count: int
    lend_count: int
    like_count: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    profile_image_url: Optional[str] = None


class LocationUpdate(BaseModel):
    lat: float
    lng: float


class LocationResponse(BaseModel):
    region_name: str
    full_address: str
    lat: float
    lng: float


class UserSettingsUpdate(BaseModel):
    notification_radius_m: int
    interest_keywords: list[str]


class UserProfileResponse(BaseModel):
    id: int
    nickname: str
    profile_image_url: Optional[str] = None
    region_name: Optional[str] = None
    completed_transaction_count: int
    trust_score: float
    review_count: int

    class Config:
        from_attributes = True


class ReviewListItem(BaseModel):
    review_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
