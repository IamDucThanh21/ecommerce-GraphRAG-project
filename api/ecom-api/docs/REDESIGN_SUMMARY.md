# ecom_schema/ecom_product Redesign Summary

## Overview
The `ecom_product` schema has been completely redesigned to follow the comprehensive `ecom_product_schema.md` specification. This ensures alignment between the database schema definition and the SQLAlchemy ORM models.

---

## Key Changes

### 1. New Models Created

#### **ProductSeries** (`product_series.py`)
- Represents series within a product line (e.g., iPhone 17 Series, Galaxy S25)
- Fields: `line_id` (FK), `name`, `slug`, `description`
- Constraint: `UNIQUE(line_id, slug)` ensures uniqueness within a line
- Relationships: belongs to `ProductLine`, has many `Product`s

#### **ProductCategoryMapping** (`product_category_mapping.py`)
- N:N relationship table between products and categories
- Fields: `product_id`, `category_id`, `is_primary`
- Constraint: `UNIQUE(product_id, category_id)` prevents duplicate mappings
- Allows products to belong to multiple categories with one marked as primary

#### **SpecGroupTemplate** (`spec_group_template.py`)
- **Template layer** for specification groups at the category level
- Fields: `category_id` (FK), `name`, `sort_order`
- Replaces the old `spec_group` which mixed template and instance concerns
- Relationships: belongs to `ProductCategory`, has many `SpecAttributeTemplate`s

#### **SpecAttributeTemplate** (`spec_attribute_template.py`)
- **Template layer** for specification attributes
- Fields: `group_template_id`, `key` (snake_case, stable), `label`, `data_type`, `unit`, `is_filterable`, `is_required`, `sort_order`
- Data types: `text`, `number`, `boolean`, `text_list`
- Constraint: `UNIQUE(group_template_id, key)` ensures no duplicate keys per group
- Replaces the old `spec_attribute` with more detailed metadata

#### **ProductSpecGroup** (`product_spec_group.py`)
- **Instance layer** - represents a spec group for a specific product
- Fields: `product_id`, `group_template_id` (nullable for free-form groups), `name`, `sort_order`
- Can be created from template or added freely by admins
- Relationships: belongs to `Product`, `SpecGroupTemplate`, has many `ProductSpecValue`s

---

### 2. Models Updated

#### **ProductBrand**
- ✅ Added `slug` field (unique)
- ✅ Changed `description` from `String(255)` to `Text` for better content
- ✅ Added `logo_url` field (varchar 500)
- ✅ Added relationship to `Product` (direct brand link for small brands without lines/series)

#### **ProductLine**
- ✅ Added `slug` field (unique within brand: `UNIQUE(brand_id, slug)`)
- ❌ Removed `category_id` (categories now map via `ProductCategoryMapping`)
- ✅ Changed `description` from `String(255)` to `Text`
- ✅ Removed relationship to `ProductCategory`
- ✅ Added relationship to `ProductSeries`

#### **ProductCategory**
- ✅ Added `parent_id` for recursive tree hierarchy (self-referential FK)
- ✅ Added `slug` field (globally unique)
- ✅ Changed `description` from `String(255)` to `Text`
- ✅ Added self-relationships: `parent`, `children` for tree traversal
- ❌ Removed relationship to `ProductLine`
- ✅ Updated to reference `SpecGroupTemplate` instead of `SpecGroup`

#### **Product**
- ✅ Added `slug` field (globally unique)
- ✅ Added `series_id` (nullable)
- ❌ Removed `base_price` and `sale_price` (moved to variants)
- ❌ Removed `llm_spec_text` (not in spec)
- ✅ Changed `line_id` from required to optional
- ✅ Added check constraint: `series_id IS NULL OR line_id IS NOT NULL`
- ✅ Updated category relationship to use `ProductCategoryMapping`
- ✅ Replaced `spec_values` relationship with `spec_groups` (now uses ProductSpecGroup)
- ✅ Added relationships: `brand`, `series`, `category_mappings`

#### **ProductVariant**
- ✅ Added `base_price` field (price before discount)
- ✅ Renamed `price` field semantics (now represents current/sale price)
- ✅ Added `status` field (active/inactive/out_of_stock) with enum
- ✅ Changed `sku` constraint to use explicit `UNIQUE` constraint
- ✅ Added relationship to `ProductImage` items

#### **ProductImage**
- ✅ Added `variant_id` (nullable) to support variant-specific images
- ✅ Added `sort_order` field for image ordering
- ✅ Added relationship to `ProductVariant`

