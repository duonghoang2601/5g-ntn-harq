# Ngân hàng câu hỏi bảo vệ báo cáo

> Tổng hợp câu hỏi hay gặp khi bảo vệ báo cáo "Đánh giá hiệu quả cơ chế HARQ trong mạng 5G NTN".  
> Mỗi mục gồm câu hỏi ngắn → câu trả lời cốt lõi → ví dụ/số liệu từ báo cáo để chứng minh.

---

## 1. Mô phỏng Monte Carlo là gì? Tại sao dùng cho HARQ?

**Câu trả lời cốt lõi:**  
Phương pháp Monte Carlo tạo ra hàng chục nghìn thử nghiệm ngẫu nhiên (ở đây: 20 000 gói dữ liệu), mỗi thử nghiệm rút một thực hiện kênh mới, sau đó tính xác suất sự kiện (ví dụ: gói bị lỗi) bằng tần suất quan sát được.

**Tại sao dùng cho HARQ:**  
BLER của HARQ sau nhiều lần phát không có công thức đóng đơn giản — nó phụ thuộc vào phân phối kết hợp của nhiều biến ngẫu nhiên kênh Rician. Monte Carlo không cần biểu thức giải tích: chỉ cần mô phỏng đủ nhiều thử nghiệm thì xác suất thực nghiệm hội tụ về xác suất thực (luật số lớn). Với 20 000 thử nghiệm, sai số thống kê ở BLER = 10⁻³ là ±5 % (khoảng tin cậy 95 %).

**Xác minh độc lập:** Báo cáo so sánh BLER TX=1 thu được từ Monte Carlo với công thức giải tích CDF Rician (scipy.stats.ncx2), sai lệch < 0,1 dB — xác nhận mô phỏng đúng.

---

## 2. Mô hình ngưỡng thông tin tương hỗ (MI-threshold) là gì? Tại sao dùng nó?

**Định nghĩa:**  
Thay vì mô phỏng bộ giải mã LDPC thực (quá chậm), ta dùng quy tắc: gói được giải mã thành công khi tổng thông tin tương hỗ (MI) tích lũy vượt ngưỡng 1,0 bit/channel use (tương đương: năng lượng thông tin đủ để giải mã). Ngưỡng SNR tương ứng của kênh AWGN được tính qua:

$$\text{SNR}_{thr} = \Delta \cdot (2^r - 1)$$

với $\Delta = 1{,}5$ dB là khoảng cách thực thi LDPC (LDPC implementation gap), $r$ là tốc độ mã.

**Tại sao dùng:**  
- Nhanh hơn giải mã LDPC thực hàng nghìn lần.  
- Đã được kiểm chứng trong tài liệu (Richardson & Urbanke 2008; Tuninato 2025): sai lệch so với thực tế < 0,2 dB ở BLER = 10⁻³.  
- Cho phép so sánh CC và IR trong cùng một khung: MI của CC = log₂(1 + Σγᵢ/Δ), MI của IR = Σlog₂(1 + γᵢ/Δ).

---

## 3. Pipeline stall là gì? Tại sao xuất hiện ở MEO và GEO?

**Pipeline stall:**  
Trong 5G NR, bên phát dùng N tiến trình HARQ song song để lấp đầy khoảng chờ ACK/NACK. Nếu N không đủ lớn để lấp toàn bộ khoảng RTT, bên phát phải ngồi chờ (idle) — gọi là pipeline stall. Số tiến trình tối thiểu tránh stall:

$$N_{\min} = \left\lceil \frac{RTT}{T_{slot}} \right\rceil + 1$$

**Tại sao MEO/GEO bị stall:**  
RTT tỷ lệ thuận với khoảng cách quỹ đạo. Với SCS 30 kHz ($T_{slot}$ = 0,5 ms):

| Quỹ đạo | RTT | $N_{\min}$ | Giới hạn TS 38.214 | Kết quả |
|---------|-----|-----------|-------------------|---------|
| LEO 600 km | 12,9 ms | 27 | 32 | Khả thi ✓ |
| LEO 1200 km | 24,3 ms | 50 | 32 | Stall ✗ |
| MEO 10 000 km | 93,5 ms | 188 | 32 | Stall nặng ✗ |
| GEO 35 786 km | 270,6 ms | 543 | 32 | Stall 94 % ✗ |

