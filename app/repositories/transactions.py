from __future__ import annotations

from typing import Optional

from sqlalchemy import desc, func, or_, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.chat import ChatRoom
from app.models.post import Post
from app.models.transaction import Review, Transaction
from app.models.user import User


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        return self.db.execute(statement).scalars().one_or_none()

    def list_transactions(
        self,
        user_id: int,
        role: str | None,
        page: int,
        size: int,
    ) -> tuple[list[Transaction], bool]:
        statement = (
            select(Transaction)
            .options(
                joinedload(Transaction.post).selectinload(Post.images),
                selectinload(Transaction.reviews),
            )
            .order_by(desc(Transaction.completed_at), desc(Transaction.id))
        )

        if role == "borrower":
            statement = statement.where(Transaction.borrower_user_id == user_id)
        elif role == "lender":
            statement = statement.where(Transaction.lender_user_id == user_id)
        else:
            statement = statement.where(
                or_(
                    Transaction.borrower_user_id == user_id,
                    Transaction.lender_user_id == user_id,
                )
            )

        statement = statement.offset((page - 1) * size).limit(size + 1)

        transactions = list(self.db.execute(statement).scalars().unique().all())
        has_next = len(transactions) > size
        return transactions[:size], has_next

    def get_chat_room_by_id(self, chat_room_id: int) -> Optional[ChatRoom]:
        statement = (
            select(ChatRoom)
            .options(
                joinedload(ChatRoom.post).selectinload(Post.images),
                selectinload(ChatRoom.participants),
                joinedload(ChatRoom.transaction),
            )
            .where(ChatRoom.id == chat_room_id)
        )
        return self.db.execute(statement).scalars().unique().one_or_none()

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        statement = (
            select(Transaction)
            .options(
                joinedload(Transaction.post).selectinload(Post.images),
                selectinload(Transaction.reviews),
            )
            .where(Transaction.id == transaction_id)
        )
        return self.db.execute(statement).scalars().unique().one_or_none()

    def create_transaction(
        self,
        post: Post,
        chat_room: ChatRoom,
        lender_user: User,
        borrower_user: User,
    ) -> Transaction:
        transaction = Transaction(
            post_id=post.id,
            chat_room_id=chat_room.id,
            lender_user_id=lender_user.id,
            borrower_user_id=borrower_user.id,
        )

        post.status = "COMPLETED"
        lender_user.completed_transaction_count = (lender_user.completed_transaction_count or 0) + 1
        borrower_user.completed_transaction_count = (borrower_user.completed_transaction_count or 0) + 1

        try:
            self.db.add(transaction)
            self.db.add(post)
            self.db.add(lender_user)
            self.db.add(borrower_user)
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        except Exception:
            self.db.rollback()
            raise

    def create_review(
        self,
        transaction_id: int,
        reviewer_user_id: int,
        reviewee_user: User,
        rating: int,
        comment: str | None,
        tags: list[str],
    ) -> Review:
        review = Review(
            transaction_id=transaction_id,
            reviewer_user_id=reviewer_user_id,
            reviewee_user_id=reviewee_user.id,
            rating=rating,
            comment=comment,
            tags=tags,
        )

        try:
            self.db.add(review)
            self.db.flush()

            average_rating = self.db.execute(
                select(func.avg(Review.rating)).where(Review.reviewee_user_id == reviewee_user.id)
            ).scalar()
            reviewee_user.trust_score = average_rating or reviewee_user.trust_score

            self.db.add(reviewee_user)
            self.db.commit()
            self.db.refresh(review)
            return review
        except Exception:
            self.db.rollback()
            raise
