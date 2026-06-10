# 04 — NTN Phá Vỡ HARQ: RTT Explosion và Pipeline Stall

> **Mục tiêu:** Phân tích cơ chế tại sao HARQ tiêu chuẩn (16 process) thất bại trong NTN, dẫn xuất công thức $N_{\min}$, và trình bày hai giải pháp 3GPP.

---

## 1. HARQ hoạt động tốt trong mạng mặt đất — tại sao?

Trong mạng mặt đất, RTT < 1 ms (khoảng cách gNB–UE < vài trăm mét, tốc độ ánh sáng). Với 16 HARQ process và slot duration $T_{\text{slot}} = 0.5$ ms (SCS 30 kHz), pipeline luôn đầy:

$$N_{\min}^{\text{terrestrial}} = \left\lceil \frac{2T_p}{T_{\text{slot}}} \right\rceil + 1 \approx 3 \text{ process}$$

16 process dư thừa → không bao giờ có pipeline stall → throughput đạt tối đa.

---

## 2. RTT Explosion trong NTN

Trong NTN, thời gian lan truyền một chiều $T_p$ thống trị hoàn toàn RTT. Với payload regenerative [TR 38.811, Bảng 5.3.4.1-1 và 5.3.2.1-1]:

| Quỹ đạo | $T_p$ (one-way, 10° elevation) | RTT $= 2T_p$ |
|---|---|---|
| LEO 600 km | ~6,4 ms | ~12,9 ms |
| LEO 1.200 km | ~12,2 ms | ~24,3 ms |
| MEO 10.000 km | ~46,7 ms | ~93,5 ms |
| GEO 35.786 km | ~135,3 ms | ~270,6 ms |

So với mạng mặt đất (<1 ms), RTT tăng **270 đến 54.000 lần**. Đây là "RTT explosion."

---

## 3. Pipeline Stall — Cơ chế và Hậu quả

### 3.1. Cơ chế

$N$ HARQ process hoạt động theo vòng quay: process 0, 1, ..., N-1, 0, 1, ... Máy phát gửi slot mới mỗi $T_{\text{slot}}$ trên từng process. Sau $N$ slot ($N \times T_{\text{slot}}$), máy phát quay lại process 0 — lúc này cần biết ACK/NACK của lần gửi trước để tái sử dụng process đó.

Nếu $N \times T_{\text{slot}} < \text{RTT}$, máy phát quay lại process 0 **trước khi ACK về** → phải dừng chờ → **pipeline stall** [Tuninato 2025, Mục IV.A]:

> *"if the transmitter reaches the maximum number of HARQ processes, it has to wait until the first ACK is received before restarting to transmit. This kind of approach is called stop-and-wait, and the waiting time may result in a significant throughput drop."*

Theo [TR 38.821, Mục 6.4.2], đây chính là vấn đề cốt lõi mà 3GPP cần giải quyết cho NTN.

### 3.2. Số lượng process tối thiểu

Để tránh pipeline stall, cần [Tuninato 2025, Mục IV.A]:

$$N_{\min} = \left\lceil \frac{2T_p}{T_{\text{slot}}} \right\rceil + 1$$

Trong đó:
- $T_p$: one-way propagation delay (s)
- $T_{\text{slot}}$: thời lượng một slot (s), phụ thuộc SCS: $T_{\text{slot}} = 1/(14 \times \text{SCS})$
- $\lceil \cdot \rceil$: làm tròn lên (ceiling)

Ví dụ với SCS = 30 kHz ($T_{\text{slot}} = 0.5$ ms):

| Quỹ đạo | $T_p$ | $N_{\min}$ (SCS 30 kHz) | So với giới hạn 32 |
|---|---|---|---|
| LEO 600 km | 6,4 ms | 14 | ✓ Khả thi |
| LEO 1.200 km | 12,2 ms | 26 | ✓ Vừa đủ |
| MEO 10.000 km | 46,7 ms | **95** | ✗ Vượt giới hạn |
| GEO 35.786 km | 135,3 ms | **272** | ✗ Vượt giới hạn |

Với SCS nhỏ hơn (15 kHz, $T_{\text{slot}} = 1$ ms), $N_{\min}$ giảm đi một nửa — LEO 600 km chỉ cần 14 process → vẫn khả thi [Tuninato 2025, Bảng 5].

### 3.3. Giới hạn chuẩn 5G NR

Theo [TS 38.214, Mục 5.1]: tối đa **16 HARQ process** (mặc định) hoặc **32 HARQ process** nếu UE hỗ trợ. Với MEO và GEO, $N_{\min}$ vượt xa giới hạn 32 → pipeline stall không thể tránh với cấu hình tiêu chuẩn.

---

## 4. Hai giải pháp 3GPP

3GPP Rel-17 thảo luận hai hướng giải quyết [TR 38.821, Mục 6.4.2]:

### Giải pháp 1: Tăng số HARQ process

Cho phép UE sử dụng số HARQ process lớn hơn 32 để đủ lấp đầy pipeline với RTT lớn.

- **Ưu điểm:** Giữ được toàn bộ lợi ích HARQ (coding gain + diversity gain).
- **Nhược điểm:** Yêu cầu bộ nhớ soft buffer tỷ lệ với số process; phức tạp về scheduling.

### Giải pháp 2: Tắt HARQ feedback (Disable UL HARQ feedback)

Tắt NACK/ACK cho DL → máy phát không đợi phản hồi → không có pipeline stall. Dùng RLC ARQ ở lớp trên để xử lý độ tin cậy.

- **Ưu điểm:** Loại bỏ hoàn toàn vấn đề pipeline stall; đơn giản hóa thiết kế.
- **Nhược điểm:** Mất hoàn toàn HARQ soft combining (mất coding gain + diversity gain); RLC ARQ memoryless kém hiệu quả hơn [Tuninato 2025, Mục III.B].

Theo [TR 38.821, Mục 6.4.1], việc bật/tắt HARQ feedback phải được cấu hình **per UE và per HARQ process** — không phải all-or-nothing:

> *"enabling / disabling of HARQ uplink retransmission should be configurable per UE or per HARQ process."*

---

## 5. Liên quan đến 5 mô phỏng của dự án

| Mô phỏng | Vấn đề liên quan |
|---|---|
| Sim 1: BLER vs SNR | Chứng minh HARQ gain tồn tại dù kênh NTN |
| Sim 2: Throughput vs RTT | Thể hiện tác động của RTT explosion |
| **Sim 3: $N_{\min}$ theo quỹ đạo** | **Trực tiếp từ công thức này** |
| **Sim 4: GEO HARQ disable** | **Trade-off của Giải pháp 2** |
| Sim 5: Energy per bit | Hiệu quả năng lượng khi phải phát lại nhiều |

---

## Tóm tắt

```
HARQ mặt đất: 16 process, RTT < 1 ms → pipeline luôn đầy → OK
NTN:          RTT tăng 270–54.000 lần → pipeline stall
              → Nmin = ⌈2Tp/Tslot⌉ + 1
              LEO 600km: Nmin~14 → khả thi (SCS ≥ 15 kHz)
              MEO/GEO:   Nmin >> 32 → không khả thi với chuẩn hiện tại

Giải pháp 3GPP Rel-17:
  1. Tăng số HARQ process (giữ gain, tốn bộ nhớ)
  2. Tắt HARQ feedback, dùng RLC ARQ (đơn giản, mất gain)
```

---

**File tiếp theo:** `05_3gpp_standards.md` — Bản đồ các tiêu chuẩn 3GPP liên quan và điều khoản cụ thể dùng trong dự án
