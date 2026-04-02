from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class PostListItem(BaseModel):
    post_id: int
    title: str
    post_type: str  # LEND, BORROW
    price: int
    region_name: str
    is_urgent: bool
    thumbnail_url: Optional[str] = None
    like_count: int
    chat_count: int
    status: str  # AVAILABLE, RESERVED, COMPLETED
    created_at: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    post_type: str
    title: str
    content: str
    price: int
    category: str
    is_urgent: bool
    rental_period_text: str
    meeting_place_text: Optional[str] = None
    region_name: str
    lat: float
    lng: float
    image_urls: List[str]


class PostAuthor(BaseModel):
    user_id: int
    nickname: str
    profile_image_url: Optional[str] = None
    trust_score: float

    class Config:
        from_attributes = True


class PostImageSchema(BaseModel):
    image_url: str
    sort_order: int

    class Config:
        from_attributes = True


class PostDetail(BaseModel):
    post_id: int
    author: PostAuthor
    post_type: str
    title: str
    content: str
    price: int
    category: str
    is_urgent: bool
    rental_period_text: str
    meeting_place_text: Optional[str] = None
    region_name: str
    lat: float
    lng: float
    images: List[PostImageSchema]
    like_count: int
    chat_count: int
    status: str
    is_liked_by_me: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    price: Optional[int] = None
    status: Optional[str] = None
    image_urls: Optional[List[str]] = None


class PostLikeResponse(BaseModel):
    post_id: int
    like_count: int
    is_liked: bool


class PostDeleteResponse(BaseModel):
    post_id: int
    deleted: bool


class PostListResponse(BaseModel):
    posts: List[PostListItem]
    page: int
    size: int
    has_next: bool


class PostCreateResponse(BaseModel):
    post_id: int
