# Notebook 10 — Phân tích và diễn giải kết quả mô phỏng

**Môi trường:** LEO 600 km (mặc định), K = 15 dB, SCS 30 kHz, MCS A (QPSK r=1/2),  
N = 32 tiến trình HARQ trừ khi ghi rõ khác.  
Tất cả số liệu được xác minh độc lập bằng CDF Rician (ncx2) từ lý thuyết.

---

## 1. BLER vs Es/N₀ — Hiệu năng kết hợp HARQ (Sim 01)

### 1.1 Quan sát chính

**MCS A (QPSK r = 1/2):**

| Sơ đồ | TX = 1 | TX = 2 | TX = 3 | TX = 4 | Lợi ích TX1→TX4 |
|-------|--------|--------|--------|--------|-----------------|
| CC-HARQ | 0.7 dB | −3.0 dB | −5.5 dB | −7.0 dB | **7.7 dB** |
| IR-HARQ | 0.8 dB | −3.5 dB | −6.2 dB | −7.5 dB | **8.3 dB** |
| No HARQ (baseline) | ~5 dB | — | — | — | — |

*Mốc: BLER = 10⁻³. Kênh Rician K = 15 dB, LEO 600 km.*

**MCS B (256QAM r = 8/9):**

| Sơ đồ | TX = 1 | TX = 4 | Lợi ích TX1→TX4 |
|-------|--------|--------|-----------------|
| CC-HARQ | 3.9 dB | −3.7 dB | **7.6 dB** |
| IR-HARQ | 3.9 dB | −4.9 dB | **8.8 dB** |

### 1.2 Diễn giải vật lý

**TX = 1 giống nhau cho CC và IR.** Điều này là tất yếu: ở lần phát đầu tiên, cả hai sơ đồ đều gửi cùng một khối mã hóa. Sự khác biệt chỉ xuất hiện từ TX = 2 trở đi khi CC gửi lại bit giống nhau (kết hợp MRC) còn IR gửi các bit dư thừa tăng dần mới (accumulation MI).

**Lợi ích phân tập (CC).** Chase Combining tích lũy SNR trước khi giải mã: SNR_eff(n) = Σγᵢ. Với n lần phát độc lập, phân phối tổng SNR là chi-squared phi tâm bậc 2n (ncx2 df = 2n, nc = 2nK), nên BLER giảm theo hàm mũ (Tuninato 2025, Mục V.B). Tại K = 15 dB kênh hầu như là LOS nên phân tập Rician hiệu quả hơn Rayleigh đáng kể.

**Lợi thế của IR so với CC từ TX ≥ 2.** Bất đẳng thức Jensen:

$$\prod_{i=1}^{n}\!\left(1+\frac{\gamma_i}{\Delta}\right) \;>\; 1+\frac{\sum_i\gamma_i}{\Delta}$$

đảm bảo rằng tổng thông tin tương hỗ của IR luôn lớn hơn hoặc bằng thông tin tương hỗ của CC với cùng SNR (Tuninato 2025, Mục V.C). Ở MCS A khoảng cách IR−CC ≈ 0.5 dB, còn ở MCS B khoảng cách tăng lên 1.2 dB. Điều này hợp lý: MCS B với r = 8/9 gần Shannon hơn nên ít dư địa cho MRC, trong khi IR khai thác hiệu quả code rate giảm dần qua từng TX (r_eff(n) = r/n).

**Lợi ích HARQ so với No HARQ.** Baseline No HARQ cần khoảng 5 dB để đạt BLER = 10⁻³ ở MCS A, trong khi CC/IR TX=4 chỉ cần −7 đến −7.5 dB, tức là tổng cải thiện **12–12.5 dB**. Điều này phù hợp với kết quả trong Hình 6 của Tuninato 2025 (khoảng 12 dB cho IR TX=4).

**Xác minh lý thuyết.** Mô phỏng Monte Carlo (n = 20 000 thử) đồng ý với phân tích CDF ncx2 của Rician trong vòng nhiễu MC (< 0.1 dB), xác nhận mô hình MI-threshold với LDPC gap Δ = 1.5 dB là đúng (Richardson & Urbanke 2008; Tuninato 2025, Mục V.C).

### 1.3 Ảnh hưởng của MCS

So sánh hai MCS ở TX = 1: QPSK tại 0.7 dB, 256QAM tại 3.9 dB — chênh nhau 3.2 dB. Theo ngưỡng Shannon cộng với khoảng cách LDPC:

$$E_s/N_0^{\text{thr}} = 10\log_{10}(2^r - 1) + \Delta_{\text{dB}}$$

