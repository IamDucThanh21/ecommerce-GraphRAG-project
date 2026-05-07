# """SQLAlchemy ORM for customer reviews."""

# from __future__ import annotations

# from datetime import datetime
# from typing import TYPE_CHECKING, Optional

# from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from . import Base

# SCHEMA = "ecom_product"

# if TYPE_CHECKING:
#     from .product import Product


# class CustomerReview(Base):
#     __tablename__ = "customer_review"

#     product_id: Mapped[str] = mapped_column(
#         UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product._id"), nullable=False
#     )
#     customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
#     rating: Mapped[int] = mapped_column(Integer, nullable=False)
#     comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#     review_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

#     product: Mapped["Product"] = relationship(back_populates="reviews")
