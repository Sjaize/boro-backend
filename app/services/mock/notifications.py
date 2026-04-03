class MockNotificationsService:
    def list_notifications(self, user_id: int, page: int, size: int) -> dict:
        return {
            "notifications": [
                {
                    "id": 1,
                    "type": "urgent_post",
                    "title": "근처에 긴급 게시글이 올라왔어요",
                    "body": "보조배터리 급하게 빌려드려요",
                    "related_post_id": 101,
                    "related_chat_room_id": None,
                    "is_read": False,
                    "created_at": "2026-03-30T09:39:00Z",
                },
                {
                    "id": 2,
                    "type": "interest_post",
                    "title": "관심 키워드 게시글이 올라왔어요",
                    "body": "캠핑 의자 빌려드려요",
                    "related_post_id": 102,
                    "related_chat_room_id": None,
                    "is_read": False,
                    "created_at": "2026-03-30T09:35:00Z",
                },
                {
                    "id": 3,
                    "type": "chat_message",
                    "title": "새로운 채팅 메시지가 도착했어요",
                    "body": "오늘 6시에 거래 가능하신가요?",
                    "related_post_id": 101,
                    "related_chat_room_id": 55,
                    "is_read": True,
                    "created_at": "2026-03-30T09:20:00Z",
                },
            ],
            "page": page,
            "size": size,
            "has_next": False,
        }

    def register_device_token(self, user_id: int, data) -> dict:
        payload = self._to_payload(data)
        return {
            "device_token": payload.get("device_token", "mock-device-token"),
            "platform": payload.get("platform", "android"),
            "is_active": True,
        }

    def unregister_device_token(self, user_id: int, data) -> dict:
        payload = self._to_payload(data)
        return {
            "device_token": payload.get("device_token", "mock-device-token"),
            "deleted": True,
        }

    def mark_read(self, notification_id: int, user_id: int) -> dict:
        return {"id": notification_id, "is_read": True}

    def _to_payload(self, data) -> dict:
        if hasattr(data, "model_dump"):
            return data.model_dump(exclude_none=True)
        if isinstance(data, dict):
            return data
        return {}
