from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.common import UTCDatetime


class TransactionReviewInfo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"has_received_review": True, "has_written_review": False}},
    )
    has_received_review: bool
    has_written_review: bool = False


class TransactionListItem(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "transaction_id": 1,
                "post_id": 101,
                "chat_room_id": 55,
                "role": "borrower",
                "post_title": "보조배터리 구해요",
                "post_image_url": "https://picsum.photos/seed/post101/400/300",
                "price": 1100,
                "rental_period_text": "1시간",
                "chat_count": 0,
                "like_count": 0,
                "completed_at": "2026-03-30T09:41:00Z",
                "review": {"has_received_review": True},
            }
        },
    )
    transaction_id: int
    post_id: int
    chat_room_id: int
    role: str
    post_title: str
    post_image_url: Optional[str] = None
    price: int
    rental_period_text: Optional[str] = None
    chat_count: int
    like_count: int
    completed_at: UTCDatetime
    review: TransactionReviewInfo


class TransactionCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"post_id": 101, "chat_room_id": 55}}
    )
    post_id: int
    chat_room_id: int


class TransactionPostInfo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "보조배터리 구해요",
                "content": "1시간 정도 빌리고 싶어요.",
                "price": 1100,
                "category": "전자기기",
                "rental_period_text": "1시간",
                "meeting_place_text": "경희대 국제캠 정문 앞",
                "region_name": "영통동",
                "post_image_urls": ["https://picsum.photos/seed/post101/400/300"],
                "chat_count": 0,
                "like_count": 0,
            }
        },
    )
    title: str
    content: str
    price: int
    category: str
    rental_period_text: Optional[str] = None
    meeting_place_text: Optional[str] = None
    region_name: str
    post_image_urls: List[str]
    chat_count: int
    like_count: int


class WrittenReviewDetail(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "review_id": 20,
                "rating": 5,
                "comment": "Promise kept and pickup was smooth.",
                "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"],
                "created_at": "2026-04-01T10:00:00Z",
            }
        },
    )
    review_id: int
    rating: int
    comment: Optional[str] = None
    tags: List[str]
    created_at: UTCDatetime


class ReviewDetail(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "has_received_review": True,
                "has_written_review": True,
                "rating": 5,
                "comment": "시간 약속 잘 지켜주셨어요.",
                "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"],
                "written_review": {
                    "review_id": 20,
                    "rating": 5,
                    "comment": "Promise kept and pickup was smooth.",
                    "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"],
                    "created_at": "2026-04-01T10:00:00Z",
                },
            }
        },
    )
    has_received_review: bool
    has_written_review: bool
    rating: Optional[int] = None
    comment: Optional[str] = None
    tags: Optional[List[str]] = None
    written_review: Optional[WrittenReviewDetail] = None


class TransactionDetail(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "transaction_id": 1,
                "post_id": 101,
                "chat_room_id": 55,
                "lender_user_id": 2,
                "borrower_user_id": 1,
                "my_role": "borrower",
                "completed_at": "2026-03-30T09:41:00Z",
                "post": {
                    "title": "보조배터리 구해요",
                    "content": "1시간 정도 빌리고 싶어요.",
                    "price": 1100,
                    "category": "전자기기",
                    "rental_period_text": "1시간",
                    "meeting_place_text": "경희대 국제캠 정문 앞",
                    "region_name": "영통동",
                    "post_image_urls": ["https://picsum.photos/seed/post101/400/300"],
                    "chat_count": 0,
                    "like_count": 0,
                },
                "review": {
                    "has_received_review": True,
                    "rating": 5,
                    "comment": "시간 약속 잘 지켜주셨어요.",
                    "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"],
                },
            }
        },
    )
    transaction_id: int
    post_id: int
    chat_room_id: int
    lender_user_id: int
    borrower_user_id: int
    my_role: str
    completed_at: UTCDatetime
    post: TransactionPostInfo
    review: ReviewDetail


class ReviewCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rating": 5,
                "comment": "시간 약속 잘 지켜주셨어요.",
                "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"],
            }
        }
    )
    rating: int
    comment: Optional[str] = None
    tags: List[str]


class ReviewResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "review_id": 20,
                "transaction_id": 1,
                "rating": 5,
                "comment": "시간 약속 잘 지켜주셨어요.",
                "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"],
                "created_at": "2026-04-01T10:00:00Z",
            }
        },
    )
    review_id: int
    transaction_id: int
    rating: int
    comment: Optional[str] = None
    tags: List[str]
    created_at: UTCDatetime


class TransactionListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transactions": [
                    {
                        "transaction_id": 1,
                        "post_id": 101,
                        "chat_room_id": 55,
                        "role": "borrower",
                        "post_title": "보조배터리 구해요",
                        "post_image_url": "https://picsum.photos/seed/post101/400/300",
                        "price": 1100,
                        "rental_period_text": "1시간",
                        "chat_count": 0,
                        "like_count": 0,
                        "completed_at": "2026-03-30T09:41:00Z",
                        "review": {"has_received_review": True},
                    }
                ],
                "page": 1,
                "size": 10,
                "has_next": False,
            }
        }
    )
    transactions: List[TransactionListItem]
    page: int
    size: int
    has_next: bool


class TransactionCreateResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_id": 10,
                "post_id": 101,
                "chat_room_id": 55,
                "lender_user_id": 2,
                "borrower_user_id": 1,
                "completed_at": "2026-04-01T10:00:00Z",
            }
        }
    )
    transaction_id: int
    post_id: int
    chat_room_id: int
    lender_user_id: int
    borrower_user_id: int
    completed_at: UTCDatetime
