# Prompt: Sinh Jupyter Notebook import dữ liệu điện thoại vào Neo4j Knowledge Graph

## Mục tiêu
Tạo một Jupyter Notebook Python hoàn chỉnh để xử lý và import dữ liệu sản phẩm điện thoại vào Neo4j knowledge graph. Pipeline nhận vào hai nguồn dữ liệu cho mỗi sản phẩm:
1. **Structured scores** — JSON object chứa các thông số đã được AI trích xuất và chấm điểm (ví dụ bên dưới)
2. **Raw spec CSV** — JSON string chứa thông số kỹ thuật thô từ trang bán hàng (ví dụ bên dưới)

---

## Kiến trúc đồ thị (Neo4j Schema)

### Các node đã tồn tại (KHÔNG tạo mới, chỉ MATCH hoặc MERGE):
- `Product {product_id, name, sku}`
- `Specification` — 1-1 với Product, đã được tạo sẵn
- `Variant {variant_id, storage, ram}` — đã linked với Product
- `QualityProfile` — đã linked với Product
- `ProductMeta` — đã linked với Product

### Các node cần tạo/cập nhật trong notebook này:

**1. Component** (riêng cho từng Product, không dùng chung)
```
(Specification)-[:HAS_COMPONENT]->(Component {name: <tên nhóm>, product_id: <id>})
```
Danh sách Component chuẩn:
- `Display` — thông số màn hình
- `CameraRear` — camera sau
- `CameraFront` — camera trước
- `Processor` — chip, GPU, CPU
- `Battery` — pin, sạc
- `Body` — thân máy, chất liệu, kích thước
- `Connectivity` — kết nối mạng, Wi-Fi, Bluetooth, GPS
- `Memory` — RAM, bộ nhớ trong (chỉ cho thông số thô; variant-specific đã xử lý ở pipeline khác)
- `Software` — OS, giao diện

**2. ComponentItem** (DÙNG CHUNG giữa các sản phẩm — MERGE theo name+value)

Chỉ tạo ComponentItem node khi giá trị có **cardinality thấp** (< ~20 giá trị phân biệt trên toàn bộ catalog) VÀ được dùng để filter/so sánh sản phẩm. Các trường hợp này:

| Field nguồn | ComponentItem.name chuẩn | Ví dụ value |
|---|---|---|
| Công nghệ màn hình | `panel_tech` | AMOLED, Super AMOLED, IPS, LTPO |
| Tần số quét | `refresh_rate` | 60Hz, 90Hz, 120Hz, 144Hz |
| Kiểu màn hình / Notch | `notch_type` | Punch-hole, Dynamic Island, Giọt nước, Toàn màn hình |
| OIS / Chống rung | `ois` | OIS, EIS, OIS+EIS, Không |
| Xếp loại chip | `chip_tier` | S, A, B, C, D |
| GPU (dòng) | `gpu_family` | Adreno, Mali, Apple GPU, Immortalis |
| Kháng nước / bụi | `ip_rating` | IP68, IP67, IP65, IP54, Không |
| Chất lượng mặt lưng | `back_material` | Kính, Nhựa, Titan, Nhôm, Da |
| Chất lượng khung viền | `frame_material` | Nhôm, Nhựa, Titan, Thép |
| Cảm biến vân tay (loại) | `fingerprint_type` | Trong màn hình, Cạnh bên, Mặt sau, Không |
| Công nghệ tản nhiệt | `cooling_tech` | Vapor chamber, Heat pipe, Graphite, Không |
| Mạng di động | `network_gen` | 5G, 4G, LTE |

Quan hệ: `(Component)-[:HAS_COMPONENT_ITEM]->(ComponentItem {name, value})`

**3. Property trực tiếp trên Component** (KHÔNG tạo node riêng — unique hoặc near-unique):

Gán thẳng làm property trên node Component khi giá trị là số liên tục hoặc gần unique:

