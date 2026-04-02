from __future__ import annotations

from datetime import datetime, timedelta, timezone

import httpx
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import BadRequestError, InvalidTokenError
from app.repositories.auth import AuthRepository

KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class AuthService:
    def __init__(self, db: Session):
        self.repo = AuthRepository(db)

    def oauth_login(self, provider: str, access_token: str) -> dict:
        if provider == "kakao":
            user_info = self._get_kakao_user_info(access_token)
        else:
            raise BadRequestError("지원하지 않는 provider입니다.")

        provider_user_id = str(user_info["id"])
        kakao_account = user_info.get("kakao_account", {})
        profile = kakao_account.get("profile", {})
        nickname = profile.get("nickname") or f"user_{provider_user_id[:8]}"
        profile_image_url = profile.get("profile_image_url")
        email = kakao_account.get("email")

        user = self.repo.get_user_by_social_account(provider, provider_user_id)
        is_new_user = user is None

        if is_new_user:
            user = self.repo.create_user_with_social_account(
                nickname=nickname,
                profile_image_url=profile_image_url,
                provider=provider,
                provider_user_id=provider_user_id,
                provider_email=email,
            )

        return {
            "access_token": self._create_access_token(user.id),
            "refresh_token": self._create_refresh_token(user.id),
            "is_new_user": is_new_user,
        }

    def refresh_token(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "refresh":
                raise InvalidTokenError()
            user_id = payload.get("sub")
            if user_id is None:
                raise InvalidTokenError()
        except JWTError:
            raise InvalidTokenError()

        return {"access_token": self._create_access_token(int(user_id))}

    def logout(self, refresh_token: str) -> None:
        pass  # stateless JWT — 클라이언트에서 토큰 삭제

    def withdrawal(self, user_id: int) -> None:
        self.repo.delete_user(user_id)

    def _get_kakao_user_info(self, access_token: str) -> dict:
        with httpx.Client() as client:
            response = client.get(
                KAKAO_USER_ME_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
        if response.status_code != 200:
            print(f"[Kakao] status={response.status_code} body={response.text}")
            raise InvalidTokenError()
        return response.json()

    def _create_access_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": str(user_id), "type": "access", "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def _create_refresh_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {"sub": str(user_id), "type": "refresh", "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
