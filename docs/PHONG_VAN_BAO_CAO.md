# Ngân hàng câu hỏi bảo vệ báo cáo

> Tổng hợp câu hỏi hay gặp khi bảo vệ báo cáo "Đánh giá hiệu quả cơ chế HARQ trong mạng 5G NTN".  
> Phạm vi báo cáo: **IR-HARQ**, quỹ đạo **LEO 600 km và LEO 1200 km**, MCS A (QPSK r=1/2), SCS 30 kHz mặc định, K=15 dB.  
> Mỗi mục gồm câu hỏi ngắn → câu trả lời cốt lõi → ví dụ/số liệu từ báo cáo để chứng minh.

---

## 1. Mô phỏng Monte Carlo là gì? Tại sao dùng cho HARQ?

**Câu trả lời cốt lõi:**  
Phương pháp Monte Carlo tạo ra hàng chục nghìn thử nghiệm ngẫu nhiên (ở đây: 20 000 gói dữ liệu), mỗi thử nghiệm rút một thực hiện kênh mới, sau đó tính xác suất sự kiện (ví dụ: gói bị lỗi) bằng tần suất quan sát được.

**Tại sao dùng cho HARQ:**  
BLER của HARQ sau nhiều lần phát không có công thức đóng đơn giản — nó phụ thuộc vào phân phối kết hợp của nhiều biến ngẫu nhiên kênh Rician. Monte Carlo không cần biểu thức giải tích: chỉ cần mô phỏng đủ nhiều thử nghiệm thì xác suất thực nghiệm hội tụ về xác suất thực (luật số lớn). Với 20 000 thử nghiệm, sai số thống kê ở BLER = 10⁻³ là ±5 % (khoảng tin cậy 95 %).

---

## 2. Mô hình ngưỡng thông tin tương hỗ (MI-threshold) là gì? Tại sao dùng nó?

**Định nghĩa:**  
Thay vì mô phỏng bộ giải mã LDPC thực (quá chậm), ta dùng quy tắc: gói được giải mã thành công khi tổng thông tin tương hỗ (MI) tích lũy vượt ngưỡng 1,0 bit/channel use. Ngưỡng SNR tương ứng của kênh AWGN được tính qua:

$$\text{SNR}_{thr} = \Delta \cdot (2^r - 1)$$

với $\Delta = 1{,}5$ dB là khoảng cách thực thi LDPC, $r$ là tốc độ mã. Với $r = 1/2$: SNR$_{thr}$ (AWGN) = $-2{,}3$ dB.

**Tại sao dùng:**  
- Nhanh hơn giải mã LDPC thực hàng nghìn lần.  
- Đã được kiểm chứng: sai lệch so với thực tế < 0,2 dB ở BLER = 10⁻³ (Richardson & Urbanke 2008; Tuninato 2025).

**Chú ý quan trọng:**  
Ngưỡng AWGN là −2,3 dB nhưng trong kênh Rician K=15 dB, BLER=10⁻³ đạt ở **+2,0 dB** — lề fading Rician khoảng 4,3 dB. Đây là lý do TX=1 và No HARQ cùng cho kết quả giống nhau và cùng cần +2,0 dB.

---

## 3. Pipeline stall là gì? Tại sao xuất hiện ngay ở LEO?

**Pipeline stall:**  
Trong 5G NR, bên phát dùng N tiến trình HARQ song song để lấp đầy khoảng chờ ACK/NACK. Nếu N không đủ lớn để lấp toàn bộ khoảng RTT, bên phát phải ngồi chờ (idle) — gọi là pipeline stall. Số tiến trình tối thiểu tránh stall:

$$N_{\min} = \left\lceil \frac{RTT}{T_{slot}} \right\rceil + 1$$

**Tại sao LEO 1200 km cũng bị stall với SCS ≥ 30 kHz:**  
RTT tỷ lệ thuận với khoảng cách quỹ đạo. Với SCS 30 kHz ($T_{slot}$ = 0,5 ms):

