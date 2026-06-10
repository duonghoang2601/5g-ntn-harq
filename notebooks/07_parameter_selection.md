# 07 — Lựa chọn Tham số Mô phỏng: Căn cứ và Lý giải

> **Mục tiêu:** Mỗi tham số trong mô phỏng phải có lý do chọn rõ ràng — không phải số tùy ý. File này ghi lại toàn bộ lý giải đó.

---

## 1. Cấu hình cơ sở (Baseline) — theo IEEE paper

Tất cả tham số cơ sở được lấy từ cấu hình PDSCH trong [Tuninato 2025, Bảng 4 và Bảng 8] để đảm bảo kết quả có thể so sánh trực tiếp.

### 1.1. Tham số kênh

| Tham số | Giá trị | Lý do chọn | Nguồn |
|---|---|---|---|
| Mô hình kênh | LMS (Rician flat fading) | Kênh vệ tinh có LOS rõ — Rician phù hợp hơn Rayleigh | [Tuninato 2025, Mục IV] |
| K-factor | **15 dB** (chính), 20 dB (tham chiếu) | Đại diện điều kiện kênh suburban/rural LEO; 20 dB là near-AWGN để bound trên | [Tuninato 2025, Mục IV] |
| Tốc độ đầu cuối | **50 km/h** (chính); 0, 150, 900 km/h (sweep) | 50 km/h là thiết bị di động thông thường; 900 km/h cho phương tiện tốc độ cao | [Tuninato 2025, Mục IV] |
| Quỹ đạo cơ sở | **LEO 600 km** | Đây là LEO tiêu chuẩn 3GPP [TR 38.811, Bảng 5.3.4.1-1]; RTT đủ nhỏ để HARQ còn khả thi | [Tuninato 2025, Mục IV] |

### 1.2. Tham số HARQ và mã hóa

| Tham số | Giá trị | Lý do chọn | Nguồn |
|---|---|---|---|
| Mã hóa kênh | **LDPC** | Mã hóa tiêu chuẩn 5G NR cho PDSCH | [TS 38.212, Mục 5.3] |
| RV sequence | **{0, 2, 3, 1}** | Thứ tự chuẩn 3GPP cho IR, xác định qua $k_0$ trong circular buffer | [TS 38.212, Bảng 5.4.2.1-2] |
| Số lần phát tối đa | **4** (1 gốc + 3 phát lại) | Giới hạn chuẩn 5G NR per HARQ process | [Tuninato 2025, Mục III.A] |
| Target BLER | **$10^{-3}$** | Target dùng trong link adaptation của IEEE paper | [Tuninato 2025, Mục V.C] |

### 1.3. Tham số waveform và numerology

| Tham số | Giá trị | Lý do chọn | Nguồn |
|---|---|---|---|
| Waveform | **OFDM** (PDSCH) | Waveform tiêu chuẩn 5G NR DL | [Tuninato 2025, Mục III] |
| SCS (Subcarrier Spacing) | **15 kHz** và **30 kHz** (sweep) | Hai SCS phổ biến nhất ở FR1 (sub-6 GHz); ảnh hưởng trực tiếp đến $T_{\text{slot}}$ và $N_{\min}$ | [Tuninato 2025, Bảng 5] |
| MCS A | **QPSK, code rate 1/2** | Code rate thấp → ít room cho IR coding gain → đại diện kịch bản kênh xấu | [Tuninato 2025, Bảng 8] |
| MCS B | **256QAM, code rate 8/9** | Code rate cao → IR coding gain lớn → đại diện kịch bản kênh tốt | [Tuninato 2025, Bảng 8] |

---

## 2. Mở rộng của dự án này (Đóng góp mới)

Phần này là nơi dự án **vượt ra ngoài** IEEE paper và tạo ra giá trị nghiên cứu mới.

### 2.1. Mở rộng quỹ đạo

| Quỹ đạo | Độ cao | RTT (regenerative) | Lý do thêm vào |
|---|---|---|---|
| LEO 600 km | Cơ sở | ~12,9 ms | Baseline từ IEEE paper |
| LEO 1.200 km | 1.200 km | ~24,3 ms | Sweep RTT tăng dần |
| MEO 10.000 km | 10.000 km | ~93,5 ms | Biên giới khả năng HARQ |
| GEO 35.786 km | 35.786 km | ~270,6 ms | Trường hợp HARQ disable |

Giá trị RTT từ [TR 38.811, Bảng 5.3.4.1-1 và 5.3.2.1-1].

### 2.2. Thêm chiều năng lượng

IEEE paper không phân tích energy per bit. Dự án này thêm:

$$E_{\text{bit}} = \frac{P_{\text{phát}} \cdot \bar{n}_{\text{tx}} \cdot T_{\text{slot}}}{k}$$

Trong đó $\bar{n}_{\text{tx}}$ là số lần phát trung bình, $k$ là số information bits per TB.

*(Công thức này là định nghĩa năng lượng đơn giản — chưa có trong bộ ref/ hiện tại. Sẽ bổ sung nếu cần trích dẫn trong báo cáo.)*

### 2.3. Phân tích HARQ disable cho GEO

Dự án mô phỏng so sánh định lượng giữa:
- GEO với HARQ disable + RLC ARQ (theo hướng [TR 38.821, Mục 6.4.1])
- GEO với tăng số HARQ process (theo hướng [TR 38.821, Mục 6.4.2])

---

## 3. Tham số cố định trong mọi mô phỏng

| Tham số | Giá trị | Nguồn |
|---|---|---|
| Payload type | Regenerative | [Tuninato 2025, Mục IV.A] — phân tích Nmin dùng regenerative |
| Góc ngẩng UE | 10° (worst case) | [TR 38.811, Bảng 5.3.4.1-1] — góc ngẩng tối thiểu |
| Góc ngẩng gateway | 5° | [TR 38.811, Bảng 5.3.4.1-1] |
| Số HARQ process tối đa | 32 | [TS 38.214, Mục 5.1] — giới hạn UE capability |
| Channel estimation | Genie-aided (hoàn hảo) | [Tuninato 2025, Mục III] — loại trừ ảnh hưởng CE để đánh giá HARQ thuần |

---

## 4. Tham số sweep (biến đổi theo từng mô phỏng)

| Mô phỏng | Biến sweep | Dải giá trị |
|---|---|---|
| Sim 1: BLER vs SNR | $E_s/N_0$ | -15 dB đến 30 dB |
| Sim 2: Throughput vs RTT | RTT | 13–545 ms (theo quỹ đạo) |
| Sim 3: $N_{\min}$ | SCS, quỹ đạo | SCS ∈ {15, 30, 60, 120} kHz |
| Sim 4: GEO disable | Số phát lại RLC | 1–32 |
| Sim 5: Energy/bit | Số phát lại HARQ | 1–4 |

---

## Tóm tắt

Toàn bộ tham số cơ sở có nguồn rõ ràng từ [Tuninato 2025] và các TS/TR 3GPP. Phần mở rộng (MEO/GEO, energy/bit, HARQ disable comparison) là đóng góp mới của dự án, có căn cứ từ [TR 38.821] và [TR 38.811].

---

**File tiếp theo:** `08_module_design.md` — Thiết kế kiến trúc mô phỏng: các module và sơ đồ khối
