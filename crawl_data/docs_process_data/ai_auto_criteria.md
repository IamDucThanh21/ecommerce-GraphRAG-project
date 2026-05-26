# Tiêu chí AI tự đánh giá được — Scoring Rubric
> Nguồn dữ liệu: spec JSON + description + giá sản phẩm  
> Ví dụ minh họa: Samsung Galaxy M55 12GB 256GB  
> Thang điểm: **1–5** (trừ các tiêu chí dạng categorical hoặc boolean)

---

## Ghi chú cách đọc
- **Nguồn**: Trường dữ liệu lấy từ đâu trong input
- **Giá trị mẫu**: Giá trị thực tế từ Samsung M55
- **Xử lý**: Rule-based (công thức cứng) hoặc LLM (đọc hiểu văn bản)
- **Scoring Rubric**: Quy tắc chấm điểm cụ thể — nhìn vào là biết ngay cho bao nhiêu điểm

---

## 1. Phân khúc & Tuổi đời

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Phân khúc giá** | `price` | 7.990.000đ | Rule-based | Categorical: `Giá rẻ` < 6tr / `Trung bình` 6–12tr / `Cao cấp` > 12tr |
| **Tuổi đời** | `Thời điểm ra mắt` | 03/2024 → ~14 tháng | Rule-based | Categorical: `Mới nhất` < 12 tháng / `Trung bình` 12–36 tháng / `Cũ` > 36 tháng |

---

## 2. Thông tin chung

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Hệ sinh thái** | `Hệ điều hành` | Android 14 | Rule-based | Categorical: `iOS` / `Android` / `HarmonyOS` |
| **Thương hiệu** | Tên sản phẩm | Samsung | Rule-based | Categorical: Samsung / Apple / Xiaomi / Oppo / Vivo / Realme / OnePlus / Google... |
| **Xuất xứ** | Brand dictionary | Samsung → Hàn Quốc | Rule-based | Categorical: Hàn Quốc / Mỹ / Trung Quốc / Nhật Bản / Đài Loan |
| **Giao diện OS** | Brand + OS | Samsung + Android | Rule-based | Categorical: `One UI` / `MIUI` / `HyperOS` / `OxygenOS` / `ColorOS` / `Stock Android` / `iOS` |
| **Màu sắc hỗ trợ** | `product_color` | Đen, Xanh lá | Rule-based | Số lượng màu: 1 / 2 / 3 / 4+ |
| **Phiên bản OS ra mắt** | `Hệ điều hành` | Android 14 | Rule-based | Categorical: Android 12 / 13 / 14 / 15 — dùng để tính số năm update còn lại |

---

## 3. Camera

> **Lưu ý parse**: Trường `Camera sau` trong spec thường chứa nhiều camera gộp thành một chuỗi, mỗi camera trên một dòng riêng. Cần tách từng dòng, xác định loại camera (main / ultrawide / telephoto / macro / depth) rồi mới lấy giá trị. **Camera chính** = dòng được đánh dấu "main", "chính", "góc rộng chính" HOẶC camera có MP cao nhất nếu không rõ. **Không tính** macro ≤ 2MP và depth sensor vào bất kỳ tiêu chí nào.

