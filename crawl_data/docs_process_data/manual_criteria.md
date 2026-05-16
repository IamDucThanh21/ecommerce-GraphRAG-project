# Tiêu chí tự đánh giá thủ công — Scoring Rubric
> Những tiêu chí này **không thể lấy từ spec, description hoặc giá** một cách đáng tin cậy.  
> Cần: human judgment, lookup nguồn ngoài, hoặc trải nghiệm thực tế.  
> Ví dụ minh họa: Samsung Galaxy M55 12GB 256GB

---

## Ghi chú cột
- **Nguồn tra cứu**: Lấy thông tin từ đâu
- **Tần suất cập nhật**: Bao lâu cần xem lại một lần
- **Giá trị mẫu (M55)**: Gợi ý điểm cho M55 kèm lý do
- **Scoring Rubric**: Quy tắc chấm điểm chi tiết

---

## 1. Use Case — Mức độ phù hợp

> Đây là nhóm **quan trọng nhất** với chatbot recommend.  
> Chấm điểm 1–5 cho từng use case — **một sản phẩm có thể đạt điểm cao ở nhiều use case cùng lúc**.  
> Đây **không phải** xếp hạng so sánh giữa các máy — mà là đánh giá máy này phục vụ use case đó tốt đến đâu.

| Use Case | Nguồn tra cứu | Tần suất | Giá trị mẫu (M55) | Scoring Rubric |
|---|---|---|---|---|
| **Gaming** | GSMArena benchmark, AnTuTu thực tế, YouTube gaming review | 1 lần khi nhập | **3/5** — Chip SD 7 Gen 1 đủ chơi game tầm trung mượt, không đủ cho game nặng max setting. Thiếu tản nhiệt chuyên dụng | `5` Chơi mọi game max setting, không throttle sau 30 phút / `4` Chơi game nặng setting cao, ổn định / `3` Chơi tốt game tầm trung, game nặng phải giảm setting / `2` Chỉ phù hợp game nhẹ / `1` Lag ngay cả game nhẹ |
| **Camera / Creator** | Sample ảnh từ GSMArena, DxOMark, YouTube camera review | 1 lần khi nhập | **3/5** — Camera 50MP f/1.8 + OIS tốt cho tầm giá, nhưng zoom kém (1x), thiếu telephoto thật | `5` Ảnh chất lượng flagship, video ProRes/Log, zoom quang tốt, xuất sắc mọi điều kiện ánh sáng / `4` Ảnh rất tốt tầm trung-cao, video 4K ổn định, đủ cho content creator / `3` Ảnh tốt điều kiện sáng, video 4K cơ bản, phù hợp người dùng bình thường / `2` Ảnh chấp nhận được, video 1080p / `1` Camera kém, chỉ dùng chụp lưu niệm |
| **Văn phòng** | Đánh giá tổng hợp: RAM + pin + trọng lượng + màn hình + OS | 1 lần khi nhập | **4/5** — RAM 12GB đa nhiệm tốt, pin 5000mAh cả ngày, nhẹ 180g, màn 6.7" thoải mái | `5` Pin > 1 ngày, RAM ≥ 12GB, màn ≥ 6.5", thiết kế lịch sự, hỗ trợ office đầy đủ / `4` Pin cả ngày, RAM ≥ 8GB, màn tốt, đủ dùng văn phòng / `3` Đáp ứng việc nhẹ, có thể cần sạc giữa ngày / `2` Pin yếu hoặc RAM thấp, không đủ đa nhiệm / `1` Không phù hợp làm việc |
| **Mạng xã hội** | Đánh giá: camera selfie + UI mượt + màn hình + pin | 1 lần khi nhập | **4/5** — Selfie 50MP rất tốt, màn Super AMOLED+ sắc nét, UI mượt 120Hz | `5` Selfie xuất sắc, UI cực mượt, màn hình rực rỡ, pin thoải mái cả ngày / `4` Selfie tốt, màn đẹp, trải nghiệm mượt / `3` Selfie chấp nhận, màn ổn, dùng được / `2` Selfie thường, màn LCD / `1` Selfie kém, màn TFT |
| **Học tập** | Đánh giá: pin + trọng lượng + giá + màn hình đọc tài liệu + đa nhiệm | 1 lần khi nhập | **4/5** — Pin trâu, nhẹ, giá hợp lý tầm trung, màn to rõ đọc tài liệu | `5` Pin > 1 ngày, nhẹ ≤ 185g, giá hợp lý, màn ≥ 6.5" đọc rõ / `4` Pin cả ngày, đủ nhẹ, giá phù hợp sinh viên / `3` Pin tạm, giá vừa phải, dùng được cho học tập / `2` Pin yếu hoặc giá quá cao so với nhu cầu / `1` Không phù hợp |
| **Kinh doanh** | Đánh giá: bảo mật + eSIM + thiết kế + pin + thương hiệu | 1 lần khi nhập | **2/5** — Thiếu eSIM, khung nhựa không sang, không phù hợp hình ảnh doanh nhân | `5` eSIM + IP68 + thiết kế cao cấp + bảo mật doanh nghiệp + pin cả ngày / `4` eSIM hoặc thiết kế cao cấp + bảo mật tốt + pin tốt / `3` Thiết kế chấp nhận, bảo mật cơ bản / `2` Thiếu 1–2 yếu tố quan trọng / `1` Hoàn toàn không phù hợp |
| **Thể thao / Outdoor** | Đánh giá: IP rating + độ bền + GPS + pin + trọng lượng | 1 lần khi nhập | **2/5** — Không có IP rating, không phù hợp dùng ngoài trời, mưa, thể thao | `5` IP68 + GPS đa hệ thống + pin trâu + nhẹ + chống sốc / `4` IP67+ + GPS tốt + pin ổn / `3` IP65 + GPS cơ bản / `2` Không IP nhưng GPS tốt, pin khá / `1` Không có IP, GPS yếu |

