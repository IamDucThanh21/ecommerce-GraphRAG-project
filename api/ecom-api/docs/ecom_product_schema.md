# Schema: ecom_product (PostgreSQL)

> **Mục đích:** Định nghĩa toàn bộ bảng và quan hệ cho service quản lý sản phẩm trong kiến trúc microservice.  

---

## Nhóm 1 — Taxonomy (Brand / Line / Series)

### `product_brand`
> Hãng sản xuất. Mức cao nhất trong hierarchy sản phẩm.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `name` | varchar(255) | NOT NULL | Apple, Samsung, Sony... |
| `slug` | varchar(255) | NOT NULL | Unique toàn bảng, dùng cho URL |
| `description` | text | NULL | |
| `logo_url` | varchar(500) | NULL | |

**Constraints:** `UNIQUE (slug)`

---

### `product_line`
> Dòng sản phẩm của một brand. VD: iPhone, iPad, Galaxy S, Galaxy Tab.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `brand_id` | uuid | NOT NULL | FK → `product_brand.id` |
| `name` | varchar(255) | NOT NULL | iPhone, Galaxy Tab... |
| `slug` | varchar(255) | NOT NULL | Unique trong phạm vi brand |
| `description` | text | NULL | |

**Constraints:** `UNIQUE (brand_id, slug)`  
**Foreign keys:** `brand_id` → `product_brand(id)` ON DELETE RESTRICT

---

### `product_series`
> Series trong một dòng sản phẩm. VD: iPhone 17 Series, Galaxy S25, Galaxy M55.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `line_id` | uuid | NOT NULL | FK → `product_line.id` |
| `name` | varchar(255) | NOT NULL | iPhone 17 Series, Galaxy S25... |
| `slug` | varchar(255) | NOT NULL | Unique trong phạm vi line |
| `description` | text | NULL | |

**Constraints:** `UNIQUE (line_id, slug)`  
**Foreign keys:** `line_id` → `product_line(id)` ON DELETE RESTRICT

---

## Nhóm 2 — Category

### `product_category`
> Danh mục sản phẩm dạng cây đệ quy. VD: Điện tử → Điện thoại → Android.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `parent_id` | uuid | NULL | FK → `product_category.id`. NULL = root node |
| `name` | varchar(255) | NOT NULL | Điện thoại, Tai nghe, Laptop... |
| `slug` | varchar(255) | NOT NULL | Unique toàn bảng |
| `description` | text | NULL | |

**Constraints:** `UNIQUE (slug)`  
**Foreign keys:** `parent_id` → `product_category(id)` ON DELETE RESTRICT

---

### `product_category_mapping`
> Quan hệ N-N giữa product và category. Một product có thể thuộc nhiều category.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `product_id` | uuid | NOT NULL | FK → `product.id` |
| `category_id` | uuid | NOT NULL | FK → `product_category.id` |
| `is_primary` | boolean | NOT NULL | Đúng một bản ghi `true` trên mỗi product |

**Constraints:** `UNIQUE (product_id, category_id)`  
**Foreign keys:**
- `product_id` → `product(id)` ON DELETE CASCADE
- `category_id` → `product_category(id)` ON DELETE RESTRICT

**Indexes:** `(product_id)`, `(category_id)`

---

## Nhóm 3 — Spec Template (khuôn mẫu theo category)

### `spec_group_template`
> Nhóm spec được định nghĩa theo category. VD: category "Điện thoại" có nhóm Màn hình, Camera, Chipset, Pin.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `category_id` | uuid | NOT NULL | FK → `product_category.id` |
| `name` | varchar(255) | NOT NULL | Màn hình, Camera, Pin, Giao tiếp... |
| `sort_order` | int | NOT NULL | Default 0 |

**Foreign keys:** `category_id` → `product_category(id)` ON DELETE CASCADE  
**Indexes:** `(category_id)`

---

### `spec_attribute_template`
> Từng thuộc tính spec trong một nhóm template. Định nghĩa kiểu dữ liệu, đơn vị và có filterable không.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `group_template_id` | uuid | NOT NULL | FK → `spec_group_template.id` |
| `key` | varchar(100) | NOT NULL | snake_case, stable key. VD: `screen_size`, `chipset`, `ram` |
| `label` | varchar(255) | NOT NULL | Tên hiển thị. VD: Kích thước màn hình, Chipset |
| `data_type` | varchar(20) | NOT NULL | `text` \| `number` \| `boolean` \| `text_list` |
| `unit` | varchar(50) | NULL | inches, MP, GHz, GB... |
| `is_filterable` | boolean | NOT NULL | Default false. Có dùng để filter sản phẩm không |
| `is_required` | boolean | NOT NULL | Default false. Bắt buộc nhập khi tạo product thuộc category này |
| `sort_order` | int | NOT NULL | Default 0 |

