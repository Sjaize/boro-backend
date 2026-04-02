from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.core.exceptions import InvalidTokenError, NotFoundError
from app.models.user import User
from app.repositories.posts import PostRepository
from app.repositories.transactions import TransactionRepository
from app.repositories.users import UserRepository
from app.services.impl import posts as impl_posts
from app.services.impl import transactions as impl_transactions
from app.services.impl import users as impl_users
from app.services.impl.chats import ChatsService
from app.services.impl.notifications import NotificationsService
from app.services.mock import auth as mock_auth
from app.services.mock import chats as mock_chats
from app.services.mock import notifications as mock_notifications
from app.services.mock import posts as mock_posts
from app.services.mock import transactions as mock_transactions
from app.services.mock import users as mock_users

MOCK_CURRENT_USER = {"id": 1, "nickname": "홍길동", "region_name": "역삼동"}


async def get_current_user(
    x_user_id: int | None = Header(default=None, alias="X-User-Id"),
    db: Session = Depends(get_db),
) -> dict:
    if settings.MOCK_MODE:
        return MOCK_CURRENT_USER

    # Until JWT auth is wired, an explicit header keeps non-mock flows testable.
    if x_user_id is None:
        raise InvalidTokenError()

    user = db.get(User, x_user_id)
    if user is None:
        raise NotFoundError("사용자를 찾을 수 없습니다.")

    return {
        "id": user.id,
        "nickname": user.nickname,
        "region_name": user.region_name,
    }


def get_auth_service():
    if settings.MOCK_MODE:
        return mock_auth.MockAuthService()
    raise NotImplementedError


def get_users_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_users_service(
    repository: UserRepository = Depends(get_users_repository),
):
    if settings.MOCK_MODE:
        return mock_users.MockUsersService()
    return impl_users.UsersService(repository)


def get_posts_repository(db: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(db)


def get_posts_service(
    repository: PostRepository = Depends(get_posts_repository),
):
    if settings.MOCK_MODE:
        return mock_posts.MockPostsService()
    return impl_posts.PostsService(repository)


def get_chats_service(db: Session = Depends(get_db)):
    if settings.MOCK_MODE:
        return mock_chats.MockChatsService()
    return ChatsService(db)


def get_transactions_repository(
    db: Session = Depends(get_db),
) -> TransactionRepository:
    return TransactionRepository(db)


def get_transactions_service(
    repository: TransactionRepository = Depends(get_transactions_repository),
):
    if settings.MOCK_MODE:
        return mock_transactions.MockTransactionsService()
    return impl_transactions.TransactionsService(repository)


def get_notifications_service(db: Session = Depends(get_db)):
    if settings.MOCK_MODE:
        return mock_notifications.MockNotificationsService()
    return NotificationsService(db)
