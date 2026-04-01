from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class TransactionReviewInfo(BaseModel):
    has_received_review: bool

    class Config:
        from_attributes = True


class TransactionListItem(BaseModel):
    transaction_id: int
    post_id: int
    chat_room_id: int
    role: str  # borrower, lender
    post_title: str
    post_image_url: Optional[str] = None
    price: int
    rental_period_text: Optional[str] = None
    chat_count: int
    like_count: int
    completed_at: datetime
    review: TransactionReviewInfo

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    post_id: int
    chat_room_id: int


class TransactionPostInfo(BaseModel):
    title: str
    content: str
    price: int
    category: str
    rental_period_text: Optional[str] = None
    meeting_place_text: Optional[str] = None
    post_image_urls: List[str]
    chat_count: int
    like_count: int

    class Config:
        from_attributes = True


class ReviewDetail(BaseModel):
    has_received_review: bool
    rating: Optional[int] = None
    comment: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True


class TransactionDetail(BaseModel):
    transaction_id: int
    post_id: int
    chat_room_id: int
    lender_user_id: int
    borrower_user_id: int
    my_role: str
    completed_at: datetime
    post: TransactionPostInfo
    review: ReviewDetail

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    rating: int
    comment: Optional[str] = None
    tags: List[str]


class ReviewResponse(BaseModel):
    review_id: int
    transaction_id: int
    rating: int
    comment: Optional[str] = None
    tags: List[str]
    created_at: datetime

    class Config:
        from_attributes = True
