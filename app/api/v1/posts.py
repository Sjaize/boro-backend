from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_posts_service

router = APIRouter(prefix="/api/posts", tags=["Posts"])


@router.get("")
async def list_posts(
    keyword: Optional[str] = Query(None),
    post_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    is_urgent: Optional[bool] = Query(None),
    region_name: Optional[str] = Query(None),
    page: int = Query(1),
    size: int = Query(20),
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


@router.post("")
async def create_post(
    body: dict,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.create_post(current_user["id"], body)}


@router.get("/{post_id}")
async def get_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.get_post(post_id, current_user["id"])}


@router.patch("/{post_id}")
async def update_post(
    post_id: int,
    body: dict,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.update_post(post_id, current_user["id"], body)}


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.delete_post(post_id, current_user["id"])}


@router.post("/{post_id}/likes")
async def like_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.like_post(post_id, current_user["id"])}


@router.delete("/{post_id}/likes")
async def unlike_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.unlike_post(post_id, current_user["id"])}


@router.post("/{post_id}/chats")
async def create_chat_from_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.create_chat_from_post(post_id, current_user["id"])}
