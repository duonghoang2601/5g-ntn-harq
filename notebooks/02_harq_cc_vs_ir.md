# 02 — Chase Combining vs Incremental Redundancy: Phân tích kỹ thuật

> **Mục tiêu:** Hiểu hai cơ chế HARQ soft combining — CC và IR — về mặt toán học, hiệu năng thực tế từ kết quả mô phỏng, và lý do 5G NR chọn IR làm cơ chế mặc định.

---

## 1. Bối cảnh: Hai cách tận dụng tín hiệu lỗi

Như đã nêu trong `01_arq_to_harq.md`, điểm mấu chốt của HARQ là **không vứt bỏ tín hiệu đã nhận dù lỗi**. Câu hỏi tiếp theo: *kết hợp như thế nào?*

Có hai kỹ thuật cơ bản [amain.pdf, Mục I.A]:

> *"The first, chase combining, involves retransmitting the same information, allowing the receiver to perform soft combining, such as maximum ratio combining... The second technique, incremental redundancy, transmits additional coded bits at each retransmission, effectively lowering the coding rate and improving the error correction capacity."*

---

## 2. Chase Combining (CC) — Kết hợp bản sao

### 2.1. Cơ chế

Máy phát gửi **cùng một tập bit** ở mọi lần truyền (luôn dùng RV0). Máy thu tích lũy các phiên bản nhận được $y_1, y_2, \ldots, y_n$ trong soft buffer rồi cộng chúng lại trước khi đưa vào decoder.

Phép cộng LLR (Log-Likelihood Ratio) tương đương với MRC (Maximum Ratio Combining):

$$\text{LLR}_{\text{tổng}}^{(n)} = \sum_{i=1}^{n} \text{LLR}_i$$

*(Công thức LLR combining là kết quả chuẩn từ lý thuyết MRC — chưa có dạng tường minh này trong bộ ref/ hiện tại. Khái niệm MRC soft combining được xác nhận trong [amain.pdf, Mục I.A].)*

### 2.2. Hiệu quả: Diversity Gain thuần túy

Khi cộng $n$ bản sao độc lập qua kênh Rician với cùng SNR trung bình $\bar{\gamma}$, SNR hiệu dụng tăng tuyến tính:

$$\bar{\gamma}_{\text{eff}}^{(n)} = n \cdot \bar{\gamma}$$

*(Công thức SNR combining là kết quả lý thuyết MRC chuẩn — chưa có trong bộ ref/ hiện tại.)*

**Điểm quan trọng:** Code rate **không thay đổi** — máy thu vẫn giải mã cùng một mã với cùng tốc độ. Lợi ích duy nhất là SNR tăng do cộng dồn năng lượng. Đây gọi là **diversity gain**.

### 2.3. Yêu cầu bộ nhớ

Máy thu chỉ cần lưu **tổng LLR tích lũy** — bộ nhớ không tăng theo số lần phát lại [amain.pdf, Mục I.A]:

> *"This technique requires less memory resources because only the combined information needs to be stored."*

---

## 3. Incremental Redundancy (IR) — Tăng dần độ dư thừa

### 3.1. Cơ chế

Máy phát dùng **RV khác nhau** mỗi lần phát ({0, 2, 3, 1} theo [TS 38.212, Bảng 5.4.2.1-2]). Mỗi RV chỉ định vị trí bắt đầu $k_0$ khác nhau trong circular buffer → mỗi lần phát cung cấp một tập bit **mới** (chủ yếu là parity bits bổ sung).

Máy thu tích lũy toàn bộ các lần phát vào soft buffer, decoder nhìn thấy codeword ngày càng dài hơn qua từng lần.

### 3.2. Hiệu quả: Coding Gain + Diversity Gain

Code rate hiệu dụng giảm dần qua từng lần phát:

$$r_{\text{eff}}(n) = \frac{k}{\sum_{i=1}^{n} m_i}$$

Trong đó $k$ là số systematic bits, $m_i$ là số bit gửi ở lần $i$ [định nghĩa bằng lời trong Tuninato 2025, Mục V.C]. Code rate giảm → LDPC decoder có nhiều bit kiểm tra hơn → **khả năng sửa lỗi tăng**.

IR mang lại **hai loại lợi ích** chồng nhau:
- **Diversity gain:** giống CC — nhiều năng lượng hơn cho cùng một codeword.
- **Coding gain:** do code rate giảm — decoder có thêm redundancy bits mới để sửa lỗi.

Theo [Tuninato 2025, Mục V.C]:

