class MockNotificationsService:
    def list_notifications(self, user_id: int, page: int, size: int) -> dict:
        return {
            "notifications": [
                {
                    "id": 1,
                    "type": "urgent_post",
                    "title": "주변에 물건이 필요한 사람이 있어요!",
                    "body": "보조배터리 필요해요",
                    "related_post_id": 101,
                    "related_chat_room_id": None,
                    "is_read": False,
                    "created_at": "2026-03-30T09:39:00Z",
                },
                {
                    "id": 2,
                    "type": "interest_post",
                    "title": "관심 키워드 등록한 물건 게시글이 올라왔어요!",
                    "body": "보조배터리 빌려드려요",
                    "related_post_id": 102,
                    "related_chat_room_id": None,
                    "is_read": False,
                    "created_at": "2026-03-30T09:35:00Z",
                },
                {
                    "id": 3,
                    "type": "chat_message",
                    "title": "새로운 채팅 메시지가 도착했어요!",
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

    def mark_read(self, notification_id: int, user_id: int) -> dict:
        return {"id": notification_id, "is_read": True}
