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

## 4. Tại sao không đánh giá SE Goodput?

**Vì báo cáo tập trung vào 3 chiều cốt lõi:**  
1. Hiệu quả link: BLER vs SNR (Thí nghiệm 1)  
2. Ràng buộc pipeline N_min (Thí nghiệm 2)  
3. Hiệu quả năng lượng trên bit (Thí nghiệm 3)

SE Goodput = util × (1 − BLER) × r × log₂M là chỉ tiêu kết hợp của cả 3 chiều trên. Trong phạm vi báo cáo, LEO 600 km với SCS 30 kHz đạt util = 100% (không stall), nên SE Goodput ≈ (1 − BLER_final) × 0,5 bit/s/Hz — không cung cấp thêm thông tin mới so với BLER.

---

## 5. Tại sao cần phân tập (diversity)?

**Vấn đề trong kênh fading:**  
Kênh Rician có gain |h|² ngẫu nhiên. Nếu chỉ có 1 lần phát (No HARQ) và lần đó gặp "deep fade" (|h|² thấp, SNR tức thời γ < ngưỡng), gói bị lỗi và **không có cơ hội phục hồi**.

**Phân tập thời gian qua IR-HARQ:**  
IR-HARQ khai thác **phân tập thời gian**: mỗi TX sử dụng một thực hiện kênh **độc lập** (i.i.d. trong mô hình fast-fading). Xác suất để TẤT CẢ 4 lần phát đều gặp deep fade cùng lúc rất nhỏ:

$$\Pr[\text{BLER\_final}] = \Pr[\gamma_1 < thr] \times \Pr[\gamma_2 < thr] \times \ldots$$

Cụ thể hơn: MI tích lũy $I^{(n)} = \tfrac{1}{r}\sum_{i=1}^{n}\log_2(1+\gamma_i/\Delta)$ tận dụng từng thực hiện kênh mới; ngay cả khi TX=1 gặp fading, TX=2 hay TX=3 từ kênh khác có thể bù lại.

**Tại sao kênh Rician K=15 dB cần đến 4 TX?**  
K=15 dB nghĩa là kênh có LOS mạnh → ít fading hơn Rayleigh. Nếu kênh tốt, TX=1 thường đủ. Nhưng ở SNR thấp (dưới 2 dB), ngay cả kênh LOS mạnh vẫn thất bại vì SNR trung bình chưa đủ. 4 TX cho phép tích lũy đủ MI từ nhiều kênh để "vượt ngưỡng" — đây là bản chất cộng năng lượng qua nhiều lần phát.

**Trong mô phỏng báo cáo:**  
Với i.i.d. channel (mỗi TX một thực hiện độc lập), phân tập bậc n = n TX. Đường waterfall dốc hơn mỗi TX thêm vào (bậc tự do của phân phối chi-bình phương tăng từ 2 lên 2n) — quan sát được trong Hình 4.1.

---

## 6. Tại sao chọn BLER target là 10⁻³?

**Tiêu chuẩn 3GPP:**  
BLER = 10⁻³ là mục tiêu thiết kế chuẩn của lớp HARQ trong 3GPP NR (TS 38.214). Ý nghĩa: tối đa 1 gói trong 1000 gói bị lỗi sau tất cả các lần phát HARQ.

**Tại sao 10⁻³ là đủ tốt?**  
HARQ không hoạt động đơn độc — bên trên nó có lớp RLC ARQ. Sau HARQ, các gói còn lỗi tiếp tục được sửa bởi ARQ ở lớp RLC. Tổng BLER cuối sau 2 lớp ≈ 10⁻³ × 10⁻³ = 10⁻⁶, đủ tốt cho hầu hết dịch vụ viễn thông.

**Tại sao không chọn 10⁻⁶ hay 10⁻¹?**  
- 10⁻⁶: Cần SNR quá cao, lãng phí năng lượng. HARQ ở lớp trên xử lý phần còn lại.  
- 10⁻¹: Quá nhiều gói lỗi đẩy lên lớp trên, tăng độ trễ và overhead.  
- 10⁻³: Điểm cân bằng — thực tế là **ngưỡng "waterfall knee"** của đường BLER, nơi hệ thống chuyển từ "thường thất bại" sang "thường thành công".

