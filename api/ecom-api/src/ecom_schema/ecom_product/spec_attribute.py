"""
DEPRECATED: This module has been replaced by spec_attribute_template module.

- SpecAttribute (old) → SpecAttributeTemplate (template definition per group)

The new architecture separates:
  1. Template layer: SpecAttributeTemplate (defines how specs should look)
  2. Instance layer: ProductSpecValue (actual values for each product)

Please update your imports to use:
  from .spec_attribute_template import SpecAttributeTemplate
"""

# Re-export for backwards compatibility during migration
from .spec_attribute_template import SpecAttributeTemplate as SpecAttribute

__all__ = ["SpecAttribute"]

