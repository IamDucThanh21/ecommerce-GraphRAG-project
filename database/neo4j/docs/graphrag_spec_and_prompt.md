# Phone Product GraphRAG — Full Specification & Copilot Prompt

---

## PART 1: GRAPH DATABASE SPECIFICATION

### 1.1 Overview

A GraphRAG-based product knowledge graph for a phone e-commerce chatbot.
The graph must support:
- Local queries: "What colors does iPhone 17 Pro Max have?"
- Global queries: "Which phones have the same chip as iPhone 17 Pro?"
- Comparison queries: "Compare camera specs between iPhone 17 Pro and iPhone 16 Pro Max"
- Recommendation queries: "Which phone upgraded from iPhone 15?"

---

### 1.2 Node Definitions

#### `Brand`
| Property     | Type   | Description                      |
|--------------|--------|----------------------------------|
| `brand_id`   | String | Unique ID, e.g. `"apple"`       |
| `name`       | String | e.g. `"Apple"`                  |
| `country`    | String | e.g. `"USA"`                    |

#### `Series`
| Property     | Type   | Description                          |
|--------------|--------|--------------------------------------|
| `series_id`  | String | Unique slug, e.g. `"iphone-17"`     |
| `name`       | String | e.g. `"iPhone 17"`                  |

#### `Model`
The core entity representing a phone model (e.g. iPhone 17 Pro Max).
All variants (storage, color) of the same model share this node.

| Property           | Type    | Description                                          |
|--------------------|---------|------------------------------------------------------|
| `model_id`         | String  | Unique slug, e.g. `"iphone-17-pro-max"`             |
| `name`             | String  | e.g. `"iPhone 17 Pro Max"`                          |
| `tier`             | String  | `"standard"` / `"pro"` / `"pro_max"` / `"plus"` / `"air"` / `"e"` |
| `release_year`     | Integer | e.g. `2025`                                          |
| `status`           | String  | `"available"` / `"discontinued"` / `"upcoming"`     |
| `os`               | String  | e.g. `"iOS 26"`                                      |
| `colors_available` | List    | All color names, e.g. `["Cam Vũ Trụ", "Bạc", "Xanh Đậm"]` |
| `storage_options`  | List    | Available storage in GB, e.g. `[256, 512, 1024, 2048]` |
| `summary`          | String  | 2–3 sentence LLM-readable description for GraphRAG  |
| `tagline`          | String  | Short highlights, e.g. `"Chip A19 Pro, 48MP, IP68"` |
| `text_content`     | String  | Full text block for GraphRAG community indexing      |
| **Denormalized specs** (for fast query without graph traversal): | | |
| `chip`             | String  | e.g. `"A19 Pro"`                                    |
| `display_size_in`  | Float   | e.g. `6.9`                                          |
| `display_hz`       | Integer | e.g. `120`                                          |
| `main_camera_mp`   | Integer | e.g. `48`                                           |
| `weight_g`         | Integer | e.g. `231`                                          |
| `ip_rating`        | String  | e.g. `"IP68"`                                       |
| `back_material`    | String  | e.g. `"Kính"`                                       |
| `frame_material`   | String  | e.g. `"Titanium"` / `"Nhôm"`                       |

#### `ModelStorage`
Represents a specific storage tier of a model. Price lives here because
price differs by storage but NOT by color.

| Property          | Type   | Description                              |
|-------------------|--------|------------------------------------------|
| `model_storage_id`| String | e.g. `"iphone-17-pro-max-256gb"`        |
| `storage_gb`      | Integer| e.g. `256`                              |
| `base_price`      | Float  | Original price in VND                   |
| `sale_price`      | Float  | Current sale price in VND               |
| `currency`        | String | `"VND"`                                 |

**Key design decision:** Price does NOT go on Variant (SKU), because within
the same model, all colors at the same storage have the same price.
This avoids duplicating price data N times (once per color).

