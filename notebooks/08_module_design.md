# 08 — Thiết kế Module Mô phỏng: Kiến trúc và Sơ đồ khối

> **Mục tiêu:** Định nghĩa rõ từng module code, input/output, và lý do thiết kế — để việc implement từng block là straightforward và có thể kiểm tra độc lập.

---

## 1. Sơ đồ khối tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│                    SIMULATION PIPELINE                       │
│                                                             │
│  [Data bits k]                                              │
│       ↓                                                     │
│  [LDPC Encoder] ─── code rate r, LDPC base graph           │
│       ↓                                                     │
│  [Rate Matcher] ─── circular buffer, chọn RV theo idx      │
│       ↓                                                     │
│  [Modulator] ──────── QPSK / 256QAM                        │
│       ↓                                                     │
│  [LMS Channel] ────── Rician K-factor, Doppler, AWGN       │
│       ↓                                                     │
│  [Demodulator] ─────── soft symbols → LLR                  │
│       ↓                                                     │
│  [Soft Buffer] ─────── tích lũy LLR qua các lần phát       │
│       ↓                                                     │
│  [LDPC Decoder] ────── belief propagation                   │
│       ↓                                                     │
│  [CRC Check] ───────── ACK / NACK                          │
│       ↓                                                     │
│  [HARQ Process Mgr] ── điều phối N process song song       │
│       ↓                                                     │
│  [Metrics Collector] ─ BLER, SE, latency, energy/bit       │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Cấu trúc thư mục code

```
src/
├── channel/
│   └── lms_channel.py       # Rician flat fading + Jake's Doppler
├── harq/
│   ├── ldpc_codec.py        # Wrapper LDPC encode/decode (5G Toolbox)
│   ├── rate_matcher.py      # Circular buffer + RV selection
│   ├── soft_buffer.py       # LLR accumulation
│   ├── cc_harq.py           # Chase Combining (lặp RV0)
│   ├── ir_harq.py           # Incremental Redundancy (RV {0,2,3,1})
│   └── process_manager.py   # N HARQ process song song + RTT model
├── sim/
│   ├── sim_01_bler_vs_snr.py
│   ├── sim_02_throughput_vs_rtt.py
│   ├── sim_03_nmin_optimization.py
│   ├── sim_04_geo_disable.py
│   └── sim_05_energy.py
└── plots/
    └── plot_utils.py        # Figure generation
```

---

## 3. Module chi tiết

### 3.1. `lms_channel.py` — Kênh LMS

**Input:** K_dB, n_samples, speed_kmh, fc_GHz, snr_dB  
**Output:** tín hiệu nhận $y = h \cdot x + n$, chuỗi hệ số kênh $h$

```
Rician channel:
  h = √(K/(K+1))·e^(jφ₀)   ← thành phần LOS
    + √(1/(K+1))·h_scatter   ← Jake's Doppler fading [TR 38.811, 6.7.1]

AWGN:
  n ~ CN(0, σ²),  σ² = E_s / SNR
```

Tham số K = 15 dB và 20 dB theo [Tuninato 2025, Mục IV]. Jake's Doppler spectrum theo [TR 38.811, Mục 6.7.1].

### 3.2. `rate_matcher.py` — Circular Buffer và RV

**Input:** encoded bits (LDPC output), rv_id ∈ {0,1,2,3}, G (số bit cần gửi)  
**Output:** chuỗi G bit đã được chọn từ circular buffer

Logic: theo thuật toán bit selection trong [TS 38.212, Mục 5.4.2.1] — đọc từ vị trí $k_0$ (tra Bảng 5.4.2.1-2 theo rv_id và LDPC base graph) và đọc vòng tròn đủ G bit.

Thứ tự RV thực tế: rv_id sequence = {0, 2, 3, 1} → tương ứng index {0, 2, 3, 1} trong bảng [Tuninato 2025, Mục III.A; TS 38.212, Bảng 5.4.2.1-2].