### 3A. Camera sau

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Số lượng camera sau (thật)** | `Camera sau` | 50MP + 8MP → 2 camera thật (macro 2MP không tính) | Rule-based | `1` = 1 camera / `2` = 2 camera / `3` = 3 camera / `4` = 4 camera trở lên. ⚠ Chỉ đếm camera có MP ≥ 5MP và không phải macro/depth. Tối đa 4 điểm — không có mức 5 vì số lượng camera ≥ 4 đều nhận giá trị như nhau |
| **Độ phân giải camera chính** | `Camera sau` — dòng camera chính | 50MP | Rule-based | `1` ≤ 12MP / `2` 13–24MP / `3` 25–47MP / `4` 48–63MP / `5` ≥ 64MP. Lấy MP của camera chính, không phải camera MP cao nhất |
| **Aperture / Khẩu độ camera chính** | `Camera sau` — dòng camera chính | f/1.8 | Rule-based | `5` ≤ f/1.6 / `4` f/1.7–f/1.8 / `3` f/1.9–f/2.0 / `2` f/2.1–f/2.4 / `1` > f/2.4. Số f càng nhỏ = thu sáng tốt hơn = ảnh đêm tốt hơn. Nếu không tìm thấy aperture trên dòng camera chính → `N/A` |
| **OIS / Chống rung** | `Camera sau` + `Tính năng camera` + description | OIS camera chính | Rule-based + LLM | `5` OIS camera chính + OIS telephoto (periscope) / `4` OIS camera chính + EIS/gyro-EIS video / `3` Chỉ OIS camera chính / `2` Chỉ EIS hoặc VDIS (điện tử, không phải quang học) / `1` Không có chống rung. Keywords: OIS, chống rung quang học, optical stabilization → quang học. EIS, gyro-EIS, VDIS, electronic stabilization → điện tử |
| **Zoom quang học** | `Camera sau` + `Tính năng camera` + description | Không có → điểm 1 | Rule-based + LLM | `1` Không có zoom quang (chỉ digital zoom) / `2` Zoom quang 2x / `3` Zoom quang 3–4x / `4` Zoom quang 5–7x / `5` Zoom quang ≥ 8x (periscope). **Quy tắc detect**: (1) Tìm pattern "Nx zoom quang", "zoom quang học Nx", "optical Nx" — lấy số N. (2) Nếu có camera telephoto ≥ 5MP nhưng không ghi rõ bội số → mặc định 3x. (3) Nếu chỉ ghi "zoom quang" không có bội số → điểm 2. (4) Nếu chỉ có digital zoom hoặc không đề cập → điểm 1. ⚠ Không nhầm "zoom số 40x" (digital) với zoom quang |
| **Quay video camera sau** | `Quay video` | 4K@30fps | Rule-based | `1` ≤ 1080p@30fps hoặc 720p / `2` 1080p@60fps / `3` 4K@30fps / `4` 4K@60fps / `5` 4K@120fps hoặc 8K. Lấy độ phân giải + fps cao nhất trong chuỗi. ⚠ Trường `Quay video` chỉ áp dụng cho camera SAU |
| **Chất lượng kính lens camera** | `Tính năng camera` + description + `Camera sau` | Không đề cập → điểm 3 | LLM | `5` Sapphire crystal / `4` Gorilla Glass, Ceramic Shield, Victus, hoặc kính cường lực có thương hiệu / `3` Kính thường, không đề cập (mặc định 3) |

### 3B. Camera trước

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Độ phân giải camera trước** | `Camera trước` | 50MP | Rule-based | `1` ≤ 8MP / `2` 9–15MP / `3` 16–23MP / `4` 24–31MP / `5` ≥ 32MP. Lấy số MP đầu tiên trong chuỗi Camera trước |
| **Aperture camera trước** | `Camera trước` | f/2.4 | Rule-based | `5` ≤ f/1.8 / `4` f/1.9–f/2.0 / `3` f/2.1–f/2.2 / `2` f/2.3–f/2.4 / `1` > f/2.4. Aperture camera trước ảnh hưởng đến chất lượng selfie thiếu sáng. Nếu không có → `N/A` |
| **Quay video camera trước** | `Quay video trước` | 4K@30fps | Rule-based | `1` ≤ 1080p@30fps / `2` 1080p@60fps / `3` 4K@30fps / `4` 4K@60fps / `5` 4K@120fps. Nếu không có trường `Quay video trước` hoặc trống → `N/A`. ⚠ Tách biệt hoàn toàn với `Quay video` (camera sau) |

