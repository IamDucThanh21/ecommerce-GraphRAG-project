from pydantic import BaseModel
from fluvius.query.field import UUIDField
from fluvius.data import UUID_TYPE


class BrandIdScope(BaseModel):
    brand_id: UUID_TYPE = UUIDField("Brand ID")

class ProductIdScope(BaseModel):
    product_id: UUID_TYPE = UUIDField("Product ID")