Tại GEO với N = 32, hệ số sử dụng chỉ đạt util = 32/543 = **5,89 %** — nghĩa là 94,11 % thời gian bên phát ngồi không.

---

## 4. Goodput là gì? Dùng để đánh giá cái gì?

**Goodput (hay Throughput hiệu dụng)** là lượng dữ liệu *hữu ích* (gói được nhận đúng) truyền được trên một đơn vị thời gian và băng thông. Khác với throughput thô (đếm cả gói lỗi bị phát lại), goodput chỉ đếm dữ liệu thực sự đến đúng đích.

Trong báo cáo, SE Goodput (Spectral Efficiency Goodput) được định nghĩa:

$$SE_{GP} = \text{util} \times (1 - BLER_{final}) \times r \times \log_2 M \quad \text{[bit/s/Hz]}$$

- **util** = N/N_min: tỷ lệ thời gian bên phát thực sự phát (không stall)  
- **(1 − BLER_final)**: xác suất gói được nhận đúng sau tối đa 4 TX  
- **r · log₂M**: tốc độ bit danh nghĩa của MCS

**Ý nghĩa:** SE Goodput cho thấy tác động *kép* của pipeline stall — không chỉ là lãng phí thời gian mà còn trực tiếp làm giảm băng thông khả dụng theo tỷ lệ util.

---

## 5. Các thuật ngữ kỹ thuật chính cần nắm

| Thuật ngữ | Định nghĩa |
|-----------|-----------|
| **HARQ** | Hybrid ARQ: kết hợp FEC (sửa lỗi xuôi) + ARQ (phát lại có xác nhận) |
| **CC-HARQ** | Chase Combining: mỗi lần phát lại gửi lại *cùng* khối bit, thu gộp bằng MRC |
| **IR-HARQ** | Incremental Redundancy: mỗi lần phát lại gửi *bit dư thừa mới* (RV khác nhau) |
| **BLER** | Block Error Rate: tỷ lệ gói bị lỗi sau giải mã |
| **RTT** | Round-Trip Time: thời gian từ khi phát đến khi nhận được ACK/NACK |
| **NTN** | Non-Terrestrial Network: mạng không mặt đất (vệ tinh, UAV) |
| **LEO/MEO/GEO** | Quỹ đạo thấp (~600 km) / trung (~10 000 km) / cao (~36 000 km) |
| **SCS** | Subcarrier Spacing: khoảng cách sóng mang con trong OFDM (15/30/60/120 kHz) |
| **MCS** | Modulation and Coding Scheme: bộ điều chế + tốc độ mã (ví dụ: QPSK r=1/2) |
| **Rician K** | Tỷ số công suất LOS / tán xạ; K=15 dB = kênh LOS rất mạnh |
| **Pipeline stall** | Trạng thái bên phát phải chờ vì không đủ tiến trình HARQ để lấp RTT |
| **util** | Hệ số sử dụng đường truyền: util = min(1, N/N_min) |
| **SE Goodput** | Hiệu suất phổ thực tế tính đến cả stall và lỗi: util × (1−BLER) × r × log₂M |
| **RLC ARQ** | ARQ ở lớp RLC (lớp trên): không có soft combining, nhưng util = 100 % |
| **MI** | Mutual Information (thông tin tương hỗ): đo lượng thông tin kênh có thể mang |
| **LDPC gap Δ** | Khoảng cách giữa ngưỡng Shannon và ngưỡng giải mã LDPC thực tế (~1,5 dB) |

---

## 6. Tại sao lại có UE (User Equipment) trong báo cáo vệ tinh?

Trong kiến trúc 5G NTN (TR 38.811), vệ tinh đóng vai trò **trạm thu phát di động (gNB) trên quỹ đạo** hoặc là relay. UE (thiết bị người dùng) — điện thoại, thiết bị IoT, thiết bị đầu cuối vệ tinh — giao tiếp trực tiếp với vệ tinh qua giao diện vô tuyến NR Uu, giống hệt cách giao tiếp với gNB mặt đất.

