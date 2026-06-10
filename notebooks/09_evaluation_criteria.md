# 09 — Tiêu chí Đánh giá: Định nghĩa và Công thức

> **Mục tiêu:** Định nghĩa chính xác từng metric được dùng để đánh giá hiệu năng HARQ trong NTN — mỗi công thức đều có nguồn trích dẫn.

---

## 1. BLER — Block Error Rate

### Định nghĩa

BLER là tỷ lệ số transport block (TB) bị lỗi (không giải mã được sau CRC check) trên tổng số TB được gửi [Tuninato 2025, Mục III]:

$$\text{BLER} = \frac{N_{\text{TB, bị lỗi}}}{N_{\text{TB, tổng}}}$$

Trong mô phỏng, một TB được coi là lỗi nếu CRC fail sau lần phát cuối cùng (tổng cộng 4 lần).

### Cách đo

- **BLER vs $E_s/N_0$:** đường cong BLER theo SNR cho từng scheme (No HARQ, CC, IR) và từng lần phát (ReTx = 0, 1, 2, 3).
- **Target BLER:** $10^{-3}$ — ngưỡng dùng để xác định điểm hoạt động tối ưu [Tuninato 2025, Mục V.C].

### Ý nghĩa

Mỗi lần phát lại HARQ dịch đường cong BLER sang trái (về phía SNR thấp hơn) — đây là HARQ gain trực tiếp quan sát được [Tuninato 2025, Mục V.C]:

> *"each retransmission shifts the BLER curve toward lower values of $E_s/N_0$, at the cost of a lower SE."*

---

## 2. SE — Spectral Efficiency (Hiệu suất phổ)

### 2.1. SE danh nghĩa

SE danh nghĩa không tính đến lỗi [Tuninato 2025, Eq. (1)]:

$$\text{SE} = \log_2(M) \cdot \frac{k}{n} \quad \left[\frac{\text{bit}}{\text{s} \cdot \text{Hz}}\right]$$

Trong đó $M$ là bậc điều chế, $k/n$ là code rate.

### 2.2. SE dựa trên goodput (SE thực tế)

SE thực tế tính số bit thông tin nhận đúng trên tổng thời gian truyền [Tuninato 2025, Eq. (2)]:

$$\text{SE}_{\text{GP}} = \frac{N_{\text{TB, đúng}} \cdot N_{b/\text{TB}}}{B \cdot T} \quad \left[\frac{\text{bit}}{\text{s} \cdot \text{Hz}}\right]$$

Trong đó:
- $N_{\text{TB, đúng}}$: số TB nhận đúng
- $N_{b/\text{TB}}$: số information bits mỗi TB
- $B$: bandwidth (Hz)
- $T = T_{\text{slot}} \cdot N_{\text{slots}}$: tổng thời gian quan sát

**Lý do dùng SE_GP thay vì SE danh nghĩa:** Khi HARQ phải phát lại, số slot dùng cho một TB tăng lên → SE thực tế giảm, dù BLER cải thiện. Trade-off này chỉ thấy qua SE_GP [Tuninato 2025, Mục III].

---

## 3. Latency — Độ trễ đầu cuối

### Định nghĩa

Độ trễ tổng của một TB bao gồm [Tuninato 2025, Mục III và Hình 5]:

$$L_{\text{TB}} = T_{\text{proc}} + \bar{n}_{\text{tx}} \cdot (T_{\text{slot}} + \text{RTT})$$

Trong đó:
- $T_{\text{proc}}$: thời gian xử lý tại UE và gNB (thường bỏ qua trong link-level sim)
- $\bar{n}_{\text{tx}}$: số lần phát trung bình ($1 \leq \bar{n}_{\text{tx}} \leq 4$)
- RTT = $2T_p$ theo quỹ đạo [TR 38.811, Bảng 5.3.4.1-1]

*(Công thức latency tổng quát này là mô hình đơn giản hóa của hình Fig. 5 trong [Tuninato 2025]. Không có dạng tường minh dưới dạng equation trong paper — đây là hình thức hóa từ diagram.)*

### Pipeline stall latency

Khi $N < N_{\min}$, pipeline stall xảy ra và latency thêm một khoảng chờ:

$$L_{\text{stall}} = \text{RTT} - N \cdot T_{\text{slot}}$$

mỗi khi tất cả $N$ process đều đang chờ ACK.

---

## 4. Energy per bit — Năng lượng trên mỗi bit thành công

### Định nghĩa

$$E_{\text{bit}} = \frac{P_{\text{phát}} \cdot \bar{n}_{\text{tx}} \cdot T_{\text{slot}}}{k \cdot (1 - \text{BLER}_{\text{final}})} \quad [\text{J/bit}]$$

Trong đó:
- $P_{\text{phát}}$: công suất phát (chuẩn hóa = 1 trong mô phỏng)
- $\bar{n}_{\text{tx}}$: số lần phát trung bình
- $k$: số information bits per TB
- $\text{BLER}_{\text{final}}$: BLER sau tất cả các lần HARQ

*(Công thức năng lượng này là metric gốc của dự án, chưa có trong bộ ref/ hiện tại. Được xây dựng từ nguyên lý cơ bản về energy = power × time.)*

### Ý nghĩa

- HARQ càng phát lại nhiều → $\bar{n}_{\text{tx}}$ càng lớn → energy/bit tăng.
- Nhưng HARQ cũng giảm BLER → nhiều TB thành công hơn → mẫu số tăng.
- Trade-off này khác nhau giữa CC và IR, và giữa các quỹ đạo.

---

## 5. $N_{\min}$ — Số HARQ process tối thiểu

Đã định nghĩa trong `04_ntn_breaks_harq.md`. Nhắc lại:

$$N_{\min} = \left\lceil \frac{2T_p}{T_{\text{slot}}} \right\rceil + 1 \quad [\text{Tuninato 2025, Mục IV.A}]$$

Metric này không phải performance metric mà là **design parameter** — được tính toán trước để xác định cấu hình HARQ cần thiết cho từng quỹ đạo.

---

## 6. Tóm tắt metric theo từng mô phỏng

| Mô phỏng | Metric chính | Metric phụ |
|---|---|---|
| Sim 1: BLER vs SNR | BLER | SE_GP |
| Sim 2: Throughput vs RTT | SE_GP (throughput) | Latency |
| Sim 3: $N_{\min}$ | $N_{\min}$ | Pipeline stall rate |
| Sim 4: GEO disable | BLER, SE_GP | Latency |
| Sim 5: Energy | $E_{\text{bit}}$ | $\bar{n}_{\text{tx}}$ |

---

**File tiếp theo:** Sau khi có kết quả mô phỏng → `10_results_interpretation.md`