### 3C. Tính năng AI camera

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Tính năng AI camera** | `Tính năng camera` + description | HDR, Night Mode, VDIS | LLM | `1` Không có tính năng AI nào / `2` Chỉ có HDR cơ bản hoặc 1 tính năng AI đơn giản (beautify, bộ lọc) / `3` Night Mode + HDR (2 tính năng AI thực sự) / `4` Night Mode + HDR + AI Portrait/xóa phông + ít nhất 1 tính năng xóa vật thể hoặc AI Zoom / `5` Đầy đủ tier 4 + có thêm: AI Generative Edit, ProRAW/Log format, hoặc tích hợp AI assistant (Gemini, Apple Intelligence). **Keywords tier 2**: HDR, beautify, bộ lọc màu. **Keywords tier 3**: Night mode, ban đêm, nightography, chế độ đêm. **Keywords tier 4**: AI Portrait, chân dung, xóa phông, xóa vật thể, AI eraser, Photo Assist. **Keywords tier 5**: Generative edit, ProRAW, Apple Log, AI eraser + generative, Google Gemini tích hợp camera |

---

> ⚠ **Lưu ý quan trọng khi parse**: Một số sản phẩm ghi thông tin zoom và OIS trong `Tính năng camera` thay vì `Camera sau` (ví dụ Samsung A07 ghi "Zoom quang học 10x" trong Tính năng camera). Luôn kiểm tra cả 3 trường: `Camera sau` + `Tính năng camera` + `description` khi score OIS và Zoom quang học.

---

## 4. Màn hình

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Kích thước** | `Kích thước màn hình` | 6.7 inch | Rule-based | `1` < 5.5" / `2` 5.5–5.9" / `3` 6.0–6.3" / `4` 6.4–6.7" / `5` > 6.7". ⚠ Màn lớn hơn không phải luôn tốt hơn — chatbot cần kết hợp với nhu cầu user |
| **Công nghệ màn hình** | `Công nghệ màn hình` | Super AMOLED Plus | Rule-based | `5` LTPO OLED / ProMotion XDR / `4` Super AMOLED+ / AMOLED+ / `3` AMOLED / OLED thường / `2` IPS LCD cao cấp / `1` LCD TFT thường |
| **Tần số quét** | `Tần số quét` | 120Hz cố định | Rule-based | `1` 60Hz / `2` 90Hz / `3` 120Hz cố định / `4` 120Hz adaptive (LTPO) / `5` 144Hz+ hoặc LTPO 1–120Hz |
| **Độ sáng tối đa** | `Tính năng màn hình` | 1000 nit | Rule-based | `1` < 500 nit / `2` 500–799 nit / `3` 800–999 nit / `4` 1000–1999 nit / `5` ≥ 2000 nit |
| **Chất lượng màu** | description + spec | Không đề cập P3 | LLM | `5` DCI-P3 ≥ 99% / `4` 90–98% DCI-P3 / `3` sRGB đầy đủ / `2` Không đề cập chuẩn màu cụ thể / `1` LCD màu thường |
| **Kính bảo vệ màn hình** | description + spec | Không đề cập | LLM | `5` Ceramic Shield / Gorilla Glass Victus 2 / `4` Gorilla Glass Victus / GG 7+ / `3` Gorilla Glass 5 / Dragon Trail / `2` Gorilla Glass 3 / `1` Không rõ / Kính thường |
| **Kiểu màn hình / Notch** | `Kiểu màn hình` | Đục lỗ | Rule-based | Categorical: `Dynamic Island` / `Đục lỗ` / `Giọt nước` / `Toàn màn hình` / `Notch tai thỏ` |
| **Độ phân giải màn hình** | `Độ phân giải màn hình` | 1080 x 2400 (FHD+) | Rule-based | `1` HD (720p trở xuống) / `2` HD+ (720 x 1600 dạng) / `3` FHD / FHD+ (1080p) / `4` QHD / QHD+ (1440p) / `5` 4K (2160p trở lên). **Quy tắc parse**: (1) Tìm 2 số trong chuỗi (width × height), lấy giá trị nhỏ hơn làm chiều ngắn. (2) ≤ 720 → 1 / 721–900 → 2 / 901–1200 → 3 / 1201–1800 → 4 / > 1800 → 5. ⚠ Một số sản phẩm ghi "1080 x 2400 pixels (FullHD+)" — bỏ chữ, chỉ lấy số. Màn hình gập có thể có 2 chuỗi độ phân giải (màn chính + màn phụ) — chỉ lấy màn chính |
| **Hỗ trợ bút stylus** | description | Không | LLM | Categorical: `Tích hợp sẵn` / `Hỗ trợ (mua thêm)` / `Không` |