| Quỹ đạo | RTT | $N_{\min}$ | Giới hạn TS 38.214 | Kết quả |
|---------|-----|-----------|-------------------|---------|
| LEO 600 km | 12,9 ms | 27 | 32 | Khả thi ✓ |
| LEO 1200 km | 24,3 ms | 50 | 32 | Stall ✗ |

LEO 1200 km chỉ khả thi ở SCS 15 kHz ($N_{\min}$ = 26 ≤ 32). Nghịch lý: SCS cao hơn *tăng* $N_{\min}$ vì $T_{slot}$ ngắn hơn nhưng RTT vật lý không đổi.

---

## 4. Tại sao báo cáo không đánh giá SE Goodput?

**Vì báo cáo tập trung vào 3 chiều cốt lõi:**  
1. Hiệu quả link: BLER vs SNR (Thí nghiệm 1)  
2. Ràng buộc pipeline N_min (Thí nghiệm 2)  
3. Hiệu quả năng lượng trên bit (Thí nghiệm 3)

SE Goodput = util × (1 − BLER) × r × log₂M là chỉ tiêu kết hợp của cả 3 chiều trên. Trong phạm vi báo cáo, LEO 600 km với SCS 30 kHz đạt util = 100% (không stall), nên SE Goodput ≈ (1 − BLER_final) × 0,5 bit/s/Hz — không cung cấp thêm thông tin mới so với BLER.

---

## 5. Các thuật ngữ kỹ thuật chính cần nắm

| Thuật ngữ | Định nghĩa |
|-----------|-----------|
| **HARQ** | Hybrid ARQ: kết hợp FEC (sửa lỗi xuôi) + ARQ (phát lại có xác nhận) |
| **IR-HARQ** | Incremental Redundancy: mỗi lần phát lại gửi *bit dư thừa mới* (RV khác nhau) |
| **BLER** | Block Error Rate: tỷ lệ gói bị lỗi sau giải mã |
| **RTT** | Round-Trip Time: thời gian từ khi phát đến khi nhận được ACK/NACK |
| **NTN** | Non-Terrestrial Network: mạng không mặt đất (vệ tinh, UAV) |
| **LEO** | Low Earth Orbit: quỹ đạo thấp (~600–1200 km) |
| **SCS** | Subcarrier Spacing: khoảng cách sóng mang con (15/30/60/120 kHz) |
| **MCS A** | Modulation and Coding Scheme A: QPSK, r=1/2 |
| **Rician K** | Tỷ số công suất LOS / tán xạ; K=15 dB = kênh LOS rất mạnh |
| **Pipeline stall** | Trạng thái bên phát phải chờ vì không đủ tiến trình HARQ để lấp RTT |
| **util** | Hệ số sử dụng đường truyền: util = min(1, N/N_min) |
| **E_bit** | Năng lượng chuẩn hóa trên bit thông tin được giao thành công |
| **MI** | Mutual Information: đo lượng thông tin kênh có thể mang |
| **LDPC gap Δ** | Khoảng cách giữa ngưỡng Shannon và ngưỡng giải mã LDPC thực tế (~1,5 dB) |

---

## 6. Tại sao lại có UE (User Equipment) trong báo cáo vệ tinh?

Trong kiến trúc 5G NTN (TR 38.811), vệ tinh đóng vai trò **trạm thu phát di động (gNB) trên quỹ đạo** hoặc là relay. UE (thiết bị người dùng) — điện thoại, thiết bị IoT, thiết bị đầu cuối vệ tinh — giao tiếp trực tiếp với vệ tinh qua giao diện vô tuyến NR Uu, giống hệt cách giao tiếp với gNB mặt đất.

3GPP Rel-17 chuẩn hóa chính xác giao diện này, bao gồm cả HARQ. "UE di chuyển 50 km/h" trong báo cáo chỉ đặc tả điều kiện fading của đầu cuối — hoàn toàn phù hợp với ngữ cảnh vệ tinh.

---

## 7. Incremental Redundancy hoạt động thế nào? Tại sao tốt hơn truyền đơn?

