class MockPostsService:
    def list_posts(self, filters: dict) -> dict:
        return {
            "posts": [
                {
                    "post_id": 1,
                    "title": "전동 드릴 빌려드려요",
                    "post_type": "LEND",
                    "price": 5000,
                    "region_name": "역삼동",
                    "is_urgent": False,
                    "thumbnail_url": "https://picsum.photos/seed/post1/400/300",
                    "like_count": 5,
                    "chat_count": 2,
                    "status": "AVAILABLE",
                    "created_at": "2026-03-31T09:00:00Z",
                },
                {
                    "post_id": 2,
                    "title": "보조배터리 급하게 필요해요",
                    "post_type": "BORROW",
                    "price": 1000,
                    "region_name": "강남구",
                    "is_urgent": True,
                    "thumbnail_url": None,
                    "like_count": 2,
                    "chat_count": 4,
                    "status": "AVAILABLE",
                    "created_at": "2026-03-31T08:30:00Z",
                },
                {
                    "post_id": 3,
                    "title": "캠핑 텐트 대여해드려요",
                    "post_type": "LEND",
                    "price": 15000,
                    "region_name": "서초구",
                    "is_urgent": False,
                    "thumbnail_url": "https://picsum.photos/seed/post3/400/300",
                    "like_count": 12,
                    "chat_count": 7,
                    "status": "AVAILABLE",
                    "created_at": "2026-03-30T17:00:00Z",
                },
            ],
            "page": filters.get("page", 1),
            "size": filters.get("size", 20),
            "has_next": False,
        }

    def create_post(self, user_id: int, data: dict) -> dict:
        return {"post_id": 101}

    def get_post(self, post_id: int, user_id: int) -> dict:
        return {
            "post_id": post_id,
            "author": {
                "user_id": 2,
                "nickname": "동네주민",
                "profile_image_url": "https://picsum.photos/seed/user2/200",
                "trust_score": 4.8,
            },
            "post_type": "LEND",
            "title": "전동 드릴 빌려드려요",
            "content": "거의 새것입니다. 1일 기준 대여해드려요. 역삼역 근처에서 직거래 가능합니다.",
            "price": 5000,
            "category": "공구",
            "is_urgent": False,
            "rental_period_text": "1일 기준",
            "meeting_place_text": "역삼역 3번 출구",
            "region_name": "역삼동",
            "lat": 37.5006,
            "lng": 127.0364,
            "images": [
                {"image_url": "https://picsum.photos/seed/post1a/800/600", "sort_order": 1},
                {"image_url": "https://picsum.photos/seed/post1b/800/600", "sort_order": 2},
            ],
            "like_count": 5,
            "chat_count": 2,
            "status": "AVAILABLE",
            "is_liked_by_me": False,
            "created_at": "2026-03-31T09:00:00Z",
        }

    def update_post(self, post_id: int, user_id: int, data: dict) -> dict:
        return {"post_id": post_id}

    def delete_post(self, post_id: int, user_id: int) -> dict:
        return {"post_id": post_id, "deleted": True}

    def like_post(self, post_id: int, user_id: int) -> dict:
        return {"post_id": post_id, "like_count": 6, "is_liked": True}

    def unlike_post(self, post_id: int, user_id: int) -> dict:
        return {"post_id": post_id, "like_count": 5, "is_liked": False}

    def create_chat_from_post(self, post_id: int, user_id: int) -> dict:
        return {"chat_room_id": 12, "is_new": True}
