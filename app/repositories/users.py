from __future__ import annotations

from typing import Optional

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, selectinload

from app.models.post import Post, PostLike
from app.models.transaction import Review, Transaction
from app.models.user import User, UserInterestKeyword


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        statement = (
            select(User)
            .options(selectinload(User.interest_keywords))
            .where(User.id == user_id)
        )
        return self.db.execute(statement).scalars().unique().one_or_none()

    def count_borrow_transactions(self, user_id: int) -> int:
        statement = select(func.count(Transaction.id)).where(Transaction.borrower_user_id == user_id)
        return int(self.db.execute(statement).scalar() or 0)

    def count_lend_transactions(self, user_id: int) -> int:
        statement = select(func.count(Transaction.id)).where(Transaction.lender_user_id == user_id)
        return int(self.db.execute(statement).scalar() or 0)

    def count_post_likes(self, user_id: int) -> int:
        statement = select(func.count(PostLike.id)).where(PostLike.user_id == user_id)
        return int(self.db.execute(statement).scalar() or 0)

    def count_received_reviews(self, user_id: int) -> int:
        statement = select(func.count(Review.id)).where(Review.reviewee_user_id == user_id)
        return int(self.db.execute(statement).scalar() or 0)

    def list_received_reviews(self, user_id: int, page: int, size: int) -> tuple[list[Review], bool]:
        statement = (
            select(Review)
            .where(Review.reviewee_user_id == user_id)
            .order_by(desc(Review.created_at), desc(Review.id))
            .offset((page - 1) * size)
            .limit(size + 1)
        )

        reviews = list(self.db.execute(statement).scalars().all())
        has_next = len(reviews) > size
        return reviews[:size], has_next

    def list_user_posts(
        self,
        user_id: int,
        post_type: str | None,
        page: int,
        size: int,
    ) -> tuple[list[Post], bool]:
        statement = (
            select(Post)
            .options(selectinload(Post.images))
            .where(Post.user_id == user_id)
            .order_by(desc(Post.created_at), desc(Post.id))
        )

        if post_type is not None:
            statement = statement.where(Post.post_type == post_type)

        statement = statement.offset((page - 1) * size).limit(size + 1)

        posts = list(self.db.execute(statement).scalars().all())
        has_next = len(posts) > size
        return posts[:size], has_next

    def list_liked_posts(self, user_id: int, page: int, size: int) -> tuple[list[Post], bool]:
        statement = (
            select(Post)
            .join(PostLike, PostLike.post_id == Post.id)
            .options(selectinload(Post.images))
            .where(PostLike.user_id == user_id)
            .order_by(desc(PostLike.created_at), desc(Post.id))
            .offset((page - 1) * size)
            .limit(size + 1)
        )

        posts = list(self.db.execute(statement).scalars().unique().all())
        has_next = len(posts) > size
        return posts[:size], has_next

    def update_profile(
        self,
        user: User,
        *,
        nickname: str | None,
        profile_image_url: str | None,
    ) -> User:
        if nickname is not None:
            user.nickname = nickname

        if profile_image_url is not None:
            user.profile_image_url = profile_image_url

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_location(self, user: User, *, lat: float, lng: float) -> User:
        user.current_lat = lat
        user.current_lng = lng

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_settings(
        self,
        user: User,
        *,
        notification_radius_m: int | None,
        interest_keywords: list[str] | None,
    ) -> User:
        if notification_radius_m is not None:
            user.notification_radius_m = notification_radius_m

        if interest_keywords is not None:
            user.interest_keywords = [
                UserInterestKeyword(keyword=keyword)
                for keyword in interest_keywords
            ]

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