| Field nguồn | Property trên Component | Kiểu dữ liệu |
|---|---|---|
| Kích thước màn hình | `Display.screen_size_inch` | Float |
| Độ phân giải màn hình | `Display.resolution` | String |
| Độ sáng tối đa | `Display.brightness_nits` | Integer |
| Chất lượng kính màn hình | `Display.glass_protection` | String |
| Độ phân giải camera chính | `CameraRear.main_mp` | Integer |
| Số camera sau thật | `CameraRear.lens_count` | Integer |
| Aperture camera chính | `CameraRear.aperture` | String |
| Zoom quang học | `CameraRear.optical_zoom` | String |
| Quay video (parse thành structured) | `CameraRear.video_max_resolution`, `CameraRear.video_max_fps` | String, Integer |
| Tên chip cụ thể | `Processor.chip_name` | String |
| AnTuTu score | `Processor.antutu_score` | Integer |
| Tên GPU cụ thể | `Processor.gpu_name` | String |
| Số nhân CPU / cấu hình | `Processor.cpu_config` | String |
| Dung lượng pin | `Battery.capacity_mah` | Integer |
| Sạc có dây (tốc độ) | `Battery.wired_charging_w` | Integer |
| Cổng sạc | `Battery.charging_port` | String |
| Trọng lượng | `Body.weight_g` | Integer |
| Độ mỏng | `Body.thickness_mm` | Float |
| Kích thước (dimensions) | `Body.dimensions` | String |
| Wi-Fi chuẩn | `Connectivity.wifi_standard` | String |
| Bluetooth phiên bản | `Connectivity.bluetooth_version` | String |
| Hỗ trợ thẻ nhớ (dung lượng tối đa) | `Memory.sd_card_max_gb` | Integer hoặc None |
| Phiên bản OS ra mắt | `Software.os_version` | String |
| Giao diện OS | `Software.ui_skin` | String |

**4. Feature node** (DÙNG CHUNG — MERGE theo name)

Quan hệ: `(Product)-[:HAS_FEATURE]->(Feature {name})`

Danh sách Feature chuẩn — chỉ tạo khi xác nhận có (không tạo khi N/A hoặc "Không"):

```python
FEATURE_MAP = {
    # Kết nối
    "NFC": ["nfc", "công nghệ nfc"],
    "Jack 3.5mm": ["jack 3.5", "jack tai nghe 3.5", "cổng tai nghe"],
    "eSIM": ["esim"],
    "5G": ["5g", "hỗ trợ 5g"],
    "Wi-Fi 6": ["wi-fi 6", "wifi 6", "802.11ax"],
    "Wi-Fi 6E": ["wi-fi 6e", "wifi 6e"],
    # GPS chuẩn (mỗi chuẩn là 1 Feature riêng)
    "GPS": ["gps"],
    "GALILEO": ["galileo"],
    "GLONASS": ["glonass"],
    "BeiDou": ["beidou", "bds"],
    "QZSS": ["qzss"],
    # Phần cứng đặc biệt
    "Stylus": ["bút stylus", "hỗ trợ bút", "s-pen", "stylus"],
    "Foldable": ["điện thoại gập", "gập"],
    "Action Button": ["action button"],
    "Camera Button": ["camera button"],
    "SOS Button": ["nút sos", "nút khẩn cấp"],
    "Desktop Mode": ["desktop mode", "dex", "desktop"],
    # Sạc
    "Wireless Charging": ["sạc không dây", "wireless charging"],
    "Reverse Charging": ["sạc ngược", "reverse charging"],
    "Bypass Charging": ["bypass charging"],
    "MagSafe": ["magsafe"],
    # Bảo mật
    "Face ID": ["face id", "nhận diện khuôn mặt", "face unlock", "mở khóa khuôn mặt"],
    "Under-display Fingerprint": ["cảm biến vân tay trong màn hình", "vân tay trong màn hình"],
    # Thẻ nhớ
    "MicroSD": ["microsd", "thẻ nhớ", "khe cắm thẻ nhớ"],
    # AI
    "On-device AI": ["on-device", "ai on-device"],
    # Tiện ích
    "Smart Switch": ["smart switch"],
    "Call Recording": ["ghi âm cuộc gọi"],
}
```

**5. Variant override ComponentItem**

RAM và Storage từ raw spec → gán thành property trên Variant (không tạo ComponentItem node):
```python
# MATCH Variant theo product_id + storage value
# SET variant.ram = parsed_ram, variant.storage = parsed_storage
```

**6. QualityProfile properties** (cập nhật node đã tồn tại):
```python
QUALITY_PROFILE_FIELDS = {
    "camera_day_score": "Chất lượng ảnh ban ngày",
    "camera_night_score": "Chất lượng ảnh ban đêm",
    "video_score": "Chất lượng video thực tế",
    "selfie_score": "Chất lượng selfie thực tế",
    "ai_score": "AI Score tổng hợp",
    "value_retention": "Điểm giữ giá",
    "os_update_years": "Số năm OS update",
    "software_quality": "Chất lượng phần mềm / ít bloatware",
    "ai_type": "AI on-device vs Cloud",
    "ai_features": "Danh sách tính năng AI thực tế",
}
```

---

## Logic parse quan trọng