---

## 5. Hiệu năng

> **Nguồn chip rank**: File `chip_mobile_rank.csv` từ Thế Giới Di Động gồm 130 chip, mỗi chip có: tên, điểm xếp loại (15–97), AnTuTu 10, Geekbench 6, thiết bị đại diện. Đây là nguồn tham chiếu chính để score chip tier.

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Chip tier** | `Chipset` → lookup chip_mobile_rank.csv | Snapdragon 7 Gen 1 | Rule-based (lookup) | Lookup tên chip trong bảng rank, lấy điểm xếp loại rồi map: `5` điểm ≥ 85 (A+) / `4` điểm 70–84 (A+ thấp hoặc A) / `3` điểm 50–69 (A–B) / `2` điểm 30–49 (B–C) / `1` điểm < 30 (C). **Quy tắc match tên chip**: Normalize tên về lowercase, bỏ dấu ®/™, thử match exact trước, nếu không có thì fuzzy match bỏ qua "plus/pro" ở cuối. Nếu không tìm thấy trong bảng → fallback về rule keyword bên dưới |
| **Chip tier (fallback)** | `Chipset` — keyword matching | Snapdragon 7 Gen 1 | Rule-based | Dùng khi chip không có trong bảng rank. `5` SD 8 Elite/Gen 3+, A18 Pro/A19 Pro, D9400, Exynos 2600 / `4` SD 8 Gen 2/3, A16/A17, D9200/9300, Exynos 2400 / `3` SD 7 Gen 1/2/3, A13/A15, D8100/8200, Exynos 1480/2200, Kirin 9000 / `2` SD 6 Gen 1, D7200/7300, Exynos 1380, Helio G96/G99, Kirin 980 / `1` SD 4xx, Helio G91 trở xuống, Unisoc T/SC series, Kirin 659 trở xuống |
| **AnTuTu score** | chip_mobile_rank.csv — cột AnTuTu 10 | ~650.000 (SD 7 Gen 1) | Rule-based (lookup) | Lookup AnTuTu từ bảng rank theo tên chip. **Không dùng để score 1–5** — lưu nguyên giá trị số để dùng cho: (1) Tính gaming score tổng hợp, (2) Tìm sản phẩm `similar_to` trong graph (cùng tier AnTuTu), (3) Giải thích cho user ("chip này mạnh tương đương..."). Nếu không lookup được → `N/A` |
| **Xếp loại chip** | chip_mobile_rank.csv — cột Điểm & Xếp loại | 3/5 tier | Rule-based (lookup) | Categorical: `A+` / `A` / `B` / `C` — lưu thêm để dùng khi chatbot giải thích bằng ngôn ngữ tự nhiên ("chip hạng A+, đây là chip flagship") |
| **RAM** | `Dung lượng RAM` | 12GB | Rule-based | `1` ≤ 3GB / `2` 4–5GB / `3` 6–7GB / `4` 8–11GB / `5` ≥ 12GB. **⚠ Parse MB**: Nếu giá trị chứa "MB" hoặc số > 1000 không có đơn vị → chia cho 1024 để ra GB rồi mới score. Ví dụ: "4096 MB" → 4GB → điểm 2. "3 GB" và "3072 MB" đều → điểm 1 |
| **Bộ nhớ trong** | `Bộ nhớ trong` | 256GB | Rule-based | `1` ≤ 32GB / `2` 64GB / `3` 128GB / `4` 256GB / `5` ≥ 512GB. **⚠ Parse MB/TB**: (1) Nếu thấy "MB" hoặc số > 1000 không có đơn vị GB → chia 1024 để ra GB. (2) Nếu thấy "TB" → nhân 1024 để ra GB. Ví dụ: "64000 MB" → 62.5GB → 64GB → điểm 2 / "1 TB" → 1024GB → điểm 5 / "512 MB" (feature phone) → 0.5GB → điểm 1. Sau khi convert, làm tròn về mốc gần nhất: < 48 → 32GB / 48–96 → 64GB / 97–192 → 128GB / 193–384 → 256GB / > 384 → 512GB+ |
| **GPU tier** | `GPU` | Adreno 644 | Rule-based | `5` Adreno 750+/830, Apple GPU 5–6 lõi Pro, Mali-G925/Immortalis / `4` Adreno 720–740, Mali-G715/G720, Apple GPU 4 lõi / `3` Adreno 644–700, Mali-G68/G610 / `2` Adreno 610–642, Mali-G57/G52 / `1` Adreno ≤ 505, Mali-G51 trở xuống, PowerVR, GE8322. ⚠ Nếu có AnTuTu lookup được → GPU tier có thể infer từ AnTuTu: ≥ 2M → tier 5, 1.5–2M → tier 4, 900K–1.5M → tier 3, 500–900K → tier 2, < 500K → tier 1 |
| **Hệ điều hành** | `Hệ điều hành` | Android 14 | Rule-based | Categorical: Android 12 / 13 / 14 / 15 / iOS 17 / iOS 18... |
| **Công nghệ tản nhiệt** | description | Không đề cập | LLM | `5` Vapor Chamber lớn có thương hiệu (gaming phone) / `4` Vapor Chamber tiêu chuẩn / `3` Heat Pipe / `2` Graphite sheet / `1` Không đề cập (mặc định cơ bản) |
| **Bypass charging** | description | Không | LLM | Boolean: `Có` / `Không` — keywords: "bypass charging", "direct charging", "sạc trực tiếp khi chơi game" |

