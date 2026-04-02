from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_users_service
from app.schemas.common import DataResponse
from app.schemas.post import PostListResponse
from app.schemas.user import (
    LocationResponse,
    LocationUpdate,
    ReviewListResponse,
    UserMeResponse,
    UserProfileResponse,
    UserSettingsResponse,
    UserSettingsUpdate,
    UserUpdate,
    UserUpdateResponse,
)

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=DataResponse[UserMeResponse])
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.get_my_profile(current_user["id"])}


@router.patch("/me", response_model=DataResponse[UserUpdateResponse])
async def update_my_profile(
    body: UserUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.update_my_profile(current_user["id"], body)}


@router.put("/me/location", response_model=DataResponse[LocationResponse])
async def update_location(
    body: LocationUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.update_location(current_user["id"], body.lat, body.lng)}


@router.patch("/me/settings", response_model=DataResponse[UserSettingsResponse])
async def update_settings(
    body: UserSettingsUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.update_settings(current_user["id"], body)}


@router.get("/me/posts", response_model=DataResponse[PostListResponse])
async def get_my_posts(
    post_type: Optional[str] = Query(None),
    page: int = Query(1),
    size: int = Query(10),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.get_my_posts(current_user["id"], post_type, page, size)}


@router.get("/me/likes", response_model=DataResponse[PostListResponse])
async def get_my_likes(
    page: int = Query(1),
    size: int = Query(10),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.get_my_likes(current_user["id"], page, size)}


@router.get("/{user_id}", response_model=DataResponse[UserProfileResponse])
async def get_user_profile(user_id: int, service=Depends(get_users_service)):
    return {"data": service.get_user_profile(user_id)}


@router.get("/{user_id}/reviews", response_model=DataResponse[ReviewListResponse])
async def get_user_reviews(
    user_id: int,
    page: int = Query(1),
    size: int = Query(10),
    service=Depends(get_users_service),
):
    return {"data": service.get_user_reviews(user_id, page, size)}


@router.get("/{user_id}/posts", response_model=DataResponse[PostListResponse])
async def get_user_posts(
    user_id: int,
    post_type: Optional[str] = Query(None),
    page: int = Query(1),
    size: int = Query(10),
    service=Depends(get_users_service),
):
    return {"data": service.get_user_posts(user_id, post_type, page, size)}
