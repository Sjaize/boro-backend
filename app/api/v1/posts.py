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


@router.get(
    "",
    response_model=DataResponse[PostListResponse],
    summary="게시글 목록 조회",
    description=(
        "게시글 목록을 조회합니다.\n\n"
        "**필터 파라미터:**\n"
        "- `keyword`: 제목 검색\n"
        "- `post_type`: `LEND` (빌려드려요) / `BORROW` (구해요)\n"
        "- `category`: 카테고리 필터\n"
        "- `is_urgent`: 급구 여부\n"
        "- `region_name`: 지역명 필터\n"
        "- `sort`: 정렬 기준 (`created_at`, `price`)"
    ),
)
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


@router.post(
    "",
    response_model=DataResponse[PostCreateResponse],
    summary="게시글 작성",
    description="새 게시글을 작성합니다. 이미지 URL은 `/api/images/presigned-url`로 먼저 업로드 후 전달하세요.",
)
async def create_post(
    body: PostCreate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.create_post(current_user["id"], body)}


@router.get(
    "/{post_id}",
    response_model=DataResponse[PostDetail],
    summary="게시글 상세 조회",
    description="게시글 상세 정보를 조회합니다.",
)
async def get_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.get_post(post_id, current_user["id"])}


@router.patch(
    "/{post_id}",
    response_model=DataResponse[PostCreateResponse],
    summary="게시글 수정",
    description="게시글 내용을 수정합니다. 작성자만 수정할 수 있습니다.",
)
async def update_post(
    post_id: int,
    body: PostUpdate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.update_post(post_id, current_user["id"], body)}


@router.delete(
    "/{post_id}",
    response_model=DataResponse[PostDeleteResponse],
    summary="게시글 삭제",
    description="게시글을 삭제합니다. 작성자만 삭제할 수 있습니다.",
)
async def delete_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.delete_post(post_id, current_user["id"])}


@router.post(
    "/{post_id}/likes",
    response_model=DataResponse[PostLikeResponse],
    summary="게시글 찜하기",
    description="게시글을 찜합니다.",
)
async def like_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.like_post(post_id, current_user["id"])}


@router.delete(
    "/{post_id}/likes",
    response_model=DataResponse[PostLikeResponse],
    summary="게시글 찜 취소",
    description="게시글 찜을 취소합니다.",
)
async def unlike_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.unlike_post(post_id, current_user["id"])}


@router.post(
    "/{post_id}/chats",
    response_model=DataResponse[ChatRoomCreateResponse],
    summary="게시글에서 채팅방 생성",
    description="게시글 작성자와 채팅방을 생성합니다. 이미 채팅방이 있으면 기존 채팅방을 반환합니다.",
)
async def create_chat_from_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_posts_service),
):
    return {"data": service.create_chat_from_post(post_id, current_user["id"])}
