# 05 — Bản đồ Tiêu chuẩn 3GPP: Điều khoản nào dùng trong dự án này?

> **Mục tiêu:** Hiểu vai trò của từng tài liệu 3GPP trong bộ ref/ và chỉ ra chính xác điều khoản nào được sử dụng cho từng thành phần của dự án.

---

## 1. Tổng quan bộ tài liệu 3GPP liên quan

| Tài liệu | Loại | Nội dung chính |
|---|---|---|
| TR 38.811 | Technical Report | Mô hình kênh NTN, kịch bản triển khai, propagation delay |
| TR 38.821 | Technical Report | Giải pháp NTN, HARQ optimization, HARQ disable |
| TS 38.212 | Technical Spec | Mã hóa kênh LDPC, rate matching, RV, circular buffer |
| TS 38.213 | Technical Spec | Thủ tục vật lý lớp điều khiển, HARQ-ACK timing |
| TS 38.214 | Technical Spec | Thủ tục vật lý lớp dữ liệu, HARQ process count, MCS |

TR = Technical Report (nghiên cứu, không bắt buộc thực hiện). TS = Technical Specification (bắt buộc thực hiện trong sản phẩm).

---

## 2. TR 38.811 — Mô hình kênh NTN (Release 15)

**Vai trò:** Định nghĩa mô hình kênh và kịch bản triển khai NTN làm nền tảng cho mọi mô phỏng.

### Điều khoản dùng trong dự án:

| Mục | Nội dung | Dùng ở đâu |
|---|---|---|
| Mục 5.2 + Bảng 5.2-1 | Kịch bản D1–D5 (quỹ đạo, tần số, beam) | Chọn kịch bản mô phỏng |
| Mục 5.3.1.1 | Định nghĩa propagation delay one-way | Tính RTT |
| Bảng 5.3.2.1-1 | Propagation delay GEO 35.786 km | RTT cho GEO |
| Bảng 5.3.4.1-1 | Propagation delay LEO 600/1.500 km, MEO 10.000 km | RTT cho LEO/MEO |
| Bảng 5.3.5-1 | Tóm tắt max one-way delay theo kịch bản | Tham chiếu |
| Eq. 6.6-1 | Công thức tổng suy hao đường truyền | Mô hình kênh |
| Mục 6.6.1, Bảng 6.6.1-1 | Xác suất LOS theo góc ngẩng và môi trường | LMS model |
| Mục 6.7.1 | Flat fading — mô hình hai trạng thái ITU (LMS) với phân phối Loo | Channel model |
| Mục 6.7.2 | Frequency selective fading, K-factor theo bảng | K-factor reference |
| Bảng 6.9.2-3, 6.9.2-4 | NTN-TDL-C/D với $K_1 = 10.224$ dB / $11.707$ dB | TDL model |

### Phiên bản sử dụng: TR 38.811 V15.4.0 (2020-09)

---

## 3. TR 38.821 — Giải pháp NTN (Release 16)

**Vai trò:** Ghi lại kết quả nghiên cứu và các giải pháp 3GPP đề xuất cho các vấn đề NTN — đặc biệt là HARQ.

### Điều khoản dùng trong dự án:

| Mục | Nội dung | Dùng ở đâu |
|---|---|---|
| Mục 6.4.1 | Disabling of HARQ in NR NTN — thảo luận tắt HARQ feedback | Sim 4: GEO disable |
| Mục 6.4.2 | HARQ Optimization — tăng số process vs tắt HARQ | Sim 3 + Sim 4 |
| Mục 7.2.1.4 | Kết luận RAN2 về HARQ: cấu hình per-UE, per-process | Thiết kế process manager |
| Mục 7.2.2 | RLC ARQ — status reporting, sequence numbers | Hiểu RLC ARQ |

### Phiên bản sử dụng: TR 38.821 V16.2.0 (2023-03)

---

## 4. TS 38.212 — Mã hóa kênh và Rate Matching (Release 17)

**Vai trò:** Định nghĩa chính xác cách LDPC encoder tạo ra codeword, cách circular buffer hoạt động, và cách RV xác định tập bit gửi đi.

### Điều khoản dùng trong dự án:

| Mục / Bảng | Nội dung | Dùng ở đâu |
|---|---|---|
| Mục 5.4.2.1 | Rate matching cho LDPC — thuật toán bit selection từ circular buffer | Hiện thực HARQ encoder |
| Bảng 5.4.2.1-2 | Vị trí bắt đầu $k_0$ cho từng RV (rv_id) và LDPC base graph | Xác định tập bit mỗi lần phát |

Bảng 5.4.2.1-2 xác định $k_0$ theo rv_id ∈ {0, 1, 2, 3} tương ứng với thứ tự truyền {RV0, RV2, RV3, RV1} — đây là nền tảng của IR trong 5G NR.

### Phiên bản: TS 38.212 V17 (file ref: 38212-hd0.docx)

---

## 5. TS 38.213 — Thủ tục lớp vật lý: Điều khiển (Release 17)

**Vai trò:** Định nghĩa thủ tục UE để báo cáo HARQ-ACK — timing, kênh PUCCH, định dạng.

### Điều khoản liên quan:

| Mục | Nội dung |
|---|---|
| Mục 9.2.3 | UE procedure for reporting HARQ-ACK — timing K1 từ PDSCH đến PUCCH |

Trong mô phỏng link-level của dự án, timing feedback HARQ được đơn giản hóa thành RTT tổng thể — TS 38.213 được tham chiếu để hiểu cấu trúc thực tế nhưng không implement chi tiết.

### Phiên bản: TS 38.213 V17 (file ref: 38213-hd0.docx)

---

## 6. TS 38.214 — Thủ tục lớp vật lý: Dữ liệu (Release 17)

**Vai trò:** Định nghĩa thủ tục UE để nhận PDSCH, số HARQ process, MCS và bảng code rate.

### Điều khoản dùng trong dự án:

| Mục / Bảng | Nội dung | Dùng ở đâu |
|---|---|---|
| Mục 5.1 | Số HARQ process tối đa: 16 (mặc định) hoặc 32 (UE capability) | Giới hạn Sim 3 |
| Bảng 5.1.3.1-1 | MCS index table — mapping từ MCS index sang modulation order và code rate | Chọn MCS A và B |

Theo [TS 38.214, Mục 5.1]: *"For downlink, a maximum of 16 HARQ processes per cell are supported by the UE, or subject to UE capability, a maximum of 32 HARQ processes."*

### Phiên bản: TS 38.214 V17 (file ref: 38214-hg0.docx)

---

## 7. Tài liệu bổ sung trong ref/

### RAN1 Contribution — HARQ Feedback Disabling
File `R1-220xxxx FLS#1 on 9.12.3 disabling of HARQ feedback`: tài liệu đóng góp nội bộ 3GPP về cơ chế tắt HARQ feedback tại giai đoạn Feature Lead Summary — nền tảng cho điều khoản cuối trong TR 38.821 Mục 6.4.1.

### amain.pdf — MDS-HARQ
Bài báo về HARQ kết hợp mã MDS (Maximum Distance Separable) với partial feedback. Cung cấp định nghĩa CC và IR [Mục I.A] dùng làm nền lý thuyết cho `02_harq_cc_vs_ir.md`.

### Seminar Giordani (Univ. Padova, 2025)
Tổng quan NTN trong 5G/6G — dùng cho động lực nghiên cứu và bức tranh big picture [03_what_is_ntn.md].

---

## Tóm tắt — Bản đồ trích dẫn

```
Kênh truyền NTN          → TR 38.811 (Mục 6.6, 6.7, Bảng 5.3.x)
RTT và Nmin               → TR 38.811 (Bảng 5.3.x) + IEEE Tuninato 2025
LDPC + RV + circular buf  → TS 38.212 (Mục 5.4.2.1, Bảng 5.4.2.1-2)
HARQ process count        → TS 38.214 (Mục 5.1)
HARQ timing (ACK/NACK)   → TS 38.213 (Mục 9.2.3)
HARQ disable GEO          → TR 38.821 (Mục 6.4.1, 6.4.2)
Simulation parameters     → IEEE Tuninato 2025 (Tab. 4, 5, 8)
CC vs IR definitions      → amain.pdf (Mục I.A)
```

---

**File tiếp theo:** `06_channel_model_lms.md` — Mô hình kênh LMS: phân phối Loo, K-factor, và cách hiện thực trong mô phỏng
