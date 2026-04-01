class MockAuthService:
    def oauth_login(self, provider: str, access_token: str) -> dict:
        return {
            "access_token": "mock-access-token-abc123",
            "refresh_token": "mock-refresh-token-xyz789",
            "is_new_user": False,
        }

    def refresh_token(self, refresh_token: str) -> dict:
        return {"access_token": "mock-access-token-refreshed-abc456"}

    def logout(self, refresh_token: str) -> None:
        return None

    def withdrawal(self, user_id: int) -> None:
        return None
