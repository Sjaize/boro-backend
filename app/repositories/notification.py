from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all_by_user_id(self, user_id: int, page: int, size: int) -> tuple[list[Notification], bool]:
        offset = (page - 1) * size
        items = (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .offset(offset)
            .limit(size + 1)
            .all()
        )
        has_next = len(items) > size
        return items[:size], has_next

    def find_by_id(self, notification_id: int) -> Notification | None:
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def mark_read(self, notification: Notification) -> Notification:
        notification.is_read = True
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def find_recent_location_candidates(
        self,
        *,
        excluded_user_id: int,
        updated_after: datetime,
    ) -> list[User]:
        statement = (
            select(User)
            .where(User.id != excluded_user_id)
            .where(User.status == "active")
            .where(User.nearby_urgent_alerts_enabled.is_(True))
            .where(User.current_lat.is_not(None))
            .where(User.current_lng.is_not(None))
            .where(User.location_updated_at.is_not(None))
            .where(User.notification_radius_m.is_not(None))
            .where(User.notification_radius_m > 0)
            .where(User.location_updated_at >= updated_after)
        )
        return list(self.db.execute(statement).scalars().all())

    def create_notifications(self, notifications: list[Notification]) -> list[Notification]:
        if not notifications:
            return []

        self.db.add_all(notifications)
        self.db.commit()

        for notification in notifications:
            self.db.refresh(notification)

        return notifications