---

## 2. Đối tượng người dùng — Mức độ phù hợp

> Chấm điểm 1–5 cho từng đối tượng.  
> Dựa trên tổng hợp use case + giá + thiết kế + tính năng đặc thù của từng nhóm.

| Đối tượng | Nguồn tra cứu | Tần suất | Giá trị mẫu (M55) | Scoring Rubric |
|---|---|---|---|---|
| **Học sinh cấp 3** | Giá + pin + độ bền + camera selfie | 1 lần khi nhập | **4/5** — Giá 8tr hơi cao nhưng pin trâu, selfie 50MP, thiết kế đẹp phù hợp | `5` Giá ≤ 6tr + pin trâu + selfie tốt + đủ bền / `4` Giá 6–10tr + đủ các yếu tố trên / `3` Giá hợp lý nhưng thiếu 1 yếu tố / `2` Giá quá cao hoặc pin quá yếu / `1` Không phù hợp |
| **Sinh viên** | Giá + đa nhiệm + pin + camera + trọng lượng | 1 lần khi nhập | **4/5** — RAM 12GB đa nhiệm tốt, pin cả ngày, camera đủ dùng, giá tầm trung | `5` Cân bằng tốt: giá ≤ 10tr, RAM ≥ 8GB, pin ≥ 4500mAh, camera tốt, nhẹ / `4` Đáp ứng tốt hầu hết / `3` Đáp ứng nhu cầu cơ bản / `2` Thiếu 1–2 yếu tố quan trọng / `1` Không phù hợp |
| **Dân văn phòng** | Pin + màn hình + trọng lượng + thiết kế chuyên nghiệp | 1 lần khi nhập | **3/5** — Đủ dùng nhưng thiết kế nhựa, thiếu eSIM, không nổi bật | `5` Thiết kế lịch sự, pin ≥ 1 ngày, nhẹ, eSIM, bảo mật tốt / `4` Đáp ứng tốt hầu hết / `3` Dùng được, không có yếu tố nào xuất sắc / `2` Pin yếu hoặc thiết kế không phù hợp văn phòng / `1` Không phù hợp |
| **Freelancer** | Camera + màn hình + hiệu năng + pin + đa năng | 1 lần khi nhập | **3/5** — Camera tầm trung, không có zoom, thiếu tính năng creator cao cấp | `5` Camera flagship + màn hình chất + hiệu năng đủ edit + pin cả ngày / `4` Camera tốt + hiệu năng đủ cho edit nhẹ / `3` Đủ dùng freelance đơn giản / `2` Camera hoặc hiệu năng yếu / `1` Không phù hợp |
| **Gamer** | AnTuTu + gaming review + tản nhiệt + Hz + pin | Lookup AnTuTu | **3/5** — SD 7 Gen 1 chơi game tầm trung, 120Hz mượt, nhưng thiếu tản nhiệt chuyên dụng | `5` AnTuTu > 1.5M + tản nhiệt vapor + 144Hz+ + bypass charging / `4` AnTuTu > 900K + 120Hz + pin trâu / `3` AnTuTu 500–900K + 120Hz + pin ổn / `2` AnTuTu < 500K hoặc 60Hz / `1` Không phù hợp chơi game |
| **Nhiếp ảnh gia** | DxOMark + sample ảnh thực tế + zoom + video specs | DxOMark / review | **2/5** — Không zoom quang, không ProRAW/Log, chất lượng tầm trung | `5` DxOMark > 150 hoặc flagship camera + zoom quang ≥ 5x + ProRAW/Log / `4` Camera rất tốt + zoom quang + 4K ổn định / `3` Camera tốt tầm trung, đủ ảnh casual / `2` Camera trung bình, thiếu zoom / `1` Camera kém |
| **Người lớn tuổi** | Kích thước màn + độ sáng + loa + trọng lượng + dễ dùng | 1 lần khi nhập | **3/5** — Màn lớn 6.7" sáng tốt, nhưng không jack tai nghe, thiếu nút SOS | `5` Màn ≥ 6.5" sáng + loa to rõ + nhẹ + jack 3.5mm + nút SOS + UI đơn giản / `4` Màn lớn + loa tốt + nhẹ, còn thiếu 1 yếu tố / `3` Đáp ứng cơ bản: màn to, dễ nhìn / `2` Màn nhỏ hoặc loa yếu / `1` Không phù hợp |
| **Doanh nhân** | Thiết kế + eSIM + bảo mật + pin + hình ảnh thương hiệu | 1 lần khi nhập | **2/5** — Khung nhựa, không eSIM, không IP, không phù hợp hình ảnh doanh nhân | `5` Thiết kế cao cấp (titanium/kính) + eSIM + IP68 + bảo mật tốt + thương hiệu uy tín / `4` Thiết kế tốt + eSIM + bảo mật ổn / `3` Thiết kế chấp nhận, thiếu eSIM hoặc IP / `2` Thiếu 2 yếu tố trở lên / `1` Hoàn toàn không phù hợp |

