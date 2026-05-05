from enum import Enum

class ProductStatusEnum(str, Enum):
    """Product status enumeration."""
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    DISCONTINUED = "DISCONTINUED"
    ARCHIVED = "ARCHIVED"

class SpecTypeEnum(str, Enum):
    """Specification type enumeration."""
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    JSON = "JSON"
    SELECT = "SELECT"
    MULTISELECT = "MULTISELECT"