class ChatsService:
    def list_chat_rooms(self, user_id: int, type_filter: str, page: int, size: int) -> dict:
        raise NotImplementedError

    def get_chat_room(self, chat_room_id: int, user_id: int) -> dict:
        raise NotImplementedError

    def list_messages(self, chat_room_id: int, user_id: int, cursor: int | None, size: int) -> dict:
        raise NotImplementedError

    def send_message(self, chat_room_id: int, user_id: int, data: dict) -> dict:
        raise NotImplementedError

    def mark_read(self, chat_room_id: int, user_id: int, last_read_message_id: int) -> dict:
        raise NotImplementedError