> **AnTuTu dùng được trong graph như thế nào?**
> - **Gaming score tổng hợp** = `(antutu / 2.000.000 × 0.4) + (man_tan_so_quet_score × 0.3) + (tan_nhiet_score × 0.2) + (ram_score × 0.1)` → normalize về 1–5
> - **similar_to edge weight**: Hai sản phẩm có AnTuTu cách nhau < 15% → có thể coi là thay thế nhau về hiệu năng
> - **Giải thích tự nhiên**: "Chip này mạnh tương đương Galaxy S23 Ultra (SD 8 Gen 2, AnTuTu ~1.75M)"

---

## 6. Pin

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Dung lượng pin** | `Pin` | 5000 mAh | Rule-based | `1` ≤ 3000 mAh / `2` 3001–3999 mAh / `3` 4000–4499 mAh / `4` 4500–4999 mAh / `5` ≥ 5000 mAh |
| **Sạc có dây** | `Công nghệ sạc` | 45W | Rule-based | `1` ≤ 10W / `2` 11–24W / `3` 25–44W / `4` 45–66W / `5` ≥ 67W |
| **Sạc không dây** | description | Không hỗ trợ | LLM | `1` Không có / `2` Qi ≤ 7.5W / `3` 10–14W / `4` 15–24W / `5` ≥ 25W (MagSafe 25W, Qi2) |
| **Sạc ngược** | description | Không | LLM | Boolean: `Có` / `Không` |

---