**Constraints:** `UNIQUE (group_template_id, key)`  
**Foreign keys:** `group_template_id` → `spec_group_template(id)` ON DELETE CASCADE

---

## Nhóm 4 — Product (core)

### `product`
> Bảng trung tâm. Gắn với brand (bắt buộc), line và series (tùy chọn), và một primary category.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `brand_id` | uuid | NOT NULL | FK → `product_brand.id`. Luôn có. |
| `line_id` | uuid | NULL | FK → `product_line.id`. Nullable — brand nhỏ không có line. |
| `series_id` | uuid | NULL | FK → `product_series.id`. Nullable — có line nhưng không có series. |
| `category_id` | uuid | NOT NULL | FK → `product_category.id`. Primary category, luôn có. |
| `name` | varchar(500) | NOT NULL | iPhone 17 Pro Max 256GB |
| `slug` | varchar(500) | NOT NULL | Unique toàn bảng |
| `description` | text | NULL | |
| `status` | varchar(20) | NOT NULL | `draft` \| `active` \| `discontinued`. Default `draft` |

**Constraints:**
- `UNIQUE (slug)`
- `CHECK (series_id IS NULL OR line_id IS NOT NULL)` — nếu có series thì phải có line

**Foreign keys:**
- `brand_id` → `product_brand(id)` ON DELETE RESTRICT
- `line_id` → `product_line(id)` ON DELETE SET NULL
- `series_id` → `product_series(id)` ON DELETE SET NULL
- `category_id` → `product_category(id)` ON DELETE RESTRICT

**Indexes:** `(brand_id)`, `(category_id)`, `(status)`, `(line_id)`, `(series_id)`

---

### `product_variant`
> Biến thể của product. VD: iPhone 17 Pro Max màu Đen 256GB vs 512GB.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `product_id` | uuid | NOT NULL | FK → `product.id` |
| `sku` | varchar(255) | NOT NULL | Unique toàn bảng, mã quản lý kho |
| `price` | numeric(15,2) | NOT NULL | Giá bán hiện tại |
| `base_price` | numeric(15,2) | NOT NULL | Giá gốc trước khuyến mãi |
| `stock_quantity` | int | NOT NULL | Default 0 |
| `attributes` | jsonb | NULL | VD: `{"color": "Black", "storage": "256GB"}` — thuộc tính phân biệt variant |
| `status` | varchar(20) | NOT NULL | `active` \| `inactive` \| `out_of_stock`. Default `active` |

**Constraints:** `UNIQUE (sku)`  
**Foreign keys:** `product_id` → `product(id)` ON DELETE CASCADE  
**Indexes:** `(product_id)`, `(sku)`, GIN index trên `attributes`

---

### `product_image`
> Ảnh của product hoặc variant cụ thể. `variant_id` nullable để hỗ trợ ảnh chung cho product.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `product_id` | uuid | NOT NULL | FK → `product.id` |
| `variant_id` | uuid | NULL | FK → `product_variant.id`. NULL = ảnh chung cho product. |
| `image_url` | varchar(1000) | NOT NULL | URL ảnh |
| `is_primary` | boolean | NOT NULL | Default false. Ảnh đại diện |
| `sort_order` | int | NOT NULL | Default 0 |

**Foreign keys:**
- `product_id` → `product(id)` ON DELETE CASCADE
- `variant_id` → `product_variant(id)` ON DELETE CASCADE

**Indexes:** `(product_id)`, `(variant_id)`

---

## Nhóm 5 — Spec Value (dữ liệu thực tế của từng product)

### `product_spec_group`
> Instance nhóm spec của một product cụ thể. Tạo ra từ `spec_group_template`, hoặc admin thêm tự do (group_template_id nullable).

| Column | Type | Nullable | Note |
|---|---|---|---|
| `product_id` | uuid | NOT NULL | FK → `product.id` |
| `group_template_id` | uuid | NULL | FK → `spec_group_template.id`. NULL = nhóm tự do không theo template. |
| `name` | varchar(255) | NOT NULL | Copy từ template hoặc admin tự đặt |
| `sort_order` | int | NOT NULL | Default 0 |

**Foreign keys:**
- `product_id` → `product(id)` ON DELETE CASCADE
- `group_template_id` → `spec_group_template(id)` ON DELETE SET NULL