**IR-HARQ:**  
Mỗi lần phát lại gửi một phần *bit dư thừa khác* (RV ∈ {0,2,3,1} — lấy từ các vùng khác nhau của circular buffer LDPC). Bên thu tích lũy thông tin tương hỗ:
$$I^{(n)} = \frac{1}{r} \sum_{i=1}^{n} \log_2\!\left(1 + \frac{\gamma_i}{\Delta}\right)$$

**Tại sao IR tốt hơn truyền đơn (No HARQ):**  
- No HARQ: 1 TX, nếu kênh xấu → gói lỗi, không phục hồi.  
- IR-HARQ: tối đa 4 TX, tích lũy MI từ mỗi TX. Mỗi TX thêm log₂(1+γᵢ/Δ) → tổng MI tăng dần.  
- Bất đẳng thức Jensen: tổng log lớn hơn log của tổng, nên IR tích lũy MI hiệu quả hơn Chase Combining.

**Kết quả từ mô phỏng:**  
TX=4 đạt BLER = 10⁻³ tại −7,0 dB, trong khi No HARQ cần +2,0 dB → IR-HARQ giảm yêu cầu SNR đi **9,0 dB**.

---

## 8. Payload tái sinh (regenerative payload) là gì?

**Định nghĩa:** Vệ tinh có payload tái sinh (*regenerative*) giải mã toàn bộ tín hiệu nhận được từ mặt đất, xử lý gói IP/NR, rồi phát lại tín hiệu mới xuống mặt đất — giống như một gNB đặt trên quỹ đạo. Đối lập với payload trong suốt (*bent-pipe*) chỉ khuếch đại và chuyển tần tín hiệu.

**Ảnh hưởng đến RTT:**  
- **Payload tái sinh:** RTT = (truyền lan lên + xuống) + trễ xử lý trên vệ tinh — **nhỏ hơn khoảng 2×** so với bent-pipe.

Báo cáo sử dụng RTT của payload tái sinh (TR 38.811 Bảng 5.3.4.1-1): LEO 600 km = **12,88 ms**, LEO 1200 km = **24,32 ms** (góc ngẩng 10°).

---

## 9. Hướng dẫn đọc và thuyết trình các biểu đồ Chương 4

### Hình 4.1 — BLER vs $E_s/N_0$ (Thí nghiệm 1)

**Mô tả biểu đồ:**  
Hệ trục bán-log. Trục x: $E_s/N_0$ (dB) từ −12 đến +8 dB. Trục y: BLER (log từ 10⁻⁷ đến 1). Có 6 đường:
- Đường chấm xám (×): **No HARQ** — baseline 1 lần phát.  
- 4 đường xanh tăng dần độ đậm: **IR TX=1 (nhạt) → TX=4 (đậm nhất)** — đậm hơn = nhiều TX hơn = hiệu năng tốt hơn.  
- Đường ngang đứt xám: **mục tiêu BLER = 10⁻³**.

**Cách đọc — gióng xuống từ vạch 10⁻³:**  
Tìm giao điểm của mỗi đường với vạch ngang BLER = 10⁻³, sau đó chiếu xuống trục x:

| Đường | Màu | Giao điểm với BLER=10⁻³ |
|-------|-----|------------------------|
| No HARQ | xám chấm | **+2,0 dB** |
| IR TX=1 | xanh nhạt nhất | **+2,0 dB** (= No HARQ) |
| IR TX=2 | xanh vừa | **−2,5 dB** |
| IR TX=3 | xanh đậm vừa | **−5,0 dB** |
| IR TX=4 | xanh đậm nhất | **−7,0 dB** |

**Độ lợi tổng:** Đường đậm nhất (TX=4) giao BLER=10⁻³ ở −7,0 dB. Đường xám (No HARQ) giao ở +2,0 dB. Khoảng cách = **9,0 dB** — đây là độ lợi SNR của IR-HARQ.

**Tại sao TX=1 và No HARQ cùng 2,0 dB?**  
TX=1 của IR-HARQ là lần phát đầu tiên — chưa có tích lũy MI, giống hệt No HARQ. Chỉ từ TX=2 trở đi mới có phân tập.

