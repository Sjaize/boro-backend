from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import BadRequestError, ConflictError, ForbiddenError, NotFoundError
from app.models.chat import ChatRoom
from app.models.post import Post
from app.models.transaction import Review, Transaction
from app.repositories.transactions import TransactionRepository

ALLOWED_TRANSACTION_ROLES = {"borrower", "lender"}
DEFAULT_PAGE = 1
DEFAULT_SIZE = 10
MIN_REVIEW_RATING = 1
MAX_REVIEW_RATING = 5


class TransactionsService:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def list_transactions(self, user_id: int, role: str | None, page: int, size: int) -> dict:
        self._ensure_user_exists(user_id)

        normalized_role = self._normalize_role(role)
        normalized_page = self._normalize_positive_int(page, "page", DEFAULT_PAGE)
        normalized_size = self._normalize_positive_int(size, "size", DEFAULT_SIZE)

        transactions, has_next = self.transaction_repository.list_transactions(
            user_id,
            normalized_role,
            normalized_page,
            normalized_size,
        )

        return {
            "transactions": [
                self._serialize_transaction_list_item(transaction, user_id)
                for transaction in transactions
            ],
            "page": normalized_page,
            "size": normalized_size,
            "has_next": has_next,
        }

    def create_transaction(self, user_id: int, data) -> dict:
        self._ensure_user_exists(user_id)

        payload = self._to_payload(data)
        post_id = self._normalize_required_id(payload.get("post_id"), "post_id")
        chat_room_id = self._normalize_required_id(payload.get("chat_room_id"), "chat_room_id")

        chat_room = self.transaction_repository.get_chat_room_by_id(chat_room_id)
        if chat_room is None:
            raise NotFoundError("채팅방을 찾을 수 없습니다.")

        post = chat_room.post
        if post is None:
            raise NotFoundError("거래 게시글을 찾을 수 없습니다.")

        if post.id != post_id:
            raise BadRequestError("post_id와 chat_room_id가 일치하지 않습니다.")

        if not self._is_chat_participant(chat_room, user_id):
            raise ForbiddenError()

        if chat_room.transaction is not None:
            raise ConflictError("이미 완료된 거래입니다.")

        if post.status == "COMPLETED":
            raise ConflictError("이미 완료된 게시글입니다.")

        lender_user_id, borrower_user_id = self._resolve_transaction_participants(post, chat_room)
        lender_user = self.transaction_repository.get_user_by_id(lender_user_id)
        borrower_user = self.transaction_repository.get_user_by_id(borrower_user_id)

        if lender_user is None or borrower_user is None:
            raise NotFoundError("거래 참여자를 찾을 수 없습니다.")

        try:
            transaction = self.transaction_repository.create_transaction(
                post,
                chat_room,
                lender_user,
                borrower_user,
            )
        except IntegrityError as exc:
            raise ConflictError("이미 완료된 거래입니다.") from exc

        return {
            "transaction_id": transaction.id,
            "post_id": transaction.post_id,
            "chat_room_id": transaction.chat_room_id,
            "lender_user_id": transaction.lender_user_id,
            "borrower_user_id": transaction.borrower_user_id,
            "completed_at": transaction.completed_at,
        }

    def get_transaction(self, transaction_id: int, user_id: int) -> dict:
        transaction = self._get_transaction_or_raise(transaction_id)
        self._ensure_transaction_participant(transaction, user_id)

        post = transaction.post
        if post is None:
            raise NotFoundError("거래 게시글을 찾을 수 없습니다.")

        my_role = self._get_transaction_role(transaction, user_id)
        received_review = self._get_received_review(transaction, user_id)

        return {
            "transaction_id": transaction.id,
            "post_id": transaction.post_id,
            "chat_room_id": transaction.chat_room_id,
            "lender_user_id": transaction.lender_user_id,
            "borrower_user_id": transaction.borrower_user_id,
            "my_role": my_role,
            "completed_at": transaction.completed_at,
            "post": {
                "title": post.title,
                "content": post.content,
                "price": post.price or 0,
                "category": post.category or "",
                "rental_period_text": post.rental_period_text,
                "meeting_place_text": post.meeting_place_text,
                "region_name": post.region_name or "",
                "post_image_urls": [image.image_url for image in post.images],
                "chat_count": post.chat_count or 0,
                "like_count": post.like_count or 0,
            },
            "review": {
                "has_received_review": received_review is not None,
                "rating": received_review.rating if received_review is not None else None,
                "comment": received_review.comment if received_review is not None else None,
                "tags": received_review.tags if received_review is not None else None,
            },
        }

    def create_review(self, transaction_id: int, user_id: int, data) -> dict:
        transaction = self._get_transaction_or_raise(transaction_id)
        self._ensure_transaction_participant(transaction, user_id)

        if self._get_review_written_by(transaction, user_id) is not None:
            raise ConflictError("이미 리뷰를 작성했습니다.")

        payload = self._to_payload(data)
        rating = self._normalize_rating(payload.get("rating"))
        comment = self._normalize_optional_string(payload.get("comment"))
        tags = self._normalize_tags(payload.get("tags"))

        reviewee_user_id = self._get_counterparty_user_id(transaction, user_id)
        reviewee_user = self.transaction_repository.get_user_by_id(reviewee_user_id)
        if reviewee_user is None:
            raise NotFoundError("리뷰 대상 사용자를 찾을 수 없습니다.")

        try:
            review = self.transaction_repository.create_review(
                transaction.id,
                user_id,
                reviewee_user,
                rating,
                comment,
                tags,
            )
        except IntegrityError as exc:
            raise ConflictError("이미 리뷰를 작성했습니다.") from exc

        return {
            "review_id": review.id,
            "transaction_id": review.transaction_id,
            "rating": review.rating,
            "comment": review.comment,
            "tags": review.tags or [],
            "created_at": review.created_at,
        }

    def _get_transaction_or_raise(self, transaction_id: int) -> Transaction:
        transaction = self.transaction_repository.get_transaction_by_id(transaction_id)
        if transaction is None:
            raise NotFoundError("거래를 찾을 수 없습니다.")
        return transaction

    def _ensure_user_exists(self, user_id: int) -> None:
        user = self.transaction_repository.get_user_by_id(user_id)
        if user is None:
            raise NotFoundError("사용자를 찾을 수 없습니다.")

    def _ensure_transaction_participant(self, transaction: Transaction, user_id: int) -> None:
        if user_id not in {transaction.lender_user_id, transaction.borrower_user_id}:
            raise ForbiddenError()

    def _serialize_transaction_list_item(self, transaction: Transaction, user_id: int) -> dict:
        post = transaction.post
        if post is None:
            raise NotFoundError("거래 게시글을 찾을 수 없습니다.")

        post_image_url = post.images[0].image_url if post.images else None
        received_review = self._get_received_review(transaction, user_id)

        return {
            "transaction_id": transaction.id,
            "post_id": transaction.post_id,
            "chat_room_id": transaction.chat_room_id,
            "role": self._get_transaction_role(transaction, user_id),
            "post_title": post.title,
            "post_image_url": post_image_url,
            "price": post.price or 0,
            "rental_period_text": post.rental_period_text,
            "chat_count": post.chat_count or 0,
            "like_count": post.like_count or 0,
            "completed_at": transaction.completed_at,
            "review": {
                "has_received_review": received_review is not None,
            },
        }

    def _get_received_review(self, transaction: Transaction, user_id: int) -> Review | None:
        for review in transaction.reviews:
            if review.reviewee_user_id == user_id:
                return review
        return None

    def _get_review_written_by(self, transaction: Transaction, user_id: int) -> Review | None:
        for review in transaction.reviews:
            if review.reviewer_user_id == user_id:
                return review
        return None

    def _get_transaction_role(self, transaction: Transaction, user_id: int) -> str:
        if transaction.borrower_user_id == user_id:
            return "borrower"
        return "lender"

    def _get_counterparty_user_id(self, transaction: Transaction, user_id: int) -> int:
        if transaction.borrower_user_id == user_id:
            return transaction.lender_user_id
        return transaction.borrower_user_id

    def _resolve_transaction_participants(self, post: Post, chat_room: ChatRoom) -> tuple[int, int]:
        author_user_id = post.user_id
        requester_user_id = chat_room.created_by_user_id

        if author_user_id == requester_user_id:
            raise BadRequestError("거래 참여자 정보가 올바르지 않습니다.")

        if post.post_type == "LEND":
            return author_user_id, requester_user_id

        if post.post_type == "BORROW":
            return requester_user_id, author_user_id

        raise BadRequestError("지원하지 않는 post_type입니다.")

    def _is_chat_participant(self, chat_room: ChatRoom, user_id: int) -> bool:
        return any(participant.user_id == user_id for participant in chat_room.participants)

    def _normalize_role(self, role: str | None) -> str | None:
        if role is None:
            return None

        normalized_role = str(role).strip().lower()
        if normalized_role not in ALLOWED_TRANSACTION_ROLES:
            raise BadRequestError("지원하지 않는 role입니다.")
        return normalized_role

    def _normalize_required_id(self, value, field_name: str) -> int:
        return self._normalize_positive_int(value, field_name, None)

    def _normalize_positive_int(self, value, field_name: str, default_value: int | None) -> int:
        if value is None:
            if default_value is None:
                raise BadRequestError(f"{field_name}은 필수입니다.")
            return default_value

        try:
            normalized_value = int(value)
        except (TypeError, ValueError) as exc:
            raise BadRequestError(f"{field_name}은 숫자여야 합니다.") from exc

        if normalized_value < 1:
            raise BadRequestError(f"{field_name}은 1 이상이어야 합니다.")

        return normalized_value

    def _normalize_rating(self, value) -> int:
        rating = self._normalize_required_id(value, "rating")
        if rating < MIN_REVIEW_RATING or rating > MAX_REVIEW_RATING:
            raise BadRequestError("rating은 1 이상 5 이하여야 합니다.")
        return rating

    def _normalize_optional_string(self, value) -> str | None:
        if value is None:
            return None

        normalized_value = str(value).strip()
        return normalized_value or None

    def _normalize_tags(self, tags) -> list[str]:
        if tags is None:
            return []

        if not isinstance(tags, list):
            raise BadRequestError("tags는 배열이어야 합니다.")

        normalized_tags = []
        for tag in tags:
            normalized_tag = self._normalize_optional_string(tag)
            if normalized_tag is None:
                raise BadRequestError("tags에는 비어 있는 값을 포함할 수 없습니다.")
            normalized_tags.append(normalized_tag)

        return normalized_tags

    def _to_payload(self, data) -> dict:
        if hasattr(data, "model_dump"):
            return data.model_dump(exclude_none=True)

        if isinstance(data, dict):
            return data

        raise BadRequestError("요청 본문 형식이 올바르지 않습니다.")
