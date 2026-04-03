import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.chats import ChatsRepository
from app.core.exceptions import NotFoundError, ForbiddenError
from app.models.user import User

logger = logging.getLogger(__name__)

class ChatsService:
    def __init__(self, db: Session, ws_manager=None):
        self.db = db
        self.repo = ChatsRepository(db)
        self.ws_manager = ws_manager

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
            
        # 상대방의 마지막 읽은 메시지 ID 가져오기
        participants = self.repo.get_participants(chat_room_id)
        partner = next((p for p in participants if p.user_id != user_id), None)
        partner_last_read_id = partner.last_read_message_id if partner and partner.last_read_message_id else 0
            
        messages = self.repo.list_messages(chat_room_id, cursor, size)
        
        result = []
        for msg in messages:
            result.append({
                "message_id": msg.id,
                "sender_user_id": msg.sender_user_id,
                "message_type": msg.message_type,
                "content": msg.content,
                "created_at": msg.created_at,
                "is_mine": msg.sender_user_id == user_id,
                "is_read": msg.id <= partner_last_read_id
            })
            
        next_cursor = result[-1]["message_id"] if len(result) == size else None
        
        return {
            "messages": result,
            "next_cursor": next_cursor,
            "has_next": len(result) == size
        }

    async def send_message(self, chat_room_id: int, user_id: int, data: dict) -> dict:
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
        
        # 상대방 찾기
        participants = self.repo.get_participants(chat_room_id)
        partner = next((p for p in participants if p.user_id != user_id), None)
        
        is_read = False
        should_notify_partner = False
        if partner and self.ws_manager and self.ws_manager.is_user_in_room(partner.user_id, chat_room_id):
            # 상대방이 현재 방에 접속 중이면 즉시 읽음 처리
            self.repo.mark_as_read(chat_room_id, partner.user_id, message.id)
            is_read = True
        else:
            # 상대방이 없거나 접속 중이 아니면 안 읽음 카운트 증가
            self.repo.increment_unread_counts(chat_room_id, user_id)
            if partner:
                should_notify_partner = True

        self.db.commit()

        if should_notify_partner:
            try:
                from app.services.impl.notifications import NotificationsService
                sender_user = self.db.get(User, user_id)
                sender_nickname = sender_user.nickname if sender_user else "알 수 없음"
                post_id = my_participant.chat_room.post_id
                NotificationsService(self.db).notify_chat_message(
                    partner_user_id=partner.user_id,
                    chat_room_id=chat_room_id,
                    post_id=post_id,
                    sender_nickname=sender_nickname,
                    message_content=message.content,
                )
            except Exception:
                logger.exception("Failed to send chat notification for message %s", message.id)

        if self.ws_manager:
            await self.ws_manager.broadcast_to_room(
                chat_room_id,
                {
                    "type": "NEW_MESSAGE",
                    "chat_room_id": chat_room_id,
                    "message_id": message.id,
                    "sender_user_id": user_id,
                    "message_type": message.message_type,
                    "content": message.content,
                    "created_at": message.created_at.isoformat() + "Z",
                },
            )
        
        # 발신자에게 즉시 응답 전송 (상대방이 읽었는지 여부 포함 가능)
        return {
            "message_id": message.id,
            "chat_room_id": chat_room_id,
            "sender_user_id": user_id,
            "message_type": message.message_type,
            "content": message.content,
            "created_at": message.created_at,
            "is_mine": True,
            "is_read": is_read
        }

    async def mark_read(self, chat_room_id: int, user_id: int, last_read_message_id: int) -> dict:
        my_participant = self.repo.mark_as_read(chat_room_id, user_id, last_read_message_id)
        if not my_participant:
            raise ForbiddenError("채팅방에 참여하고 있지 않습니다.")
            
        self.db.commit()
        
        # 상대방에게 내가 읽었음을 실시간으로 알림
        participants = self.repo.get_participants(chat_room_id)
        partner = next((p for p in participants if p.user_id != user_id), None)
        
        if partner and self.ws_manager:
            await self.ws_manager.broadcast_to_user(
                partner.user_id,
                {
                    "type": "MESSAGE_READ",
                    "chat_room_id": chat_room_id,
                    "last_read_message_id": last_read_message_id
                }
            )
            
        return {
            "chat_room_id": chat_room_id,
            "last_read_message_id": last_read_message_id,
            "unread_count": 0
        }