**Điểm nhấn khi thuyết trình:**  
> "Nhìn vào đường xanh đậm nhất — IR TX=4 — nó cắt vạch BLER 10⁻³ ở −7 dB. Chiếu xuống trục x thì thấy. Đường xám No HARQ cắt ở +2 dB. Khoảng cách là 9 dB — đó là lợi thế của IR-HARQ: cùng chất lượng dịch vụ nhưng yêu cầu SNR ít hơn 9 dB, tức là có thể phục vụ thiết bị ở xa hơn hoặc dùng công suất thấp hơn."

**Câu hỏi thầy hay hỏi:**  
- *"Tại sao bước nhảy TX=1→TX=2 lớn (4,5 dB) còn TX=3→TX=4 nhỏ (2 dB)?"* → TX=2 cứu những gói kênh xấu, thêm MI từ kênh thứ hai độc lập → lợi lớn. Đến TX=4, gói còn lại là những gói kênh cực xấu, thêm MI mỗi TX được ít hơn.  
- *"Kênh Rician K=15 dB có ảnh hưởng gì đến hình dạng đường?"* → K lớn → kênh gần tất định (LOS mạnh) → đường waterfall dốc hơn Rayleigh. Khi tích lũy n TX, bậc tự do của phân phối chi-bình phương tăng lên 2n → waterfall càng dốc.

---

### Hình 4.2 — $N_{\min}$ theo SCS (Thí nghiệm 2)

**Mô tả biểu đồ:**  
Biểu đồ cột nhóm. Trục x: 2 nhóm (LEO 600 km, LEO 1200 km). Mỗi nhóm: 4 cột màu = 4 SCS (15/30/60/120 kHz). Trục y: $N_{\min}$ (số tiến trình HARQ tối thiểu). **Đường đỏ ngang**: giới hạn N = 32 (TS 38.214). Cột vượt đường đỏ = không khả thi.

**Cách đọc:**  
- Cột dưới đường đỏ → SCS đó khả thi.  
- Số trên cột: **đen** = khả thi; **đỏ đậm** = vượt giới hạn.

**Bảng giá trị:**

| Quỹ đạo | SCS 15 kHz | SCS 30 kHz | SCS 60 kHz | SCS 120 kHz |
|---------|-----------|-----------|-----------|------------|
| LEO 600 km | **14** ✓ | **27** ✓ | 53 ✗ | 105 ✗ |
| LEO 1200 km | **26** ✓ | 50 ✗ | 99 ✗ | 196 ✗ |

Chỉ **3/8 tổ hợp** khả thi: LEO 600 km SCS 15 và 30 kHz; LEO 1200 km SCS 15 kHz.

**Điểm nhấn khi thuyết trình:**  
> "Trong 8 tổ hợp quỹ đạo × SCS, chỉ 3 tổ hợp thỏa mãn N_min ≤ 32. Điểm quan trọng: SCS cao hơn — thường gắn với băng thông rộng hơn — lại làm N_min tăng. Ở LEO 600 km, SCS 120 kHz cần 105 tiến trình, gấp hơn 3 lần giới hạn. Nguyên nhân: T_slot ngắn hơn nên cần nhiều tiến trình hơn để lấp cùng một RTT vật lý — RTT không phụ thuộc băng thông."

**Câu hỏi thầy hay hỏi:**  
- *"SCS 30 kHz ở LEO 600 km có N_min=27, tại sao chọn N=32?"* → N=32 là giới hạn tối đa TS 38.214. N=32 ≥ 27 → util = 100%, cấu hình tối ưu.  
- *"Nếu 3GPP tăng giới hạn N lên 64 thì sao?"* → LEO 1200 km SCS 30 kHz (N_min=50) sẽ khả thi, và một số tổ hợp SCS 60 kHz cũng sẽ mở ra.

---

### Hình 4.3 — Năng lượng/bit vs $E_s/N_0$ (Thí nghiệm 3)

