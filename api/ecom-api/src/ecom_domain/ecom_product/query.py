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

        backend_model = "_product_category_list"
        name = "Product Category List"
        desc = "Query categories with brand summary data."

    name: Optional[str] = StringField("Category Name", source="name")
    description: Optional[str] = StringField("Description", source="description")
    brand_count: Optional[int] = IntegerField("Brand Count", source="brand_count")
    brand_names: Optional[List[str]] = ArrayField("Brand Names", source="brand_names")


@resource("product_brand_line_list")
class ProductBrandLineListQuery(DomainQueryResource):
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_product_brand_line_list"
        name = "Product Brand Line List"
        desc = "Query product brand and product line pairs."

    name: Optional[str] = StringField("Brand Name", source="name")
    description: Optional[str] = StringField("Brand Description", source="description")
    line_id: Optional[str] = UUIDField("Product Line ID", source="line_id")
    line_name: Optional[str] = StringField("Line Name", source="line_name")
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
        desc = "Query products with primary image and sale price."

    name: Optional[str] = StringField("Product Name", source="name")
    description: Optional[str] = StringField("Description", source="description")
    status: Optional[str] = StringField("Status", source="status")
    line_id: Optional[str] = UUIDField("Product Line ID", source="line_id")
    line_name: Optional[str] = StringField("Line Name", source="line_name")
    brand_id: Optional[str] = UUIDField("Brand ID", source="brand_id")
    brand_name: Optional[str] = StringField("Brand Name", source="brand_name")
    category_id: Optional[str] = UUIDField("Category ID", source="category_id")
    category_name: Optional[str] = StringField("Category Name", source="category_name")
    base_price: Optional[float] = FloatField("Base Price", source="base_price")
    price: Optional[float] = FloatField("Variant Price", source="price")
    sku: Optional[str] = StringField("SKU", source="sku")
    stock_quantity: Optional[int] = IntegerField("Stock Quantity", source="stock_quantity")
    sale_price: Optional[float] = FloatField("Sale Price", source="sale_price")
    discount_percent: Optional[float] = FloatField("Discount Percent", source="discount_percent")
    gift: Optional[bool] = BooleanField("Gift", source="gift")
    promo_valid_from: Optional[datetime] = DatetimeField("Promo Valid From", source="promo_valid_from")
    promo_valid_to: Optional[datetime] = DatetimeField("Promo Valid To", source="promo_valid_to")
    primary_image_url: Optional[str] = StringField("Primary Image URL", source="primary_image_url")


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
        desc = "Query full product detail rows including variants, images and specs."

    name: Optional[str] = StringField("Product Name", source="name")
    description: Optional[str] = StringField("Description", source="description")
    status: Optional[str] = StringField("Status", source="status")
    llm_spec_text: Optional[str] = StringField("LLM Spec Text", source="llm_spec_text")
    line_id: Optional[str] = UUIDField("Product Line ID", source="line_id")
    line_name: Optional[str] = StringField("Line Name", source="line_name")
    brand_id: Optional[str] = UUIDField("Brand ID", source="brand_id")
    brand_name: Optional[str] = StringField("Brand Name", source="brand_name")
    brand_description: Optional[str] = StringField("Brand Description", source="brand_description")
    category_id: Optional[str] = UUIDField("Category ID", source="category_id")
    category_name: Optional[str] = StringField("Category Name", source="category_name")
    variant_id: Optional[str] = UUIDField("Variant ID", source="variant_id")
    sku: Optional[str] = StringField("SKU", source="sku")
    base_price: Optional[float] = FloatField("Base Price", source="base_price")
    price: Optional[float] = FloatField("Variant Price", source="price")
    stock_quantity: Optional[int] = IntegerField("Stock Quantity", source="stock_quantity")
    variant_attributes: Optional[dict] = JSONField("Variant Attributes", source="variant_attributes")
    sale_price: Optional[float] = FloatField("Sale Price", source="sale_price")
    discount_percent: Optional[float] = FloatField("Discount Percent", source="discount_percent")
    gift: Optional[bool] = BooleanField("Gift", source="gift")
    promo_valid_from: Optional[datetime] = DatetimeField("Promo Valid From", source="promo_valid_from")
    promo_valid_to: Optional[datetime] = DatetimeField("Promo Valid To", source="promo_valid_to")
    images: Optional[List[dict]] = JSONField("Images", source="images")
    specs_json: Optional[dict] = JSONField("Specs JSON", source="specs_json")


@resource("product_spec_detail")
class ProductSpecDetailQuery(DomainQueryResource):
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_product_spec_detail"
        name = "Product Spec Detail"
        desc = "Query grouped product specification rows."

    product_id: Optional[str] = UUIDField("Product ID", source="product_id")
    product_name: Optional[str] = StringField("Product Name", source="product_name")
    group_id: Optional[str] = UUIDField("Group ID", source="group_id")
    group_name: Optional[str] = StringField("Group Name", source="group_name")
    group_sort_order: Optional[int] = IntegerField("Group Sort Order", source="group_sort_order")
    category_id: Optional[str] = UUIDField("Category ID", source="category_id")
    attribute_id: Optional[str] = UUIDField("Attribute ID", source="attribute_id")
    attribute_name: Optional[str] = StringField("Attribute Name", source="attribute_name")
    data_type: Optional[str] = StringField("Data Type", source="data_type")
    unit: Optional[str] = StringField("Unit", source="unit")
    attribute_sort_order: Optional[int] = IntegerField("Attribute Sort Order", source="attribute_sort_order")
    value_text: Optional[str] = StringField("Value Text", source="value_text")
    value_number: Optional[float] = FloatField("Value Number", source="value_number")
    value_boolean: Optional[bool] = BooleanField("Value Boolean", source="value_boolean")
    value_json: Optional[dict] = JSONField("Value JSON", source="value_json")
    display_value: Optional[str] = StringField("Display Value", source="display_value")


@resource("product_review_list")
class ProductReviewListQuery(DomainQueryResource):
    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')
        
        backend_model = "_product_review_list"
        name = "Product Review List"
        desc = "Query product reviews with rating and comment text."

    product_id: Optional[str] = UUIDField("Product ID", source="product_id")
    product_name: Optional[str] = StringField("Product Name", source="product_name")
    customer_name: Optional[str] = StringField("Customer Name", source="customer_name")
    rating: Optional[int] = IntegerField("Rating", source="rating")
    comment: Optional[str] = StringField("Comment", source="comment")
    review_date: Optional[datetime] = DatetimeField("Review Date", source="review_date")