### Parse video spec
```python
import re

def parse_video_spec(raw: str) -> dict:
    """
    Input: "HD 720p@120fps\nFullHD 1080p@30fps" hoặc "1080p@30/60fps, 4K@30fps"
    Output: {
        "video_max_resolution": "1080p",
        "video_max_fps": 60,
        "video_modes_raw": "1080p@30/60fps"  # giữ lại để debug
    }
    """
    if not raw or raw.strip().lower() in ["n/a", "không đề cập", ""]:
        return {}
    
    RESOLUTION_RANK = {"8k": 5, "4k": 4, "2k": 3, "1080p": 2, "fullhd": 2, "720p": 1, "hd": 1, "480p": 0}
    
    modes = []
    # Match pattern: resolution@fps hoặc resolution @fps
    pattern = r'(\d{3,4}p|4k|8k|fullhd|hd)\s*@\s*([\d/]+)\s*fps'
    for match in re.finditer(pattern, raw, re.IGNORECASE):
        res = match.group(1).lower().replace("fullhd", "1080p").replace("hd", "720p")
        fps_list = [int(f) for f in match.group(2).split("/")]
        modes.append({"resolution": res, "max_fps": max(fps_list)})
    
    if not modes:
        return {"video_modes_raw": raw}
    
    # Lấy mode có resolution cao nhất, nếu bằng nhau lấy fps cao nhất
    best = max(modes, key=lambda m: (RESOLUTION_RANK.get(m["resolution"], 0), m["max_fps"]))
    return {
        "video_max_resolution": best["resolution"],
        "video_max_fps": best["max_fps"],
        "video_modes_raw": raw,
    }
```

### Parse GPS features
```python
GPS_STANDARDS = ["GPS", "GALILEO", "GLONASS", "QZSS", "BEIDOU", "BDS", "A-GPS", "NavIC"]

def parse_gps_features(raw: str) -> list[str]:
    """
    Input: "QZSS, GPS, GLONASS, GALILEO, BEIDOU"
    Output: ["GPS", "GALILEO", "GLONASS", "QZSS", "BeiDou"]
    """
    if not raw or raw.strip().lower() in ["n/a", ""]:
        return []
    found = []
    raw_upper = raw.upper()
    for std in GPS_STANDARDS:
        if std in raw_upper:
            label = "BeiDou" if std in ["BEIDOU", "BDS"] else std
            if label not in found:
                found.append(label)
    return found
```

### Parse camera spec từ raw
```python
def parse_camera_rear(raw_value: str) -> dict:
    """
    Input: "Chính 50 MP\nPhụ 5 MP, 2 MP" hoặc "50 MP"
    Output: {"main_mp": 50, "lens_count": 3}
    """
    result = {}
    mp_matches = re.findall(r'(\d+(?:\.\d+)?)\s*mp', raw_value, re.IGNORECASE)
    if mp_matches:
        result["main_mp"] = float(mp_matches[0])
        result["lens_count"] = len(mp_matches)
    return result
```

### Parse IP rating
```python
def parse_ip_rating(raw: str) -> str | None:
    """
    Input: "IP68" hoặc "Chỉ số kháng nước IP54" hoặc "Không"
    Output: "IP68" hoặc None
    """
    if not raw or raw.strip().lower() in ["n/a", "không", ""]:
        return None
    match = re.search(r'IP\d{2}', raw, re.IGNORECASE)
    return match.group(0).upper() if match else None
```

### Normalize về N/A
```python
NA_VALUES = {"n/a", "không đề cập", "không", "không có", "none", "", "nan"}

def is_na(value) -> bool:
    if value is None:
        return True
    return str(value).strip().lower() in NA_VALUES
```

### Detect Feature từ raw spec
```python
def extract_features_from_raw(raw_spec: dict) -> list[str]:
    """
    Nhận raw spec dict (đã parse từ CSV string),
    trả về list Feature.name chuẩn đã xác nhận có.
    """
    features = set()
    full_text = json.dumps(raw_spec, ensure_ascii=False).lower()
    
    for feature_name, keywords in FEATURE_MAP.items():
        for kw in keywords:
            if kw.lower() in full_text:
                features.add(feature_name)
                break
    
    # GPS: parse riêng
    for section in raw_spec.values():
        for item in section:
            if "gps" in item.get("name", "").lower():
                for gps_feat in parse_gps_features(item.get("value", "")):
                    features.add(gps_feat)
    
    return list(features)
```

---

## Nguồn dữ liệu đầu vào

