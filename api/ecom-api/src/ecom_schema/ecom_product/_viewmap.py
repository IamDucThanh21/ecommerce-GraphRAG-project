from __future__ import annotations

from typing import List, Optional
from sqlalchemy import ARRAY, Boolean, DateTime, Float, Integer, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from . import SCHEMA, ViewBase


class CategoryBrandListView(ViewBase):
    __tablename__ = "_category_brand_list"
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
    slug: Mapped[Optional[str]] = mapped_column(String(255))
    logo_url: Mapped[Optional[str]] = mapped_column(String(2048))
    category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    category_name: Mapped[Optional[str]] = mapped_column(String(255))
    product_count: Mapped[int] = mapped_column(Integer, nullable=False)


class CategoryBrandLineListView(ViewBase):
    __tablename__ = "_category_brand_line_list"
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
    slug: Mapped[Optional[str]] = mapped_column(String(255))
    brand_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    brand_name: Mapped[Optional[str]] = mapped_column(String(255))
    brand_logo_url: Mapped[Optional[str]] = mapped_column(String(2048))
    product_count: Mapped[int] = mapped_column(Integer, nullable=False)
    category_names: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))

class CategoryBrandSeriesListView(ViewBase):
    __tablename__ = "_category_brand_series_list"
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
    slug: Mapped[Optional[str]] = mapped_column(String(255))
    line_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    line_name: Mapped[Optional[str]] = mapped_column(String(255))
    brand_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    brand_name: Mapped[Optional[str]] = mapped_column(String(255))
    brand_logo_url: Mapped[Optional[str]] = mapped_column(String(2048))
    product_count: Mapped[int] = mapped_column(Integer, nullable=False)
    category_names: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))

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
    # description: Mapped[Optional[str]] = mapped_column(String(2048))
    slug: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(64))
    brand_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    brand_name: Mapped[Optional[str]] = mapped_column(String(255))
    line_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    line_name: Mapped[Optional[str]] = mapped_column(String(255))
    series_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    series_name: Mapped[Optional[str]] = mapped_column(String(255))
    category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    category_name: Mapped[Optional[str]] = mapped_column(String(255))
    primary_image_url: Mapped[Optional[str]] = mapped_column(String(2048))
    sku: Mapped[Optional[str]] = mapped_column(String(255))
    price: Mapped[Optional[float]] = mapped_column(Float)
    base_price: Mapped[Optional[float]] = mapped_column(Float)
    stock_quantity: Mapped[Optional[int]] = mapped_column(Integer)
    variant_status: Mapped[Optional[str]] = mapped_column(String(64))
    tag: Mapped[Optional[str]] = mapped_column(String(255))


class ProductVariantListView(ViewBase):
    __tablename__ = "_product_variant_list"
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
    product_slug: Mapped[Optional[str]] = mapped_column(String(255))
    product_status: Mapped[Optional[str]] = mapped_column(String(64))
    sku: Mapped[Optional[str]] = mapped_column(String(255))
    price: Mapped[Optional[float]] = mapped_column(Float)
    base_price: Mapped[Optional[float]] = mapped_column(Float)
    stock_quantity: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(64))
    tag: Mapped[Optional[str]] = mapped_column(String(255))
    attributes: Mapped[Optional[JSON]] = mapped_column(JSON)
    primary_image_url: Mapped[Optional[str]] = mapped_column(String(2048))
    image_urls: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    specs: Mapped[Optional[JSON]] = mapped_column(JSON)


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
    slug: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(64))
    brand_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    brand_name: Mapped[Optional[str]] = mapped_column(String(255))
    brand_slug: Mapped[Optional[str]] = mapped_column(String(255))
    brand_logo_url: Mapped[Optional[str]] = mapped_column(String(2048))
    line_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    line_name: Mapped[Optional[str]] = mapped_column(String(255))
    line_slug: Mapped[Optional[str]] = mapped_column(String(255))
    series_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    series_name: Mapped[Optional[str]] = mapped_column(String(255))
    series_slug: Mapped[Optional[str]] = mapped_column(String(255))
    primary_category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    primary_category_name: Mapped[Optional[str]] = mapped_column(String(255))
    category_names: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    primary_image_url: Mapped[Optional[str]] = mapped_column(String(2048))
    image_urls: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    variant_count: Mapped[Optional[int]] = mapped_column(Integer)
    price_min: Mapped[Optional[float]] = mapped_column(Float)
    price_max: Mapped[Optional[float]] = mapped_column(Float)
    total_stock: Mapped[Optional[int]] = mapped_column(Integer)
    specs: Mapped[Optional[JSON]] = mapped_column(JSON)
    spec_groups: Mapped[Optional[JSON]] = mapped_column(JSON)
