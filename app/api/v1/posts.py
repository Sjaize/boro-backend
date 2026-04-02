from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_posts_service
from app.schemas.chat import ChatRoomCreateResponse
from app.schemas.common import DataResponse
from app.schemas.post import (
    PostCreate,
    PostCreateResponse,
    PostDeleteResponse,
    PostDetail,
    PostLikeResponse,
    PostListResponse,
    PostUpdate,
)

router = APIRouter(prefix="/api/posts", tags=["Posts"])


@router.get("", response_model=DataResponse[PostListResponse])
async def list_posts(
    keyword: Optional[str] = Query(None),
    post_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    is_urgent: Optional[bool] = Query(None),
    region_name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at"),
    service=Depends(get_posts_service),
):
    filters = {
        "keyword": keyword,
        "post_type": post_type,
        "category": category,
        "is_urgent": is_urgent,
        "region_name": region_name,
        "page": page,
        "size": size,
        "sort": sort,
    }
    return {"data": service.list_posts(filters)}


@router.post("", response_model=DataResponse[PostCreateResponse])
async def create_post(
    body: PostCreate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.create_post(current_user["id"], body)}


@router.get("/{post_id}", response_model=DataResponse[PostDetail])
async def get_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.get_post(post_id, current_user["id"])}


@router.patch("/{post_id}", response_model=DataResponse[PostCreateResponse])
async def update_post(
    post_id: int,
    body: PostUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.update_post(post_id, current_user["id"], body)}


@router.delete("/{post_id}", response_model=DataResponse[PostDeleteResponse])
async def delete_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.delete_post(post_id, current_user["id"])}


@router.post("/{post_id}/likes", response_model=DataResponse[PostLikeResponse])
async def like_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.like_post(post_id, current_user["id"])}


@router.delete("/{post_id}/likes", response_model=DataResponse[PostLikeResponse])
async def unlike_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.unlike_post(post_id, current_user["id"])}


@router.post("/{post_id}/chats", response_model=DataResponse[ChatRoomCreateResponse])
async def create_chat_from_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.create_chat_from_post(post_id, current_user["id"])}
