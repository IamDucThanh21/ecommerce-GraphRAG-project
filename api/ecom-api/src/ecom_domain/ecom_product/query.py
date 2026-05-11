from typing import List, Optional
from datetime import datetime

from fluvius.query import DomainQueryManager, DomainQueryResource
from fluvius.query.field import (
    StringField,
    UUIDField,
    BooleanField,
    IntegerField,
    FloatField,
    ArrayField,
    JSONField,
    DateField,
    DatetimeField,
)

from .domain import ECOMProductServiceDomain
from .state import ECOMProductStateManager


class ECOMProductQueryManager(DomainQueryManager):
    """Query manager for ECOM Product domain."""

    __data_manager__ = ECOMProductStateManager

    class Meta(DomainQueryResource.Meta):
        prefix = ECOMProductServiceDomain.Meta.namespace
        tags = ECOMProductServiceDomain.Meta.tags


resource = ECOMProductQueryManager.register_resource
endpoint = ECOMProductQueryManager.register_endpoint


@resource("product_category_list")
class ProductCategoryListQuery(DomainQueryResource):
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "product_category"

    name: Optional[str] = StringField("Category Name", source="name")
    description: Optional[str] = StringField("Description", source="description")
    slug: Optional[int] = IntegerField("Slug", source="slug")

@resource("category-brand-list")
class ProductBrandListQuery(DomainQueryResource):
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_product_brand_list"
        name = "Product Brand List"
        desc = "Query brands with product and category counts."

    name: Optional[str] = StringField("Brand Name", source="name")
    description: Optional[str] = StringField("Description", source="description")
    slug: Optional[str] = StringField("Brand Slug", source="slug")
    logo_url: Optional[str] = StringField("Brand Logo URL", source="logo_url")
    category_id: Optional[str] = UUIDField("Category ID", source="category_id")
    category_name: Optional[str] = StringField("Category Name", source="category_name")
    product_count: Optional[int] = IntegerField("Product Count", source="product_count")

@resource("product_line_list")
class ProductLineListQuery(DomainQueryResource):
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_product_line_list"
        name = "Product Line List"
        desc = "Query product lines with aggregated product and category info."

    name: Optional[str] = StringField("Line Name", source="name")
    description: Optional[str] = StringField("Description", source="description")
    slug: Optional[str] = StringField("Line Slug", source="slug")
    brand_id: Optional[str] = UUIDField("Brand ID", source="brand_id")
    brand_name: Optional[str] = StringField("Brand Name", source="brand_name")
    brand_logo_url: Optional[str] = StringField("Brand Logo URL", source="brand_logo_url")
    product_count: Optional[int] = IntegerField("Product Count", source="product_count")
    product_names: Optional[List[str]] = ArrayField("Product Names", source="product_names")
    category_count: Optional[int] = IntegerField("Category Count", source="category_count")
    category_names: Optional[List[str]] = ArrayField("Category Names", source="category_names")

@resource("product_brand_line_list")
class ProductBrandLineListQuery(DomainQueryResource):
    """DEPRECATED - Use product_line_list instead."""
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_product_line_list"
        name = "Product Brand Line List (Deprecated)"
        desc = "Query product brand and product line pairs. DEPRECATED - Use product_line_list."

    name: Optional[str] = StringField("Brand Name", source="name")
    description: Optional[str] = StringField("Brand Description", source="description")
    line_id: Optional[str] = UUIDField("Product Line ID", source="_id")
    line_name: Optional[str] = StringField("Line Name", source="name")
    category_id: Optional[str] = UUIDField("Category ID", source="category_id")
    category_name: Optional[str] = StringField("Category Name", source="category_name")
    product_count: Optional[int] = IntegerField("Product Count", source="product_count")


@resource("product_list")
class ProductListQuery(DomainQueryResource):
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_product_list"
        name = "Product List"
        desc = "Query products with brand, line, series and category info."

    name: Optional[str] = StringField("Product Name", source="name")
    description: Optional[str] = StringField("Description", source="description")
    slug: Optional[str] = StringField("Product Slug", source="slug")
    status: Optional[str] = StringField("Product Status", source="status")
    brand_id: Optional[str] = UUIDField("Brand ID", source="brand_id")
    brand_name: Optional[str] = StringField("Brand Name", source="brand_name")
    line_id: Optional[str] = UUIDField("Product Line ID", source="line_id")
    line_name: Optional[str] = StringField("Product Line Name", source="line_name")
    series_id: Optional[str] = UUIDField("Product Series ID", source="series_id")
    series_name: Optional[str] = StringField("Product Series Name", source="series_name")
    category_id: Optional[str] = UUIDField("Category ID", source="category_id")
    category_name: Optional[str] = StringField("Category Name", source="category_name")
    primary_image_url: Optional[str] = StringField("Primary Image URL", source="primary_image_url")
    sku: Optional[str] = StringField("SKU", source="sku")
    price: Optional[float] = FloatField("Variant Price", source="price")
    base_price: Optional[float] = FloatField("Base Price", source="base_price")
    stock_quantity: Optional[int] = IntegerField("Stock Quantity", source="stock_quantity")
    variant_status: Optional[str] = StringField("Variant Status", source="variant_status")
    tag: Optional[str] = StringField("Variant Tag", source="tag")


