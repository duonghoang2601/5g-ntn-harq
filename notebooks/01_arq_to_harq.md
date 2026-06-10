# 01 — Từ ARQ đến HARQ: Lịch sử, Kiến trúc và Cơ chế hoạt động

> **Mục tiêu:** Hiểu tại sao ARQ không đủ, tại sao HARQ ra đời, và trong 5G NR nó được hiện thực hóa cụ thể như thế nào — từ LDPC, circular buffer đến RV sequence.

---

## 1. ARQ thuần túy — Ba biến thể và giới hạn của chúng

ARQ (Automatic Repeat reQuest) là họ giao thức phát lại dựa trên phản hồi lỗi từ phía thu. Máy thu kiểm tra lỗi bằng CRC (Cyclic Redundancy Check); nếu phát hiện lỗi → gửi NACK → máy phát truyền lại gói tin **từ đầu** (không tận dụng tín hiệu cũ).

> *Lưu ý trích dẫn: Ba biến thể ARQ dưới đây là kiến thức giáo khoa chuẩn. Trong bộ ref/ hiện tại, RLC ARQ được mô tả ở mức giao thức trong [Tuninato 2025, Mục III.B] và [TR 38.821, Mục 7.2.2], nhưng không có phân tích Stop-and-Wait / Go-Back-N / Selective Repeat. Cần bổ sung giáo trình nếu báo cáo yêu cầu trích dẫn ba biến thể này.*

### 1.1. Stop-and-Wait ARQ
Máy phát gửi **một** gói tin rồi chờ ACK/NACK trước khi gửi gói tiếp theo.

- **Ưu điểm:** Đơn giản, bộ đệm nhỏ.
- **Nhược điểm nghiêm trọng:** Hiệu suất kênh (channel utilization) cực thấp khi RTT lớn. Trong thời gian chờ ACK, kênh truyền bị bỏ trống.

Hiệu suất kênh lý tưởng của Stop-and-Wait khi không có lỗi:

$$\eta_{\text{SW}} = \frac{T_{\text{frame}}}{T_{\text{frame}} + \text{RTT}}$$

*(Công thức giáo khoa chuẩn — chưa có trong bộ ref/ hiện tại. Cần bổ sung giáo trình nếu báo cáo yêu cầu trích dẫn.)*

Với GEO RTT = 544 ms [TR 38.811, Bảng 5.3.2.1-1] và $T_{\text{frame}}$ = 1 ms (1 slot 5G NR) → $\eta \approx 0.18\%$ — thảm họa. Vấn đề này được IEEE paper mô tả là "under-utilization of the available resources" [Tuninato 2025, Mục IV.A].

### 1.2. Go-Back-N ARQ
Máy phát gửi liên tục nhiều gói trong cửa sổ phát (window size $W$). Khi phát hiện lỗi ở gói $k$, máy thu yêu cầu phát lại từ gói $k$ trở đi (kể cả các gói sau $k$ đã nhận đúng).

- **Ưu điểm:** Sử dụng kênh tốt hơn khi $W$ đủ lớn.
- **Nhược điểm:** Lãng phí — phải truyền lại cả gói đúng.

### 1.3. Selective Repeat ARQ
Chỉ phát lại đúng gói bị lỗi, giữ nguyên các gói đúng.

- **Ưu điểm:** Hiệu quả nhất trong họ ARQ.
- **Nhược điểm:** Bộ đệm máy thu lớn hơn; vẫn **vứt bỏ hoàn toàn** tín hiệu của gói lỗi — đây là điểm mấu chốt mà HARQ khắc phục.

**Vấn đề chung của tất cả ARQ:** Bản phát lại trước bị **discard** — năng lượng đã thu được không được tận dụng. Đây là sự lãng phí về mặt vật lý.

---

## 2. FEC — Sửa lỗi không cần phản hồi

FEC (Forward Error Correction) thêm bit dư thừa vào dữ liệu để máy thu tự sửa lỗi. Trong 5G NR, mã hóa kênh cho PDSCH dùng **LDPC (Low-Density Parity-Check)** [Tuninato 2025, Mục III.A].

- **Ưu điểm:** Không cần RTT để sửa lỗi.
- **Nhược điểm:** Code rate cố định — overhead dư thừa dù kênh tốt; nếu lỗi vượt quá khả năng sửa của mã, gói tin vẫn bị lỗi và phải xử lý ở tầng trên.

Bài toán: **kênh thay đổi liên tục** — mã FEC tốt ở SNR thấp thì overhead quá lớn ở SNR cao, và ngược lại.

