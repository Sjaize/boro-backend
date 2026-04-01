from fastapi import APIRouter, Depends

from app.core.deps import get_auth_service, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/oauth/{provider}")
async def oauth_login(provider: str, body: dict, service=Depends(get_auth_service)):
    return {"data": service.oauth_login(provider, body.get("access_token", ""))}


@router.post("/refresh")
async def refresh_token(body: dict, service=Depends(get_auth_service)):
    return {"data": service.refresh_token(body.get("refresh_token", ""))}


@router.post("/logout")
async def logout(body: dict, service=Depends(get_auth_service)):
    service.logout(body.get("refresh_token", ""))
    return {"data": None}


@router.delete("/withdrawal")
async def withdrawal(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_auth_service),
):
    service.withdrawal(current_user["id"])
    return {"data": None}