3GPP Rel-17 chuẩn hóa chính xác giao diện này, bao gồm cả HARQ. Do đó, "UE tĩnh" hay "UE di chuyển 50 km/h" trong báo cáo chỉ đặc tả điều kiện fading của đầu cuối — hoàn toàn phù hợp với ngữ cảnh vệ tinh.

---

## 7. Chase Combining và Incremental Redundancy khác nhau thế nào?

**Chase Combining (CC):**  
Bên phát gửi lại *y hệt* gói ban đầu (RV = 0). Bên thu cộng tín hiệu nhận được theo MRC — tương đương cộng SNR:
$$\gamma_{eff}^{(n)} = \sum_{i=1}^{n} \gamma_i$$

**Incremental Redundancy (IR):**  
Mỗi lần phát lại gửi một phần *bit dư thừa khác* (RV ∈ {0,2,3,1} — lấy từ các vùng khác nhau của circular buffer LDPC). Bên thu tích lũy thông tin tương hỗ:
$$I^{(n)} = \frac{1}{r} \sum_{i=1}^{n} \log_2\!\left(1 + \frac{\gamma_i}{\Delta}\right)$$

**Tại sao IR luôn tốt hơn CC từ TX ≥ 2:**  
Bất đẳng thức Jensen: với hàm lõm log₂, tổng log lớn hơn log của tổng:
$$\sum_i \log_2(1+\gamma_i/\Delta) \;\geq\; \log_2\!\left(1 + \sum_i \gamma_i/\Delta\right)$$
Do đó MI của IR ≥ MI của CC, dấu bằng chỉ khi TX = 1 hoặc tất cả γᵢ bằng nhau.

**Kết quả từ mô phỏng:** IR vượt CC 0,5 dB ở MCS A (QPSK r=1/2) và 1,2 dB ở MCS B (256QAM r=8/9). Khoảng cách tăng theo MCS vì tốc độ mã cao hơn làm lợi thế tích lũy MI của IR rõ rệt hơn.

---

## 8. Payload tái sinh (regenerative payload) là gì?

**Định nghĩa:** Vệ tinh có payload tái sinh (*regenerative*) giải mã toàn bộ tín hiệu nhận được từ mặt đất, xử lý gói IP/NR, rồi phát lại tín hiệu mới xuống mặt đất — giống như một gNB đặt trên quỹ đạo. Đối lập với payload trong suốt (*bent-pipe*) chỉ khuếch đại và chuyển tần tín hiệu.

**Ảnh hưởng đến RTT:**  
- **Payload trong suốt:** RTT = 2 × (truyền lan lên) + 2 × (truyền lan xuống) + trễ xử lý mặt đất.  
- **Payload tái sinh:** RTT = (truyền lan lên + xuống) + trễ xử lý trên vệ tinh — **nhỏ hơn khoảng 2×** vì vệ tinh phản hồi ACK ngay mà không cần đợi tín hiệu xuống tới trạm mặt đất.

Báo cáo sử dụng RTT của payload tái sinh (TR 38.811 Bảng 5.3.4.1-1) vì đây là cấu hình 3GPP Rel-17 khuyến nghị cho 5G NTN. RTT GEO ở góc ngẩng 10°: **270,57 ms** (so với ~540 ms nếu dùng bent-pipe).

---

## 9. Hướng dẫn đọc và thuyết trình các biểu đồ Chương 4

### Hình 4.1 & 4.2 — BLER vs $E_s/N_0$ (Thí nghiệm 1)

**Cách đọc:**  
- Trục x: SNR (dB) — càng phải càng tốt.  
- Trục y: BLER (thang log) — mục tiêu thiết kế là BLER = 10⁻³ (đường ngang đứt xám).  
- Mỗi đường là một số lần phát TX = 1..4; màu đậm hơn = nhiều TX hơn.  
- Nhìn xem mỗi TX dịch đường sang trái bao nhiêu dB so với TX trước.