**Trong báo cáo:**  
Tất cả so sánh SNR threshold đều tại BLER = 10⁻³. Ví dụ: IR TX=4 đạt BLER=10⁻³ ở −7,0 dB. Nếu dùng mục tiêu 10⁻² thì threshold thấp hơn vài dB (dễ đạt hơn), nếu dùng 10⁻⁴ thì cao hơn.

---

## 7. Các thuật ngữ kỹ thuật chính cần nắm

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
| **Phân tập thời gian** | Dùng nhiều thực hiện kênh độc lập để giảm BLER; IR-HARQ = phân tập bậc n |

---

## 8. Tại sao lại có UE trong báo cáo vệ tinh?

Trong kiến trúc 5G NTN (TR 38.811), vệ tinh đóng vai trò **gNB trên quỹ đạo**. UE (điện thoại, IoT, đầu cuối vệ tinh) giao tiếp trực tiếp với vệ tinh qua giao diện NR Uu — giống hệt gNB mặt đất. 3GPP Rel-17 chuẩn hóa giao diện này bao gồm HARQ. "UE di chuyển 50 km/h" chỉ đặc tả điều kiện fading.

---

## 9. IR-HARQ hoạt động thế nào? Tại sao tốt hơn truyền đơn?

**IR-HARQ:**  
Mỗi lần phát lại gửi *bit dư thừa khác* (RV ∈ {0,2,3,1}). Bên thu tích lũy MI:
$$I^{(n)} = \frac{1}{r} \sum_{i=1}^{n} \log_2\!\left(1 + \frac{\gamma_i}{\Delta}\right)$$

**Tại sao tốt hơn No HARQ:**  
No HARQ: 1 TX, kênh xấu → gói lỗi, không phục hồi. IR-HARQ: tối đa 4 TX, MI tích lũy dần đến ngưỡng. Bất đẳng thức Jensen: tổng log lớn hơn log của tổng → IR hiệu quả hơn Chase Combining.

**Kết quả:** TX=4 đạt BLER=10⁻³ ở −7,0 dB; No HARQ cần +2,0 dB → lợi **9,0 dB**.

---

## 10. Payload tái sinh là gì?

Vệ tinh payload tái sinh giải mã tín hiệu từ mặt đất, xử lý gói, phát lại — như gNB trên quỹ đạo. RTT ngắn hơn ~2× so với bent-pipe. Báo cáo dùng: LEO 600 km = **12,88 ms**, LEO 1200 km = **24,32 ms** (TR 38.811, góc 10°).

---

## 11. Hướng dẫn đọc biểu đồ và thuyết minh bảng số liệu Chương 4

---

### Hình 4.1 — BLER vs $E_s/N_0$ (Thí nghiệm 1)

**Mô tả:** Hệ trục bán-log. Trục x: $E_s/N_0$ (−12 đến +8 dB). Trục y: BLER (log). 6 đường: No HARQ (xám chấm), IR TX=1 (xanh nhạt) đến TX=4 (xanh đậm nhất), vạch ngang đứt 10⁻³.

**Cách đọc — gióng xuống từ vạch 10⁻³:**

| Đường | Màu | Giao BLER=10⁻³ |
|-------|-----|----------------|
| No HARQ / IR TX=1 | xám / xanh nhạt | **+2,0 dB** |
| IR TX=2 | xanh vừa | **−2,5 dB** |
| IR TX=3 | xanh đậm | **−5,0 dB** |
| IR TX=4 | xanh đậm nhất | **−7,0 dB** |

**Điểm nhấn khi thuyết trình:**  
> "Nhìn vào đường đậm nhất — IR TX=4 — nó cắt vạch 10⁻³ ở −7 dB. Đường No HARQ cắt ở +2 dB. Chênh lệch 9 dB là độ lợi của IR-HARQ: cùng chất lượng dịch vụ nhưng cần ít SNR hơn 9 dB. TX=1 và No HARQ cùng điểm vì TX=1 chưa có tích lũy."