### Nguồn 1 — Structured scores JSON (từ AI extraction):
```json
{
  "name": "Xiaomi POCO X7 Pro 5G 12GB 256GB",
  "sku": "dien-thoai-xiaomi-poco-x7-pro-5g",
  "Phân khúc giá": "Trung bình",
  "Công nghệ màn hình": "AMOLED",
  "Tần số quét": "120Hz",
  "Kích thước màn hình": "6.67 inches",
  "Độ sáng tối đa": "3200 nits",
  "Độ phân giải màn hình": "1220 x 2712 pixels",
  "Kiểu màn hình / Notch": "N/A",
  "Số lượng camera sau (thật)": 1,
  "Độ phân giải camera chính": "50MP",
  "Aperture camera chính": "N/A",
  "OIS / Chống rung": "N/A",
  "Zoom quang học": "N/A",
  "Quay video camera sau": "1080p@30/60fps",
  "Quay video camera trước": "1080p@30/60fps",
  "Tính năng AI camera": "N/A",
  "Chip tier": "Dimensity 8400-Ultra",
  "AnTuTu score": 1934134,
  "Xếp loại chip": "A",
  "RAM": "12 GB",
  "Bộ nhớ trong": "256 GB",
  "GPU tier": "Mali G615",
  "Hệ điều hành": "Android 14",
  "Công nghệ tản nhiệt": "N/A",
  "Bypass charging": "N/A",
  "Dung lượng pin": "6000 mAh",
  "Sạc có dây": "90W",
  "Sạc không dây": "Không hỗ trợ",
  "Sạc ngược": "N/A",
  "Mạng di động": "5G",
  "NFC": "Có",
  "Jack 3.5mm": "Không",
  "Hỗ trợ SIM": "2 SIM (Nano-SIM)",
  "eSIM": "N/A",
  "Hỗ trợ thẻ nhớ": "Không",
  "Kháng nước / bụi": "IP68",
  "Chất lượng mặt lưng": "Kính",
  "Chất lượng khung viền": "Nhựa",
  "Độ mỏng": "N/A",
  "Trọng lượng": "N/A",
  "Cảm biến vân tay": "Cảm biến vân tay trong màn hình",
  "Nhận diện khuôn mặt": "N/A",
  "Điện thoại gập": "không gập",
  "Hỗ trợ bút stylus": "N/A",
  "Hỗ trợ AI": "N/A",
  "Desktop Mode / DeX": "N/A",
  "GPS": "GPS, GALILEO, GLONASS, QZSS, BDS (B1I+B1c)",
  "Action Button": "N/A",
  "Camera Button": "N/A",
  "Nút SOS / khẩn cấp": "N/A",
  "Chất lượng ảnh ban ngày": "4",
  "Chất lượng ảnh ban đêm": "3",
  "Chất lượng video thực tế": "4",
  "Chất lượng selfie thực tế": "4",
  "AI Score tổng hợp": "3",
  "AI on-device vs Cloud": "Cloud",
  "Danh sách tính năng AI thực tế": "Chế độ tiên tiến, Quay video thông minh",
  "Điểm giữ giá": "Thấp-Trung bình (~30-45%)",
  "Số năm OS update": "3 năm",
  "Chất lượng phần mềm / ít bloatware": "Trung bình - có quảng cáo",
  "Gaming (Use Case)": "3",
  "Camera / Creator (Use Case)": "3",
  "Văn phòng (Use Case)": "4",
  "Mạng xã hội (Use Case)": "4",
  "Thể thao / Outdoor (Use Case)": "3",
  "Học sinh cấp 3 (Đối tượng)": "4",
  "Sinh viên (Đối tượng)": "3",
  "Dân văn phòng (Đối tượng)": "3",
  "Freelancer (Đối tượng)": "3",
  "Gamer (Đối tượng)": "3",
  "Nhiếp ảnh gia (Đối tượng)": "3",
  "Người lớn tuổi (Đối tượng)": "3",
  "Doanh nhân (Đối tượng)": "3",
  "Học tập (Đối tượng)": "3",
  "Kinh doanh (Đối tượng)": "3"
}
```

### Nguồn 2 — Raw spec CSV string (từ trang bán hàng):
```
"{""Màn hình"": [{""name"": ""Kích thước màn hình"", ""value"": ""6.7 inches""},...], ...}"
```
Parse bằng `json.loads()` sau khi unescape. Dùng để bổ sung các trường còn thiếu trong nguồn 1 (Wi-Fi chuẩn, Bluetooth version, CPU config, cổng sạc, tính năng camera text...).

---

## Thứ tự xử lý trong notebook