#### `ColorFamily`
Abstract concept of a color name that spans multiple phone generations.
e.g. "Titan Tự Nhiên" appears on iPhone 15 Pro AND 16 Pro, but they look
different — so each generation has its own `ColorVariant` node, but both
link to the same `ColorFamily`.

| Property     | Type   | Description                                      |
|--------------|--------|--------------------------------------------------|
| `family_id`  | String | Slugified color name, e.g. `"titan-tu-nhien"`   |
| `name`       | String | e.g. `"Titan Tự Nhiên"`                         |

#### `ColorVariant`
The actual physical color as it appears on a specific model generation.
Different generations with the same color name may have different hex values,
so this is NOT shared across models.

| Property          | Type   | Description                                         |
|-------------------|--------|-----------------------------------------------------|
| `color_variant_id`| String | e.g. `"iphone-17-pro-max-cam-vu-tru"`              |
| `name`            | String | Display name, e.g. `"Cam Vũ Trụ"`                 |
| `model_specific`  | String | model_id this color belongs to                      |
| `image_url`       | String | URL to product image for this color                 |
| `color_price`     | Float  | Price for this color (same as ModelStorage.sale_price in current data) |

#### `Variant` (SKU)
The actual purchasable unit. A specific combination of ModelStorage × ColorVariant.
Stock lives here. This is what a customer actually adds to cart.

| Property  | Type   | Description                                              |
|-----------|--------|----------------------------------------------------------|
| `sku_id`  | String | e.g. `"iphone-17-pro-max-256gb-cam-vu-tru"`            |
| `stock`   | String | `"in_stock"` / `"out_of_stock"` / `"pre_order"`        |

#### `SpecCategory`
Groups related technical specifications. Corresponds to spec table sections.
Examples: "Màn hình", "Camera sau", "Chip & hiệu năng", "Pin & sạc".

| Property          | Type   | Description                                         |
|-------------------|--------|-----------------------------------------------------|
| `spec_category_id`| String | e.g. `"iphone-17-pro-max-camera-sau"`              |
| `name`            | String | Vietnamese category name, e.g. `"Camera sau"`      |
| `features`        | String | JSON string of non-node specs: `[{"name":"...", "value":"..."}]` |

**Design rule:** Only camera lens specs become SpecItem nodes. Everything else
(video capabilities, AI features, software features) goes into `features` as
a JSON property on SpecCategory. This avoids creating hundreds of leaf nodes
with no relationships.

#### `SpecItem`
Individual technical spec that can be SHARED across models. Only used for
camera lenses (main, telephoto, ultrawide, front), because these can appear
on multiple phone generations and GraphRAG benefits from the shared connection.

| Property          | Type    | Description                                           |
|-------------------|---------|-------------------------------------------------------|
| `spec_item_id`    | String  | e.g. `"iphone-17-pro-max-camera-sau-camera-chinh"`   |
| `name`            | String  | e.g. `"Camera chính"` / `"Telephoto"` / `"Góc siêu rộng"` |
| `value`           | String  | Full spec string, e.g. `"48MP, f/1.6, OIS gen 2"`  |
| `numeric_value`   | Float   | Extracted number for comparison, e.g. `48.0`         |

---

### 1.3 Relationship Definitions

```
(Brand)         -[:HAS_SERIES]->          (Series)
(Series)        -[:HAS_MODEL]->           (Model)
(Model)         -[:HAS_CONFIG]->          (ModelStorage)
(Model)         -[:HAS_VARIANT]->         (Variant)
(Model)         -[:HAS_SPEC]->            (SpecCategory)
(SpecCategory)  -[:HAS_SPEC_ITEM]->       (SpecItem)
(Variant)       -[:OF_CONFIG]->           (ModelStorage)       — price lookup
(Variant)       -[:HAS_COLOR]->           (ColorVariant)
(ColorVariant)  -[:BELONGS_TO_FAMILY]->   (ColorFamily)
(Model)         -[:UPGRADE_OF]->          (Model)              — newer → older
(Model)         -[:SHARES_CHIP]->         (Model)              — same chip family
```

