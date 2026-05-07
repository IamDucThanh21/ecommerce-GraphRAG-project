# """SQLAlchemy ORM for product promotions."""

# from __future__ import annotations

# from datetime import datetime
# from typing import TYPE_CHECKING, Optional

# from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from . import Base

# SCHEMA = "ecom_product"

# if TYPE_CHECKING:
#     from .product import Product


# class Promotion(Base):
#     __tablename__ = "promotion"

#     product_id: Mapped[str] = mapped_column(
#         UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product._id"), nullable=False
#     )
#     discount_percent: Mapped[int] = mapped_column(Integer, nullable=False)
#     gift: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
#     valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
#     valid_to: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

#     product: Mapped["Product"] = relationship(back_populates="promotions")