**Điểm nhấn khi thuyết trình:**  
> "Nhìn vào TX=4 của IR-HARQ (đường xanh đậm nhất), nó đạt BLER = 10⁻³ ở −7,5 dB. Trong khi đó No HARQ cần +5 dB để đạt cùng BLER. Hiệu chênh 12,5 dB — đó là độ lợi HARQ. IR tốt hơn CC 0,5 dB tại cùng điểm làm việc vì tích lũy thông tin tương hỗ hiệu quả hơn (bất đẳng thức Jensen)."

---

### Hình 4.3 — SE Goodput vs RTT (Thí nghiệm 2)

**Cách đọc:**  
- Trục x: RTT (ms); các đường thẳng đứng xám là RTT của từng quỹ đạo.  
- Trục y: SE Goodput (bit/s/Hz); tối đa ~0,5 = giới hạn lý thuyết QPSK r=1/2.  
- 4 đường màu = 4 cấu hình N (số tiến trình HARQ).  
- Đường nào sụp đổ sớm hơn (sang trái hơn) = N nhỏ hơn → stall sớm hơn.

**Điểm nhấn khi thuyết trình:**  
> "Tại RTT = 13 ms (LEO 600 km, đường xám trái cùng), N = 32 vẫn đạt SE = 0,5 — không stall. Nhưng khi RTT tăng sang GEO (270 ms), cả 4 đường đều gần bằng 0. Đây là 'thảm họa pipeline': dù kênh tốt, bên phát cứ phải ngồi chờ."

---

### Hình 4.4 — N_min theo quỹ đạo và SCS (Thí nghiệm 3)

**Cách đọc:**  
- Biểu đồ cột nhóm; mỗi nhóm là một quỹ đạo; màu sắc = SCS.  
- Đường đỏ ngang = giới hạn N = 32 (TS 38.214).  
- Cột nào vượt đường đỏ → không khả thi; số màu đỏ đậm hiển thị giá trị.

**Điểm nhấn khi thuyết trình:**  
> "Chỉ 3 cột nằm dưới đường đỏ: LEO 600 SCS 15/30 kHz và LEO 1200 SCS 15 kHz. Toàn bộ MEO và GEO đều vượt giới hạn. Nghịch lý: SCS cao hơn (cột phải hơn trong mỗi nhóm) lại làm N_min tăng vì T_slot ngắn hơn."

---

### Hình 4.5 — GEO: HARQ vs RLC ARQ (Thí nghiệm 4)

**Cách đọc:**  
- 3 bảng con: (a) BLER, (b) SE Goodput, (c) Độ trễ.  
- Xanh = HARQ-IR N=32; Xanh lá đứt = RLC ARQ (HARQ disabled).

**Điểm nhấn khi thuyết trình:**  
> "(a) BLER: HARQ-IR đạt BLER cực thấp (< 10⁻⁸ trên toàn dải SNR) vì 4 TX kết hợp. RLC ARQ có BLER cao hơn (chỉ 1 TX). Nhưng nhìn sang (b) SE Goodput: HARQ-IR chỉ đạt 0,03 bit/s/Hz (flat), còn RLC ARQ đạt 0,5 bit/s/Hz — tức 16,7 lần hơn. BLER thấp của HARQ hoàn toàn bị xóa bởi util = 5,89 %. (c) Độ trễ: hai phương án xấp xỉ nhau ở SNR cao (~500 ms) vì cùng chịu RTT vệ tinh."

---

### Hình 4.6 — Năng lượng/bit vs SNR (Thí nghiệm 5)

**Cách đọc:**  
- Trục y log: năng lượng/bit (J/bit); thấp hơn = hiệu quả hơn.  
- Tại SNR thấp (−5 dB): No HARQ cần ~10⁶ J/bit vì BLER ≈ 1, hầu hết năng lượng bị lãng phí.  
- Tại SNR cao: cả 3 đường hội tụ về ~5×10⁻⁴ J/bit vì avg_ntx → 1.

**Điểm nhấn khi thuyết trình:**  
> "Tại −5 dB, khoảng cách No HARQ và HARQ là 10 decade trên trục log — tức HARQ dùng ít năng lượng hơn 10⁹ lần để phát thành công một bit. Với thiết bị IoT vệ tinh dùng pin, đây là lợi thế cực kỳ lớn ở vùng coverage edge khi SNR thấp."
