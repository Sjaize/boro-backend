from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

http_bearer = HTTPBearer(auto_error=False)

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
from app.services.impl.auth import AuthService
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
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    x_user_id: int | None = Header(default=None, alias="X-User-Id"),
    db: Session = Depends(get_db),
) -> dict:
    if settings.MOCK_MODE:
        return MOCK_CURRENT_USER

    if credentials:
        try:
            payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "access":
                raise InvalidTokenError()
            user_id = int(payload.get("sub"))
        except JWTError:
            raise InvalidTokenError()
    elif x_user_id is not None:
        user_id = x_user_id
    else:
        raise InvalidTokenError()

    user = db.get(User, user_id)
    if user is None:
        raise NotFoundError("사용자를 찾을 수 없습니다.")

    return {
        "id": user.id,
        "nickname": user.nickname,
        "region_name": user.region_name,
    }


def get_auth_service(db: Session = Depends(get_db)):
    if settings.MOCK_MODE:
        return mock_auth.MockAuthService()
    return AuthService(db)


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
