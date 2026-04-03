from __future__ import annotations

import json
import logging
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from math import asin, cos, radians, sin, sqrt
from pathlib import Path

import httpx
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import BadRequestError, ForbiddenError, NotFoundError
from app.models.notification import Notification, UserDeviceToken
from app.models.post import Post
from app.repositories.notification import NotificationRepository

EARTH_RADIUS_M = 6_371_000
URGENT_LOCATION_MAX_AGE_HOURS = 6
URGENT_POST_TITLE = "근처에 긴급 게시글이 올라왔어요"
NOTIFICATION_NOT_FOUND_MESSAGE = "알림을 찾을 수 없습니다."
ALLOWED_PLATFORMS = {"android", "ios", "web"}
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
FCM_SCOPE = "https://www.googleapis.com/auth/firebase.messaging"

logger = logging.getLogger(__name__)


class NotificationsService:
    def __init__(self, db: Session):
        self.repo = NotificationRepository(db)

    def list_notifications(self, user_id: int, page: int, size: int) -> dict:
        notifications, has_next = self.repo.find_all_by_user_id(user_id, page, size)
        return {
            "notifications": [
                {
                    "id": n.id,
                    "type": n.type,
                    "title": n.title,
                    "body": n.body,
                    "related_post_id": n.related_post_id,
                    "related_chat_room_id": n.related_chat_room_id,
                    "is_read": n.is_read,
                    "created_at": n.created_at.isoformat(),
                }
                for n in notifications
            ],
            "page": page,
            "size": size,
            "has_next": has_next,
        }

    def register_device_token(self, user_id: int, data) -> dict:
        payload = self._to_payload(data)
        device_token = self._normalize_required_string(payload.get("device_token"), "device_token")
        platform = self._normalize_platform(payload.get("platform"))

        token = self.repo.upsert_device_token(
            user_id=user_id,
            device_token=device_token,
            platform=platform,
        )
        return self._serialize_device_token(token)

    def unregister_device_token(self, user_id: int, data) -> dict:
        payload = self._to_payload(data)
        device_token = self._normalize_required_string(payload.get("device_token"), "device_token")
        deleted = self.repo.deactivate_device_token(user_id=user_id, device_token=device_token)
        return {"device_token": device_token, "deleted": deleted}

    def mark_read(self, notification_id: int, user_id: int) -> dict:
        notification = self.repo.find_by_id(notification_id)
        if not notification:
            raise NotFoundError(NOTIFICATION_NOT_FOUND_MESSAGE)
        if notification.user_id != user_id:
            raise ForbiddenError()
        notification = self.repo.mark_read(notification)
        return {"id": notification.id, "is_read": notification.is_read}

    def notify_urgent_post(self, post: Post) -> int:
        if not post.is_urgent:
            return 0

        if post.lat is None or post.lng is None:
            return 0

        candidates = self.repo.find_recent_location_candidates(
            excluded_user_id=post.user_id,
            updated_after=self._utcnow() - timedelta(hours=URGENT_LOCATION_MAX_AGE_HOURS),
        )

        notifications: list[Notification] = []
        for user in candidates:
            if user.current_lat is None or user.current_lng is None:
                continue

            distance_m = self._calculate_distance_m(
                post.lat,
                post.lng,
                user.current_lat,
                user.current_lng,
            )
            notification_radius_m = int(user.notification_radius_m or 0)
            if distance_m > notification_radius_m:
                continue

            notifications.append(
                Notification(
                    user_id=user.id,
                    type="urgent_post",
                    title=URGENT_POST_TITLE,
                    body=post.title,
                    related_post_id=post.id,
                )
            )

        persisted_notifications = self.repo.create_notifications(notifications)
        invalid_device_tokens = self._send_push_notifications(persisted_notifications)
        if invalid_device_tokens:
            self.repo.deactivate_device_tokens(invalid_device_tokens)

        return len(persisted_notifications)

    def _send_push_notifications(self, notifications: list[Notification]) -> list[str]:
        if not notifications:
            return []

        fcm_access_token, fcm_project_id = self._get_fcm_access_token_and_project_id()
        if not fcm_access_token or not fcm_project_id:
            return []

        user_ids = list({notification.user_id for notification in notifications})
        device_tokens = self.repo.find_active_device_tokens_by_user_ids(user_ids)
        if not device_tokens:
            return []

        tokens_by_user_id: dict[int, list[UserDeviceToken]] = {}
        for device_token in device_tokens:
            tokens_by_user_id.setdefault(device_token.user_id, []).append(device_token)

        invalid_device_tokens: list[str] = []
        for notification in notifications:
            for device_token in tokens_by_user_id.get(notification.user_id, []):
                result = self._send_single_fcm_message(
                    access_token=fcm_access_token,
                    project_id=fcm_project_id,
                    device_token=device_token,
                    notification=notification,
                )
                if result == "invalid":
                    invalid_device_tokens.append(device_token.device_token)

        return invalid_device_tokens

    def _send_single_fcm_message(
        self,
        *,
        access_token: str,
        project_id: str,
        device_token: UserDeviceToken,
        notification: Notification,
    ) -> str:
        request_body = {
            "message": {
                "token": device_token.device_token,
                "notification": {
                    "title": notification.title,
                    "body": notification.body,
                },
                "data": {
                    "type": notification.type,
                    "notification_id": str(notification.id),
                    "related_post_id": str(notification.related_post_id or ""),
                    "related_chat_room_id": str(notification.related_chat_room_id or ""),
                },
            }
        }
        request_url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

        try:
            response = httpx.post(
                request_url,
                json=request_body,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json; charset=UTF-8",
                },
                timeout=settings.FCM_TIMEOUT_SECONDS,
            )
        except httpx.HTTPError:
            logger.exception("Failed to send FCM push for notification %s", notification.id)
            return "failed"

        if response.is_success:
            return "sent"

        response_text = response.text
        if self._is_invalid_device_token_response(response.status_code, response_text):
            logger.warning("FCM token became invalid for user %s", device_token.user_id)
            return "invalid"

        logger.warning(
            "FCM send failed with status %s for notification %s: %s",
            response.status_code,
            notification.id,
            response_text,
        )
        return "failed"

    def _get_fcm_access_token_and_project_id(self) -> tuple[str | None, str | None]:
        # Try JSON string from env var first, then fall back to file path
        raw_json = settings.FCM_SERVICE_ACCOUNT_JSON.strip()
        if raw_json:
            try:
                service_account_info = json.loads(raw_json)
            except json.JSONDecodeError:
                logger.exception("FCM_SERVICE_ACCOUNT_JSON is not valid JSON.")
                return None, None
        else:
            service_account_path = settings.FCM_SERVICE_ACCOUNT_FILE.strip()
            if not service_account_path:
                return None, None

            service_account_file = Path(service_account_path)
            if not service_account_file.exists():
                logger.warning("FCM service account file was not found: %s", service_account_file)
                return None, None

            try:
                service_account_info = json.loads(service_account_file.read_text(encoding="utf-8"))
            except OSError:
                logger.exception("Unable to read FCM service account file.")
                return None, None
            except json.JSONDecodeError:
                logger.exception("FCM service account file is not valid JSON.")
                return None, None

        access_token = self._request_google_access_token(service_account_info)
        if access_token is None:
            return None, None

        project_id = settings.FCM_PROJECT_ID.strip() or service_account_info.get("project_id")
        if not project_id:
            logger.warning("FCM project id is missing.")
            return None, None

        return access_token, project_id

    def _request_google_access_token(self, service_account_info: dict) -> str | None:
        client_email = service_account_info.get("client_email")
        private_key = service_account_info.get("private_key")
        private_key_id = service_account_info.get("private_key_id")

        if not client_email or not private_key:
            logger.warning("FCM service account JSON is missing required fields.")
            return None

        now = int(datetime.now(UTC).timestamp())
        assertion = jwt.encode(
            {
                "iss": client_email,
                "scope": FCM_SCOPE,
                "aud": GOOGLE_TOKEN_URL,
                "iat": now,
                "exp": now + 3600,
            },
            private_key,
            algorithm="RS256",
            headers={"kid": private_key_id} if private_key_id else None,
        )

        try:
            response = httpx.post(
                GOOGLE_TOKEN_URL,
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                    "assertion": assertion,
                },
                timeout=settings.FCM_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except httpx.HTTPError:
            logger.exception("Failed to obtain Google access token for FCM.")
            return None

        return response.json().get("access_token")

    def _is_invalid_device_token_response(self, status_code: int, response_text: str) -> bool:
        if status_code in {404, 410}:
            return True

        normalized_text = response_text.upper()
        return "UNREGISTERED" in normalized_text or "REGISTRATION TOKEN" in normalized_text

    def _calculate_distance_m(
        self,
        origin_lat: Decimal | float,
        origin_lng: Decimal | float,
        target_lat: Decimal | float,
        target_lng: Decimal | float,
    ) -> float:
        origin_lat_rad = radians(float(origin_lat))
        origin_lng_rad = radians(float(origin_lng))
        target_lat_rad = radians(float(target_lat))
        target_lng_rad = radians(float(target_lng))

        lat_diff = target_lat_rad - origin_lat_rad
        lng_diff = target_lng_rad - origin_lng_rad

        haversine = (
            sin(lat_diff / 2) ** 2
            + cos(origin_lat_rad) * cos(target_lat_rad) * sin(lng_diff / 2) ** 2
        )
        arc = 2 * asin(sqrt(haversine))
        return EARTH_RADIUS_M * arc

    def _normalize_required_string(self, value, field_name: str) -> str:
        if value is None:
            raise BadRequestError(f"{field_name} is required.")

        normalized_value = str(value).strip()
        if not normalized_value:
            raise BadRequestError(f"{field_name} cannot be blank.")

        return normalized_value

    def _normalize_platform(self, value) -> str:
        normalized_value = self._normalize_required_string(value, "platform").lower()
        if normalized_value not in ALLOWED_PLATFORMS:
            raise BadRequestError("platform must be one of android, ios, web.")
        return normalized_value

    def _serialize_device_token(self, token: UserDeviceToken) -> dict:
        return {
            "device_token": token.device_token,
            "platform": token.platform,
            "is_active": token.is_active,
        }

    def _to_payload(self, data) -> dict:
        if hasattr(data, "model_dump"):
            return data.model_dump(exclude_none=True)

        if isinstance(data, dict):
            return data

        raise BadRequestError("Request body format is invalid.")

    def _utcnow(self) -> datetime:
        return datetime.now(UTC).replace(tzinfo=None)