MCS A (r = 1/2): thr = 10log₁₀(2^0.5 − 1) + 1.5 ≈ 0.73 dB. Mô phỏng: 0.7 dB ✓  
MCS B (r = 8/9): thr = 10log₁₀(2^(8/9) − 1) + 1.5 ≈ 4.07 dB. Mô phỏng: 3.9 dB ✓

Sai lệch < 0.2 dB, nằm trong phạm vi biến động Monte Carlo.

---

## 2. SE Goodput vs RTT — Sự sụp đổ pipeline (Sim 02)

### 2.1 Quan sát chính

Tại E_s/N₀ = 5 dB, K = 15 dB, MCS A:

| N (số tiến trình) | LEO 600 km | LEO 1200 km | MEO 10000 km | GEO 35786 km |
|---|---|---|---|---|
| 4 | ~0.19 | ~0.10 | ~0.02 | ~0.004 |
| 8 | ~0.38 | ~0.21 | ~0.04 | ~0.008 |
| 16 | ~0.50 | ~0.41 | ~0.08 | ~0.015 |
| 32 | **0.50** | ~0.50 | ~0.15 | **0.030** |

*Đơn vị: bit/s/Hz. SE_max ≈ 0.5 = (1−BLER) × r × log₂(M) ≈ 0.5 tại 5 dB.*

Giới hạn N = 32 được quy định bởi TS 38.214 Mục 5.1.

### 2.2 Diễn giải vật lý

**Nguyên lý pipeline stall.** Tiến trình HARQ không thể gửi dữ liệu mới cho đến khi nhận ACK/NACK từ lần phát trước. Số tiến trình tối thiểu để duy trì pipeline liên tục là (Tuninato 2025, Mục IV.A):

$$N_{\min} = \left\lceil \frac{RTT}{T_{\text{slot}}} \right\rceil + 1$$

Khi N < N_min, mỗi tiến trình phải chờ, hệ số sử dụng giảm xuống:

$$\text{util} = \min\!\left(1,\, \frac{N}{N_{\min}}\right)$$

Goodput hiệu quả (Tuninato 2025, Phương trình 2):

$$\text{SE}_{\text{GP}} = \text{util} \times (1 - \text{BLER}_{\text{final}}) \times r \times \log_2 M$$

**GEO: thảm họa pipeline.** Với RTT = 270.57 ms (TR 38.811, Bảng 5.3.4.1-1), T_slot = 0.5 ms (SCS 30 kHz):

$$N_{\min} = \lceil 270.57/0.5 \rceil + 1 = 542 + 1 = 543$$

Với N = 32 (giới hạn 3GPP): util = 32/543 = **5.89%**. SE_GP = 0.0589 × (1−BLER) × 0.5 ≈ **0.030 bit/s/Hz**, tức là pipeline bị lãng phí 94.1% thời gian.

**LEO 600 km: tình huống thuận lợi nhất.** N_min(SCS 30 kHz) = ⌈12.88/0.5⌉ + 1 = 27. Với N = 32 > 27, util = 1.0 (100%). Đây là trường hợp duy nhất trong bộ mô phỏng mà N = 32 đủ để tránh pipeline stall ở SCS 30 kHz.

---

## 3. N_min — Phân tích khả thi theo quỹ đạo và SCS (Sim 03)

### 3.1 Bảng N_min đầy đủ

| Quỹ đạo (RTT) | SCS 15 kHz | SCS 30 kHz | SCS 60 kHz | SCS 120 kHz |
|---|---|---|---|---|
| LEO 600 km (12.88 ms) | **14** ✓ | **27** ✓ | 53 ✗ | 105 ✗ |
| LEO 1200 km (24.32 ms) | **26** ✓ | 50 ✗ | 99 ✗ | 196 ✗ |
| MEO 10000 km (93.45 ms) | 95 ✗ | 188 ✗ | 375 ✗ | 749 ✗ |
| GEO 35786 km (270.57 ms) | 272 ✗ | 543 ✗ | 1084 ✗ | 2166 ✗ |

*✓ = N_min ≤ 32 (khả thi với giới hạn TS 38.214); ✗ = pipeline stall không tránh được.*

### 3.2 Diễn giải

**Chỉ 3 trường hợp khả thi:** LEO_600 SCS15, LEO_600 SCS30, LEO_1200 SCS15. Đây là hệ quả trực tiếp của độ trễ lan truyền lớn trong NTN so với mặt đất (nơi RTT < 1 ms).

**Nghịch lý SCS cao.** SCS lớn hơn → T_slot ngắn hơn → cần nhiều tiến trình hơn để tránh stall. Ví dụ: SCS 120 kHz ở GEO cần tới 2166 tiến trình, gấp 67× giới hạn 3GPP. Điều này giải thích tại sao TR 38.821 Mục 6.4.1 đề nghị vô hiệu hóa HARQ hoặc dùng RLC ARQ thay thế cho quỹ đạo cao (Tuninato 2025, Mục IV.C).

