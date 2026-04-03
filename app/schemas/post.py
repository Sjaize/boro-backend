from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.common import UTCDatetime


class PostListItem(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "post_id": 1,
                "title": "전동 드릴 빌려드려요",
                "post_type": "LEND",
                "price": 5000,
                "region_name": "역삼동",
                "is_urgent": False,
                "thumbnail_url": "https://picsum.photos/seed/post1/400/300",
                "like_count": 5,
                "chat_count": 2,
                "status": "AVAILABLE",
                "created_at": "2026-03-31T09:00:00Z",
            }
        },
    )
    post_id: int
    title: str
    post_type: str
    price: int
    region_name: str
    is_urgent: bool
    thumbnail_url: Optional[str] = None
    like_count: int
    chat_count: int
    status: str
    created_at: UTCDatetime


class PostCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "post_type": "LEND",
                "title": "전동 드릴 빌려드려요",
                "content": "거의 새것입니다. 1일 기준 대여해드려요.",
                "price": 5000,
                "category": "공구",
                "is_urgent": False,
                "rental_period_text": "1일 기준",
                "meeting_place_text": "역삼역 3번 출구",
                "region_name": "역삼동",
                "lat": 37.5006,
                "lng": 127.0364,
                "image_urls": ["https://picsum.photos/seed/post1a/800/600"],
            }
        }
    )
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
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "user_id": 2,
                "nickname": "동네주민",
                "profile_image_url": "https://picsum.photos/seed/user2/200",
                "trust_score": 4.8,
            }
        },
    )
    user_id: int
    nickname: str
    profile_image_url: Optional[str] = None
    trust_score: float


class PostImageSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"image_url": "https://picsum.photos/seed/post1a/800/600", "sort_order": 1}
        },
    )
    image_url: str
    sort_order: int


class PostDetail(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "post_id": 1,
                "author": {
                    "user_id": 2,
                    "nickname": "동네주민",
                    "profile_image_url": "https://picsum.photos/seed/user2/200",
                    "trust_score": 4.8,
                },
                "post_type": "LEND",
                "title": "전동 드릴 빌려드려요",
                "content": "거의 새것입니다. 1일 기준 대여해드려요. 역삼역 근처에서 직거래 가능합니다.",
                "price": 5000,
                "category": "공구",
                "is_urgent": False,
                "rental_period_text": "1일 기준",
                "meeting_place_text": "역삼역 3번 출구",
                "region_name": "역삼동",
                "lat": 37.5006,
                "lng": 127.0364,
                "images": [
                    {"image_url": "https://picsum.photos/seed/post1a/800/600", "sort_order": 1},
                    {"image_url": "https://picsum.photos/seed/post1b/800/600", "sort_order": 2},
                ],
                "like_count": 5,
                "chat_count": 2,
                "status": "AVAILABLE",
                "is_liked_by_me": False,
                "created_at": "2026-03-31T09:00:00Z",
            }
        },
    )
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
    created_at: UTCDatetime


class PostUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "전동 드릴 빌려드려요 (수정)",
                "price": 4500,
                "status": "RESERVED",
            }
        }
    )
    title: Optional[str] = None
    content: Optional[str] = None
    price: Optional[int] = None
    status: Optional[str] = None
    image_urls: Optional[List[str]] = None


class PostLikeResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"post_id": 1, "like_count": 6, "is_liked": True}}
    )
    post_id: int
    like_count: int
    is_liked: bool


class PostDeleteResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"post_id": 1, "deleted": True}}
    )
    post_id: int
    deleted: bool


class PostListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "posts": [
                    {
                        "post_id": 1,
                        "title": "전동 드릴 빌려드려요",
                        "post_type": "LEND",
                        "price": 5000,
                        "region_name": "역삼동",
                        "is_urgent": False,
                        "thumbnail_url": "https://picsum.photos/seed/post1/400/300",
                        "like_count": 5,
                        "chat_count": 2,
                        "status": "AVAILABLE",
                        "created_at": "2026-03-31T09:00:00Z",
                    }
                ],
                "page": 1,
                "size": 20,
                "has_next": False,
            }
        }
    )
    posts: List[PostListItem]
    page: int
    size: int
    has_next: bool


class PostCreateResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"post_id": 101}})
    post_id: int