**Câu hỏi thầy hay hỏi:**  
- *"TX=1→TX=2 nhảy 4,5 dB còn TX=3→TX=4 chỉ 2 dB, tại sao?"* → TX=2 cứu gói kênh xấu nhất (lợi lớn). TX=4 chỉ cứu phần còn lại rất nhỏ → lợi ít hơn.

---

### Bảng 4.1 — Điểm làm việc BLER=10⁻³

| Sơ đồ | $E_s/N_0$ tại BLER=10⁻³ | Độ lợi vs No HARQ |
|-------|------------------------|-------------------|
| No HARQ / IR TX=1 | +2,0 dB | 0 |
| IR TX=2 | −2,5 dB | 4,5 dB |
| IR TX=3 | −5,0 dB | 7,0 dB |
| IR TX=4 | −7,0 dB | **9,0 dB** |

**Thuyết minh bảng:**  
> "Bảng này tổng hợp các điểm giao của đường BLER với vạch mục tiêu 10⁻³. Mỗi TX bổ sung dịch điểm làm việc sang trái 2–4,5 dB. Cột 'Độ lợi' đo tiết kiệm SNR so với No HARQ — TX=4 tiết kiệm 9 dB, có nghĩa là hệ thống có thể đặt thiết bị ở xa hơn hoặc dùng công suất thấp hơn mà vẫn đạt cùng chất lượng."

**Chú thích quan trọng:** TX=1 và No HARQ cùng giá trị (+2,0 dB) vì TX=1 là lần phát duy nhất, chưa có tích lũy MI — điều này xác nhận tính nhất quán của mô hình mô phỏng. Ngưỡng AWGN lý thuyết −2,3 dB; chênh lệch 4,3 dB là **lề fading Rician** ở kênh K=15 dB.

---

### Hình 4.2 — $N_{\min}$ theo SCS (Thí nghiệm 2)

**Mô tả:** Biểu đồ cột nhóm. 2 nhóm (LEO 600 km, LEO 1200 km), 4 cột/nhóm (SCS 15/30/60/120 kHz). Đường đỏ ngang = giới hạn N=32. Cột vượt = không khả thi.

**Cách đọc:**  
Nhìn cột nào nằm dưới đường đỏ → cấu hình đó hoạt động được. Số màu đen = khả thi, số màu đỏ đậm = vượt giới hạn.

**Điểm nhấn khi thuyết trình:**  
> "Chỉ 3/8 ô xanh dưới đường đỏ. Đáng chú ý: SCS 120 kHz ở LEO 600 km cần 105 tiến trình — gấp 3 lần giới hạn — dù băng thông rộng hơn. Lý do: RTT là thời gian lan truyền vật lý, không phụ thuộc SCS. SCS cao chỉ làm T_slot ngắn hơn nên cần nhiều tiến trình hơn để lấp cùng khoảng RTT."

---

### Bảng 4.2 — N_min đầy đủ

| Quỹ đạo | SCS 15 kHz | SCS 30 kHz | SCS 60 kHz | SCS 120 kHz |
|---------|-----------|-----------|-----------|------------|
| LEO 600 km | **14** ✓ | **27** ✓ | 53 ✗ | 105 ✗ |
| LEO 1200 km | **26** ✓ | 50 ✗ | 99 ✗ | 196 ✗ |

**Thuyết minh bảng:**  
> "Bảng đọc theo hàng ngang: với mỗi quỹ đạo, tìm SCS nào có N_min ≤ 32 (in đậm + dấu ✓). LEO 600 km có 2 cấu hình khả thi; LEO 1200 km chỉ có 1. Hàng LEO 1200 km: N_min tăng từ 26 lên 196 khi SCS tăng từ 15 lên 120 kHz — tỷ lệ đúng bằng 8x vì T_slot giảm 8 lần."