### 3.3. `soft_buffer.py` — Tích lũy LLR

**Input:** LLR array của lần phát hiện tại  
**Output:** LLR array đã cộng dồn

```
CC: buffer = sum of all received LLR arrays (cùng bit position)
IR: buffer = concatenate LLR arrays (bit position khác nhau)
```

Nguyên lý CC (LLR cộng) và IR (LLR ghép) theo [amain.pdf, Mục I.A].

### 3.4. `process_manager.py` — Quản lý N HARQ Process

**Input:** N (số process), RTT (ms), T_slot (ms), payload_type  
**Output:** scheduling timeline, throughput, latency per TB

**Logic:**
- Duy trì N process song song, mỗi process theo dõi: trạng thái (IDLE/WAITING_ACK/RETRANSMITTING), RV hiện tại, số lần phát đã dùng.
- Sau mỗi T_slot: kiểm tra process nào đã chờ đủ RTT → nhận ACK/NACK giả lập.
- Nếu tất cả N process đều đang WAITING_ACK → **pipeline stall** → ghi nhận idle time.
- Công thức $N_{\min}$ theo [Tuninato 2025, Mục IV.A]: $N_{\min} = \lceil 2T_p/T_{\text{slot}} \rceil + 1$.

### 3.5. `cc_harq.py` và `ir_harq.py`

**cc_harq.py:** luôn dùng rv_id = 0 (lặp lại bit giống nhau); soft_buffer dùng LLR cộng.

**ir_harq.py:** cycle qua rv_id = {0, 2, 3, 1}; soft_buffer dùng LLR ghép (concatenate theo bit position).

---

## 4. Năm script mô phỏng

### Sim 1 — `sim_01_bler_vs_snr.py`
So sánh BLER vs $E_s/N_0$ cho: No HARQ / CC-HARQ / IR-HARQ.  
**Sweep:** SNR từ -15 dB đến 30 dB; fix LEO 600 km, K=15 dB, MCS A và B.  
**Output:** BLER curve cho từng scheme, mỗi MCS.

### Sim 2 — `sim_02_throughput_vs_rtt.py`
Throughput (Mbit/s) vs RTT theo quỹ đạo.  
**Sweep:** RTT ∈ {12.9, 24.3, 93.5, 270.6} ms; fix N=16 và N=32 để thấy stall.  
**Output:** throughput curve thể hiện rõ điểm stall.

### Sim 3 — `sim_03_nmin_optimization.py`
Số HARQ process tối thiểu $N_{\min}$ theo quỹ đạo và SCS.  
**Sweep:** SCS ∈ {15, 30, 60, 120} kHz; quỹ đạo LEO 600/1200, MEO, GEO.  
**Output:** bảng và đường cong $N_{\min}$, đánh dấu vùng vượt giới hạn 32.

### Sim 4 — `sim_04_geo_disable.py`
So sánh GEO: HARQ (N lớn) vs HARQ disable (RLC ARQ).  
**Metric:** BLER, SE, latency.  
**Output:** trade-off curve cho quyết định disable.

### Sim 5 — `sim_05_energy.py`
Energy per successfully delivered bit vs số lần phát lại và scheme HARQ.  
**Sweep:** $\bar{n}_{\text{tx}}$ từ 1 đến 4; CC vs IR; LEO vs GEO.  
**Output:** energy efficiency curve.

---

## 5. Lý do thiết kế modular

- Mỗi module có thể test độc lập (unit test lms_channel, rate_matcher riêng).
- Dễ thay thế: ví dụ thay Jake's model bằng geometry-based Doppler mà không đụng đến phần còn lại.
- Dễ mở rộng: thêm quỹ đạo mới chỉ cần thay tham số RTT trong process_manager.

---

**File tiếp theo:** `09_evaluation_criteria.md` — Định nghĩa và công thức cho từng metric đánh giá