## 7. Kết nối

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Mạng di động** | `Hỗ trợ mạng` | 5G | Rule-based | Categorical: `5G` / `4G LTE` / `3G` |
| **Wi-Fi** | `Wi-Fi` | Wi-Fi 6 (802.11ax) | Rule-based | `1` Wi-Fi 4 (n) / `2` Wi-Fi 5 (ac) / `3` Wi-Fi 6 (ax) / `4` Wi-Fi 6E / `5` Wi-Fi 7 (be) |
| **Bluetooth** | `Bluetooth` | v5.2 | Rule-based | `1` ≤ BT 4.x / `2` BT 5.0 / `3` BT 5.1–5.2 / `4` BT 5.3 / `5` BT 5.4+ hoặc BT 6.0 |
| **GPS** | `GPS` | 5 hệ thống | Rule-based | `1` GPS only / `2` GPS + GLONASS / `3` + Galileo / `4` + BeiDou / `5` ≥ 5 hệ thống |
| **NFC** | `Công nghệ NFC` | Có | Rule-based | Boolean: `Có` / `Không` |
| **Jack 3.5mm** | `Jack tai nghe 3.5` | Không | Rule-based | Boolean: `Có` / `Không` |
| **Hỗ trợ SIM** | `Thẻ SIM` | 2 SIM Nano | Rule-based | Categorical: `1 SIM` / `2 SIM` / `1 SIM + eSIM` / `2 SIM + eSIM` |
| **eSIM** | `Thẻ SIM` + description | Không | LLM | Boolean: `Có` / `Không` |
| **Hỗ trợ thẻ nhớ** | `Khe cắm thẻ nhớ` | microSDXC | Rule-based | Categorical: `Không` / `microSD` / `microSDXC` |

---

## 8. Độ bền

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Kháng nước / bụi** | spec + description | Không đề cập → Không | LLM | `1` Không có / `2` IP52–IP53 / `3` IP54–IP65 / `4` IP67 (1m, 30 phút) / `5` IP68 (≥ 1.5m, 30 phút+) |

---

## 9. Cấu tạo

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Chất lượng mặt lưng** | description | Nhựa phủ mờ | LLM | `5` Titanium / `4` Kính Gorilla / kính cao cấp / `3` Nhựa phủ mờ hoặc vân cao cấp / `2` Nhựa bóng thường / `1` Không rõ |
| **Chất lượng khung viền** | description | Nhựa bo cong | LLM | `5` Titanium / `4` Nhôm nguyên khối 6000/7000 series / `3` Nhôm thường / `2` Nhựa cao cấp / `1` Nhựa thường |
| **Độ mỏng** | `Kích thước` (chiều dày) | 7.8mm | Rule-based | `5` ≤ 7.0mm / `4` 7.1–7.9mm / `3` 8.0–8.9mm / `2` 9.0–9.9mm / `1` ≥ 10mm |
| **Trọng lượng** | `Trọng lượng` | 180g | Rule-based | `5` ≤ 160g / `4` 161–185g / `3` 186–210g / `2` 211–235g / `1` > 235g |
| **Số màu sắc** | `product_color` | 2 màu | Rule-based | Số tùy chọn màu: 1 / 2 / 3 / 4+ |
| **Kiểu màn hình / Notch** | `Kiểu màn hình` | Đục lỗ | Rule-based | Categorical: `Dynamic Island` / `Đục lỗ` / `Giọt nước` / `Toàn màn hình` / `Notch tai thỏ` |
| **Điện thoại gập** | tên + description | Không | Rule-based | Categorical: `Không` / `Fold (gập dọc)` / `Flip (gập ngang)` |

---

## 10. Bảo mật sinh trắc học

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Cảm biến vân tay** | `Cảm biến vân tay` | Trong màn hình (quang học) | Rule-based | Categorical: `Siêu âm dưới màn` (nhanh, chính xác nhất) / `Quang học dưới màn` / `Cạnh viền` / `Mặt lưng` / `Không có` |
| **Nhận diện khuôn mặt** | description + spec | Không đề cập | LLM | Categorical: `3D Face ID` (Apple / cao cấp) / `2D nhận diện khuôn mặt` / `Không có` |
| **Mật khẩu / PIN** | OS | Android → Có | Rule-based | Boolean: mọi smartphone đều `Có` |

