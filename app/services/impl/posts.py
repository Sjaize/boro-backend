from __future__ import annotations

import logging
from decimal import Decimal

from app.core.exceptions import BadRequestError, ConflictError, ForbiddenError, NotFoundError
from app.models.post import Post
from app.repositories.posts import PostRepository
from app.services.impl.notifications import NotificationsService

ALLOWED_POST_TYPES = {"LEND", "BORROW"}
ALLOWED_POST_STATUSES = {"AVAILABLE", "RESERVED", "COMPLETED"}
ALLOWED_SORTS = {"created_at", "price", "like_count"}
DEFAULT_PAGE = 1
DEFAULT_SIZE = 20
logger = logging.getLogger(__name__)


class PostsService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def list_posts(self, filters: dict) -> dict:
        normalized_filters = self._normalize_list_filters(filters)
        posts, has_next = self.post_repository.list_posts(normalized_filters)

        return {
            "posts": [self._serialize_post_list_item(post) for post in posts],
            "page": normalized_filters["page"],
            "size": normalized_filters["size"],
            "has_next": has_next,
        }

    def create_post(self, user_id: int, data) -> dict:
        self._ensure_user_exists(user_id)
        payload = self._normalize_create_payload(data)
        post = self.post_repository.create_post(user_id, payload)
        notifications_service = NotificationsService(self.post_repository.db)
        if post.is_urgent:
            try:
                notifications_service.notify_urgent_post(post)
            except Exception:
                logger.exception("Failed to create urgent notifications for post %s", post.id)
        try:
            notifications_service.notify_interest_post(post)
        except Exception:
            logger.exception("Failed to create interest notifications for post %s", post.id)
        return {"post_id": post.id}

    def get_post(self, post_id: int, user_id: int) -> dict:
        post = self._get_post_or_raise(post_id)
        is_liked_by_me = self.post_repository.get_post_like(post_id, user_id) is not None
        return self._serialize_post_detail(post, is_liked_by_me)

    def update_post(self, post_id: int, user_id: int, data) -> dict:
        post = self._get_post_or_raise(post_id)
        self._ensure_post_owner(post, user_id)

        payload = self._normalize_update_payload(data)
        if not payload:
            raise BadRequestError("수정할 데이터가 없습니다.")

        updated_post = self.post_repository.update_post(post, payload)
        return {"post_id": updated_post.id}

    def delete_post(self, post_id: int, user_id: int) -> dict:
        post = self._get_post_or_raise(post_id)
        self._ensure_post_owner(post, user_id)

        if self.post_repository.has_transactions(post.id):
            raise ConflictError("거래가 연결된 게시글은 삭제할 수 없습니다.")

        if self.post_repository.has_chat_rooms(post.id):
            raise ConflictError("채팅이 시작된 게시글은 삭제할 수 없습니다.")

        self.post_repository.delete_post(post)
        return {"post_id": post_id, "deleted": True}

    def like_post(self, post_id: int, user_id: int) -> dict:
        post = self._get_post_or_raise(post_id)
        existing_like = self.post_repository.get_post_like(post_id, user_id)

        if existing_like is None:
            post = self.post_repository.add_post_like(post, user_id)

        return {
            "post_id": post_id,
            "like_count": post.like_count,
            "is_liked": True,
        }

    def unlike_post(self, post_id: int, user_id: int) -> dict:
        post = self._get_post_or_raise(post_id)
        existing_like = self.post_repository.get_post_like(post_id, user_id)

        if existing_like is not None:
            post = self.post_repository.remove_post_like(post, existing_like)

        return {
            "post_id": post_id,
            "like_count": post.like_count,
            "is_liked": False,
        }

    def create_chat_from_post(self, post_id: int, user_id: int) -> dict:
        post = self._get_post_or_raise(post_id)

        if post.user_id == user_id:
            raise BadRequestError("내 게시글에는 채팅방을 생성할 수 없습니다.")

        chat_room = self.post_repository.get_chat_room(post_id, user_id)
        if chat_room is not None:
            return {"chat_room_id": chat_room.id, "is_new": False}

        chat_room = self.post_repository.create_chat_room(post, user_id)
        return {"chat_room_id": chat_room.id, "is_new": True}

    def _normalize_list_filters(self, filters: dict) -> dict:
        page = self._normalize_positive_int(filters.get("page"), "page", DEFAULT_PAGE)
        size = self._normalize_positive_int(filters.get("size"), "size", DEFAULT_SIZE)
        sort = (filters.get("sort") or "created_at").strip()

        if sort not in ALLOWED_SORTS:
            raise BadRequestError("지원하지 않는 정렬 기준입니다.")

        return {
            "keyword": self._normalize_optional_string(filters.get("keyword")),
            "post_type": self._normalize_post_type(filters.get("post_type"), required=False),
            "category": self._normalize_optional_string(filters.get("category")),
            "is_urgent": filters.get("is_urgent"),
            "region_name": self._normalize_optional_string(filters.get("region_name")),
            "page": page,
            "size": size,
            "sort": sort,
        }

    def _normalize_create_payload(self, data) -> dict:
        payload = self._to_payload(data)

        return {
            "post_type": self._normalize_post_type(payload.get("post_type"), required=True),
            "title": self._normalize_required_string(payload.get("title"), "title"),
            "content": self._normalize_required_string(payload.get("content"), "content"),
            "price": self._normalize_non_negative_int(payload.get("price"), "price"),
            "category": self._normalize_required_string(payload.get("category"), "category"),
            "is_urgent": bool(payload.get("is_urgent", False)),
            "rental_period_text": self._normalize_required_string(
                payload.get("rental_period_text"),
                "rental_period_text",
            ),
            "meeting_place_text": self._normalize_optional_string(payload.get("meeting_place_text")),
            "region_name": self._normalize_required_string(payload.get("region_name"), "region_name"),
            "lat": self._normalize_coordinate(payload.get("lat"), "lat", -90, 90),
            "lng": self._normalize_coordinate(payload.get("lng"), "lng", -180, 180),
            "image_urls": self._normalize_image_urls(payload.get("image_urls")),
        }

    def _normalize_update_payload(self, data) -> dict:
        payload = self._to_payload(data, exclude_none=True)
        normalized_payload = {}

        if "title" in payload:
            normalized_payload["title"] = self._normalize_required_string(payload.get("title"), "title")

        if "content" in payload:
            normalized_payload["content"] = self._normalize_required_string(payload.get("content"), "content")

        if "price" in payload:
            normalized_payload["price"] = self._normalize_non_negative_int(payload.get("price"), "price")

        if "status" in payload:
            normalized_payload["status"] = self._normalize_status(payload.get("status"))

        if "image_urls" in payload:
            normalized_payload["image_urls"] = self._normalize_image_urls(payload.get("image_urls"))

        return normalized_payload

    def _get_post_or_raise(self, post_id: int) -> Post:
        post = self.post_repository.get_post_by_id(post_id)
        if post is None:
            raise NotFoundError("게시글을 찾을 수 없습니다.")
        return post

    def _ensure_user_exists(self, user_id: int) -> None:
        user = self.post_repository.get_user_by_id(user_id)
        if user is None:
            raise NotFoundError("사용자를 찾을 수 없습니다.")

    def _ensure_post_owner(self, post: Post, user_id: int) -> None:
        if post.user_id != user_id:
            raise ForbiddenError()

    def _serialize_post_list_item(self, post: Post) -> dict:
        thumbnail_url = post.images[0].image_url if post.images else None

        return {
            "post_id": post.id,
            "title": post.title,
            "post_type": post.post_type,
            "price": post.price or 0,
            "region_name": post.region_name or "",
            "is_urgent": bool(post.is_urgent),
            "thumbnail_url": thumbnail_url,
            "like_count": post.like_count or 0,
            "chat_count": post.chat_count or 0,
            "status": post.status,
            "created_at": post.created_at,
        }

    def _serialize_post_detail(self, post: Post, is_liked_by_me: bool) -> dict:
        author = post.author
        if author is None:
            raise NotFoundError("게시글 작성자를 찾을 수 없습니다.")

        return {
            "post_id": post.id,
            "author": {
                "user_id": author.id,
                "nickname": author.nickname,
                "profile_image_url": author.profile_image_url,
                "trust_score": self._to_float(author.trust_score),
            },
            "post_type": post.post_type,
            "title": post.title,
            "content": post.content,
            "price": post.price or 0,
            "category": post.category or "",
            "is_urgent": bool(post.is_urgent),
            "rental_period_text": post.rental_period_text or "",
            "meeting_place_text": post.meeting_place_text,
            "region_name": post.region_name or "",
            "lat": self._to_float(post.lat),
            "lng": self._to_float(post.lng),
            "images": [
                {
                    "image_url": image.image_url,
                    "sort_order": image.sort_order or 0,
                }
                for image in post.images
            ],
            "like_count": post.like_count or 0,
            "chat_count": post.chat_count or 0,
            "status": post.status,
            "is_liked_by_me": is_liked_by_me,
            "created_at": post.created_at,
        }

    def _normalize_post_type(self, post_type, *, required: bool) -> str | None:
        if post_type is None:
            if required:
                raise BadRequestError("post_type은 필수입니다.")
            return None

        normalized_post_type = str(post_type).strip().upper()
        if normalized_post_type not in ALLOWED_POST_TYPES:
            raise BadRequestError("지원하지 않는 post_type입니다.")
        return normalized_post_type

    def _normalize_status(self, status) -> str:
        normalized_status = self._normalize_required_string(status, "status").upper()
        if normalized_status not in ALLOWED_POST_STATUSES:
            raise BadRequestError("지원하지 않는 status입니다.")
        return normalized_status

    def _normalize_required_string(self, value, field_name: str) -> str:
        if value is None:
            raise BadRequestError(f"{field_name}은 필수입니다.")

        normalized_value = str(value).strip()
        if not normalized_value:
            raise BadRequestError(f"{field_name}은 비워둘 수 없습니다.")

        return normalized_value

    def _normalize_optional_string(self, value) -> str | None:
        if value is None:
            return None

        normalized_value = str(value).strip()
        return normalized_value or None

    def _normalize_non_negative_int(self, value, field_name: str) -> int:
        if value is None:
            raise BadRequestError(f"{field_name}은 필수입니다.")

        try:
            normalized_value = int(value)
        except (TypeError, ValueError) as exc:
            raise BadRequestError(f"{field_name}은 숫자여야 합니다.") from exc

        if normalized_value < 0:
            raise BadRequestError(f"{field_name}은 0 이상이어야 합니다.")

        return normalized_value

    def _normalize_positive_int(self, value, field_name: str, default_value: int) -> int:
        if value is None:
            return default_value

        try:
            normalized_value = int(value)
        except (TypeError, ValueError) as exc:
            raise BadRequestError(f"{field_name}은 숫자여야 합니다.") from exc

        if normalized_value < 1:
            raise BadRequestError(f"{field_name}은 1 이상이어야 합니다.")

        return normalized_value

    def _normalize_coordinate(self, value, field_name: str, minimum: int, maximum: int) -> float:
        if value is None:
            raise BadRequestError(f"{field_name}은 필수입니다.")

        try:
            normalized_value = float(value)
        except (TypeError, ValueError) as exc:
            raise BadRequestError(f"{field_name}은 숫자여야 합니다.") from exc

        if normalized_value < minimum or normalized_value > maximum:
            raise BadRequestError(f"{field_name} 값이 올바르지 않습니다.")

        return normalized_value

    def _normalize_image_urls(self, image_urls) -> list[str]:
        if image_urls is None:
            return []

        if not isinstance(image_urls, list):
            raise BadRequestError("image_urls는 배열이어야 합니다.")

        normalized_urls = []
        for image_url in image_urls:
            normalized_urls.append(self._normalize_required_string(image_url, "image_urls"))

        return normalized_urls

    def _to_payload(self, data, *, exclude_none: bool = False) -> dict:
        if hasattr(data, "model_dump"):
            return data.model_dump(exclude_none=exclude_none)

        if isinstance(data, dict):
            return {key: value for key, value in data.items() if not exclude_none or value is not None}

        raise BadRequestError("요청 본문 형식이 올바르지 않습니다.")

    def _to_float(self, value: Decimal | float | int | None) -> float:
        if value is None:
            return 0.0

        return float(value)