> *"The higher the initial nominal code rate, the higher the coding gain provided by the HARQ incremental redundancy: at each retransmission, more new redundancy bits are added to the codeword at the receiver."*

### 3.3. Yêu cầu bộ nhớ

Máy thu phải lưu **toàn bộ LLR của từng lần phát riêng lẻ** vì mỗi lần gửi bit khác nhau — bộ nhớ lớn hơn CC [amain.pdf, Mục I.A]:

> *"This method increases the complexity of the decoding process and demands more memory resources from the UE."*

---

## 4. So sánh định lượng từ kết quả thực nghiệm

Theo mô phỏng link-level trong [Tuninato 2025, Mục V.C] trên kênh LMS với $K = 15$ dB, tốc độ đầu cuối 50 km/h:

| MCS | Modulation | Code rate | Tổng HARQ gain (tại BLER=$10^{-2}$) |
|---|---|---|---|
| MCS A | QPSK | 1/2 | **>8 dB** |
| MCS B | 256QAM | 8/9 | **~18 dB** |

**Giải thích:** MCS B (256QAM, code rate 8/9) có code rate ban đầu rất cao → mỗi lần phát lại bổ sung nhiều parity bits mới → coding gain lớn hơn nhiều so với MCS A (QPSK, code rate 1/2 đã thấp sẵn, ít room cho IR).

Đây là bằng chứng thực nghiệm cho nguyên lý: **IR hiệu quả nhất khi code rate ban đầu cao** (tức là khi kênh tốt nhưng gói tin vẫn lỗi do noise burst).

---

## 5. CC vs IR trong 5G NR: IR là mặc định

Trong 5G NR với mã LDPC và circular buffer [TS 38.212, Mục 5.4.2.1], thứ tự RV mặc định là {0, 2, 3, 1} — mỗi RV cho bit tập hợp khác nhau. Đây chính là **IR thuần túy**.

CC trong 5G NR chỉ xảy ra khi máy phát lặp lại RV0 nhiều lần (không theo thứ tự {0,2,3,1}). Trong thực tế mô phỏng của dự án này (theo cấu hình [Tuninato 2025, Tab. 4]), chúng tôi dùng thứ tự RV chuẩn → IR.

### Khi nào CC vẫn được dùng?

- Thiết bị IoT đơn giản với bộ nhớ nhỏ (không đủ soft buffer cho IR).
- Một số triển khai NB-IoT.
- Phân tích lý thuyết làm baseline so sánh (như trong dự án này).

---

## 6. Ý nghĩa với NTN

Trong mạng vệ tinh, RTT lớn → mỗi lần phát lại cách nhau hàng chục đến hàng trăm ms. Hai hệ quả:

**1. Coherence time:** Kênh có thể thay đổi đáng kể giữa các lần phát lại. Nếu kênh decorrelate hoàn toàn, IR vẫn hoạt động tốt (vì bit mới từ RV mới); CC cũng vẫn hoạt động nhưng diversity gain có thể giảm nếu pha giữa các bản sao không tương quan. [Tuninato 2025, Mục IV.B] phân tích vấn đề này qua coherence time và số HARQ process tương quan.

**2. Memory:** Với IR, soft buffer phải lưu LLR của nhiều lần phát cách nhau hàng trăm ms → yêu cầu bộ nhớ lớn hơn, đặc biệt nếu số HARQ process tăng để bù RTT. Đây là trade-off thực tế trong thiết kế thiết bị NTN.

---

## Tóm tắt

```
Chase Combining (CC):
  • Cùng bit (RV0) mỗi lần → diversity gain thuần túy
  • Code rate cố định
  • Bộ nhớ nhỏ (chỉ lưu tổng LLR)
  • Hiệu quả khi code rate ban đầu thấp

Incremental Redundancy (IR):
  • RV khác nhau {0,2,3,1} → bit mới mỗi lần → coding gain + diversity gain
  • Code rate giảm dần qua các lần phát
  • Bộ nhớ lớn hơn (lưu từng LLR riêng)
  • Hiệu quả hơn CC, đặc biệt khi code rate ban đầu cao
  • Mặc định trong 5G NR (LDPC + circular buffer)

Trong NTN: IR vẫn là lựa chọn tốt hơn, nhưng coherence time và
yêu cầu bộ nhớ cần tính đến khi tăng số HARQ process theo RTT.
```

---

**File tiếp theo:** `03_what_is_ntn.md` — Mạng không mặt đất: LEO, MEO, GEO và vai trò trong chiến lược 5G toàn cầu