**Indexes:** `(product_id)`

---

### `product_spec_value`
> Giá trị spec thực tế của product. Lưu đồng thời `value_text`, `value_number`, `value_boolean` để hỗ trợ cả hiển thị lẫn filter.

| Column | Type | Nullable | Note |
|---|---|---|---|
| `product_spec_group_id` | uuid | NOT NULL | FK → `product_spec_group.id` |
| `attribute_template_id` | uuid | NULL | FK → `spec_attribute_template.id`. NULL = spec tự do của admin. |
| `key` | varchar(100) | NOT NULL | Luôn có. Copy từ `template.key` hoặc admin tự đặt (snake_case). |
| `label` | varchar(255) | NOT NULL | Luôn có. Tên hiển thị. |
| `value_text` | text | NULL | Dùng cho `data_type = text / text_list`. VD: "Super Retina XDR" |
| `value_number` | numeric | NULL | Dùng để filter số (`>=`, `<=`). VD: `6.9` |
| `value_unit` | varchar(50) | NULL | inches, MP, GB, Hz... |
| `value_boolean` | boolean | NULL | Dùng cho `data_type = boolean`. VD: `true` (có NFC) |
| `is_filterable` | boolean | NOT NULL | Default false. Override từ template hoặc admin tự set cho spec tự do. |
| `sort_order` | int | NOT NULL | Default 0 |

**Foreign keys:**
- `product_spec_group_id` → `product_spec_group(id)` ON DELETE CASCADE
- `attribute_template_id` → `spec_attribute_template(id)` ON DELETE SET NULL

**Indexes:**
- `(product_spec_group_id)`
- `(key, value_number) WHERE is_filterable = true` — phục vụ filter tìm kiếm sản phẩm theo spec số
- `(key, value_text) WHERE is_filterable = true` — phục vụ filter theo text

---

## Tóm tắt quan hệ

| From | Cardinality | To | Note |
|---|---|---|---|
| `product_brand` | 1 : N | `product_line` | Brand có nhiều dòng sản phẩm |
| `product_line` | 1 : N | `product_series` | Dòng sp có nhiều series |
| `product_brand` | 1 : N | `product` | Brand nhỏ gắn product trực tiếp (line/series nullable) |
| `product_line` | 1 : N | `product` | Product thuộc dòng sp (nullable) |
| `product_series` | 1 : N | `product` | Product thuộc series (nullable) |
| `product_category` | 1 : N | `product_category` | Self-join, cây danh mục đệ quy |
| `product_category` | 1 : N | `spec_group_template` | Category định nghĩa khuôn mẫu spec |
| `spec_group_template` | 1 : N | `spec_attribute_template` | Nhóm chứa nhiều thuộc tính |
| `product` | N : N | `product_category` | Qua bảng `product_category_mapping` |
| `product` | 1 : N | `product_variant` | Product có nhiều biến thể |
| `product` | 1 : N | `product_image` | Ảnh chung cho product |
| `product_variant` | 1 : N | `product_image` | Ảnh riêng cho variant (`variant_id` nullable) |
| `product` | 1 : N | `product_spec_group` | Spec được nhóm theo product |
| `spec_group_template` | 1 : N | `product_spec_group` | Template instantiate thành spec thực tế (nullable) |
| `product_spec_group` | 1 : N | `product_spec_value` | Nhóm chứa nhiều giá trị spec |
| `spec_attribute_template` | 1 : N | `product_spec_value` | Typed by template (nullable cho spec tự do) |

---

## Lưu ý thiết kế

- **Nullable FK có chủ đích:** `line_id` và `series_id` trong `product` nullable để hỗ trợ brand nhỏ không có đầy đủ hierarchy. Check constraint đảm bảo tính nhất quán: `series_id IS NULL OR line_id IS NOT NULL`.
- **Hybrid spec template:** `group_template_id` và `attribute_template_id` nullable để admin có thể thêm spec tự do ngoài template mà vẫn giữ `key` và `label` để hiển thị và sync sang Neo4j.
- **3 cột value song song:** `value_text`, `value_number`, `value_boolean` trong `product_spec_value` để phục vụ cả hiển thị (text) và filter (number). VD: màn hình 6.9 inch lưu `value_number = 6.9` để query `>= 6.5` và `value_text = "6.9 inches"` để hiển thị.
- **Partial index trên spec:** `(key, value_number) WHERE is_filterable = true` giúp filter nhanh mà không tốn storage index cho các spec chỉ để hiển thị.