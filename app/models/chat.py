from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.db import Base


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)
    created_by_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    last_message_preview = Column(String(255))
    last_message_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    post = relationship("Post", back_populates="chat_rooms")
    participants = relationship("ChatRoomParticipant", back_populates="chat_room", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="chat_room", cascade="all, delete-orphan")
    transaction = relationship("Transaction", back_populates="chat_room", uselist=False)

    __table_args__ = (UniqueConstraint("post_id", "created_by_user_id", name="uq_chat_room_post_user"),)


class ChatRoomParticipant(Base):
    __tablename__ = "chat_room_participants"

    id = Column(BigInteger, primary_key=True, index=True)
    chat_room_id = Column(BigInteger, ForeignKey("chat_rooms.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    role = Column(String(20))  # lender, borrower
    last_read_message_id = Column(BigInteger)
    unread_count = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    chat_room = relationship("ChatRoom", back_populates="participants")

    __table_args__ = (UniqueConstraint("chat_room_id", "user_id", name="uq_chat_room_participant"),)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(BigInteger, primary_key=True, index=True)
    chat_room_id = Column(BigInteger, ForeignKey("chat_rooms.id"), nullable=False)
    sender_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    message_type = Column(String(20), default="text")  # text, image
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    chat_room = relationship("ChatRoom", back_populates="messages")
