from __future__ import annotations

from typing import List, Optional
from sqlalchemy import ARRAY, Boolean, DateTime, Float, Integer, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from . import SCHEMA, ViewBase


class ProductCategoryListView(ViewBase):
    __tablename__ = "_product_category_list"
    __table_args__ = {"schema": SCHEMA, "info": {"is_view": True}}

    _id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    _created: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _updated: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _creator: Mapped[Optional[str]] = mapped_column(String(255))
    _updater: Mapped[Optional[str]] = mapped_column(String(255))
    _deleted: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _etag: Mapped[Optional[str]] = mapped_column(String(64))
    _realm: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(2048))
    brand_count: Mapped[int] = mapped_column(Integer, nullable=False)
    brand_names: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))


class ProductBrandLineListView(ViewBase):
    __tablename__ = "_product_brand_line_list"
    __table_args__ = {"schema": SCHEMA, "info": {"is_view": True}}

    _id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    _created: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _updated: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _etag: Mapped[Optional[str]] = mapped_column(String(64))
    _realm: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(2048))
    line_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    line_name: Mapped[Optional[str]] = mapped_column(String(255))
    category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    category_name: Mapped[Optional[str]] = mapped_column(String(255))
    line_created: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    line_updated: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    line_etag: Mapped[Optional[str]] = mapped_column(String(64))
    product_count: Mapped[int] = mapped_column(Integer, nullable=False)


class ProductListView(ViewBase):
    __tablename__ = "_product_list"
    __table_args__ = {"schema": SCHEMA, "info": {"is_view": True}}

    _id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    _created: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _updated: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _creator: Mapped[Optional[str]] = mapped_column(String(255))
    _updater: Mapped[Optional[str]] = mapped_column(String(255))
    _deleted: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _etag: Mapped[Optional[str]] = mapped_column(String(64))
    _realm: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(2048))
    status: Mapped[Optional[str]] = mapped_column(String(64))
    line_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    line_name: Mapped[Optional[str]] = mapped_column(String(255))
    brand_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    brand_name: Mapped[Optional[str]] = mapped_column(String(255))
    category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    category_name: Mapped[Optional[str]] = mapped_column(String(255))
    base_price: Mapped[Optional[float]] = mapped_column(Float)
    price: Mapped[Optional[float]] = mapped_column(Float)
    sku: Mapped[Optional[str]] = mapped_column(String(255))
    stock_quantity: Mapped[Optional[int]] = mapped_column(Integer)
    sale_price: Mapped[Optional[float]] = mapped_column(Float)
    discount_percent: Mapped[Optional[float]] = mapped_column(Float)
    gift: Mapped[Optional[bool]] = mapped_column(Boolean)
    promo_valid_from: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    promo_valid_to: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    primary_image_url: Mapped[Optional[str]] = mapped_column(String(2048))


class ProductDetailView(ViewBase):
    __tablename__ = "_product_detail"
    __table_args__ = {"schema": SCHEMA, "info": {"is_view": True}}

    _id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    _created: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _updated: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _creator: Mapped[Optional[str]] = mapped_column(String(255))
    _updater: Mapped[Optional[str]] = mapped_column(String(255))
    _deleted: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _etag: Mapped[Optional[str]] = mapped_column(String(64))
    _realm: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(2048))
    status: Mapped[Optional[str]] = mapped_column(String(64))
    llm_spec_text: Mapped[Optional[str]] = mapped_column(String)
    line_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    line_name: Mapped[Optional[str]] = mapped_column(String(255))
    brand_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    brand_name: Mapped[Optional[str]] = mapped_column(String(255))
    brand_description: Mapped[Optional[str]] = mapped_column(String(2048))
    category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    category_name: Mapped[Optional[str]] = mapped_column(String(255))
    variant_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    sku: Mapped[Optional[str]] = mapped_column(String(255))
    base_price: Mapped[Optional[float]] = mapped_column(Float)
    price: Mapped[Optional[float]] = mapped_column(Float)
    stock_quantity: Mapped[Optional[int]] = mapped_column(Integer)
    variant_attributes: Mapped[Optional[JSON]] = mapped_column(JSON)
    sale_price: Mapped[Optional[float]] = mapped_column(Float)
    discount_percent: Mapped[Optional[float]] = mapped_column(Float)
    gift: Mapped[Optional[bool]] = mapped_column(Boolean)
    promo_valid_from: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    promo_valid_to: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    images: Mapped[Optional[List[dict]]] = mapped_column(ARRAY(JSON))
    specs_json: Mapped[Optional[JSON]] = mapped_column(JSON)


class ProductSpecDetailView(ViewBase):
    __tablename__ = "_product_spec_detail"
    __table_args__ = {"schema": SCHEMA, "info": {"is_view": True}}

    _id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    _created: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _updated: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _etag: Mapped[Optional[str]] = mapped_column(String(64))
    _realm: Mapped[Optional[str]] = mapped_column(String(255))
    product_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    product_name: Mapped[Optional[str]] = mapped_column(String(255))
    group_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    group_name: Mapped[Optional[str]] = mapped_column(String(255))
    group_sort_order: Mapped[Optional[int]] = mapped_column(Integer)
    category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    attribute_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    attribute_name: Mapped[Optional[str]] = mapped_column(String(255))
    data_type: Mapped[Optional[str]] = mapped_column(String(64))
    unit: Mapped[Optional[str]] = mapped_column(String(64))
    attribute_sort_order: Mapped[Optional[int]] = mapped_column(Integer)
    value_text: Mapped[Optional[str]] = mapped_column(String(2048))
    value_number: Mapped[Optional[float]] = mapped_column(Float)
    value_boolean: Mapped[Optional[bool]] = mapped_column(Boolean)
    value_json: Mapped[Optional[JSON]] = mapped_column(JSON)
    display_value: Mapped[Optional[str]] = mapped_column(String(2048))


class ProductReviewListView(ViewBase):
    __tablename__ = "_product_review_list"
    __table_args__ = {"schema": SCHEMA, "info": {"is_view": True}}

    _id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    _created: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _updated: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _creator: Mapped[Optional[str]] = mapped_column(String(255))
    _updater: Mapped[Optional[str]] = mapped_column(String(255))
    _deleted: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _etag: Mapped[Optional[str]] = mapped_column(String(64))
    _realm: Mapped[Optional[str]] = mapped_column(String(255))
    product_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    product_name: Mapped[Optional[str]] = mapped_column(String(255))
    customer_name: Mapped[Optional[str]] = mapped_column(String(255))
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(String(4096))
    review_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
