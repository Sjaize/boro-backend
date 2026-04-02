from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.repositories.notification import NotificationRepository


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
            raise NotFoundError("알림을 찾을 수 없습니다.")
        if notification.user_id != user_id:
            raise ForbiddenError()
        notification = self.repo.mark_read(notification)
        return {"id": notification.id, "is_read": notification.is_read}