---

## 3. Hiệu năng thực chiến

> Những thông số này cần **lookup từ nguồn ngoài** — không có trong spec bán lẻ.

| Tiêu chí | Nguồn tra cứu | Tần suất | Giá trị mẫu (M55) | Scoring Rubric |
|---|---|---|---|---|
| **Gaming score (AnTuTu)** | [NanoreView](https://nanoreview.net) hoặc AnTuTu database | 1 lần khi nhập | SD 7 Gen 1 ≈ 650.000–750.000 → **3/5** | `5` ≥ 1.500.000 / `4` 900.000–1.499.999 / `3` 500.000–899.999 / `2` 300.000–499.999 / `1` < 300.000 |
| **Thời gian sạc thực tế (phút)** | [GSMArena charging test](https://gsmarena.com) | 1 lần khi nhập | 45W → ~65–70 phút → **3/5** | `5` ≤ 30 phút / `4` 31–45 phút / `3` 46–70 phút / `2` 71–90 phút / `1` > 90 phút |
| **Pin thực tế (giờ)** | [GSMArena battery endurance test](https://gsmarena.com) | 1 lần khi nhập | 5000mAh + SD 7 Gen 1 → khoảng 110–120h endurance → **4/5** | `5` GSMArena endurance ≥ 130h / `4` 100–129h / `3` 80–99h / `2` 60–79h / `1` < 60h |

---

## 4. Độ giữ giá / Giá trị theo thời gian

> Lookup thực tế từ thị trường mua bán cũ. Công thức: **(Giá cũ ÷ Giá mới lúc mua) × 100%** sau 12 tháng.

| Tiêu chí | Nguồn tra cứu | Tần suất | Giá trị mẫu (M55) | Scoring Rubric |
|---|---|---|---|---|
| **% giá còn lại sau 12 tháng** | Chợ Tốt, Facebook Marketplace, CellphoneS thu cũ | Mỗi quý | CellphoneS thu cũ 7.490.000đ / giá mới 7.990.000đ = 93% → chưa đủ 12 tháng để đánh giá chính xác | `Cao` ≥ 70% / `Trung bình` 50–69% / `Thấp` < 50% |
| **Điểm giữ giá** | Tính từ % trên | Mỗi quý | Chưa đủ dữ liệu 12 tháng | `5` ≥ 70% / `4` 60–69% / `3` 50–59% / `2` 35–49% / `1` < 35%. Tham khảo: iPhone giữ giá ~70–85% / Samsung flagship ~55–65% / Samsung mid ~40–55% / Xiaomi/Oppo ~30–45% |

---

## 5. Phần mềm & Hỗ trợ lâu dài

| Tiêu chí | Nguồn tra cứu | Tần suất | Giá trị mẫu (M55) | Scoring Rubric |
|---|---|---|---|---|
| **Số năm OS update** | Trang chính thức hãng / thông báo chính sách | 1 lần + cập nhật khi đổi chính sách | Samsung M series: **4 năm** (03/2024 → ~2028) | `5` ≥ 7 năm (iPhone, Pixel 9, Galaxy S25) / `4` 5–6 năm / `3` 4 năm / `2` 3 năm / `1` ≤ 2 năm |
| **Số năm bản vá bảo mật** | Trang chính thức hãng | 1 lần + cập nhật | Samsung M series: **5 năm** (~2029) | `5` ≥ 7 năm / `4` 5–6 năm / `3` 4 năm / `2` 3 năm / `1` ≤ 2 năm |
| **Số năm update còn lại** | Tính: năm kết thúc hỗ trợ − năm hiện tại | Hàng năm | Hết hỗ trợ ~2028, hiện 2025 → còn ~3 năm → **3/5** | `5` ≥ 5 năm / `4` 4 năm / `3` 3 năm / `2` 2 năm / `1` ≤ 1 năm |
| **Chất lượng phần mềm / ít bloatware** | User review, YouTube thực tế | 1 lần + sau major update | One UI trên M series: ổn định, ít bloatware → **3/5** | `5` Stock Android / iOS / OxygenOS — sạch hoàn toàn / `4` One UI / ZenUI — ít bloatware, tùy chỉnh tốt / `3` ColorOS / HyperOS — vừa phải / `2` MIUI nhiều quảng cáo / `1` Nặng nề, chậm theo thời gian |

---

## 6. Camera thực tế

> Spec chỉ cho biết thông số trên giấy — chất lượng ảnh thực tế cần xem sample và review chuyên sâu.

| Tiêu chí | Nguồn tra cứu | Tần suất | Giá trị mẫu (M55) | Scoring Rubric |
|---|---|---|---|---|
| **Chất lượng ảnh ban ngày** | Sample ảnh từ GSMArena, YouTube camera review | 1 lần khi nhập | Tốt cho tầm trung, màu sắc rực Samsung, chi tiết ổn → **3/5** | `5` Sắc nét tuyệt vời, màu chuẩn, dynamic range rộng / `4` Rất tốt cho phân khúc / `3` Tốt điều kiện lý tưởng / `2` Chấp nhận được / `1` Kém |
| **Chất lượng ảnh ban đêm** | Sample ảnh đêm từ reviewer | 1 lần khi nhập | Nightography + OIS giúp ảnh đêm khá tốt tầm trung → **3/5** | `5` Gần như không noise, chi tiết tốt, ánh sáng tự nhiên / `4` Rất tốt, ít noise / `3` Chấp nhận được, noise nhưng nhìn được / `2` Nhiều noise, mất chi tiết / `1` Tối và nát |
| **Chất lượng video thực tế** | YouTube video sample | 1 lần khi nhập | 4K@30fps + gyro-EIS, ổn định tầm trung → **3/5** | `5` 4K ổn định xuất sắc, màu chuẩn, ProRes/Log / `4` 4K@60fps ổn định tốt / `3` 4K@30fps đủ dùng, EIS chấp nhận / `2` Rung hoặc chỉ 1080p / `1` Video chất lượng kém |
| **Chất lượng selfie thực tế** | Sample selfie từ reviewer | 1 lần khi nhập | 50MP f/2.4 → sắc nét ngày, tối kém do aperture nhỏ → **3/5** | `5` Sắc nét, da tự nhiên, tốt cả ngày lẫn tối / `4` Rất tốt ngày, ổn tối / `3` Tốt ban ngày, tối chấp nhận / `2` Chỉ dùng được ban ngày / `1` Selfie kém |

---

## 7. AI — Chi tiết tính năng

> Description thường chỉ nói chung chung "AI" hoặc "Điện thoại AI" — cần xác minh tính năng thực tế.

| Tiêu chí | Nguồn tra cứu | Tần suất | Giá trị mẫu (M55) | Scoring Rubric |
|---|---|---|---|---|
| **AI on-device vs Cloud** | Samsung.com / trang chính thức hãng | 1 lần + cập nhật firmware | M55 không phải Galaxy AI flagship → hầu hết là cloud-based | Categorical: `On-device` (không cần mạng) / `Cloud` (cần internet) / `Hybrid` / `Không rõ` |
| **Danh sách tính năng AI thực tế** | Trang chính thức + release notes | Sau mỗi major update | M55: Nightography, Super HDR. Không có Circle to Search, không có Live Translate | Liệt kê cụ thể — chỉ đếm tính năng thực sự hoạt động, không phải marketing |
| **AI Score tổng hợp** | Tổng hợp từ 2 tiêu chí trên | Sau mỗi major update | Chỉ có AI camera cơ bản → **2/5** | `5` ≥ 5 tính năng AI on-device có ích / `4` 3–4 tính năng rõ ràng / `3` 2 tính năng AI thực sự / `2` Chỉ AI camera (Night Mode, HDR) / `1` Không có AI thực chất |

---

## Tổng kết

| Nhóm | Số tiêu chí | Thời gian ước tính / sản phẩm |
|---|---|---|
| Use case (7 mục) | 7 điểm | ~5 phút |
| Đối tượng người dùng (8 mục) | 8 điểm | ~5 phút |
| Hiệu năng thực chiến (3 mục) | 3 điểm + lookup | ~10 phút |
| Độ giữ giá (2 mục) | 2 điểm + lookup | ~5 phút |
| Phần mềm & hỗ trợ (4 mục) | 4 điểm | ~5 phút |
| Camera thực tế (4 mục) | 4 điểm | ~5 phút |
| AI chi tiết (3 mục) | 3 điểm | ~3 phút |
| **Tổng** | **31 tiêu chí** | **~35–40 phút / sản phẩm** |

---

## Nguồn tra cứu chuẩn

| Loại thông tin | Nguồn |
|---|---|
| Spec đầy đủ + benchmark pin + charging test | [GSMArena](https://gsmarena.com) |
| AnTuTu score lookup | [NanoreView](https://nanoreview.net) |
| Camera sample + điểm DxOMark | [DxOMark](https://dxomark.com) / GSMArena camera test |
| Giá cũ / độ giữ giá | [Chợ Tốt](https://chotot.com) / Facebook Marketplace / CellphoneS thu cũ |
| Chính sách update phần mềm | Samsung: [security.samsungmobile.com](https://security.samsungmobile.com) / Apple: apple.com/support |
| Đánh giá thực tế tổng hợp | YouTube: GSMArena, Dave2D, MKBHD / Việt Nam: ThanhLong38, Manh Nguyen Tech |

---

## Gợi ý thứ tự thực hiện với 50 sản phẩm đầu tiên

**Bước 1** — Điền Use case + Đối tượng người dùng trước (~10 phút/máy). Đây là phần ảnh hưởng nhiều nhất đến chất lượng recommend.

**Bước 2** — Lookup AnTuTu + pin thực tế từ GSMArena (~10 phút/máy). Làm theo batch — tra 50 máy cùng lúc nhanh hơn từng máy một.

**Bước 3** — Điền chính sách update phần mềm (~2 phút/máy nếu biết chính sách theo dòng sản phẩm — Samsung M series dùng chung 1 chính sách).

**Bước 4** — Độ giữ giá + camera thực tế + AI. Có thể làm sau khi hệ thống đã chạy được.

> 💡 **Mẹo**: Tạo một Google Sheet với 50 dòng sản phẩm và 31 cột điểm. Điền một loạt theo từng cột (Use case Gaming cho tất cả 50 máy) sẽ nhanh hơn nhiều so với làm từng sản phẩm một — não đang ở cùng một "mode" đánh giá nên nhất quán hơn.
