from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_notifications_service
from app.schemas.common import DataResponse
from app.schemas.notification import (
    DeviceTokenDeleteRequest,
    DeviceTokenDeleteResponse,
    DeviceTokenRegisterRequest,
    DeviceTokenResponse,
    NotificationListResponse,
    NotificationReadResponse,
)

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get(
    "",
    response_model=DataResponse[NotificationListResponse],
    summary="알림 목록 조회",
    description="내 알림 목록을 최신순으로 조회합니다.",
)
async def list_notifications(
    page: int = Query(1),
    size: int = Query(20),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_notifications_service),
):
    return {"data": service.list_notifications(current_user["id"], page, size)}


@router.post(
    "/device-tokens",
    response_model=DataResponse[DeviceTokenResponse],
    summary="디바이스 토큰 등록",
    description="FCM 또는 APNs 디바이스 토큰을 등록하거나 최신 상태로 갱신합니다.",
)
async def register_device_token(
    body: DeviceTokenRegisterRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_notifications_service),
):
    return {"data": service.register_device_token(current_user["id"], body)}


@router.delete(
    "/device-tokens",
    response_model=DataResponse[DeviceTokenDeleteResponse],
    summary="디바이스 토큰 비활성화",
    description="로그아웃 또는 앱 제거 시 해당 디바이스 토큰을 비활성화합니다.",
)
async def unregister_device_token(
    body: DeviceTokenDeleteRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_notifications_service),
):
    return {"data": service.unregister_device_token(current_user["id"], body)}


@router.patch(
    "/{notification_id}/read",
    response_model=DataResponse[NotificationReadResponse],
    summary="알림 읽음 처리",
    description="특정 알림을 읽음 상태로 변경합니다.",
)
async def mark_read(
    notification_id: int,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_notifications_service),
):
    return {"data": service.mark_read(notification_id, current_user["id"])}
