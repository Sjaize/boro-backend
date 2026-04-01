from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_notifications_service

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("")
async def list_notifications(
    page: int = Query(1),
    size: int = Query(20),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_notifications_service),
):
    return {"data": service.list_notifications(current_user["id"], page, size)}


@router.patch("/{notification_id}/read")
async def mark_read(
    notification_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_notifications_service),
):
    return {"data": service.mark_read(notification_id, current_user["id"])}