---

### 1.4 CSV Data Source Schema

The input is a CSV file with 8 columns:

| Column          | Type   | Description                                                                   |
|-----------------|--------|-------------------------------------------------------------------------------|
| `name`          | String | Full product name, e.g. `"iPhone 17 Pro Max 256GB \| Chính hãng"`           |
| `sku`           | String | URL slug, e.g. `"iphone-17-pro-max"` or `"iphone-16-pro-max-512gb"`        |
| `base_price`    | String | Original price, e.g. `"37.990.000đ"`                                        |
| `sale_price`    | String | Current price, e.g. `"36.990.000đ"`                                         |
| `description`   | String | Long Vietnamese HTML-like text (for LLM text content)                       |
| `specifications`| String | **JSON** — nested dict: `{category_name: [{name, value}, ...]}`             |
| `images`        | String | **JSON array** — list of image URLs                                          |
| `colors`        | String | **JSON** — `{product_color_1: {color, image_url, price}, ...}`              |

**Parsing rules:**
- Price strings: strip all non-digit characters → float (e.g. `"36.990.000đ"` → `36990000.0`)
- Storage from name: regex `(\d+)\s*(GB|TB)` — TB × 1024 = GB
- Model name: take the part before `|`, strip storage suffix
- Series name: model name minus tier suffix (Pro Max / Pro / Plus / Air / e)
- Tier detection from name: "Pro Max" → `pro_max`, "Pro" → `pro`, "Plus" → `plus`, "Air" → `air`, ends with "e" → `e`, else → `standard`
- model_id = sku with storage suffix removed, e.g. `"iphone-16-pro-max-512gb"` → `"iphone-16-pro-max"`
- Colors: each entry in colors JSON becomes one ColorVariant + one Variant SKU

---

### 1.5 Spec Extraction Rules

From `specifications` JSON, extract denormalized fields onto Model:

| Model Field      | Source Category                      | Source Item Name   | Extract Method                        |
|------------------|--------------------------------------|--------------------|---------------------------------------|
| `chip`           | "Vi xử lý & đồ họa" / "Bộ xử lý"   | "Chipset" / "Chip" | Strip "Chip " / "Apple " prefix      |
| `display_size_in`| "Màn hình"                           | "Kích thước"       | Regex `(\d+\.?\d*)\s*inches?`        |
| `display_hz`     | "Màn hình"                           | "Tần số quét"      | Regex `(\d+)\s*Hz`                   |
| `main_camera_mp` | "Camera sau"                         | "Camera sau"       | First `(\d+)\s*MP` match             |
| `weight_g`       | "Kích thước & Trọng lượng"          | "Trọng lượng"      | Regex `(\d+)\s*g`                    |
| `ip_rating`      | "Thông số khác"                      | "Kháng nước"       | Regex `IP(\d+)` → `"IP68"`          |
| `back_material`  | "Thiết kế & Trọng lượng"            | "Chất liệu mặt lưng"| Direct value                        |
| `frame_material` | "Thiết kế & Trọng lượng"            | "Chất liệu khung"  | Direct value                         |
| `os`             | "Tính năng khác"                     | "Hệ điều hành"     | Direct value                         |

**SpecCategory → SpecItem rule:**
Only create SpecItem nodes for these spec item names:
- "Camera sau", "Camera chính", "Telephoto", "Góc siêu rộng"
- "Camera trước", "Quay video", "Quay video trước"

All other items in SpecCategory → stored as JSON in `features` property.

---

### 1.6 UPGRADE_OF Relationships

Hard-coded mapping (newer → older):
- iphone-17-pro-max → iphone-16-pro-max
- iphone-17-pro → iphone-16-pro-max (cross-compare)
- iphone-17-256gb → iphone-16e
- iphone-16-pro-max → iphone-15
- iphone-17e → iphone-16e
- iphone-16e → iphone-15
- iphone-15 → iphone-14

---