**Mô tả biểu đồ:**  
Hệ trục bán-log. Trục x: $E_s/N_0$ (dB) từ −10 đến +25 dB. Trục y (log): $E_{\text{bit}}$ (J/bit), $P_{tx}=1$ W chuẩn hóa. Hai đường:
- Đường chấm xám (×): **No HARQ** — vọt lên ở SNR âm.  
- Đường xanh liền (○): **IR-HARQ** — gần phẳng trên toàn dải.

**Cách đọc:**  
- Trục y log: 1 bậc = hệ số 10 lần, 3 bậc = 1000 lần.  
- Tại SNR thấp (trái): No HARQ tăng vọt → BLER gần 100% → hầu hết năng lượng lãng phí.  
- Tại SNR cao (phải): cả hai hội tụ về ~5×10⁻⁴ J/bit → avg_ntx → 1, BLER → 0.  
- **Điểm quan trọng nhất:** ở −5 dB, đọc khoảng cách dọc giữa hai đường.

**Giá trị tại các điểm SNR:**

| $E_s/N_0$ | No HARQ ($E_{\text{bit}}$) | IR-HARQ ($E_{\text{bit}}$) | Tỷ lệ |
|-----------|--------------------------|--------------------------|-------|
| −5 dB | ~0,54 J/bit | ~1,1×10⁻³ J/bit | **~500 lần** |
| 0 dB | ~5,2×10⁻⁴ J/bit | ~5,2×10⁻⁴ J/bit | ~1 lần |
| +5 dB | ~5,0×10⁻⁴ J/bit | ~5,0×10⁻⁴ J/bit | ~1 lần |

**Tại sao tại 0 dB hai đường gần bằng nhau?**  
Ngưỡng BLER=10⁻³ của No HARQ là +2,0 dB. Tại 0 dB, kênh Rician K=15 dB còn khá tốt — BLER No HARQ chỉ ~3–5%, không quá cao → E_bit xấp xỉ bình thường. IR-HARQ hầu hết gói thành công ở TX=1 hoặc TX=2 → E_bit ≈ T_slot.

**Điểm nhấn khi thuyết trình:**  
> "Tại −5 dB, No HARQ cần 0,54 joule để giao thành công một bit — vì BLER gần 100%, hầu hết năng lượng bị lãng phí. IR-HARQ chỉ cần 1,1 millijoule/bit vì 4 TX tích lũy MI đưa BLER cuối về gần 0. Chênh lệch ~500 lần, tức gần 3 bậc độ lớn trên trục log. Với thiết bị IoT vệ tinh chạy pin, đây là sự khác biệt giữa vài giờ và hàng năm tuổi pin ở điều kiện SNR biên."

**Tại sao không phải 10⁹ lần?**  
Với kênh Rician K=15 dB, No HARQ không thất bại 100% gói tại −5 dB (BLER ≈ 99,9%, không phải 100%). E_bit bị giới hạn bởi: E_bit ≈ P_tx × T_slot / (1−BLER) ≈ 5×10⁻⁴ / 10⁻³ = 0,5 J/bit. Giá trị 500 lần là chính xác từ mô phỏng và vẫn rất ấn tượng.

**Câu hỏi thầy hay hỏi:**  
- *"avg_ntx ở +5 dB là bao nhiêu?"* → ≈ 1,00 — kênh tốt nên TX=1 luôn thành công.  
- *"Tại sao hai đường hội tụ ở SNR cao?"* → BLER_final → 0 và avg_ntx → 1 cho cả hai → E_bit → P_tx × T_slot = hằng số như nhau.  
- *"IR-HARQ ở LEO 600 km SCS 30 kHz không bị stall — điều này ảnh hưởng thế nào đến E_bit?"* → util = 100% (N=32 ≥ N_min=27), nên E_bit công thức = P_tx × avg_ntx × T_slot / (util × (1−BLER_final)) = P_tx × avg_ntx × T_slot / (1 × 1) — không có penalti pipeline stall. Đây là cấu hình lý tưởng.
