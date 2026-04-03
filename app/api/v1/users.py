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


@router.get(
    "/me",
    response_model=DataResponse[UserMeResponse],
    summary="내 프로필 조회",
    description="현재 로그인한 유저의 프로필 정보를 조회합니다.",
)
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.get_my_profile(current_user["id"])}


@router.patch(
    "/me",
    response_model=DataResponse[UserUpdateResponse],
    summary="내 프로필 수정",
    description="닉네임 또는 프로필 이미지를 수정합니다.",
)
async def update_my_profile(
    body: UserUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.update_my_profile(current_user["id"], body)}


@router.put(
    "/me/location",
    response_model=DataResponse[LocationResponse],
    summary="내 위치 업데이트",
    description="현재 위치(위도/경도)를 업데이트하고 지역명을 반환합니다.",
)
async def update_location(
    body: LocationUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.update_location(current_user["id"], body.lat, body.lng)}


@router.patch(
    "/me/settings",
    response_model=DataResponse[UserSettingsResponse],
    summary="알림 설정 변경",
    description="알림 반경(m) 및 관심 키워드를 설정합니다.",
)
async def update_settings(
    body: UserSettingsUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.update_settings(current_user["id"], body)}


@router.get(
    "/me/posts",
    response_model=DataResponse[PostListResponse],
    summary="내 게시글 목록 조회",
    description="내가 작성한 게시글 목록을 조회합니다. `post_type`으로 LEND/BORROW 필터링 가능합니다.",
)
async def get_my_posts(
    post_type: Optional[str] = Query(None),
    page: int = Query(1),
    size: int = Query(10),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.get_my_posts(current_user["id"], post_type, page, size)}


@router.get(
    "/me/likes",
    response_model=DataResponse[PostListResponse],
    summary="찜한 게시글 목록 조회",
    description="내가 찜한 게시글 목록을 조회합니다.",
)
async def get_my_likes(
    page: int = Query(1),
    size: int = Query(10),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_users_service),
):
    return {"data": service.get_my_likes(current_user["id"], page, size)}


@router.get(
    "/{user_id}",
    response_model=DataResponse[UserProfileResponse],
    summary="유저 프로필 조회",
    description="특정 유저의 공개 프로필을 조회합니다.",
)
async def get_user_profile(user_id: int, service=Depends(get_users_service)):
    return {"data": service.get_user_profile(user_id)}


@router.get(
    "/{user_id}/reviews",
    response_model=DataResponse[ReviewListResponse],
    summary="유저 받은 리뷰 목록 조회",
    description="특정 유저가 받은 리뷰 목록을 조회합니다.",
)
async def get_user_reviews(
    user_id: int,
    page: int = Query(1),
    size: int = Query(10),
    service=Depends(get_users_service),
):
    return {"data": service.get_user_reviews(user_id, page, size)}


@router.get(
    "/{user_id}/posts",
    response_model=DataResponse[PostListResponse],
    summary="유저 게시글 목록 조회",
    description="특정 유저가 작성한 게시글 목록을 조회합니다.",
)
async def get_user_posts(
    user_id: int,
    post_type: Optional[str] = Query(None),
    page: int = Query(1),
    size: int = Query(10),
    service=Depends(get_users_service),
):
    return {"data": service.get_user_posts(user_id, post_type, page, size)}
