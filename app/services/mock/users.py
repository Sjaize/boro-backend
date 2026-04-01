class MockUsersService:
    def get_my_profile(self, user_id: int) -> dict:
        return {
            "id": 1,
            "nickname": "홍길동",
            "profile_image_url": "https://picsum.photos/seed/user1/200",
            "region_name": "역삼동",
            "trust_score": 4.8,
            "borrow_count": 3,
            "lend_count": 5,
            "like_count": 12,
        }

    def update_my_profile(self, user_id: int, data: dict) -> dict:
        return {
            "id": 1,
            "nickname": data.get("nickname", "홍길동"),
            "profile_image_url": data.get("profile_image_url", "https://picsum.photos/seed/user1/200"),
        }

    def update_location(self, user_id: int, lat: float, lng: float) -> dict:
        return {
            "region_name": "강남구",
            "full_address": "서울특별시 강남구 역삼동",
            "lat": lat,
            "lng": lng,
        }

    def update_settings(self, user_id: int, data: dict) -> dict:
        return {
            "notification_radius_m": data.get("notification_radius_m", 1500),
            "interest_keywords": data.get("interest_keywords", ["전자기기", "가구"]),
        }

    def get_user_profile(self, user_id: int) -> dict:
        return {
            "id": user_id,
            "nickname": f"유저{user_id}",
            "profile_image_url": f"https://picsum.photos/seed/user{user_id}/200",
            "region_name": "역삼동",
            "completed_transaction_count": 10,
            "trust_score": 4.7,
            "review_count": 8,
        }

    def get_user_reviews(self, user_id: int, page: int, size: int) -> dict:
        return {
            "reviews": [
                {
                    "review_id": 1,
                    "rating": 5,
                    "comment": "시간 약속을 잘 지켜줬어요!",
                    "created_at": "2026-03-30T12:34:56Z",
                },
                {
                    "review_id": 2,
                    "rating": 4,
                    "comment": "물건 상태가 설명과 일치했어요.",
                    "created_at": "2026-03-28T09:00:00Z",
                },
            ],
            "page": page,
            "size": size,
            "has_next": False,
        }

    def get_my_posts(self, user_id: int, post_type: str | None, page: int, size: int) -> dict:
        return {
            "posts": [
                {
                    "post_id": 1,
                    "title": "보조배터리 구해요",
                    "post_type": "BORROW",
                    "price": 1100,
                    "region_name": "역삼동",
                    "like_count": 3,
                    "chat_count": 2,
                    "status": "AVAILABLE",
                    "created_at": "2026-03-30T12:34:56Z",
                },
                {
                    "post_id": 2,
                    "title": "우산 빌려드려요",
                    "post_type": "LEND",
                    "price": 2000,
                    "region_name": "역삼동",
                    "like_count": 5,
                    "chat_count": 1,
                    "status": "AVAILABLE",
                    "created_at": "2026-03-29T10:00:00Z",
                },
            ],
            "page": page,
            "size": size,
            "has_next": False,
        }

    def get_user_posts(self, user_id: int, post_type: str | None, page: int, size: int) -> dict:
        return {
            "posts": [
                {
                    "post_id": 3,
                    "title": "드릴 빌려드려요",
                    "post_type": "LEND",
                    "price": 5000,
                    "region_name": "역삼동",
                    "like_count": 2,
                    "chat_count": 0,
                    "status": "AVAILABLE",
                    "created_at": "2026-03-27T08:00:00Z",
                }
            ],
            "page": page,
            "size": size,
            "has_next": False,
        }

    def get_my_likes(self, user_id: int, page: int, size: int) -> dict:
        return {
            "posts": [
                {
                    "post_id": 5,
                    "title": "캠핑 의자 빌려드려요",
                    "post_type": "LEND",
                    "price": 3000,
                    "region_name": "강남구",
                    "like_count": 8,
                    "chat_count": 3,
                    "status": "AVAILABLE",
                    "created_at": "2026-03-25T14:00:00Z",
                }
            ],
            "page": page,
            "size": size,
            "has_next": False,
        }