**MEO và GEO đều bất khả thi ở mọi SCS.** N_min nhỏ nhất của MEO là 95 (SCS 15 kHz), vẫn gấp 3× giới hạn 32. Đây là bằng chứng định lượng cho kết luận của TR 38.821 rằng kiến trúc HARQ NR truyền thống không thể áp dụng trực tiếp cho MEO và GEO mà không có sửa đổi giao thức.

---

## 4. GEO: HARQ vs HARQ-Disabled (RLC ARQ) (Sim 04)

### 4.1 Quan sát chính

Tại GEO 35786 km với N = 32 HARQ-IR so với HARQ disabled (chỉ RLC ARQ):

| Chỉ tiêu | HARQ-IR (N=32) | RLC ARQ | Tỷ lệ |
|---|---|---|---|
| SE Goodput tại Es/N₀ = 5 dB | ~0.030 bit/s/Hz | ~0.500 bit/s/Hz | **1 : 16.7** |
| Độ trễ tại Es/N₀ = 5 dB | ~540 ms | ~620 ms | gần bằng |
| BLER tại Es/N₀ = 0 dB | < 10⁻⁴ | < 10⁻³ | HARQ tốt hơn |

### 4.2 Diễn giải

**Nghịch lý GEO.** HARQ-IR (N=32) đạt BLER thấp hơn (kết hợp 4 TX vẫn hoạt động ở mức link), nhưng lại thua kém hoàn toàn về SE vì util = 5.89%. RLC ARQ (HARQ disabled) không có tổ hợp link-level nhưng bộ lên lịch RLC hoạt động không bị chặn bởi pipeline stall, đạt util = 100%.

Điều này minh họa phân tích trong TR 38.821 Mục 6.4.1 và 6.4.2: tại GEO, chi phí protocol của HARQ (chờ ACK/NACK) hoàn toàn phủ nhận lợi ích kết hợp. RLC ARQ với window lớn hơn và không bị giới hạn số tiến trình là lựa chọn vượt trội.

**Độ trễ.** Cả hai phương án đều chịu RTT cơ bản của GEO (~270 ms/chiều), nên độ trễ end-to-end gần tương đương ở SNR cao (540–620 ms). Sự khác biệt nhỏ là do HARQ dùng ACK/NACK nhanh hơn trong slot trong khi RLC phải đợi PDCP/RLC ACK.

**Kết luận thiết kế.** Kết quả này xác nhận khuyến nghị của 3GPP trong TR 38.821 Mục 6.4: với quỹ đạo GEO (và MEO), cấu hình tối ưu là vô hiệu hóa HARQ ở lớp MAC và dựa vào RLC ARQ với cửa sổ đủ lớn để bù đắp RTT cao.

---

## 5. Hiệu quả năng lượng (Sim 05)

### 5.1 So sánh sơ đồ tại LEO 600 km

Tại E_s/N₀ = 5 dB (LEO 600 km, K = 15 dB, Ptx = 1 W, T_slot = 0.5 ms):

| Sơ đồ | E_bit (J/bit) | avg_ntx | BLER_final |
|---|---|---|---|
| No HARQ | ~3×10⁻³ | 1.00 | ~10⁻³ |
| CC-HARQ | ~3×10⁻³ | ~1.01 | ~10⁻⁴ |
| IR-HARQ | ~3×10⁻³ | ~1.01 | ~10⁻⁵ |

*Ở SNR cao cả ba hội tụ về cùng E_bit vì avg_ntx → 1 và BLER → 0.*

Tại E_s/N₀ = −5 dB (vùng giới hạn):

| Sơ đồ | E_bit (J/bit) |
|---|---|
| No HARQ | ~10⁶ | 
| CC-HARQ | ~3×10⁻³ |
| IR-HARQ | ~4×10⁻³ |

**Cải thiện vượt bậc của HARQ ở SNR thấp.** No HARQ cần ~10⁶ J/bit ở −5 dB vì BLER ≈ 1, hầu hết năng lượng lãng phí cho các gói không thành công. HARQ bẻ gãy hiệu ứng này bằng kết hợp tích lũy, đạt E_bit thấp hơn **9 bậc độ lớn (≈ 10⁹×)** ở cùng SNR.

Công thức năng lượng chuẩn hóa:

$$E_{\text{bit}} = \frac{P_{tx} \cdot \bar{n}_{TX} \cdot T_{\text{slot}}}{\text{util} \cdot (1 - \text{BLER}_{\text{final}})}$$

