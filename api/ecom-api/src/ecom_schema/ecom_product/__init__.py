from .. import create_base_model, create_view_model, logger

SCHEMA = "ecom_product"
USER_PROFILE_SCHEMA = 'ecom_user'
Base = create_base_model(SCHEMA)
ViewBase = create_view_model(SCHEMA)

# Import all models to register them with the base
from . import (
    product,
    product_brand,
    product_category,
    product_line,
    product_series,
    product_category_mapping,
    product_variant,
    product_image,
    spec_group_template,
    spec_attribute_template,
    product_spec_group,
    product_spec_value,
    product_spec_flat,
    # promotion,
    # customer_review,
    _viewmap,  # noqa: F401
)

__all__ = [
    "product",
    "product_brand",
    "product_category",
    "product_line",
    "product_series",
    "product_category_mapping",
    "product_variant",
    "product_image",
    "spec_group_template",
    "spec_attribute_template",
    "product_spec_group",
    "product_spec_value",
    "product_spec_flat",
    # "promotion",
    # "customer_review",
]
