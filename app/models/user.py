from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.db import Base


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False)
    profile_image_url = Column(String(255))
    region_name = Column(String(100))
    current_lat = Column(Numeric(precision=10, scale=7))
    current_lng = Column(Numeric(precision=10, scale=7))
    location_updated_at = Column(DateTime)
    notification_radius_m = Column(Integer, default=1500)
    nearby_urgent_alerts_enabled = Column(Boolean, default=False, nullable=False)
    completed_transaction_count = Column(Integer, default=0)
    trust_score = Column(Numeric(precision=3, scale=2), default=5.0)
    status = Column(String(20), default="active")  # active, banned
    last_login_at = Column(DateTime)

    social_accounts = relationship("SocialAccount", back_populates="user", cascade="all, delete-orphan")
    interest_keywords = relationship("UserInterestKeyword", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="author")
    notifications = relationship("Notification", foreign_keys="Notification.user_id", back_populates="user")
    device_tokens = relationship("UserDeviceToken", back_populates="user", cascade="all, delete-orphan")


class SocialAccount(Base, TimestampMixin):
    __tablename__ = "social_accounts"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    provider = Column(String(20), nullable=False)  # google, kakao
    provider_user_id = Column(String(100), nullable=False)
    provider_email = Column(String(255))
    provider_name = Column(String(100))
    provider_profile_image_url = Column(String(255))

    user = relationship("User", back_populates="social_accounts")

    __table_args__ = (UniqueConstraint("provider", "provider_user_id", name="uq_social_account_provider_id"),)


class UserInterestKeyword(Base):
    __tablename__ = "user_interest_keywords"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    keyword = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="interest_keywords")

    __table_args__ = (UniqueConstraint("user_id", "keyword", name="uq_user_interest_keyword"),)
