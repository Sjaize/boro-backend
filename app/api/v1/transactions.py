from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_transactions_service
from app.schemas.common import DataResponse
from app.schemas.transaction import (
    ReviewCreate,
    ReviewResponse,
    TransactionCreate,
    TransactionCreateResponse,
    TransactionDetail,
    TransactionListResponse,
)

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.get(
    "",
    response_model=DataResponse[TransactionListResponse],
    summary="거래 목록 조회",
    description=(
        "내 거래 목록을 조회합니다.\n\n"
        "**role 파라미터:**\n"
        "- `borrower`: 빌린 거래\n"
        "- `lender`: 빌려준 거래\n"
        "- 미입력 시 전체 조회"
    ),
)
async def list_transactions(
    role: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_transactions_service),
):
    return {"data": service.list_transactions(current_user["id"], role, page, size)}


@router.post(
    "",
    response_model=DataResponse[TransactionCreateResponse],
    summary="거래 완료 처리",
    description="채팅방 기준으로 거래를 완료 처리합니다. 게시글 상태가 COMPLETED로 변경됩니다.",
)
async def create_transaction(
    body: TransactionCreate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_transactions_service),
):
    return {"data": service.create_transaction(current_user["id"], body)}


@router.get(
    "/{transaction_id}",
    response_model=DataResponse[TransactionDetail],
    summary="거래 상세 조회",
    description="거래 상세 정보 및 리뷰 현황을 조회합니다.",
)
async def get_transaction(
    transaction_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_transactions_service),
):
    return {"data": service.get_transaction(transaction_id, current_user["id"])}


@router.post(
    "/{transaction_id}/reviews",
    response_model=DataResponse[ReviewResponse],
    summary="리뷰 작성",
    description="거래 상대방에 대한 리뷰를 작성합니다. 거래당 1회만 작성 가능합니다.",
)
async def create_review(
    transaction_id: int,
    body: ReviewCreate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_transactions_service),
):
    return {"data": service.create_review(transaction_id, current_user["id"], body)}
