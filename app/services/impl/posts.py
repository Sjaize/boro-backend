class PostsService:
    def list_posts(self, filters: dict) -> dict:
        raise NotImplementedError

    def create_post(self, user_id: int, data: dict) -> dict:
        raise NotImplementedError

    def get_post(self, post_id: int, user_id: int) -> dict:
        raise NotImplementedError

    def update_post(self, post_id: int, user_id: int, data: dict) -> dict:
        raise NotImplementedError

    def delete_post(self, post_id: int, user_id: int) -> dict:
        raise NotImplementedError

    def like_post(self, post_id: int, user_id: int) -> dict:
        raise NotImplementedError

    def unlike_post(self, post_id: int, user_id: int) -> dict:
        raise NotImplementedError

    def create_chat_from_post(self, post_id: int, user_id: int) -> dict:
        raise NotImplementedError
