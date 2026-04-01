class MockChatsService:
    def list_chat_rooms(self, user_id: int, type_filter: str, page: int, size: int) -> dict:
        return {
            "chat_rooms": [
                {
                    "chat_room_id": 55,
                    "post_id": 101,
                    "post_type": "BORROW",
                    "post_title": "보조배터리 구해요",
                    "partner_nickname": "배터리왕",
                    "partner_profile_image_url": "https://picsum.photos/seed/user3/200",
                    "last_message_preview": "보조배터리 필요하시는 글 보고 연락드렸어요",
                    "last_message_at": "2026-03-30T09:39:00Z",
                    "unread_count": 3,
                },
                {
                    "chat_room_id": 56,
                    "post_id": 102,
                    "post_type": "LEND",
                    "post_title": "전동 드릴 빌려드려요",
                    "partner_nickname": "공구장인",
                    "partner_profile_image_url": "https://picsum.photos/seed/user4/200",
                    "last_message_preview": "내일 오전 10시에 역삼역 어떠세요?",
                    "last_message_at": "2026-03-30T08:15:00Z",
                    "unread_count": 0,
                },
            ],
            "page": page,
            "size": size,
            "has_next": False,
        }

    def get_chat_room(self, chat_room_id: int, user_id: int) -> dict:
        return {
            "chat_room_id": chat_room_id,
            "post": {
                "post_id": 101,
                "title": "보조배터리 구해요",
                "price": 1100,
                "rental_period_text": "1시간",
                "post_image_url": "https://picsum.photos/seed/post101/400/300",
                "post_type": "BORROW",
            },
            "participants": [
                {
                    "user_id": 1,
                    "nickname": "홍길동",
                    "profile_image_url": "https://picsum.photos/seed/user1/200",
                    "role": "borrower",
                },
                {
                    "user_id": 2,
                    "nickname": "배터리왕",
                    "profile_image_url": "https://picsum.photos/seed/user3/200",
                    "role": "lender",
                },
            ],
            "last_read_message_id": 203,
            "unread_count": 3,
            "transaction_completed": False,
        }

    def list_messages(self, chat_room_id: int, user_id: int, cursor: int | None, size: int) -> dict:
        return {
            "messages": [
                {
                    "message_id": 201,
                    "sender_user_id": 1,
                    "message_type": "text",
                    "content": "안녕하세요! 보조배터리 아직 필요하신가요?",
                    "created_at": "2026-03-30T15:58:00Z",
                    "is_mine": True,
                },
                {
                    "message_id": 202,
                    "sender_user_id": 2,
                    "message_type": "text",
                    "content": "네, 오늘 오후에 가능해요!",
                    "created_at": "2026-03-30T15:59:00Z",
                    "is_mine": False,
                },
                {
                    "message_id": 203,
                    "sender_user_id": 1,
                    "message_type": "text",
                    "content": "그럼 3시에 역삼역 3번 출구 어떠세요?",
                    "created_at": "2026-03-30T16:00:00Z",
                    "is_mine": True,
                },
            ],
            "next_cursor": None,
            "has_next": False,
        }

    def send_message(self, chat_room_id: int, user_id: int, data: dict) -> dict:
        return {
            "message_id": 210,
            "chat_room_id": chat_room_id,
            "sender_user_id": user_id,
            "message_type": data.get("message_type", "text"),
            "content": data.get("content", ""),
            "created_at": "2026-04-01T10:00:00Z",
            "is_mine": True,
        }

    def mark_read(self, chat_room_id: int, user_id: int, last_read_message_id: int) -> dict:
        return {
            "chat_room_id": chat_room_id,
            "last_read_message_id": last_read_message_id,
            "unread_count": 0,
        }
