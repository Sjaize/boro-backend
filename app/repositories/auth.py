from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import SocialAccount, User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_social_account(self, provider: str, provider_user_id: str) -> Optional[User]:
        statement = (
            select(User)
            .join(SocialAccount, SocialAccount.user_id == User.id)
            .where(SocialAccount.provider == provider)
            .where(SocialAccount.provider_user_id == provider_user_id)
        )
        return self.db.execute(statement).scalars().one_or_none()

    def create_user_with_social_account(
        self,
        nickname: str,
        profile_image_url: Optional[str],
        provider: str,
        provider_user_id: str,
        provider_email: Optional[str],
    ) -> User:
        user = User(
            nickname=nickname,
            profile_image_url=profile_image_url,
            status="active",
            trust_score=0.0,
        )
        self.db.add(user)
        self.db.flush()

        social_account = SocialAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
            provider_email=provider_email,
            provider_name=nickname,
            provider_profile_image_url=profile_image_url,
        )
        self.db.add(social_account)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> None:
        user = self.db.get(User, user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
