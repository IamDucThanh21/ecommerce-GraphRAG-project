from enum import Enum


class ProductStatusEnum(str, Enum):
    """Product status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    DISCONTINUED = "discontinued"


class ProductVariantStatusEnum(str, Enum):
    """Product variant status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"


class SpecDataTypeEnum(str, Enum):
    """Specification data type enumeration (for templates)."""
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    TEXT_LIST = "text_list"