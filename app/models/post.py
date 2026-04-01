from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.user import TimestampMixin


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    post_type = Column(String(10), nullable=False)  # LEND, BORROW
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    price = Column(Integer, default=0)
    is_urgent = Column(Boolean, default=False)
    rental_period_text = Column(String(100))
    meeting_place_text = Column(String(200))
    region_name = Column(String(100))
    lat = Column(Numeric(precision=10, scale=7))
    lng = Column(Numeric(precision=10, scale=7))
    chat_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    status = Column(String(20), default="AVAILABLE")  # AVAILABLE, RESERVED, COMPLETED

    author = relationship("User", back_populates="posts")
    images = relationship("PostImage", back_populates="post", cascade="all, delete-orphan", order_by="PostImage.sort_order")
    likes = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")
    chat_rooms = relationship("ChatRoom", back_populates="post")
    transactions = relationship("Transaction", back_populates="post")


class PostImage(Base):
    __tablename__ = "post_images"

    id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)
    image_url = Column(String(255), nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    post = relationship("Post", back_populates="images")


class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    post = relationship("Post", back_populates="likes")

    __table_args__ = (UniqueConstraint("user_id", "post_id", name="uq_user_post_like"),)