#### **ProductSpecValue**
- ✅ Replaced `product_id` FK with `product_spec_group_id`
- ✅ Replaced `attribute_id` FK with `attribute_template_id`
- ✅ Added `key` and `label` fields (copy from template or custom)
- ✅ Added `value_unit` field separate from value
- ✅ Added `is_filterable` field (allows override from template)
- ✅ Added `sort_order` field
- ✅ Removed `value_json` field (use `value_text` with JSON string instead)
- ✅ Added partial indexes for efficient filtering:
  - `(key, value_number) WHERE is_filterable = true`
  - `(key, value_text) WHERE is_filterable = true`

---

### 3. Enums Updated (`types.py`)

#### **ProductStatusEnum**
- Changed from: `DRAFT, ACTIVE, INACTIVE, OUT_OF_STOCK, DISCONTINUED, ARCHIVED`
- Changed to: `DRAFT, ACTIVE, DISCONTINUED` (lowercase values)

#### **ProductVariantStatusEnum** (new)
- Values: `ACTIVE, INACTIVE, OUT_OF_STOCK`
- Purpose: Manages variant lifecycle independent from product status

#### **SpecDataTypeEnum** (renamed)
- Changed from: `SpecTypeEnum` with values `TEXT, NUMBER, BOOLEAN, JSON, SELECT, MULTISELECT`
- Changed to: `SpecDataTypeEnum` with values `text, number, boolean, text_list` (lowercase)
- Removed `SELECT` and `MULTISELECT` (use `text_list` for multiple values)

---

### 4. Files Removed (Deprecated)

- `spec_group.py` - Now aliased to `SpecGroupTemplate` for backwards compatibility
- `spec_attribute.py` - Now aliased to `SpecAttributeTemplate` for backwards compatibility

Both files include deprecation notices directing users to the new modules.

---

### 5. Updated Exports (`__init__.py` and `_schema.py`)

New models added to exports:
- `product_series`
- `product_category_mapping`
- `spec_group_template`
- `spec_attribute_template`
- `product_spec_group`

Removed/renamed:
- `spec_group` (use `spec_group_template`)
- `spec_attribute` (use `spec_attribute_template`)

---

## Architecture Changes

### Old Architecture (Flat)
```
Product → [base_price, sale_price]
Product → SpecGroup (mixed template + instance)
     └─ SpecAttribute (template definition)
          └─ ProductSpecValue (actual values)
```

### New Architecture (Layered)
```
Category → SpecGroupTemplate (defines group structure)
     └─ SpecAttributeTemplate (defines attribute structure)

Product → ProductSpecGroup (instance of group per product)
     └─ ProductSpecValue (actual values)

Product → ProductCategoryMapping (N:N to categories)
Product → ProductVariant → [price, base_price, status]
```

### Benefits
1. **Clear separation**: Templates are immutable definitions, instances are product-specific
2. **Flexibility**: Admins can add custom spec groups/attributes without following templates
3. **Multiple categories**: Products can belong to multiple categories with primary designation
4. **Complete hierarchy**: Supporting small brands (no line/series) and large ones (full hierarchy)
5. **Variant pricing**: Base and current prices managed at variant level
6. **Efficient filtering**: Partial indexes only on filterable specs

---

## Migration Notes

### For Database Migrations
You will need to create Alembic migrations for:
1. New tables: `product_series`, `product_category_mapping`, `spec_group_template`, `spec_attribute_template`, `product_spec_group`
2. Table modifications: `product_brand`, `product_line`, `product_category`, `product`, `product_variant`, `product_image`, `product_spec_value`
3. Dropped columns: `category_id` from `product_line`, `base_price`/`sale_price`/`llm_spec_text` from `product`
4. Dropped tables: `spec_group`, `spec_attribute` (if data migrated)

### For Application Code
1. **Spec management**: Replace direct `spec_group`/`spec_attribute` with template + instance pattern
2. **Category assignment**: Use `ProductCategoryMapping` for N:N relationships
3. **Pricing**: Access prices from `ProductVariant`, not `Product`
4. **Line/Series assignment**: Series now requires Line, add validation logic
5. **Filter queries**: Use partial indexes on `ProductSpecValue` with `is_filterable=true`

---

## Validation Status

✅ All Python files validated for syntax errors
✅ All relationships properly defined
✅ All constraints and indexes specified
✅ Foreign keys with proper ON DELETE rules
✅ Check constraints for data integrity

---

## Next Steps

1. **Create database migration** using Alembic
2. **Update API endpoints** to handle new relationships
3. **Implement spec management** using template + instance pattern
4. **Add data migration scripts** for existing products/specs
5. **Update documentation** with new schema architecture
6. **Add validation rules** for required vs optional fields per category