### 1.7 text_content for GraphRAG

Each Model node must have a `text_content` property (max 2000 chars) combining:
1. Model name
2. `summary` (auto-generated from denormalized specs)
3. Top spec categories as text

This is the field that a GraphRAG indexing pipeline will read to build
community summaries.

---

## PART 2: COPILOT PROMPT

---

```
You are a senior Python developer. Build a complete Neo4j graph database import
pipeline for a phone product chatbot system using GraphRAG architecture.

## TASK
Read a CSV file of phone products and import them into a Neo4j database running
at localhost. The graph structure follows a carefully designed schema. Implement
everything in a single well-structured Python script (not a notebook).

## ENVIRONMENT
- Neo4j running at: bolt://localhost:7687
- Credentials: user="neo4j", password="password" (make it configurable via constants)
- Python packages available: neo4j, pandas
- CSV file path: passed as a command-line argument or hardcoded constant

## CSV SCHEMA
The CSV has 8 columns:
- name: str — full product name, e.g. "iPhone 17 Pro Max 256GB | Chính hãng"
- sku: str — URL slug, e.g. "iphone-17-pro-max" or "iphone-16-pro-max-512gb"
- base_price: str — price string e.g. "37.990.000đ" (Vietnamese format with dots as thousands separator)
- sale_price: str — current price string, same format
- description: str — long Vietnamese product description text
- specifications: str — JSON string: {category_name: [{name: str, value: str}, ...]}
- images: str — JSON array of image URL strings
- colors: str — JSON object: {"product_color_1": {color: str, image_url: str, price: str}, ...}

## GRAPH SCHEMA

### Nodes (with their properties):

**Brand**: brand_id (unique, e.g. "apple"), name, country

**Series**: series_id (unique, e.g. "iphone-17"), name

**Model**: model_id (unique, e.g. "iphone-17-pro-max"), name, tier, release_year,
  status, os, colors_available (list), storage_options (list of ints in GB),
  summary (auto-generated text), tagline, text_content (for GraphRAG),
  chip, display_size_in (float), display_hz (int), main_camera_mp (int),
  weight_g (int), ip_rating, back_material, frame_material

**ModelStorage**: model_storage_id (unique, e.g. "iphone-17-pro-max-256gb"),
  storage_gb (int), base_price (float, VND), sale_price (float, VND), currency="VND"

**ColorFamily**: family_id (unique, slugified color name), name

**ColorVariant**: color_variant_id (unique, e.g. "iphone-17-pro-max-cam-vu-tru"),
  name, model_specific (model_id), image_url, color_price (float)

**Variant**: sku_id (unique, e.g. "iphone-17-pro-max-256gb-cam-vu-tru"),
  stock="in_stock"

**SpecCategory**: spec_category_id (unique, e.g. "iphone-17-pro-max-camera-sau"),
  name (Vietnamese), features (JSON string of non-lens spec items)

**SpecItem**: spec_item_id (unique), name, value, numeric_value (float or null)

### Relationships:
- (Brand)-[:HAS_SERIES]->(Series)
- (Series)-[:HAS_MODEL]->(Model)
- (Model)-[:HAS_CONFIG]->(ModelStorage)
- (Model)-[:HAS_VARIANT]->(Variant)
- (Model)-[:HAS_SPEC]->(SpecCategory)
- (SpecCategory)-[:HAS_SPEC_ITEM]->(SpecItem)
- (Variant)-[:OF_CONFIG]->(ModelStorage)
- (Variant)-[:HAS_COLOR]->(ColorVariant)
- (ColorVariant)-[:BELONGS_TO_FAMILY]->(ColorFamily)
- (Model)-[:UPGRADE_OF]->(Model)
- (Model)-[:SHARES_CHIP]->(Model)

## PARSING RULES

### Price parsing:
Strip all non-digit characters, convert to float.
Example: "36.990.000đ" → 36990000.0, "36.990.000₫" → 36990000.0

### Model info extraction from (name, sku):
1. Storage: regex (\d+)\s*(GB|TB) from name. If TB, multiply by 1024.
2. Tier from name (case-insensitive):
   - contains "Pro Max" → "pro_max"
   - contains " Pro" → "pro"
   - contains " Plus" → "plus"
   - contains " Air" → "air"
   - matches pattern like "iPhone 16e" or "iPhone 17e" → "e"
   - else → "standard"
3. Model name: take name before "|", strip storage suffix (e.g. "256GB"), strip.
4. Series name: model name minus tier suffix (strip " Pro Max", " Pro", " Plus", " Air", trailing "e").
5. model_id: sku with storage suffix removed using regex -\d+(gb|tb)$ (case-insensitive).
   Example: "iphone-16-pro-max-512gb" → "iphone-16-pro-max"
6. series_id: slugify series name (lowercase, spaces to hyphens).
7. Release year mapping: iPhone 14→2022, 15→2023, 16→2024, 17→2025.

### Denormalized spec extraction from specifications JSON:
The specifications dict maps Vietnamese category names to lists of {name, value} dicts.
Extract these fields onto Model node:

- chip: look in ["Vi xử lý & đồ họa", "Bộ xử lý & Đồ họa"], item name contains "Chipset" or "Chip".
  Clean value: strip leading "Chip " or "Apple ", take first 3 words.
- display_size_in: category "Màn hình", item "Kích thước màn hình". Regex (\d+\.?\d*)\s*inches?.
- display_hz: category "Màn hình", item "Tần số quét". Regex (\d+)\s*Hz.
- main_camera_mp: category "Camera sau", item name contains "Camera sau" or "Camera chính". First (\d+)\s*MP.
- weight_g: category "Kích thước & Trọng lượng" or "Thiết kế & Trọng lượng", item "Trọng lượng". Regex (\d+)\s*g.
- ip_rating: category "Thông số khác", item contains "Kháng nước" or "Chỉ số". Regex IP(\d+), format as "IP68".
- back_material: category "Thiết kế & Trọng lượng", item "Chất liệu mặt lưng". Direct value.
- frame_material: category "Thiết kế & Trọng lượng", item "Chất liệu khung viền". Direct value.
- os: category "Tính năng khác", item "Hệ điều hành". Direct value.

### SpecCategory and SpecItem creation:
For each category in specifications:
- Create one SpecCategory node per model per category.
- Normalize category names that are duplicates (both "Vi xử lý & đồ họa" and
  "Bộ xử lý & Đồ họa" map to category_id suffix "chip").
- LENS spec items (create as SpecItem nodes):
  Item name contains any of: "Camera sau", "Camera chính", "Telephoto",
  "Góc siêu rộng", "Camera trước", "Quay video", "Quay video trước"
- ALL OTHER spec items → store as JSON array in SpecCategory.features property.
  Format: [{"name": "...", "value": "..."}, ...]

### Color and Variant creation:
For each entry in the colors JSON object:
1. Create/merge ColorFamily with family_id = slugify(color_name).
2. Create/merge ColorVariant with color_variant_id = f"{model_id}-{slugify(color_name)}".
3. Create/merge Variant with sku_id = f"{model_id}-{storage_gb}gb-{slugify(color_name)}".
4. Create relationships: Variant-[:OF_CONFIG]->ModelStorage, Variant-[:HAS_COLOR]->ColorVariant.

### UPGRADE_OF relationships (hard-coded after all models imported):
- iphone-17-pro-max → iphone-16-pro-max
- iphone-17-pro → iphone-16-pro-max
- iphone-17-256gb → iphone-16e
- iphone-16-pro-max → iphone-15
- iphone-17e → iphone-16e
- iphone-16e → iphone-15
- iphone-15 → iphone-14
Only create if both nodes exist (use OPTIONAL MATCH or check before creating).

### SHARES_CHIP relationships:
After all models imported, run a query:
MATCH pairs of Model nodes where m1.chip IS NOT NULL AND m1.chip = m2.chip AND m1.model_id < m2.model_id.
Create (m1)-[:SHARES_CHIP]->(m2) for each pair.

### text_content for GraphRAG:
After model is created, set model.text_content to a string combining:
- Model name
- Auto-generated summary: "{name} is equipped with chip {chip}, {display_size_in}-inch
  {display_hz}Hz display, {main_camera_mp}MP camera, {frame_material} frame, {ip_rating},
  released in {release_year}."
- Top 5 spec category texts joined by newline (format: "Category: features_text")
Truncate to max 2000 characters.

## NEO4J CONSTRAINTS AND INDEXES
Create these before importing (use IF NOT EXISTS):
- UNIQUE constraints on: Brand.brand_id, Series.series_id, Model.model_id,
  ModelStorage.model_storage_id, Variant.sku_id, ColorVariant.color_variant_id,
  ColorFamily.family_id, SpecCategory.spec_category_id, SpecItem.spec_item_id
- Index on: Model.chip, Model.display_size_in, SpecItem.name

## IMPLEMENTATION REQUIREMENTS

1. Use MERGE (not CREATE) for all nodes and relationships to be idempotent.
   Running the script twice must not duplicate data.

2. Use transactions properly. Group related operations in execute_write() blocks.
   Do NOT put the entire import in one massive transaction — use per-row transactions.

3. Error handling: wrap each row in try/except, log errors, continue to next row.
   Print a summary at the end: total rows, successful, failed.

4. Print progress for each row: row number, model name, counts of nodes created.

5. After import, print a verification report counting all node labels and
   relationship types.

6. Provide 5 sample Cypher queries at the end (as comments or print statements)
   demonstrating common chatbot use cases:
   - Get all colors and prices for a model
   - Compare camera specs between two models
   - Find phones with display >= X inches
   - Find phones sharing the same chip
   - Find what phone is an upgrade from a given model

7. The script must be runnable as: python import_phones.py [csv_path]
   with csv_path defaulting to "test_data.csv" if not provided.

8. Use a slugify helper function: lowercase, replace spaces with hyphens,
   remove special Vietnamese characters with transliteration OR just keep
   the raw string slugified simply (hyphens, alphanumeric only).

## CODE STRUCTURE
Organize into these sections:
1. Constants (NEO4J_URI, credentials, CSV path)
2. Helper functions (parse_price, parse_model_info, extract_denormalized_specs,
   is_lens_spec, slugify, extract_numeric)
3. Schema setup (create_constraints_and_indexes)
4. Import functions (one function per node/relationship type, all using MERGE)
5. Post-import functions (create_upgrade_of_rels, create_shares_chip_rels,
   set_text_content)
6. Verification function (count all labels and relationships, print table)
7. Main function orchestrating everything
8. Sample Cypher queries as comments at the bottom

Do NOT use async. Use synchronous neo4j driver only.
Do NOT use apoc procedures (keep it pure Cypher).
Handle None/null values gracefully — never pass Python None into a Cypher
parameter where the property should simply be absent; use conditional logic.
```

---

## PART 3: QUICK REFERENCE — NODE COUNT EXPECTATIONS

After importing the sample CSV (10 products), expect approximately:

| Node Label     | Expected Count | Notes                                    |
|----------------|----------------|------------------------------------------|
| Brand          | 1              | Apple only                               |
| Series         | ~6             | iPhone 14/15/16/17/16e/17e series        |
| Model          | ~8             | Distinct models (16 Pro Max appears once)|
| ModelStorage   | ~10            | One per CSV row (each row = 1 storage)  |
| ColorFamily    | ~15–20         | Unique color concepts                    |
| ColorVariant   | ~30–35         | Colors per model (2–6 per model)        |
| Variant (SKU)  | ~30–35         | Same as ColorVariant count              |
| SpecCategory   | ~80–100        | ~10 categories × 8–10 models           |
| SpecItem       | ~60–80         | Only lens specs                          |
```