---

## 11. Thông tin khác

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Công nghệ âm thanh** | description | Loa kép, Dolby Atmos | LLM | `5` Stereo + Dolby Atmos + tuning hãng âm thanh (Harman/AKG/Bose) / `4` Stereo + Dolby Atmos / `3` Stereo không Dolby / `2` Mono + Dolby Atmos / `1` Mono thường |
| **Hỗ trợ AI** | description | "Điện thoại AI" chung | LLM | `5` AI on-device mạnh + ≥ 4 tính năng rõ ràng (Circle to Search, Live Translate, Generative Edit...) / `4` AI on-device + 2–3 tính năng / `3` AI camera + 1–2 tính năng phần mềm / `2` Chỉ AI camera (Nightography, Super HDR) / `1` Không đề cập tính năng AI cụ thể |
| **Phụ kiện trong hộp** | description | Không đề cập | LLM | `5` Củ sạc + cáp + tai nghe + ốp lưng / `4` Củ sạc + cáp + ốp lưng / `3` Củ sạc + cáp / `2` Chỉ cáp (không củ sạc) / `1` Chỉ hướng dẫn / Không rõ |
| **Action Button** | description + spec | Không | LLM | Boolean: `Có` / `Không` — keyword: "Action Button", "nút tác vụ tùy chỉnh" |
| **Camera Button** | description + spec | Không | LLM | Boolean: `Có` / `Không` — keyword: "Camera Button", "nút chụp ảnh vật lý" |
| **Hỗ trợ thẻ nhớ** | `Khe cắm thẻ nhớ` | microSDXC | Rule-based | Categorical: `Không` / `microSD` / `microSDXC` |
| **Desktop Mode / DeX** | description + tên sản phẩm | Không | LLM | Boolean: `Có` / `Không` — keyword: "Samsung DeX", "Desktop Mode", "MIUI+", "kết nối màn hình ngoài" |
| **Nút SOS / khẩn cấp** | description + spec | Không | LLM | Boolean: `Có` / `Không` — keyword: "SOS", "Emergency SOS", "nút khẩn cấp" |

---

## Tổng kết

| Nhóm | Tổng tiêu chí | Rule-based | LLM |
|---|---|---|---|
| Phân khúc & Tuổi đời | 2 | 2 | 0 |
| Thông tin chung | 6 | 5 | 1 |
| Camera sau | 7 | 5 | 2 |
| Camera trước | 3 | 2 | 1 |
| AI camera | 1 | 0 | 1 |
| Màn hình | 9 | 6 | 3 |
| Hiệu năng | 9 | 7 | 2 |
| Màn hình | 8 | 5 | 3 |
| Hiệu năng | 7 | 4 | 3 |
| Pin | 5 | 2 | 3 |
| Kết nối | 9 | 7 | 2 |
| Độ bền | 1 | 0 | 1 |
| Cấu tạo | 7 | 5 | 2 |
| Bảo mật | 3 | 2 | 1 |
| Thông tin khác | 9 | 1 | 8 |
| **Tổng** | **66** | **39** | **27** |

---

> ⚠ **Lưu ý normalize điểm**: Tất cả điểm 1–5 là điểm **tuyệt đối** theo toàn thị trường.  
> Chatbot cần normalize trong cùng phân khúc giá khi recommend — Snapdragon 7 Gen 1 là 3/5 toàn thị trường nhưng là chip tốt nhất tầm 6–10tr, cần được ưu tiên hiển thị cho user ở phân khúc đó.

> ⚠ **Tiêu chí KHÔNG có trong file này** (cần lookup ngoài → xem file `manual_criteria.md`):  
> `Gaming score` (AnTuTu) / `Thời gian sạc thực tế` / `Pin thực tế (giờ)` / `Use case` / `Đối tượng người dùng` / `Độ giữ giá` / `Thời hạn cập nhật phần mềm`