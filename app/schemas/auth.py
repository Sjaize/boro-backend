from pydantic import BaseModel


class OAuthLoginRequest(BaseModel):
    access_token: str


class AuthResponseData(BaseModel):
    access_token: str
    refresh_token: str
    is_new_user: bool


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenRefreshResponseData(BaseModel):
    access_token: str


class LogoutRequest(BaseModel):
    refresh_token: str
