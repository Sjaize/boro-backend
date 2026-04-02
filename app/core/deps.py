from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.services.mock import auth as mock_auth
from app.services.mock import chats as mock_chats
from app.services.mock import notifications as mock_notifications
from app.services.mock import posts as mock_posts
from app.services.mock import transactions as mock_transactions
from app.services.mock import users as mock_users
from app.services.impl.notifications import NotificationsService

MOCK_CURRENT_USER = {"id": 1, "nickname": "홍길동", "region_name": "역삼동"}


async def get_current_user() -> dict:
    if settings.MOCK_MODE:
        return MOCK_CURRENT_USER
    # TODO: JWT 검증 로직
    raise NotImplementedError


def get_auth_service():
    if settings.MOCK_MODE:
        return mock_auth.MockAuthService()
    raise NotImplementedError


def get_users_service():
    if settings.MOCK_MODE:
        return mock_users.MockUsersService()
    raise NotImplementedError


def get_posts_service():
    if settings.MOCK_MODE:
        return mock_posts.MockPostsService()
    raise NotImplementedError


def get_chats_service():
    if settings.MOCK_MODE:
        return mock_chats.MockChatsService()
    raise NotImplementedError


def get_transactions_service():
    if settings.MOCK_MODE:
        return mock_transactions.MockTransactionsService()
    raise NotImplementedError


def get_notifications_service(db: Session = Depends(get_db)):
    if settings.MOCK_MODE:
        return mock_notifications.MockNotificationsService()
    return NotificationsService(db)
