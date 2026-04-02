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


@router.get("", response_model=DataResponse[TransactionListResponse])
async def list_transactions(
    role: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_transactions_service),
):
    return {"data": service.list_transactions(current_user["id"], role, page, size)}


@router.post("", response_model=DataResponse[TransactionCreateResponse])
async def create_transaction(
    body: TransactionCreate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_transactions_service),
):
    return {"data": service.create_transaction(current_user["id"], body)}


@router.get("/{transaction_id}", response_model=DataResponse[TransactionDetail])
async def get_transaction(
    transaction_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_transactions_service),
):
    return {"data": service.get_transaction(transaction_id, current_user["id"])}


@router.post("/{transaction_id}/reviews", response_model=DataResponse[ReviewResponse])
async def create_review(
    transaction_id: int,
    body: ReviewCreate,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_transactions_service),
):
    return {"data": service.create_review(transaction_id, current_user["id"], body)}
