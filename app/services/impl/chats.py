from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.chats import ChatsRepository
from app.core.exceptions import NotFoundError, ForbiddenError
from app.models.user import User

class ChatsService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ChatsRepository(db)

    def list_chat_rooms(self, user_id: int, type_filter: str, page: int, size: int) -> dict:
        chat_rooms = self.repo.list_chat_rooms(user_id, type_filter, page, size)
        total_count = self.repo.count_chat_rooms(user_id, type_filter)
        
        result = []
        for cr in chat_rooms:
            # Find the partner
            partner = None
            my_participant = None
            for p in cr.participants:
                if p.user_id != user_id:
                    partner = p
                else:
                    my_participant = p
            
            if not partner:
                continue
                
            partner_user = partner.user
            
            result.append({
                "chat_room_id": cr.id,
                "post_id": cr.post_id,
                "post_type": cr.post.post_type,
                "post_title": cr.post.title,
                "partner_nickname": partner_user.nickname if partner_user else "알 수 없음",
                "partner_profile_image_url": partner_user.profile_image_url if partner_user else None,
                "last_message_preview": cr.last_message_preview,
                "last_message_at": cr.last_message_at,
                "unread_count": my_participant.unread_count if my_participant else 0,
            })
            
        return {
            "chat_rooms": result,
            "page": page,
            "size": size,
            "has_next": total_count > page * size
        }

    def get_chat_room(self, chat_room_id: int, user_id: int) -> dict:
        cr = self.repo.get_chat_room(chat_room_id)
        if not cr:
            raise NotFoundError("채팅방을 찾을 수 없습니다.")
            
        my_participant = None
        participants = []
        for p in cr.participants:
            if p.user_id == user_id:
                my_participant = p
            
            user = p.user
            participants.append({
                "user_id": p.user_id,
                "nickname": user.nickname if user else "알 수 없음",
                "profile_image_url": user.profile_image_url if user else None,
                "role": p.role
            })
            
        if not my_participant:
            raise ForbiddenError("채팅방에 참여하고 있지 않습니다.")
            
        post = cr.post
        post_image = post.images[0].image_url if post.images else None
        
        return {
            "chat_room_id": cr.id,
            "post": {
                "post_id": post.id,
                "title": post.title,
                "price": post.price,
                "rental_period_text": post.rental_period_text,
                "post_image_url": post_image,
                "post_type": post.post_type
            },
            "participants": participants,
            "last_read_message_id": my_participant.last_read_message_id,
            "unread_count": my_participant.unread_count,
            "transaction_completed": self.repo.is_transaction_completed(chat_room_id)
        }

    def list_messages(self, chat_room_id: int, user_id: int, cursor: int | None, size: int) -> dict:
        my_participant = self.repo.get_participant(chat_room_id, user_id)
        if not my_participant:
            raise ForbiddenError("채팅방에 참여하고 있지 않습니다.")
            
        messages = self.repo.list_messages(chat_room_id, cursor, size)
        
        result = []
        for msg in messages:
            result.append({
                "message_id": msg.id,
                "sender_user_id": msg.sender_user_id,
                "message_type": msg.message_type,
                "content": msg.content,
                "created_at": msg.created_at,
                "is_mine": msg.sender_user_id == user_id
            })
            
        next_cursor = result[-1]["message_id"] if len(result) == size else None
        
        return {
            "messages": result,
            "next_cursor": next_cursor,
            "has_next": len(result) == size
        }

    def send_message(self, chat_room_id: int, user_id: int, data: dict) -> dict:
        my_participant = self.repo.get_participant(chat_room_id, user_id)
        if not my_participant:
            raise ForbiddenError("채팅방에 참여하고 있지 않습니다.")
            
        message = self.repo.create_message(
            chat_room_id,
            user_id,
            data.get("message_type", "text"),
            data.get("content", "")
        )
        
        # Update chat room last message
        self.repo.update_last_message(chat_room_id, message.content, message.created_at)
        
        # Increment unread count for others
        self.repo.increment_unread_counts(chat_room_id, user_id)
        
        self.db.commit()
        
        return {
            "message_id": message.id,
            "chat_room_id": chat_room_id,
            "sender_user_id": user_id,
            "message_type": message.message_type,
            "content": message.content,
            "created_at": message.created_at,
            "is_mine": True
        }

    def mark_read(self, chat_room_id: int, user_id: int, last_read_message_id: int) -> dict:
        my_participant = self.repo.mark_as_read(chat_room_id, user_id, last_read_message_id)
        if not my_participant:
            raise ForbiddenError("채팅방에 참여하고 있지 않습니다.")
            
        self.db.commit()
        
        return {
            "chat_room_id": chat_room_id,
            "last_read_message_id": last_read_message_id,
            "unread_count": 0
        }
