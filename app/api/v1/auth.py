from fastapi import APIRouter, Depends

from app.core.deps import get_auth_service, get_current_user
from app.schemas.auth import (
    AuthResponseData,
    LogoutRequest,
    OAuthLoginRequest,
    TokenRefreshRequest,
    TokenRefreshResponseData,
)
from app.schemas.common import DataResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post(
    "/oauth/{provider}",
    response_model=DataResponse[AuthResponseData],
    summary="소셜 로그인",
    description=(
        "카카오 OAuth 로그인을 처리합니다.\n\n"
        "**흐름:**\n"
        "1. 프론트에서 카카오 SDK로 `access_token`을 발급받습니다.\n"
        "2. 해당 토큰을 이 API에 전달합니다.\n"
        "3. 신규 유저면 자동으로 회원가입 처리됩니다.\n\n"
        "**provider:** `kakao`"
    ),
)
async def oauth_login(provider: str, body: OAuthLoginRequest, service=Depends(get_auth_service)):
    return {"data": service.oauth_login(provider, body.access_token)}


@router.post(
    "/refresh",
    response_model=DataResponse[TokenRefreshResponseData],
    summary="액세스 토큰 갱신",
    description="Refresh Token으로 만료된 Access Token을 갱신합니다.",
)
async def refresh_token(body: TokenRefreshRequest, service=Depends(get_auth_service)):
    return {"data": service.refresh_token(body.refresh_token)}


@router.post(
    "/logout",
    summary="로그아웃",
    description="로그아웃 처리합니다. 클라이언트에서 토큰을 삭제해야 합니다.",
)
async def logout(body: LogoutRequest, service=Depends(get_auth_service)):
    service.logout(body.refresh_token)
    return {"data": None}


@router.delete(
    "/withdrawal",
    summary="회원 탈퇴",
    description="현재 로그인한 유저의 계정을 삭제합니다.",
)
async def withdrawal(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_auth_service),
):
    service.withdrawal(current_user["id"])
    return {"data": None}
