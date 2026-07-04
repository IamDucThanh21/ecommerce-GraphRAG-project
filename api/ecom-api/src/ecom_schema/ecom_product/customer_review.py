# """SQLAlchemy ORM for customer reviews."""

# from __future__ import annotations

# from datetime import datetime
# from typing import TYPE_CHECKING, Optional

# from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, CheckConstraint, Index, text
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# import uuid

# from . import Base

# SCHEMA = "ecom_product"

# if TYPE_CHECKING:
#     from .product import Product

# class CustomerReview(Base):
#     __tablename__ = "customer_review"
#     __table_args__ = (
#         CheckConstraint("star >= 1 AND star <= 5", name="ck_customer_review_star"),
#         CheckConstraint("depth >= 0 AND depth <= 1", name="ck_customer_review_depth"),
#         Index("idx_customer_review_product", "product_id"),
#         Index("idx_customer_review_user", "user_id"),
#         Index("idx_customer_review_parent", "parent_id"),
#         {"schema": SCHEMA},
#     )

#     product_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey(f"{SCHEMA}.product._id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
#         UUID(as_uuid=True),
#         nullable=True,  # nullable: admin reply has no user
#     )
#     customer_name: Mapped[str] = mapped_column(String(255), nullable=True)
#     parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey(f"{SCHEMA}.customer_review._id", ondelete="CASCADE"),
#         nullable=True,
#     )
#     depth: Mapped[int] = mapped_column(
#         Integer,
#         nullable=False,
#         server_default=text("0"),
#     )
#     content: Mapped[str] = mapped_column(Text, nullable=False)
#     star: Mapped[Optional[int]] = mapped_column(
#         Integer,
#         nullable=True,  # nullable: admin reply carries no star
#     )

#     # Relationships
#     replies: Mapped[list[CustomerReview]] = relationship(
#         "CustomerReview",
#         back_populates="parent",
#         cascade="all, delete-orphan",
#         foreign_keys=[parent_id],
#     )
#     parent: Mapped[Optional[CustomerReview]] = relationship(
#         "CustomerReview",
#         back_populates="replies",
#         remote_side="CustomerReview._id",
#         foreign_keys=[parent_id],
#     )
#     product: Mapped["Product"] = relationship(back_populates="reviews")