---

## 3. HARQ — Kết hợp FEC và ARQ với soft combining

HARQ giải quyết cả hai vấn đề trên bằng cách kết hợp:
- **FEC:** Dữ liệu được mã hóa trước khi gửi (LDPC trong 5G NR).
- **ARQ:** Phản hồi ACK/NACK để quyết định phát lại.
- **Soft combining:** Thay vì vứt bỏ tín hiệu lỗi, máy thu **lưu lại** trong bộ đệm (soft buffer) và **kết hợp** với lần phát tiếp theo.

Nguyên lý: khi cộng nhiều lần nhận của cùng một codeword, SNR hiệu dụng tăng lên. Mỗi lần phát lại = thêm thông tin về cùng một codeword → LDPC decoder có nhiều dữ liệu hơn để giải mã thành công [Tuninato 2025, Mục III.A]:

> *"the received codewords are stored in a memory buffer and later combined with the retransmitted versions to obtain a single, combined codeword that is more reliable than its constituents"*

---

## 4. Kiến trúc HARQ trong 5G NR

### 4.1. Cấu trúc HARQ Process

Trong 5G NR DL (đường xuống PDSCH), mỗi UE hỗ trợ tối đa **16 HARQ process** (trong mạng mặt đất) [Tuninato 2025, Mục III.A]. Mỗi HARQ process là một luồng độc lập, xử lý một transport block (TB) riêng biệt.

Các HARQ process hoạt động song song theo mô hình **N-process Stop-and-Wait**: mỗi process thực hiện Stop-and-Wait riêng, nhưng $N$ process chạy song song → kênh được sử dụng liên tục nếu $N$ đủ lớn.

Số lần phát lại tối đa mỗi HARQ process: **3 lần phát lại**, tổng cộng **4 lần truyền** (1 lần gốc + 3 lần lại) [Tuninato 2025, Mục III.A].

### 4.2. Redundancy Version (RV) và Circular Buffer

Trong 5G NR, mỗi lần truyền tương ứng với một **Redundancy Version (RV)** khác nhau, theo thứ tự **{0, 2, 3, 1}** [Tuninato 2025, Mục III.A].

Cơ chế: LDPC encoder sinh ra một codeword dài hơn nhiều so với dữ liệu cần gửi. Toàn bộ codeword được lưu trong **circular buffer**. Mỗi RV chỉ định vị trí bắt đầu đọc $k_0$ từ circular buffer [TS 38.212, Mục 5.4.2.1, Bảng 5.4.2.1-2] → mỗi lần phát, máy phát gửi một tập bit **khác nhau** từ cùng một codeword.

```
Codeword LDPC (dài):  [... systematic bits ... | ... parity bits ...]
                              ↑RV0        ↑RV2   ↑RV3  ↑RV1
Circular buffer: đọc vòng tròn từ vị trí khác nhau mỗi RV
```

**Tại sao RV0 được ưu tiên đầu tiên?** RV0 bắt đầu từ vị trí chứa phần lớn **systematic bits** (bit dữ liệu gốc) — nếu kênh tốt, đây là đủ để giải mã. Các RV sau bổ sung thêm **parity bits** (bit kiểm tra) để giúp giải mã khi kênh xấu hơn.

Đây chính là cơ sở của **Incremental Redundancy (IR)**: mỗi lần phát lại không chỉ lặp lại mà còn cung cấp thêm thông tin mới (redundancy) cho bộ giải mã [Tuninato 2025, Mục III.A].

### 4.3. Soft Combining — Hai cơ chế

Có hai cách kết hợp tín hiệu nhận được:

**Chase Combining (CC):** Mỗi lần phát lại gửi **cùng một tập bit** (RV0 lặp lại). Máy thu cộng (MRC — Maximum Ratio Combining) các phiên bản nhận được:

$$\text{LLR}_{\text{tổng}} = \sum_{i=1}^{n} \text{LLR}_i$$

*(Công thức LLR combining là chuẩn kỹ thuật số, chưa có dạng tường minh này trong bộ ref/ hiện tại. Khái niệm soft combining được xác nhận trong [Tuninato 2025, Mục III.A].)*

Code rate không thay đổi theo số lần phát lại — chỉ có diversity gain (SNR tăng do cộng dồn).

**Incremental Redundancy (IR):** Mỗi lần phát lại gửi tập bit **khác nhau** (RV khác nhau từ circular buffer [TS 38.212, Bảng 5.4.2.1-2]). Code rate **giảm** dần theo số lần phát lại:

