from __future__ import annotations

from decimal import Decimal

from app.core.exceptions import BadRequestError, NotFoundError
from app.models.post import Post
from app.models.user import User
from app.repositories.users import UserRepository

ALLOWED_POST_TYPES = {"BORROW", "LEND"}
DEFAULT_PAGE = 1
DEFAULT_SIZE = 10
DEFAULT_NOTIFICATION_RADIUS_M = 1500


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_my_profile(self, user_id: int) -> dict:
        user = self._get_user_or_raise(user_id)

        return {
            "id": user.id,
            "nickname": user.nickname,
            "profile_image_url": user.profile_image_url,
            "region_name": user.region_name,
            "trust_score": self._to_float(user.trust_score),
            "borrow_count": self.user_repository.count_borrow_transactions(user_id),
            "lend_count": self.user_repository.count_lend_transactions(user_id),
            "like_count": self.user_repository.count_post_likes(user_id),
        }

    def update_my_profile(self, user_id: int, data: dict) -> dict:
        user = self._get_user_or_raise(user_id)
        payload = self._to_payload(data)

        nickname = None
        if "nickname" in payload:
            nickname = self._normalize_optional_string(payload.get("nickname"))
            if nickname is None:
                raise BadRequestError("nickname cannot be blank.")

        profile_image_url = None
        if "profile_image_url" in payload:
            profile_image_url = self._normalize_optional_string(payload.get("profile_image_url"))

        updated_user = self.user_repository.update_profile(
            user,
            nickname=nickname,
            profile_image_url=profile_image_url,
        )

        return {
            "id": updated_user.id,
            "nickname": updated_user.nickname,
            "profile_image_url": updated_user.profile_image_url,
        }

    def update_location(self, user_id: int, lat: float, lng: float) -> dict:
        user = self._get_user_or_raise(user_id)
        normalized_lat = self._normalize_coordinate(lat, "lat", -90, 90)
        normalized_lng = self._normalize_coordinate(lng, "lng", -180, 180)

        # TODO: 실제 운영 환경에서는 카카오/구글 API 등을 통해 역지오코딩 수행
        full_address = "서울특별시 강남구 역삼동"
        region_name = self._extract_region_name(full_address)

        updated_user = self.user_repository.update_location(
            user,
            lat=normalized_lat,
            lng=normalized_lng,
            region_name=region_name,
        )

        return {
            "region_name": updated_user.region_name or "",
            "full_address": full_address,
            "lat": self._to_float(updated_user.current_lat),
            "lng": self._to_float(updated_user.current_lng),
        }

    def _extract_region_name(self, full_address: str) -> str:
        """전체 주소에서 마지막 단어(동네명)만 추출 (예: '서울특별시 강남구 역삼동' -> '역삼동')"""
        parts = full_address.split()
        return parts[-1] if parts else ""

    def update_settings(self, user_id: int, data: dict) -> dict:
        user = self._get_user_or_raise(user_id)
        payload = self._to_payload(data)

        notification_radius_m = payload.get("notification_radius_m")
        if notification_radius_m is not None:
            notification_radius_m = self._normalize_non_negative_int(
                notification_radius_m,
                "notification_radius_m",
            )

        interest_keywords = payload.get("interest_keywords")
        if interest_keywords is not None:
            interest_keywords = self._normalize_interest_keywords(interest_keywords)

        updated_user = self.user_repository.update_settings(
            user,
            notification_radius_m=notification_radius_m,
            interest_keywords=interest_keywords,
        )

        return {
            "notification_radius_m": updated_user.notification_radius_m or DEFAULT_NOTIFICATION_RADIUS_M,
            "interest_keywords": [
                keyword.keyword
                for keyword in updated_user.interest_keywords
            ],
        }

    def get_user_profile(self, user_id: int) -> dict:
        user = self._get_user_or_raise(user_id)

        return {
            "id": user.id,
            "nickname": user.nickname,
            "profile_image_url": user.profile_image_url,
            "region_name": user.region_name,
            "completed_transaction_count": user.completed_transaction_count or 0,
            "trust_score": self._to_float(user.trust_score),
            "review_count": self.user_repository.count_received_reviews(user_id),
        }

    def get_user_reviews(self, user_id: int, page: int, size: int) -> dict:
        self._get_user_or_raise(user_id)
        normalized_page = self._normalize_positive_int(page, "page", DEFAULT_PAGE)
        normalized_size = self._normalize_positive_int(size, "size", DEFAULT_SIZE)

        reviews, has_next = self.user_repository.list_received_reviews(
            user_id,
            normalized_page,
            normalized_size,
        )

        return {
            "reviews": [
                {
                    "review_id": review.id,
                    "rating": review.rating,
                    "comment": review.comment,
                    "created_at": review.created_at,
                }
                for review in reviews
            ],
            "page": normalized_page,
            "size": normalized_size,
            "has_next": has_next,
        }

    def get_my_posts(self, user_id: int, post_type: str | None, page: int, size: int) -> dict:
        self._get_user_or_raise(user_id)
        return self._list_user_posts(user_id, post_type, page, size)

    def get_user_posts(self, user_id: int, post_type: str | None, page: int, size: int) -> dict:
        self._get_user_or_raise(user_id)
        return self._list_user_posts(user_id, post_type, page, size)

    def get_my_likes(self, user_id: int, page: int, size: int) -> dict:
        self._get_user_or_raise(user_id)
        normalized_page = self._normalize_positive_int(page, "page", DEFAULT_PAGE)
        normalized_size = self._normalize_positive_int(size, "size", DEFAULT_SIZE)

        posts, has_next = self.user_repository.list_liked_posts(
            user_id,
            normalized_page,
            normalized_size,
        )

        return {
            "posts": [self._serialize_post_summary(post) for post in posts],
            "page": normalized_page,
            "size": normalized_size,
            "has_next": has_next,
        }

    def _list_user_posts(self, user_id: int, post_type: str | None, page: int, size: int) -> dict:
        normalized_post_type = self._normalize_post_type(post_type, required=False)
        normalized_page = self._normalize_positive_int(page, "page", DEFAULT_PAGE)
        normalized_size = self._normalize_positive_int(size, "size", DEFAULT_SIZE)

        posts, has_next = self.user_repository.list_user_posts(
            user_id,
            normalized_post_type,
            normalized_page,
            normalized_size,
        )

        return {
            "posts": [self._serialize_post_summary(post) for post in posts],
            "page": normalized_page,
            "size": normalized_size,
            "has_next": has_next,
        }

    def _get_user_or_raise(self, user_id: int) -> User:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        return user

    def _serialize_post_summary(self, post: Post) -> dict:
        return {
            "post_id": post.id,
            "title": post.title,
            "post_type": post.post_type,
            "price": post.price or 0,
            "region_name": post.region_name or "",
            "like_count": post.like_count or 0,
            "chat_count": post.chat_count or 0,
            "status": post.status,
            "created_at": post.created_at,
        }

    def _normalize_post_type(self, post_type, *, required: bool) -> str | None:
        if post_type is None:
            if required:
                raise BadRequestError("post_type is required.")
            return None

        normalized_post_type = str(post_type).strip().upper()
        if normalized_post_type not in ALLOWED_POST_TYPES:
            raise BadRequestError("Unsupported post_type.")
        return normalized_post_type

    def _normalize_positive_int(self, value, field_name: str, default_value: int) -> int:
        if value is None:
            return default_value

        try:
            normalized_value = int(value)
        except (TypeError, ValueError) as exc:
            raise BadRequestError(f"{field_name} must be a number.") from exc

        if normalized_value < 1:
            raise BadRequestError(f"{field_name} must be at least 1.")

        return normalized_value

    def _normalize_non_negative_int(self, value, field_name: str) -> int:
        try:
            normalized_value = int(value)
        except (TypeError, ValueError) as exc:
            raise BadRequestError(f"{field_name} must be a number.") from exc

        if normalized_value < 0:
            raise BadRequestError(f"{field_name} must be at least 0.")

        return normalized_value

    def _normalize_coordinate(self, value, field_name: str, minimum: int, maximum: int) -> float:
        try:
            normalized_value = float(value)
        except (TypeError, ValueError) as exc:
            raise BadRequestError(f"{field_name} must be a number.") from exc

        if normalized_value < minimum or normalized_value > maximum:
            raise BadRequestError(f"{field_name} is out of range.")

        return normalized_value

    def _normalize_optional_string(self, value) -> str | None:
        if value is None:
            return None

        normalized_value = str(value).strip()
        return normalized_value or None

    def _normalize_interest_keywords(self, keywords) -> list[str]:
        if not isinstance(keywords, list):
            raise BadRequestError("interest_keywords must be a list.")

        normalized_keywords: list[str] = []
        seen_keywords: set[str] = set()
        for keyword in keywords:
            normalized_keyword = self._normalize_optional_string(keyword)
            if normalized_keyword is None:
                raise BadRequestError("interest_keywords cannot contain blank values.")
            if normalized_keyword in seen_keywords:
                continue
            seen_keywords.add(normalized_keyword)
            normalized_keywords.append(normalized_keyword)

        return normalized_keywords

    def _to_payload(self, data) -> dict:
        if hasattr(data, "model_dump"):
            return data.model_dump(exclude_none=True)

        if isinstance(data, dict):
            return data

        raise BadRequestError("Request body format is invalid.")

    def _to_float(self, value: Decimal | float | int | None) -> float:
        if value is None:
            return 0.0

        return float(value)