Notebook cần có các cell theo thứ tự sau:

### Cell 1 — Imports & config
```python
# neo4j driver, json, re, pandas
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "..."
```

### Cell 2 — Toàn bộ helper functions
Bao gồm: `is_na()`, `parse_video_spec()`, `parse_gps_features()`, `parse_camera_rear()`, `parse_ip_rating()`, `extract_features_from_raw()`, `parse_score()`, và các dict mapping: `FEATURE_MAP`, `COMPONENT_ITEM_MAP`, `QUALITY_PROFILE_FIELDS`, `USE_CASE_FIELDS`, `TARGET_USER_FIELDS`.

### Cell 3 — Toàn bộ Cypher upsert functions
Mỗi function nhận `tx` + các params, dùng `MERGE` (không dùng `CREATE`):
- `upsert_component(tx, product_id, component_name)` → trả về component node
- `upsert_component_item(tx, component_name, product_id, item_name, item_value)` → MERGE ComponentItem theo name+value, tạo relationship từ Component
- `upsert_feature(tx, product_id, feature_name)` → MERGE Feature theo name
- `upsert_quality_profile(tx, product_id, props: dict)` → SET properties trên QualityProfile
- `upsert_use_case(tx, product_id, use_case_name, score, rubric)` → MERGE + SET score trên relationship
- `upsert_target_user(tx, product_id, target_name, score, rubric)` → MERGE + SET score trên relationship

### Cell 4 — Main processing function
```python
def process_product(session, score_item: dict, raw_spec_str: str):
    product_id = score_item["sku"]  # hoặc field id khác
    raw_spec = json.loads(raw_spec_str) if raw_spec_str else {}
    
    # Bước 1: Tạo các Component node
    # Bước 2: Gán ComponentItem nodes (dùng chung)
    # Bước 3: Gán property trực tiếp lên Component
    # Bước 4: Tạo Feature nodes từ score_item + raw_spec
    # Bước 5: Update QualityProfile
    # Bước 6: Upsert UseCase scores (chỉ score >= 2)
    # Bước 7: Upsert TargetUser scores (chỉ score >= 2)
    
    # Với mỗi bước: print log tóm tắt số node/relationship tạo được
```

### Cell 5 — Load data & run
```python
# Load từ file hoặc DataFrame
# Iterate từng sản phẩm, gọi process_product()
# Xử lý lỗi per-product (try/except, log và tiếp tục)
# In summary cuối: tổng số product processed, lỗi nếu có
```

### Cell 6 — Validation queries
Sau khi import xong, chạy các Cypher query kiểm tra:
```cypher
-- Kiểm tra số Feature mỗi sản phẩm
MATCH (p:Product)-[:HAS_FEATURE]->(f:Feature)
RETURN p.name, count(f) AS feature_count
ORDER BY feature_count DESC LIMIT 10

-- Kiểm tra ComponentItem node được dùng nhiều nhất
MATCH (c:Component)-[:HAS_COMPONENT_ITEM]->(ci:ComponentItem)
RETURN ci.name, ci.value, count(c) AS usage
ORDER BY usage DESC LIMIT 20

-- Kiểm tra sản phẩm thiếu Component
MATCH (p:Product)-[:HAS_SPECIFICATION]->(s:Specification)
WHERE NOT (s)-[:HAS_COMPONENT]->()
RETURN p.name
```

---

## Ràng buộc quan trọng cần nhớ

1. **Không tạo ComponentItem khi value là N/A** — bỏ qua hoàn toàn, không tạo node với value "N/A".
2. **Không tạo Feature khi value là "Không", "N/A", hoặc "không gập"** — chỉ tạo khi xác nhận có.
3. **UseCase và TargetUser chỉ tạo relationship khi score >= 2** — tránh near-full-mesh với score 1.
4. **Mỗi Product có Component riêng** — không MERGE Component dùng chung giữa các sản phẩm.
5. **ComponentItem MERGE theo `name + value`** — hai sản phẩm cùng có `panel_tech: AMOLED` sẽ trỏ vào cùng 1 node.
6. **Feature MERGE theo `name`** — `Feature {name: "NFC"}` là node duy nhất, tất cả sản phẩm có NFC đều trỏ vào đây.
7. **Ưu tiên nguồn score_item, dùng raw_spec để bổ sung** — khi cùng field có ở cả hai nguồn, ưu tiên giá trị đã được chuẩn hóa từ score_item.
8. **Parse số trước khi lưu** — `"6000 mAh"` → `6000` (int), `"90W"` → `90` (int), `"6.67 inches"` → `6.67` (float).
