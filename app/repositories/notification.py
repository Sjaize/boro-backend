from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification, UserDeviceToken
from app.models.user import User, UserInterestKeyword


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

    def upsert_device_token(self, *, user_id: int, device_token: str, platform: str) -> UserDeviceToken:
        now = datetime.now(UTC).replace(tzinfo=None)
        token = (
            self.db.execute(
                select(UserDeviceToken).where(UserDeviceToken.device_token == device_token)
            )
            .scalars()
            .one_or_none()
        )

        if token is None:
            token = UserDeviceToken(
                user_id=user_id,
                device_token=device_token,
                platform=platform,
                is_active=True,
                last_seen_at=now,
            )
        else:
            token.user_id = user_id
            token.platform = platform
            token.is_active = True
            token.last_seen_at = now

        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def deactivate_device_token(self, *, user_id: int, device_token: str) -> bool:
        token = (
            self.db.execute(
                select(UserDeviceToken)
                .where(UserDeviceToken.user_id == user_id)
                .where(UserDeviceToken.device_token == device_token)
                .where(UserDeviceToken.is_active.is_(True))
            )
            .scalars()
            .one_or_none()
        )

        if token is None:
            return False

        token.is_active = False
        self.db.add(token)
        self.db.commit()
        return True

    def deactivate_device_tokens(self, device_tokens: list[str]) -> None:
        if not device_tokens:
            return

        tokens = (
            self.db.execute(
                select(UserDeviceToken).where(UserDeviceToken.device_token.in_(device_tokens))
            )
            .scalars()
            .all()
        )

        if not tokens:
            return

        for token in tokens:
            token.is_active = False
            self.db.add(token)

        self.db.commit()

    def find_active_device_tokens_by_user_ids(self, user_ids: list[int]) -> list[UserDeviceToken]:
        if not user_ids:
            return []

        statement = (
            select(UserDeviceToken)
            .where(UserDeviceToken.user_id.in_(user_ids))
            .where(UserDeviceToken.is_active.is_(True))
        )
        return list(self.db.execute(statement).scalars().all())

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

    def find_interest_keyword_candidates(
        self,
        *,
        excluded_user_id: int,
        title: str,
        category: str,
    ) -> list[int]:
        rows = (
            self.db.execute(
                select(UserInterestKeyword.user_id, UserInterestKeyword.keyword)
                .join(User, User.id == UserInterestKeyword.user_id)
                .where(User.id != excluded_user_id)
                .where(User.status == "active")
            )
            .all()
        )

        title_lower = title.lower()
        category_lower = category.lower()

        matched: set[int] = set()
        for user_id, keyword in rows:
            kw = keyword.lower()
            if kw in title_lower or kw in category_lower:
                matched.add(user_id)

        return list(matched)

    def create_notifications(self, notifications: list[Notification]) -> list[Notification]:
        if not notifications:
            return []

        self.db.add_all(notifications)
        self.db.commit()

        for notification in notifications:
            self.db.refresh(notification)

        return notifications
