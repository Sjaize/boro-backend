class UsersService:
    def get_my_profile(self, user_id: int) -> dict:
        raise NotImplementedError

    def update_my_profile(self, user_id: int, data: dict) -> dict:
        raise NotImplementedError

    def update_location(self, user_id: int, lat: float, lng: float) -> dict:
        raise NotImplementedError

    def update_settings(self, user_id: int, data: dict) -> dict:
        raise NotImplementedError

    def get_user_profile(self, user_id: int) -> dict:
        raise NotImplementedError

    def get_user_reviews(self, user_id: int, page: int, size: int) -> dict:
        raise NotImplementedError

    def get_my_posts(self, user_id: int, post_type: str | None, page: int, size: int) -> dict:
        raise NotImplementedError

    def get_user_posts(self, user_id: int, post_type: str | None, page: int, size: int) -> dict:
        raise NotImplementedError

    def get_my_likes(self, user_id: int, page: int, size: int) -> dict:
        raise NotImplementedError