**Kiểm tra nhanh:** N_min(LEO 600, SCS 30) = ⌈12,88/0,5⌉ + 1 = 26 + 1 = 27. N_min(LEO 1200, SCS 15) = ⌈24,32/1,0⌉ + 1 = 25 + 1 = 26. Khớp hoàn toàn.

---

### Hình 4.3 — Năng lượng/bit vs $E_s/N_0$ (Thí nghiệm 3)  ⚠️ Đọc kỹ

**Mô tả:** Hệ trục bán-log. Trục x: −10 đến +25 dB. Trục y (log): $E_{\text{bit}}$ (J/bit). Hai đường: No HARQ (xám chấm) và IR-HARQ (xanh liền).

**BA VÙNG trong hình — đọc từ trái sang phải:**

**Vùng 1: −10 đến −8 dB (cả hai đều cao)**
- Cả No HARQ lẫn IR-HARQ đều thất bại nhiều → E_bit cao. Đây là vùng dưới ngưỡng TX=4 (−7 dB).
- IR-HARQ: tại −10 dB, E_bit ≈ **0,14 J/bit** (TX=4 chưa đủ cứu gói, BLER_final ≈ 99%)
- No HARQ: tại −10 đến −6 dB, E_bit ≈ **5×10⁵ J/bit** (clipped — 100% gói thất bại, không có bit nào được giao)
- Khoảng cách No HARQ vs IR-HARQ ở đây: ~**10⁸ lần** — MAXIMUM divergence!

**Vùng 2: −8 đến 0 dB (IR-HARQ ổn định, No HARQ đang phục hồi)**
- **"Knee" của IR-HARQ ở khoảng −8 dB**: TX=4 bắt đầu cứu được hầu hết gói → E_bit của IR-HARQ giảm nhanh từ 0,14 → 2×10⁻³ J/bit rồi gần phẳng
- No HARQ: đường "cliff" dốc xuống (waterfall BLER từ ~100% xuống ~3%) từ −6 đến 0 dB
- Tại −5 dB: No HARQ = 0,54 J/bit (BLER ≈ 99,9%), IR-HARQ = 1,1×10⁻³ J/bit → **tỷ lệ ≈ 500×**

**Vùng 3: trên 0 dB (hội tụ)**
- Cả hai hội tụ về **~5×10⁻⁴ J/bit** = P_tx × T_slot (floor). avg_ntx → 1, BLER → 0.

**Giá trị chi tiết:**

| $E_s/N_0$ | No HARQ | IR-HARQ | Tỷ lệ |
|-----------|---------|---------|-------|
| −10 dB | ~5×10⁵ J/bit (capped, 100% fail) | ~0,14 J/bit | ~3×10⁶× |
| −8 dB | ~5×10⁵ J/bit (capped) | ~2×10⁻³ J/bit | **~2,5×10⁸×** (max!) |
| −5 dB | ~0,54 J/bit | ~1,1×10⁻³ J/bit | ~500× |
| 0 dB | ~5,2×10⁻⁴ J/bit | ~5,2×10⁻⁴ J/bit | ~1× |
| +5 dB | ~5,0×10⁻⁴ J/bit | ~5,0×10⁻⁴ J/bit | ~1× |

**Điểm nhấn khi thuyết trình:**  
> "Nhìn vào hình, đường xám No HARQ bắt đầu ở trên cùng (~10⁵ J/bit), sau đó có một vách đứng đổ xuống ở khoảng −6 đến −5 dB — đây là waterfall BLER của No HARQ khi kênh bắt đầu đủ tốt cho 1 TX. Đường xanh IR-HARQ bắt đầu thấp hơn nhiều (0,14 J/bit ở −10 dB), có một 'gối' ở −8 dB rồi gần phẳng từ đó — đây là điểm TX=4 bắt đầu cứu được hầu hết gói. Khoảng cách lớn nhất giữa hai đường là ở −7 đến −8 dB: ~10⁸ lần. Khi nói 500 lần ở −5 dB, đó là điểm khá gần vùng hội tụ nên No HARQ đã phần nào phục hồi."

