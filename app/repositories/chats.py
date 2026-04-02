from datetime import datetime
from typing import List, Optional
from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import Session, joinedload
from app.models.chat import ChatRoom, ChatRoomParticipant, ChatMessage
from app.models.post import Post, PostImage
from app.models.user import User
from app.models.transaction import Transaction

class ChatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_chat_rooms(self, user_id: int, type_filter: str, page: int, size: int) -> List[ChatRoom]:
        query = self.db.query(ChatRoom).options(
            joinedload(ChatRoom.post).joinedload(Post.images),
            joinedload(ChatRoom.participants).joinedload(ChatRoomParticipant.user)
        ).join(ChatRoomParticipant).filter(ChatRoomParticipant.user_id == user_id)
        
        if type_filter == "BORROW":
            query = query.join(Post).filter(Post.post_type == "BORROW")
        elif type_filter == "LEND":
            query = query.join(Post).filter(Post.post_type == "LEND")
            
        return query.order_by(desc(ChatRoom.last_message_at)).offset((page - 1) * size).limit(size).all()

    def count_chat_rooms(self, user_id: int, type_filter: str) -> int:
        query = self.db.query(ChatRoom).join(ChatRoomParticipant).filter(ChatRoomParticipant.user_id == user_id)
        
        if type_filter == "BORROW":
            query = query.join(Post).filter(Post.post_type == "BORROW")
        elif type_filter == "LEND":
            query = query.join(Post).filter(Post.post_type == "LEND")
            
        return query.count()

    def get_chat_room(self, chat_room_id: int) -> Optional[ChatRoom]:
        return self.db.query(ChatRoom).options(
            joinedload(ChatRoom.post).joinedload(Post.images),
            joinedload(ChatRoom.participants).joinedload(ChatRoomParticipant.user)
        ).filter(ChatRoom.id == chat_room_id).first()

    def get_chat_room_by_post_and_user(self, post_id: int, user_id: int) -> Optional[ChatRoom]:
        """게시글 ID와 채팅을 건 유저 ID로 기존 채팅방 조회"""
        return self.db.query(ChatRoom).filter(
            ChatRoom.post_id == post_id,
            ChatRoom.created_by_user_id == user_id
        ).first()

    def create_chat_room(self, post_id: int, created_by_user_id: int) -> ChatRoom:
        """새 채팅방 생성"""
        chat_room = ChatRoom(
            post_id=post_id,
            created_by_user_id=created_by_user_id
        )
        self.db.add(chat_room)
        self.db.flush()
        return chat_room

    def add_participant(self, chat_room_id: int, user_id: int, role: str) -> ChatRoomParticipant:
        """채팅방 참여자 추가 (lender/borrower)"""
        participant = ChatRoomParticipant(
            chat_room_id=chat_room_id,
            user_id=user_id,
            role=role
        )
        self.db.add(participant)
        self.db.flush()
        return participant

    def get_participant(self, chat_room_id: int, user_id: int) -> Optional[ChatRoomParticipant]:
        return self.db.query(ChatRoomParticipant).filter(
            ChatRoomParticipant.chat_room_id == chat_room_id,
            ChatRoomParticipant.user_id == user_id
        ).first()

    def get_participants(self, chat_room_id: int) -> List[ChatRoomParticipant]:
        return self.db.query(ChatRoomParticipant).filter(ChatRoomParticipant.chat_room_id == chat_room_id).all()

    def list_messages(self, chat_room_id: int, cursor: Optional[int], size: int) -> List[ChatMessage]:
        query = self.db.query(ChatMessage).filter(ChatMessage.chat_room_id == chat_room_id)
        if cursor:
            query = query.filter(ChatMessage.id < cursor)
        return query.order_by(desc(ChatMessage.id)).limit(size).all()

    def create_message(self, chat_room_id: int, sender_user_id: int, message_type: str, content: str) -> ChatMessage:
        message = ChatMessage(
            chat_room_id=chat_room_id,
            sender_user_id=sender_user_id,
            message_type=message_type,
            content=content
        )
        self.db.add(message)
        self.db.flush()
        return message

    def update_last_message(self, chat_room_id: int, message_preview: str, message_at: datetime):
        chat_room = self.get_chat_room(chat_room_id)
        if chat_room:
            chat_room.last_message_preview = message_preview[:255]
            chat_room.last_message_at = message_at
            self.db.add(chat_room)

    def increment_unread_counts(self, chat_room_id: int, exclude_user_id: int):
        self.db.query(ChatRoomParticipant).filter(
            ChatRoomParticipant.chat_room_id == chat_room_id,
            ChatRoomParticipant.user_id != exclude_user_id
        ).update({ChatRoomParticipant.unread_count: ChatRoomParticipant.unread_count + 1})

    def mark_as_read(self, chat_room_id: int, user_id: int, last_read_message_id: int):
        participant = self.get_participant(chat_room_id, user_id)
        if participant:
            participant.last_read_message_id = last_read_message_id
            participant.unread_count = 0
            self.db.add(participant)
        return participant

    def is_transaction_completed(self, chat_room_id: int) -> bool:
        return self.db.query(Transaction).filter(Transaction.chat_room_id == chat_room_id).first() is not None
