from __future__ import annotations

from typing import Optional

from sqlalchemy import asc, desc, or_, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.chat import ChatRoom, ChatRoomParticipant
from app.models.post import Post, PostImage, PostLike
from app.models.transaction import Transaction
from app.models.user import User


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        return self.db.execute(statement).scalars().one_or_none()

    def list_posts(self, filters: dict) -> tuple[list[Post], bool]:
        page = filters["page"]
        size = filters["size"]

        statement = select(Post).options(selectinload(Post.images))
        statement = self._apply_filters(statement, filters)
        statement = statement.order_by(*self._get_order_by(filters["sort"]))
        statement = statement.offset((page - 1) * size).limit(size + 1)

        posts = list(self.db.execute(statement).scalars().all())
        has_next = len(posts) > size
        return posts[:size], has_next

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        statement = (
            select(Post)
            .options(joinedload(Post.author), selectinload(Post.images))
            .where(Post.id == post_id)
        )
        return self.db.execute(statement).scalars().unique().one_or_none()

    def create_post(self, user_id: int, data: dict) -> Post:
        post = Post(
            user_id=user_id,
            post_type=data["post_type"],
            title=data["title"],
            content=data["content"],
            price=data["price"],
            category=data["category"],
            is_urgent=data["is_urgent"],
            rental_period_text=data["rental_period_text"],
            meeting_place_text=data.get("meeting_place_text"),
            region_name=data["region_name"],
            lat=data["lat"],
            lng=data["lng"],
        )
        post.images = self._build_images(data.get("image_urls") or [])

        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update_post(self, post: Post, data: dict) -> Post:
        updatable_fields = (
            "title",
            "content",
            "price",
            "status",
        )

        for field_name in updatable_fields:
            if field_name in data:
                setattr(post, field_name, data[field_name])

        if "image_urls" in data:
            post.images = self._build_images(data["image_urls"])

        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete_post(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()

    def has_chat_rooms(self, post_id: int) -> bool:
        statement = select(ChatRoom.id).where(ChatRoom.post_id == post_id).limit(1)
        return self.db.execute(statement).first() is not None

    def has_transactions(self, post_id: int) -> bool:
        statement = select(Transaction.id).where(Transaction.post_id == post_id).limit(1)
        return self.db.execute(statement).first() is not None

    def get_post_like(self, post_id: int, user_id: int) -> Optional[PostLike]:
        statement = select(PostLike).where(
            PostLike.post_id == post_id,
            PostLike.user_id == user_id,
        )
        return self.db.execute(statement).scalars().one_or_none()

    def add_post_like(self, post: Post, user_id: int) -> Post:
        post.like_count = (post.like_count or 0) + 1
        post_like = PostLike(user_id=user_id, post_id=post.id)

        self.db.add(post_like)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def remove_post_like(self, post: Post, post_like: PostLike) -> Post:
        post.like_count = max((post.like_count or 0) - 1, 0)

        self.db.delete(post_like)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_chat_room(self, post_id: int, created_by_user_id: int) -> Optional[ChatRoom]:
        statement = select(ChatRoom).where(
            ChatRoom.post_id == post_id,
            ChatRoom.created_by_user_id == created_by_user_id,
        )
        return self.db.execute(statement).scalars().one_or_none()

    def create_chat_room(self, post: Post, created_by_user_id: int) -> ChatRoom:
        author_role = "lender" if post.post_type == "LEND" else "borrower"
        requester_role = "borrower" if post.post_type == "LEND" else "lender"

        chat_room = ChatRoom(
            post_id=post.id,
            created_by_user_id=created_by_user_id,
        )
        chat_room.participants = [
            ChatRoomParticipant(user_id=post.user_id, role=author_role),
            ChatRoomParticipant(user_id=created_by_user_id, role=requester_role),
        ]

        post.chat_count = (post.chat_count or 0) + 1

        self.db.add(chat_room)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(chat_room)
        return chat_room

    def _apply_filters(self, statement, filters: dict):
        keyword = filters.get("keyword")
        if keyword:
            pattern = f"%{keyword}%"
            statement = statement.where(
                or_(
                    Post.title.ilike(pattern),
                    Post.content.ilike(pattern),
                )
            )

        post_type = filters.get("post_type")
        if post_type:
            statement = statement.where(Post.post_type == post_type)

        category = filters.get("category")
        if category:
            statement = statement.where(Post.category == category)

        is_urgent = filters.get("is_urgent")
        if is_urgent is not None:
            statement = statement.where(Post.is_urgent.is_(is_urgent))

        region_name = filters.get("region_name")
        if region_name:
            statement = statement.where(Post.region_name == region_name)

        return statement

    def _get_order_by(self, sort: str):
        if sort == "price":
            return (
                asc(Post.price),
                desc(Post.created_at),
            )

        if sort == "like_count":
            return (
                desc(Post.like_count),
                desc(Post.created_at),
            )

        return (desc(Post.created_at),)

    @staticmethod
    def _build_images(image_urls: list[str]) -> list[PostImage]:
        return [
            PostImage(image_url=image_url, sort_order=index)
            for index, image_url in enumerate(image_urls, start=1)
        ]
