from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.core.db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)
    chat_room_id = Column(BigInteger, ForeignKey("chat_rooms.id"), nullable=False)
    lender_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    borrower_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    post = relationship("Post", back_populates="transactions")
    chat_room = relationship("ChatRoom", back_populates="transaction")
    reviews = relationship("Review", back_populates="transaction", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("chat_room_id", name="uq_transaction_chat_room"),)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(BigInteger, primary_key=True, index=True)
    transaction_id = Column(BigInteger, ForeignKey("transactions.id"), nullable=False)
    reviewer_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    reviewee_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    tags = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    transaction = relationship("Transaction", back_populates="reviews")

    __table_args__ = (UniqueConstraint("transaction_id", "reviewer_user_id", name="uq_review_transaction_reviewer"),)
