class NotificationsService:
    def list_notifications(self, user_id: int, page: int, size: int) -> dict:
        raise NotImplementedError

    def mark_read(self, notification_id: int, user_id: int) -> dict:
        raise NotImplementedError
