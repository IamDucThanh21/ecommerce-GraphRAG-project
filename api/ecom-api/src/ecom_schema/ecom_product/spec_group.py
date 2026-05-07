"""
DEPRECATED: This module has been replaced by spec_group_template and product_spec_group modules.

- SpecGroup (old) → SpecGroupTemplate (template for category) + ProductSpecGroup (instance per product)
- SpecAttribute (old) → SpecAttributeTemplate (template definition)

Please update your imports to use:
  from .spec_group_template import SpecGroupTemplate
  from .product_spec_group import ProductSpecGroup
  from .spec_attribute_template import SpecAttributeTemplate
"""

# Re-export for backwards compatibility during migration
from .spec_group_template import SpecGroupTemplate as SpecGroup

__all__ = ["SpecGroup"]

