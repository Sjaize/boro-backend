from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from math import asin, cos, radians, sin, sqrt

from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.notification import Notification
from app.models.post import Post
from app.repositories.notification import NotificationRepository

EARTH_RADIUS_M = 6_371_000
URGENT_LOCATION_MAX_AGE_HOURS = 6
URGENT_POST_TITLE = "\uadfc\ucc98\uc5d0 \uae34\uae09 \uac8c\uc2dc\uae00\uc774 \uc62c\ub77c\uc654\uc5b4\uc694"
NOTIFICATION_NOT_FOUND_MESSAGE = "\uc54c\ub9bc\uc744 \ucc3e\uc744 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4."


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

        self.repo.create_notifications(notifications)
        return len(notifications)

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

    def _utcnow(self) -> datetime:
        return datetime.now(UTC).replace(tzinfo=None)