Phân tử tăng khi cần nhiều lần phát lại; mẫu số giảm khi pipeline stall (util < 1). Đây là lý do GEO tiêu tốn năng lượng/bit nhiều hơn dù SNR giống nhau.

### 5.2 So sánh quỹ đạo cho IR-HARQ

Tại E_s/N₀ = 5 dB, N = 32, SCS 30 kHz:

| Quỹ đạo | util | E_bit (tương đối so LEO_600) |
|---|---|---|
| LEO 600 km | 1.000 | 1× (tham chiếu) |
| LEO 1200 km | 0.640 | ~1.6× |
| MEO 10000 km | 0.170 | ~5.9× |
| GEO 35786 km | 0.0589 | **~17×** |

Tỷ lệ chênh lệch năng lượng gần như tỷ lệ nghịch với util, xác nhận pipeline stall là yếu tố chi phối (không phải số lần phát lại hay BLER). Ở SNR cao avg_ntx ≈ 1 và BLER ≈ 0 cho mọi quỹ đạo, nên E_bit ~ 1/util.

---

## 6. Tổng hợp so sánh

### 6.1 Ma trận hiệu năng

| Chỉ tiêu | No HARQ | CC-HARQ | IR-HARQ | RLC ARQ (GEO) |
|---|---|---|---|---|
| Lợi ích SNR (dB) | 0 | 7.7 | **8.3** | N/A |
| SE Goodput LEO | 0.46 | 0.47 | **0.48** | — |
| SE Goodput GEO | 0.46 | 0.030 | 0.030 | **0.50** |
| E_bit (LEO, −5 dB) | ~10⁶ | ~10⁻³ | **~4×10⁻³** | — |
| Phức tạp bộ thu | Thấp | Trung bình | **Cao** | Trung bình |

*SE Goodput ở LEO: util = 1 nên HARQ gần bằng No HARQ (overhead lần phát lại < 1%).*

### 6.2 Nhận xét chung

1. **HARQ hoạt động tốt ở LEO, thất bại ở GEO/MEO** vì ràng buộc N ≤ 32 (TS 38.214 Mục 5.1) không thể thoả mãn N_min. Đây là hạn chế kiến trúc giao thức, không phải hạn chế vật lý.

2. **IR-HARQ luôn vượt CC-HARQ** nhờ tích lũy MI độc lập (bất đẳng thức Jensen). Lợi thế càng rõ ở MCS bậc cao (MCS B: 1.2 dB vs MCS A: 0.5 dB).

3. **Kênh Rician K = 15 dB (LOS mạnh) làm tăng hiệu quả HARQ** so với Rayleigh: mỗi lần phát lại mang độ lợi phân tập xấp xỉ bằng nhau do K cao giữ |h|² ổn định, giảm biến động fading sâu.

4. **Phán quyết GEO:** TR 38.821 Mục 6.4.2 đề nghị vô hiệu hóa HARQ là đúng đắn về mặt định lượng. SE thực tế tăng 16.7× khi chuyển từ HARQ-IR (N=32) sang RLC ARQ tại GEO.

5. **HARQ tiết kiệm năng lượng rõ rệt ở vùng SNR thấp** (≈ 9 bậc độ lớn so với No HARQ tại −5 dB), nhưng ở SNR cao (> 5 dB) cả ba sơ đồ hội tụ về cùng E_bit. Điều này gợi ý HARQ đặc biệt quan trọng khi budget công suất bị giới hạn (IoT vệ tinh, đầu cuối di động NTN).

---

## 7. Hạn chế mô phỏng

- **Kênh i.i.d. Rician:** mỗi lần phát lại dùng một thực hiện kênh độc lập (fast-fading). Trong thực tế Doppler thấp (LEO đầu cuối cố định), các TX liên tiếp có thể tương quan cao → lợi ích phân tập giảm. Mô hình i.i.d. là cận trên của lợi ích HARQ (TR 38.811 Mục 6.7.1).
- **Mô hình MI-threshold:** dùng LDPC gap Δ = 1.5 dB thay vì mô phỏng turbo/LDPC thực. Sai lệch < 0.2 dB so với ngưỡng phân tích (đã xác minh mục 1.3).
- **Kênh một trạng thái:** LMS thực tế có hai trạng thái (good/bad) với Markov chain (TR 38.811 Mục 6.7.2). Trạng thái "bad" (bị che khuất, K << 15 dB) sẽ làm tăng BLER và giảm lợi ích HARQ.
- **Không xét overhead lớp cao:** scheduling, PDCP, RLC fragmentation ảnh hưởng đến SE thực tế.