$$r_{\text{eff}}(n) = \frac{k}{\sum_{i=1}^{n} m_i}$$

Trong đó $k$ là số bit dữ liệu, $m_i$ là số bit được gửi ở lần thứ $i$. Đây là hình thức hóa toán học của định nghĩa trong [Tuninato 2025, Mục III.A]: *"ratio between the amount of unique systematic bits cumulatively transmitted by each RV, and the total amount of unique bits."* Code rate giảm → khả năng sửa lỗi tăng → IR có **coding gain** thêm vào ngoài diversity gain.

**Kết luận:** IR vượt trội CC ở SNR thấp (khi cần nhiều retransmission), nhưng phức tạp hơn về bộ đệm. Phân tích chi tiết trong `02_harq_cc_vs_ir.md`.

---

## 5. ACK/NACK và vòng phản hồi

Quy trình hoàn chỉnh của một HARQ process:

```
Máy phát                          Máy thu
   |--- TB (RV0) ---------------→|
   |                              | CRC check
   |← ACK (giải mã đúng) --------|  → kết thúc process
   |← NACK (lỗi) ----------------|  → lưu LLR vào soft buffer
   |--- TB (RV2) ---------------→|
   |                              | CRC check (kết hợp với RV0)
   |← ACK / NACK ← -------------|
   ... (tối đa 4 lần tổng)
```

**Trong NTN:** Độ trễ phản hồi ACK/NACK = RTT/2. Với GEO RTT ≈ 544 ms, mỗi vòng phản hồi mất ~272 ms. Đây là lý do tại sao 16 HARQ process không đủ cho NTN và cần tăng số lượng — phân tích trong `04_ntn_breaks_harq.md`.

---

## 6. RLC ARQ trong 5G NR — Lớp phía trên

RLC ARQ là cơ chế phát lại ở lớp RLC (Radio Link Control), **phía trên** MAC/HARQ [Tuninato 2025, Mục III.B]. Khác biệt quan trọng:

| Đặc điểm | HARQ (MAC layer) | RLC ARQ (RLC layer) |
|---|---|---|
| Soft combining | Có — tích lũy LLR | Không — memoryless |
| Coding gain | Có (IR) | Không |
| Diversity gain | Có (CC và IR) | Không |
| Số lần phát lại tối đa | 3 (tổng 4) | Lên đến 32 |
| RTT tham chiếu | HARQ RTT (ngắn) | RLC RTT (dài hơn) |
| Độ phức tạp bộ đệm | Cao (soft buffer) | Thấp |

Trong mạng mặt đất, HARQ xử lý lỗi nhanh (RTT ngắn), RLC ARQ xử lý lỗi còn sót lại. Trong NTN với GEO, một số giải pháp đề xuất **tắt HARQ feedback và chỉ dùng RLC ARQ** [TR 38.821, Mục 6.4.2] — đây là chủ đề của Mô phỏng 4 trong dự án này.

---

## 7. Vị trí HARQ trong ngăn xếp giao thức 5G NR

```
Lớp Ứng dụng
     ↕
PDCP (Packet Data Convergence Protocol)
     ↕
RLC  (Radio Link Control)  ← RLC ARQ ở đây
     ↕
MAC  (Medium Access Control) ← HARQ process quản lý ở đây
     ↕
PHY  (Physical Layer) ← Soft combining, LDPC decode ở đây
```

HARQ là điểm giao giữa MAC và PHY: MAC quản lý logic phát lại (process ID, RV, ACK/NACK), còn PHY thực hiện soft combining và giải mã LDPC [Tuninato 2025, Mục III.A].

---

## Tóm tắt

```
Stop-and-Wait ARQ → đơn giản nhưng kênh bị lãng phí khi RTT lớn
Go-Back-N / SR ARQ → cải thiện nhưng vẫn vứt bỏ tín hiệu lỗi
FEC thuần túy → không cần phản hồi nhưng overhead cố định
     ↓ kết hợp
HARQ = LDPC (FEC) + ARQ feedback + soft combining
     → tận dụng mọi bit năng lượng đã nhận được
     → RV{0,2,3,1} qua circular buffer → IR có coding gain
     → 16 process song song (mặt đất) → cần nhiều hơn cho NTN
```

---

**File tiếp theo:** `02_harq_cc_vs_ir.md` — Phân tích kỹ thuật và toán học của Chase Combining vs Incremental Redundancy
