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


@router.post("/oauth/{provider}", response_model=DataResponse[AuthResponseData])
async def oauth_login(provider: str, body: OAuthLoginRequest, service=Depends(get_auth_service)):
    return {"data": service.oauth_login(provider, body.access_token)}


@router.post("/refresh", response_model=DataResponse[TokenRefreshResponseData])
async def refresh_token(body: TokenRefreshRequest, service=Depends(get_auth_service)):
    return {"data": service.refresh_token(body.refresh_token)}


@router.post("/logout")
async def logout(body: LogoutRequest, service=Depends(get_auth_service)):
    service.logout(body.refresh_token)
    return {"data": None}


@router.delete("/withdrawal")
async def withdrawal(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_auth_service),
):
    service.withdrawal(current_user["id"])
    return {"data": None}