**Câu hỏi thầy hay hỏi:**  
- *"Tại −10 dB, IR-HARQ E_bit = 0,14 J/bit — nhưng TX=4 threshold là −7 dB, tại sao còn cao?"* → Ở −10 dB (3 dB dưới ngưỡng), TX=4 BLER ≈ 99%: gần như TẤT CẢ 4 TX đều thất bại. avg_ntx ≈ 4, BLER_final ≈ 99% → E_bit ≈ 4 × 5×10⁻⁴ / 0,01 ≈ 0,14 J/bit.  
- *"Tại sao No HARQ bỗng dưng giảm từ 5×10⁵ xuống 0,54 ở −5 dB?"* → Đây là waterfall BLER của No HARQ. Tại −6 dB: BLER ≈ 1 − 10⁻⁹ (về thực tế là 100% fail). Tại −5 dB: BLER giảm nhảy xuống 99,9% (kênh Rician K=15 dB có waterfall rất dốc). E_bit = T_slot/(1−BLER) = 5×10⁻⁴/10⁻³ = 0,5 J/bit.  
- *"avg_ntx ở +5 dB là bao nhiêu?"* → ≈ 1,00 cho cả hai — kênh tốt, TX=1 luôn thành công.

---

### Bảng 4.3 — Năng lượng tại các điểm SNR

| $E_s/N_0$ | No HARQ | IR-HARQ | Tỷ lệ |
|-----------|---------|---------|-------|
| −5 dB | ~0,54 J/bit | ~1,1×10⁻³ J/bit | **~500 lần** |
| 0 dB | ~5,2×10⁻⁴ J/bit | ~5,2×10⁻⁴ J/bit | ~1 lần |
| +5 dB | ~5,0×10⁻⁴ J/bit | ~5,0×10⁻⁴ J/bit | ~1 lần |

**Thuyết minh bảng:**  
> "Bảng tổng hợp 3 điểm SNR tiêu biểu. Hàng −5 dB là điểm quan trọng nhất: No HARQ hầu như không giao được bit nào (BLER ≈ 99,9%), mỗi bit giao thành công tốn 0,54 J do phần lớn năng lượng bị lãng phí cho gói lỗi. IR-HARQ chỉ tốn 1,1 millijoule/bit vì 4 TX đủ để giao thành công. Từ 0 dB trở lên, cả hai hội tụ — kênh đủ tốt để TX=1 luôn thành công, không cần HARQ."

---

### Bảng 4.4 — Tổng hợp kết quả

| Chỉ tiêu | No HARQ | IR-HARQ (TX=4) |
|---------|---------|----------------|
| Độ lợi SNR tại BLER=10⁻³ | 0 | **+9,0 dB** |
| $E_s/N_0$ tại BLER=10⁻³ | +2,0 dB | −7,0 dB |
| Util (N=32, SCS 30 kHz) | 100% | 100% |
| $E_{\text{bit}}$ tại −5 dB | ~0,54 J/bit | ~1,1×10⁻³ J/bit |
| Tỷ lệ cải thiện $E_{\text{bit}}$ | — | **~500 lần** |

**Thuyết minh bảng:**  
> "Đây là bảng tổng hợp 'headline numbers' của toàn bộ Chương 4. Mỗi hàng tóm tắt một kết luận chính:
> - **Hàng 1 (9,0 dB):** Độ lợi SNR — IR-HARQ giảm yêu cầu SNR đi 9 dB so với No HARQ tại cùng BLER=10⁻³.
> - **Hàng 2 (−7,0 dB vs +2,0 dB):** Điểm làm việc thực tế — IR TX=4 hoạt động ở −7 dB trong khi No HARQ cần +2 dB cho cùng chất lượng.
> - **Hàng 3 (Util = 100%):** Xác nhận không có pipeline stall — N=32 ≥ N_min=27 tại LEO 600 km SCS 30 kHz.
> - **Hàng 4–5 (500 lần):** Lợi ích năng lượng ở SNR thấp — quan trọng cho IoT vệ tinh pin."