@resource("product_list_scoped")
class ProductListScopedQuery(ProductListQuery):
    """Scoped product list query - filter by brand_id, line_id, series_id or category_id."""
    
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_product_list"
        name = "Product List (Scoped)"
        desc = "Query products with scope filtering by brand, line, series or category."

    # Scope filtering fields
    scope_type: Optional[str] = StringField(
        "Scope Type", 
        source=None,  # Not from DB, used for filtering logic
        help_text="Filter scope: 'brand_id', 'line_id', 'series_id', or 'category_id'"
    )
    scope_value: Optional[str] = UUIDField(
        "Scope Value",
        source=None,  # Not from DB, the UUID to filter by
        help_text="UUID value for the selected scope type"
    )

    def apply_filters(self, query, filters):
        """Apply scope-based filtering to the query."""
        # Call parent filter logic first
        query = super().apply_filters(query, filters)
        
        # Apply scope filtering if both scope_type and scope_value are provided
        scope_type = filters.get('scope_type')
        scope_value = filters.get('scope_value')
        
        if scope_type and scope_value:
            if scope_type == 'brand_id':
                query = query.filter(self._model.brand_id == scope_value)
            elif scope_type == 'line_id':
                query = query.filter(self._model.line_id == scope_value)
            elif scope_type == 'series_id':
                query = query.filter(self._model.series_id == scope_value)
            elif scope_type == 'category_id':
                query = query.filter(self._model.category_id == scope_value)
        
        return query


@resource("product_variant_list")
class ProductVariantListQuery(DomainQueryResource):
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_product_variant_list"
        name = "Product Variant List"
        desc = "Query product variants with specs and images."

    product_id: Optional[str] = UUIDField("Product ID", source="product_id")
    product_name: Optional[str] = StringField("Product Name", source="product_name")
    product_slug: Optional[str] = StringField("Product Slug", source="product_slug")
    product_status: Optional[str] = StringField("Product Status", source="product_status")
    sku: Optional[str] = StringField("SKU", source="sku")
    price: Optional[float] = FloatField("Variant Price", source="price")
    base_price: Optional[float] = FloatField("Base Price", source="base_price")
    stock_quantity: Optional[int] = IntegerField("Stock Quantity", source="stock_quantity")
    status: Optional[str] = StringField("Variant Status", source="status")
    tag: Optional[str] = StringField("Variant Tag", source="tag")
    attributes: Optional[dict] = JSONField("Attributes", source="attributes")
    primary_image_url: Optional[str] = StringField("Primary Image URL", source="primary_image_url")
    image_urls: Optional[List[str]] = ArrayField("Image URLs", source="image_urls")
    specs: Optional[dict] = JSONField("Specs", source="specs")


@resource("product_detail")
class ProductDetailQuery(DomainQueryResource):
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_product_detail"
        name = "Product Detail"
        desc = "Query full product detail with variants, images and specs."

    name: Optional[str] = StringField("Product Name", source="name")
    description: Optional[str] = StringField("Description", source="description")
    slug: Optional[str] = StringField("Product Slug", source="slug")
    status: Optional[str] = StringField("Product Status", source="status")
    brand_id: Optional[str] = UUIDField("Brand ID", source="brand_id")
    brand_name: Optional[str] = StringField("Brand Name", source="brand_name")
    brand_slug: Optional[str] = StringField("Brand Slug", source="brand_slug")
    brand_logo_url: Optional[str] = StringField("Brand Logo URL", source="brand_logo_url")
    line_id: Optional[str] = UUIDField("Product Line ID", source="line_id")
    line_name: Optional[str] = StringField("Line Name", source="line_name")
    line_slug: Optional[str] = StringField("Line Slug", source="line_slug")
    series_id: Optional[str] = UUIDField("Product Series ID", source="series_id")
    series_name: Optional[str] = StringField("Series Name", source="series_name")
    series_slug: Optional[str] = StringField("Series Slug", source="series_slug")
    primary_category_id: Optional[str] = UUIDField("Primary Category ID", source="primary_category_id")
    primary_category_name: Optional[str] = StringField("Primary Category Name", source="primary_category_name")
    category_names: Optional[List[str]] = ArrayField("Category Names", source="category_names")
    primary_image_url: Optional[str] = StringField("Primary Image URL", source="primary_image_url")
    image_urls: Optional[List[str]] = ArrayField("Image URLs", source="image_urls")
    variant_count: Optional[int] = IntegerField("Variant Count", source="variant_count")
    price_min: Optional[float] = FloatField("Price Min", source="price_min")
    price_max: Optional[float] = FloatField("Price Max", source="price_max")
    total_stock: Optional[int] = IntegerField("Total Stock", source="total_stock")
    specs: Optional[dict] = JSONField("Specs", source="specs")
    spec_groups: Optional[dict] = JSONField("Spec Groups", source="spec_groups")
