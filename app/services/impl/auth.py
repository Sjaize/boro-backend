class AuthService:
    def oauth_login(self, provider: str, access_token: str) -> dict:
        raise NotImplementedError

    def refresh_token(self, refresh_token: str) -> dict:
        raise NotImplementedError

    def logout(self, refresh_token: str) -> None:
        raise NotImplementedError

    def withdrawal(self, user_id: int) -> None:
        raise NotImplementedError
