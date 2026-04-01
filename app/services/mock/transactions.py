class MockTransactionsService:
    def list_transactions(self, user_id: int, role: str | None, page: int, size: int) -> dict:
        return {
            "transactions": [
                {
                    "transaction_id": 1,
                    "post_id": 101,
                    "chat_room_id": 55,
                    "role": "borrower",
                    "post_title": "보조배터리 구해요",
                    "post_image_url": "https://picsum.photos/seed/post101/400/300",
                    "price": 1100,
                    "rental_period_text": "1시간",
                    "chat_count": 0,
                    "like_count": 0,
                    "completed_at": "2026-03-30T09:41:00Z",
                    "review": {"has_received_review": True},
                },
                {
                    "transaction_id": 2,
                    "post_id": 102,
                    "chat_room_id": 56,
                    "role": "borrower",
                    "post_title": "우산 구해요",
                    "post_image_url": "https://picsum.photos/seed/post102/400/300",
                    "price": 2000,
                    "rental_period_text": "반나절",
                    "chat_count": 1,
                    "like_count": 2,
                    "completed_at": "2026-03-28T09:36:00Z",
                    "review": {"has_received_review": False},
                },
            ],
            "page": page,
            "size": size,
            "has_next": False,
        }

    def create_transaction(self, user_id: int, data: dict) -> dict:
        return {
            "transaction_id": 10,
            "post_id": data.get("post_id"),
            "chat_room_id": data.get("chat_room_id"),
            "lender_user_id": 2,
            "borrower_user_id": user_id,
            "completed_at": "2026-04-01T10:00:00Z",
        }

    def get_transaction(self, transaction_id: int, user_id: int) -> dict:
        return {
            "transaction_id": transaction_id,
            "post_id": 101,
            "chat_room_id": 55,
            "lender_user_id": 2,
            "borrower_user_id": 1,
            "my_role": "borrower",
            "completed_at": "2026-03-30T09:41:00Z",
            "post": {
                "title": "보조배터리 구해요",
                "content": "1시간 정도 빌리고 싶어요.",
                "price": 1100,
                "category": "전자기기",
                "rental_period_text": "1시간",
                "meeting_place_text": "경희대 국제캠 정문 앞",
                "region_name": "영통동",
                "post_image_urls": ["https://picsum.photos/seed/post101/400/300"],
                "chat_count": 0,
                "like_count": 0,
            },
            "review": {
                "has_received_review": True,
                "rating": 5,
                "comment": "시간 약속 잘 지켜주셨어요.",
                "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"],
            },
        }

    def create_review(self, transaction_id: int, user_id: int, data: dict) -> dict:
        return {
            "review_id": 20,
            "transaction_id": transaction_id,
            "rating": data.get("rating"),
            "comment": data.get("comment"),
            "tags": data.get("tags", []),
            "created_at": "2026-04-01T10:00:00Z",
        }
