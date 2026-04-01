class TransactionsService:
    def list_transactions(self, user_id: int, role: str | None, page: int, size: int) -> dict:
        raise NotImplementedError

    def create_transaction(self, user_id: int, data: dict) -> dict:
        raise NotImplementedError

    def get_transaction(self, transaction_id: int, user_id: int) -> dict:
        raise NotImplementedError

    def create_review(self, transaction_id: int, user_id: int, data: dict) -> dict:
        raise NotImplementedError
