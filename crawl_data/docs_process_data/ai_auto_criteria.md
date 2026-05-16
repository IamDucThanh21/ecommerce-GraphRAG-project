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

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Số lượng camera sau (thật)** | `Camera sau` | 3 (bỏ macro 2MP) → 2 camera thật | Rule-based | `1` = 1 cam / `2` = 2 cam / `3` = 3 cam thật / `4` = 4 cam thật / `5` = 4+ cam thật. ⚠ Không đếm macro ≤ 2MP và depth sensor vì không có giá trị thực |
| **Độ phân giải camera chính** | `Camera sau` | 50MP | Rule-based | `1` ≤ 12MP / `2` 13–24MP / `3` 25–47MP / `4` 48–63MP / `5` ≥ 64MP |
| **Aperture / Khẩu độ** | `Camera sau` | f/1.8 | Rule-based | `5` ≤ f/1.6 / `4` f/1.7–f/1.8 / `3` f/1.9–f/2.0 / `2` f/2.1–f/2.4 / `1` > f/2.4. Số f càng nhỏ = aperture càng rộng = chụp thiếu sáng tốt hơn |
| **OIS / Chống rung** | `Camera sau` | OIS camera chính | Rule-based | `5` OIS trên cả camera chính + telephoto / `4` OIS camera chính + EIS video / `3` Chỉ OIS camera chính / `2` Chỉ EIS (gyro-EIS) / `1` Không có chống rung |
| **Zoom quang học** | `Camera sau` | Không có → 1x | Rule-based | `1` Không có (1x) / `2` 2x / `3` 3–4x / `4` 5–7x / `5` ≥ 8x |
| **Độ phân giải camera trước** | `Camera trước` | 50MP, f/2.4 | Rule-based | `1` ≤ 8MP / `2` 9–15MP / `3` 16–23MP / `4` 24–31MP / `5` ≥ 32MP |
| **Quay video tối đa** | `Quay video` | 4K@30fps | Rule-based | `1` ≤ 1080p@30fps / `2` 1080p@60fps / `3` 4K@30fps / `4` 4K@60fps / `5` 4K@120fps hoặc 8K |
| **Tính năng AI camera** | description | Nightography, Super HDR, VDIS | LLM | `1` Không có / `2` HDR cơ bản / `3` Night Mode + HDR / `4` Night + HDR + AI Portrait + xóa vật thể / `5` Tất cả trên + AI generative edit + ProRAW / Log |
| **Chất lượng kính lens** | description | Không đề cập | LLM | `5` Sapphire / `4` Kính cường lực đặc biệt có thương hiệu / `3` Kính thường hoặc không rõ (mặc định 3) |

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
| **Hỗ trợ bút stylus** | description | Không | LLM | Categorical: `Tích hợp sẵn` / `Hỗ trợ (mua thêm)` / `Không` |

---

## 5. Hiệu năng

| Tiêu chí | Nguồn | Giá trị mẫu (M55) | Xử lý | Scoring Rubric |
|---|---|---|---|---|
| **Chip (tier)** | `Chipset` | Snapdragon 7 Gen 1 | Rule-based | `5` Flagship mới nhất: SD 8 Gen 3+, A18 Pro, Dimensity 9400 / `4` Flagship -1 thế hệ: SD 8 Gen 2, A17, D9300 / `3` Tầm trung cao: SD 7 Gen 1/2/3, Exynos 1480, D8200 / `2` Tầm trung: SD 6 Gen 1, D7200, Exynos 1380 / `1` Phổ thông: SD 4xx, Helio G, Unisoc |
| **RAM** | `Dung lượng RAM` | 12GB | Rule-based | `1` ≤ 3GB / `2` 4–5GB / `3` 6–7GB / `4` 8–11GB / `5` ≥ 12GB |
| **Bộ nhớ trong** | `Bộ nhớ trong` | 256GB | Rule-based | `1` ≤ 32GB / `2` 64GB / `3` 128GB / `4` 256GB / `5` ≥ 512GB |
| **GPU tier** | `GPU` | Adreno 644 | Rule-based | `5` Adreno 750+, Apple 6-core Pro GPU, Mali-G925 / `4` Adreno 730–740, Mali-G715 / `3` Adreno 644–700, Mali-G68 / `2` Adreno 610–642, Mali-G57 / `1` Adreno ≤ 505, Mali-G52 trở xuống |
| **Hệ điều hành** | `Hệ điều hành` | Android 14 | Rule-based | Categorical: Android 12 / 13 / 14 / 15 / iOS 17 / iOS 18... |
| **Công nghệ tản nhiệt** | description | Không đề cập | LLM | `5` Vapor Chamber lớn có thương hiệu (gaming phone) / `4` Vapor Chamber tiêu chuẩn / `3` Heat Pipe / `2` Graphite sheet / `1` Không đề cập (mặc định cơ bản) |
| **Bypass charging** | description | Không | LLM | Boolean: `Có` nếu tìm thấy keyword "bypass charging" / "direct charging" / "sạc trực tiếp khi chơi game". Chủ yếu có ở ROG Phone, RedMagic |

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
| Camera | 9 | 6 | 3 |
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