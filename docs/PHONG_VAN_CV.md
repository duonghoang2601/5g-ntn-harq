# Chuẩn bị phỏng vấn FPT — Ngân hàng câu hỏi cho 4 dự án CV

> **Cách dùng tài liệu:** Phần A là kiến thức nền tảng viễn thông/RF/anten — đây là phần dễ bị hỏi nhất và cũng dễ trượt nhất nếu trả lời lan man. Mỗi câu có **gợi ý trả lời** ngắn gọn, đúng bản chất. Phần B đi sâu vào từng dự án. Học phần A trước, vì nhà tuyển dụng thường "test gốc rễ" trước khi vào dự án.

---

## Đánh giá khả năng bị hỏi sâu

| Dự án | Khả năng hỏi sâu | Lý do |
|---|---|---|
| **5G NTN HARQ** | ★★★★★ | FPT Telecom triển khai 5G; NTN là chủ đề nóng; ít SV làm |
| **DT-ISAC** | ★★★★☆ | Industry 4.0, 6G — FPT R&D rất quan tâm |
| **AI nhận diện đồng hồ số** | ★★★★☆ | Dễ demo, gần sản phẩm thực tế |
| **Định tuyến mạng cảm biến dưới nước** | ★★★☆☆ | Niche, nhưng hỏi tốt về thuật toán mạng/đồ thị |

---

# PHẦN A — KIẾN THỨC NỀN TẢNG (gốc rễ)

## A1. Truyền thông số cơ bản

### A1.1 — BER là gì? Khác BLER, SER, FER thế nào?

> **Gợi ý:**
> - **BER** (Bit Error Rate) = số bit lỗi / tổng số bit truyền. Đo ở mức bit.
> - **SER** (Symbol Error Rate) = số symbol lỗi / tổng symbol. Một symbol mang nhiều bit (QPSK = 2 bit, 256QAM = 8 bit).
> - **BLER** (Block Error Rate) = số block lỗi / tổng block. Một block lỗi nếu CRC sai **sau khi giải mã FEC**. Đây là metric chính của HARQ (vì HARQ phát lại theo block).
> - **FER** (Frame Error Rate) ≈ BLER, dùng ở lớp cao hơn.
>
> **Quan hệ BER ↔ SER:** với Gray coding, mỗi symbol lỗi thường chỉ sai 1 bit → BER ≈ SER / log₂(M).
> **Quan hệ BER ↔ BLER:** block n bit, lỗi độc lập, không mã hóa → BLER ≈ 1 − (1−BER)ⁿ. Có FEC thì phi tuyến (FEC sửa được vài bit lỗi → BLER giảm mạnh).

### A1.2 — Tốc độ bit, tốc độ symbol, baud rate khác nhau thế nào?

> **Gợi ý:**
> - **Symbol rate (baud)** = số symbol/giây = R_s.
> - **Bit rate** = R_s × log₂(M) × code_rate. Ví dụ QPSK (M=4) baud 1 Msym/s → 2 Mbit/s thô.
> - **Baud ≠ bit rate** trừ khi BPSK (1 bit/symbol).
> - Bậc điều chế càng cao (256QAM) → nhiều bit/symbol → tốc độ bit cao, nhưng cần SNR cao hơn và nhạy nhiễu hơn.

### A1.3 — Eb/N0, Es/N0, SNR, SINR khác nhau?

> **Gợi ý:**
> - **SNR** = công suất tín hiệu / công suất nhiễu (toàn băng).
> - **Es/N0** = năng lượng mỗi **symbol** / mật độ phổ nhiễu. (Dự án NTN của tôi dùng Es/N0.)
> - **Eb/N0** = năng lượng mỗi **bit thông tin** / N0 — metric "công bằng" để so sánh các MCS khác nhau.
> - Quan hệ: Es/N0 [dB] = Eb/N0 [dB] + 10·log₁₀(log₂M × r), với r = code rate.
> - **SINR** = signal / (interference + noise) — dùng khi có nhiễu từ cell/beam khác (đa người dùng).

### A1.4 — Định lý Shannon. Spectral efficiency là gì?

> **Gợi ý:**
> - **Shannon–Hartley:** C = B·log₂(1 + SNR) [bit/s]. Đây là dung lượng tối đa lý thuyết, không lỗi.
> - **Spectral efficiency** = C/B = log₂(1+SNR) [bit/s/Hz] — số bit truyền được trên mỗi Hz băng thông.
> - Trong dự án tôi, SE Goodput = util × (1−BLER) × r × log₂M — chính là SE thực tế đạt được sau khi trừ pipeline stall và lỗi.
> - **LDPC gap 1.5 dB** = khoảng cách thực thi từ giới hạn Shannon, vì mã thực không hoàn hảo.

### A1.5 — Tại sao QPSK phổ biến? 256QAM ưu/nhược điểm?

> **Gợi ý:**
> - QPSK: 2 bit/symbol, chòm sao 4 điểm cách xa → chịu nhiễu tốt, robust. Dùng khi SNR thấp (biên cell, vệ tinh).
> - 256QAM: 8 bit/symbol → tốc độ cao gấp 4 lần, nhưng 256 điểm sát nhau → cần SNR cao (~24 dB), rất nhạy nhiễu pha và phi tuyến.
> - Trade-off này chính là lý do có **AMC** (Adaptive Modulation & Coding): SNR cao dùng MCS cao, SNR thấp hạ xuống QPSK.
> - Trong dự án: MCS A (QPSK r=1/2) làm việc ở 0.7 dB; MCS B (256QAM r=8/9) cần 3.9 dB — chênh 3.2 dB.

### A1.6 — Constellation diagram, Gray coding, EVM?

> **Gợi ý:**
> - **Chòm sao**: biểu diễn symbol trên mặt phẳng I/Q. Khoảng cách Euclid giữa điểm ↔ khả năng chống lỗi.
> - **Gray coding**: 2 điểm kề nhau chỉ khác 1 bit → khi symbol bị nhận nhầm sang điểm kề, chỉ sai 1 bit → giảm BER.
> - **EVM** (Error Vector Magnitude): đo sai lệch điểm thu so với điểm lý tưởng → đánh giá chất lượng máy phát/thu.

### A1.7 — Nyquist, pulse shaping, roll-off, ISI?

> **Gợi ý:**
> - **Nyquist rate**: tốc độ lấy mẫu ≥ 2× băng thông để khôi phục tín hiệu không méo.
> - **ISI** (Inter-Symbol Interference): symbol trước "rò" sang symbol sau do kênh tán xạ thời gian.
> - **Pulse shaping** (raised cosine, RRC): giới hạn băng thông + thỏa Nyquist (zero-ISI tại điểm lấy mẫu).
> - **Roll-off factor (α)**: 0 → băng thông tối thiểu nhưng pulse dài; α lớn → tốn băng thông nhưng dễ thực thi. Băng thông = R_s(1+α).

---

## A2. Kênh truyền và lan truyền sóng

### A2.1 — Path loss. Công thức FSPL?

> **Gợi ý:**
> - **Free-Space Path Loss:** FSPL [dB] = 20·log₁₀(d) + 20·log₁₀(f) + 32.45 (d tính km, f tính MHz).
> - Suy hao tỉ lệ d² và f² → tần số càng cao, khoảng cách càng xa, suy hao càng lớn.
> - GEO ở 35 786 km, Ka band 20 GHz → FSPL ≈ 210 dB. Đây là lý do vệ tinh cần anten gain rất cao và EIRP lớn.

### A2.2 — Fading: large-scale vs small-scale? Flat vs frequency-selective? Fast vs slow?

> **Gợi ý:**
> - **Large-scale**: path loss + shadowing (che khuất bởi vật thể lớn), biến đổi chậm theo khoảng cách.
> - **Small-scale (multipath fading)**: giao thoa nhiều tia → biên độ dao động nhanh.
> - **Flat fading**: băng thông tín hiệu < coherence bandwidth → toàn bộ băng bị fade như nhau (dự án tôi giả định flat).
> - **Frequency-selective**: băng tín hiệu > coherence BW → các tần số fade khác nhau → cần equalizer/OFDM.
> - **Fast fading**: kênh đổi nhanh hơn 1 symbol (T_c < T_symbol); **slow**: kênh ổn định qua nhiều symbol.

### A2.3 — Rician vs Rayleigh? Hệ số K?

> **Gợi ý:**
> - **Rayleigh**: không có tia trực tiếp (NLOS), chỉ tán xạ → fade sâu, K=0.
> - **Rician**: có tia LOS trội + tán xạ. **K = công suất LOS / công suất tán xạ**.
> - K = 15 dB ≈ 31.6 lần → LOS chiếm ~97% công suất → kênh ổn định, ít fade sâu.
> - Vệ tinh trên cao → thường LOS rõ → Rician phù hợp hơn Rayleigh. K càng cao, BER waterfall càng dốc.

### A2.4 — Doppler shift. Tại sao LEO Doppler lớn?

> **Gợi ý:**
> - **f_D = (v/c)·f_c·cos(θ)**. LEO bay ~7.5 km/s → tại Ka band 20 GHz, Doppler đỉnh ±500 kHz.
> - Không chỉ shift mà còn **Doppler rate** (tốc độ thay đổi) lớn → cần bù Doppler động (frequency tracking).
> - GEO gần như đứng yên so với mặt đất → Doppler ≈ 0.
> - Doppler ảnh hưởng đến SCS: SCS phải đủ lớn để chống ICI (inter-carrier interference) do Doppler.

### A2.5 — Coherence time, coherence bandwidth?

> **Gợi ý:**
> - **Coherence time T_c ≈ 0.423/f_D**: thời gian kênh còn "giống chính nó". Liên quan Doppler.
> - **Coherence bandwidth B_c ≈ 1/(5·στ)**: dải tần kênh fade giống nhau. Liên quan delay spread.
> - Trong dự án: T_c ≈ 0.46 ms ≈ T_slot (SCS 30 kHz) → các lần phát lại HARQ gặp kênh gần độc lập → hợp lý dùng mô hình i.i.d.

### A2.6 — Link budget gồm những gì?

> **Gợi ý:**
> - **C/N0 = EIRP − FSPL − suy hao khác + G/T − k** (k = Boltzmann = −228.6 dBW/K/Hz).
> - Thành phần: công suất phát, gain anten phát (→ EIRP), suy hao đường truyền, suy hao mưa/khí quyển, gain anten thu / nhiệt tạp âm hệ thống (→ G/T).
> - **Margin** = C/N0 thực − C/N0 yêu cầu. Dương → link hoạt động.

### A2.7 — Nhiễu nhiệt, Noise Figure?

> **Gợi ý:**
> - **Nhiễu nhiệt**: N = kTB (k Boltzmann, T nhiệt độ, B băng thông). Ở 290K, −174 dBm/Hz.
> - **Noise Figure (NF)**: mức tạp âm bộ thu thêm vào so với lý tưởng. NF thấp → bộ thu nhạy hơn.
> - **G/T** (figure of merit bộ thu vệ tinh) = gain anten / nhiệt tạp âm hệ thống [dB/K] — càng cao càng tốt.

---

## A3. Anten và RF

### A3.1 — Gain, Directivity, Efficiency của anten?

> **Gợi ý:**
> - **Directivity**: mức độ tập trung năng lượng theo hướng (so với anten đẳng hướng).
> - **Gain** = directivity × efficiency. Tính bằng dBi (so với isotropic).
> - Anten parabol lớn → gain cao → beam hẹp. Gain ∝ (D/λ)² (D đường kính, λ bước sóng).
> - Tần số cao (Ka) → λ nhỏ → cùng kích thước vật lý cho gain cao hơn → lý do vệ tinh dùng Ka band.

### A3.2 — Phân cực anten: tuyến tính vs tròn? Tại sao vệ tinh dùng phân cực tròn?

> **Gợi ý (câu này hay được hỏi cho NTN):**
> - **Phân cực tuyến tính**: V (đứng) / H (ngang) — vector E dao động theo 1 phương.
> - **Phân cực tròn**: RHCP / LHCP — vector E quay tròn. Tổng hợp 2 thành phần vuông pha lệch 90°.
> - **Vệ tinh dùng phân cực tròn** vì:
>   1. **Faraday rotation**: tầng điện ly làm quay mặt phẳng phân cực của sóng tuyến tính → máy thu lệch phương → suy hao mismatch. Sóng tròn **không bị** ảnh hưởng bởi hiệu ứng này.
>   2. Không cần căn chỉnh chính xác hướng anten (V hay H) — thiết bị di động, cầm tay xoay tự do vẫn thu được.
> - **Polarization mismatch loss** (tuyến tính): L = cos²(θ), θ là góc lệch 2 anten. Lệch 90° → mất hoàn toàn (∞ dB).
> - **XPD** (Cross-Polarization Discrimination): mức cô lập giữa 2 phân cực. Dùng 2 phân cực trực giao (V+H hoặc RHCP+LHCP) → **polarization multiplexing** gấp đôi dung lượng trên cùng tần số.

### A3.3 — EIRP, ERP là gì?

> **Gợi ý:**
> - **EIRP** (Effective Isotropic Radiated Power) = P_tx + G_tx [dBW]. Công suất "tương đương" nếu phát đẳng hướng.
> - Đặc trưng "độ mạnh" của máy phát theo hướng búp sóng.
> - ERP dùng anten dipole nửa sóng làm chuẩn (EIRP − 2.15 dB).

### A3.4 — Beamforming, phased array?

> **Gợi ý:**
> - **Phased array**: nhiều phần tử anten, điều khiển pha từng phần tử → "lái" búp sóng điện tử mà không cần xoay cơ học.
> - **Beamforming**: tạo búp sóng định hướng → tăng gain theo hướng UE, giảm nhiễu hướng khác.
> - Vệ tinh LEO dùng multi-beam: nhiều búp phủ nhiều vùng, tái sử dụng tần số giữa các búp cách xa.
> - **Beam squint/Doppler**: với LEO di chuyển nhanh, phải cập nhật beam liên tục (beam management).

### A3.5 — Friis, VSWR, return loss, impedance matching?

> **Gợi ý:**
> - **Friis**: P_rx = P_tx·G_tx·G_rx·(λ/4πd)² — phương trình truyền cơ bản.
> - **Impedance matching**: trở kháng anten phải khớp đường truyền (50Ω) để truyền tối đa công suất.
> - **VSWR** (Voltage Standing Wave Ratio): đo độ mismatch. VSWR = 1 là hoàn hảo; cao → phản xạ nhiều.
> - **Return loss**: công suất phản xạ ngược [dB], càng lớn (âm sâu) càng tốt.

---

## A4. Đặc thù vệ tinh / NTN

### A4.1 — Góc ngẩng (elevation angle) là gì? Tại sao quan trọng?

> **Gợi ý (câu này hay hỏi):**
> - **Góc ngẩng**: góc giữa đường chân trời và đường nối UE → vệ tinh. 90° = thẳng đỉnh đầu, 0° = ngang chân trời.
> - Góc ngẩng **cao** → tốt: slant range ngắn hơn → ít suy hao, ít che khuất, K-factor cao hơn (LOS rõ), ít đi qua khí quyển.
> - Góc ngẩng **thấp** → xấu: đường truyền qua nhiều tầng khí quyển → suy hao mưa/khí quyển lớn, dễ bị tòa nhà/cây che, K-factor thấp.
> - **Min elevation angle** thường chọn 10° cho NTN (TR 38.811) — dưới đó link quá kém.
> - Trong dự án tôi: RTT lấy ở elevation 10° (trường hợp xấu nhất, slant range dài nhất).

### A4.2 — Slant range khác độ cao quỹ đạo thế nào?

> **Gợi ý:**
> - **Độ cao quỹ đạo (h)**: khoảng cách thẳng đứng vệ tinh đến mặt đất.
> - **Slant range (d)**: khoảng cách thực UE → vệ tinh, luôn ≥ h (trừ khi elevation = 90°).
> - Công thức: d = √(R_E²sin²(el) + h² + 2hR_E) − R_E·sin(el), R_E ≈ 6371 km.
> - LEO 600 km nhưng ở elevation 10° → slant range ~1900 km → RTT tính theo slant range, không phải độ cao.
> - Đây là lý do RTT LEO_600 = 12.88 ms chứ không phải 2×600/c = 4 ms.

### A4.3 — Các băng tần vệ tinh? Tại sao NTN dùng Ka?

> **Gợi ý:**
> - L (1–2 GHz), S (2–4), C (4–8), Ku (12–18), **Ka (26.5–40, NTN dùng ~20/30 GHz)**.
> - Tần thấp (L/S): suy hao thấp, xuyên mây mưa tốt, nhưng băng thông hẹp (dùng cho IoT, thoại vệ tinh).
> - Ka band: băng thông rộng → tốc độ cao, anten nhỏ gain cao, nhưng **suy hao mưa nặng** (rain fade) và cần LOS tốt.
> - Trade-off: dung lượng (Ka) vs độ tin cậy (L/S).

### A4.4 — Rain fade, atmospheric attenuation?

> **Gợi ý:**
> - **Rain fade**: mưa hấp thụ/tán xạ sóng, nặng ở tần cao (Ka). Có thể mất hàng chục dB.
> - **Atmospheric attenuation**: hấp thụ bởi oxy (~60 GHz peak), hơi nước (~22 GHz).
> - Đối phó: power control, ACM (adaptive coding modulation), site diversity (nhiều trạm mặt đất).

### A4.5 — Payload: transparent vs regenerative?

> **Gợi ý:**
> - **Transparent (bent-pipe)**: vệ tinh chỉ khuếch đại + chuyển tần, không xử lý. Đơn giản, nhưng RTT = full đường UE→sat→gateway→sat→UE.
> - **Regenerative**: vệ tinh giải mã/xử lý/tái tạo tín hiệu (gNB trên vệ tinh). RTT ngắn hơn (chỉ UE↔sat), xử lý HARQ trên vệ tinh được.
> - Dự án tôi dùng RTT regenerative (UE↔sat). Nếu transparent, RTT gấp đôi → N_min càng tệ.

### A4.6 — Handover trong LEO?

> **Gợi ý:**
> - LEO bay nhanh → mỗi vệ tinh chỉ phủ một điểm vài phút → **handover liên tục** giữa các vệ tinh.
> - Khác mạng mặt đất (UE di chuyển), ở đây **vệ tinh** di chuyển → handover do quỹ đạo, dự đoán được trước.
> - Thách thức: đồng bộ, duy trì session, độ trễ handover.

---

## A5. 5G NR cơ bản

### A5.1 — OFDM. Tại sao 5G dùng OFDM?

> **Gợi ý:**
> - Chia băng rộng thành nhiều sóng mang con (subcarrier) trực giao hẹp → mỗi subcarrier gặp **flat fading** thay vì frequency-selective.
> - Chống ISI bằng **Cyclic Prefix (CP)**: copy đuôi symbol lên đầu → hấp thụ multipath delay.
> - Trực giao → subcarrier chồng phổ nhưng không nhiễu nhau → hiệu quả phổ cao.
> - Nhược: PAPR cao (đỉnh công suất lớn), nhạy Doppler/CFO.

### A5.2 — Numerology, SCS, slot? Tại sao SCS cao cần nhiều HARQ process hơn?

> **Gợi ý:**
> - **Numerology μ**: SCS = 15·2^μ kHz. μ=0→15kHz, μ=1→30, μ=2→60, μ=3→120.
> - **Slot** = 14 OFDM symbol. Slot duration = 1ms / 2^μ → SCS cao → slot ngắn.
> - SCS 15→0.5ms? Không: 15kHz→1ms, 30→0.5ms, 60→0.25ms, 120→0.125ms.
> - **Nghịch lý HARQ**: SCS cao → T_slot ngắn → N_min = ⌈RTT/T_slot⌉+1 **tăng**. SCS 120 kHz ở GEO cần 2166 process! Băng thông lớn không rút ngắn RTT.

### A5.3 — Resource Block, Resource Element?

> **Gợi ý:**
> - **RE** (Resource Element): 1 subcarrier × 1 OFDM symbol — đơn vị nhỏ nhất.
> - **RB** (Resource Block): 12 subcarrier liên tiếp. Đơn vị cấp phát tài nguyên.
> - Scheduler gNB cấp RB cho UE theo nhu cầu + chất lượng kênh.

### A5.4 — MCS, CQI, AMC?

> **Gợi ý:**
> - **CQI** (Channel Quality Indicator): UE báo chất lượng kênh về gNB.
> - **MCS** (Modulation & Coding Scheme): tổ hợp điều chế + code rate. MCS thấp (QPSK r=1/2) robust; cao (256QAM r=8/9) tốc độ cao.
> - **AMC**: gNB chọn MCS theo CQI → tối đa throughput trong khi giữ BLER mục tiêu (thường 10%).
> - Trong NTN, RTT cao → CQI bị **lỗi thời** (outdated) khi đến gNB → AMC kém hiệu quả → đây là một thách thức NTN.

### A5.5 — RLC ARQ vs HARQ? Tại sao có cả hai?

> **Gợi ý:**
> - **HARQ** (lớp MAC): nhanh, kết hợp tín hiệu (CC/IR), sửa lỗi tầng vật lý. Feedback nhanh trong slot.
> - **RLC ARQ** (lớp RLC): chậm hơn, không kết hợp tín hiệu, làm "lưới an toàn" cho các lỗi HARQ sót lại.
> - Hai tầng bổ sung: HARQ bắt lỗi nhanh phần lớn, RLC ARQ dọn phần còn lại.
> - **Kết luận dự án tôi**: ở GEO, HARQ bị pipeline stall (util 5.89%), nên **tắt HARQ + chỉ dùng RLC ARQ** lại tốt hơn 16.7× về SE (TR 38.821 khuyến nghị).

---

# PHẦN B — CÂU HỎI THEO TỪNG DỰ ÁN

## B1. 🛰️ 5G NTN HARQ

### Cơ bản
- "NTN là gì? Khác mạng mặt đất ở điểm nào quan trọng nhất?" → RTT cao (13–271 ms), Rician LOS mạnh, path loss lớn, Doppler cao.
- "LEO/MEO/GEO — cái nào tốt nhất? Tại sao không dùng GEO hết?" → GEO RTT 270ms không real-time được; LEO RTT thấp nhưng cần constellation.
- "5G NTN chuẩn hóa ở đâu?" → 3GPP Release 17: TR 38.811, TR 38.821.
- "HARQ khác ARQ?" → HARQ lưu + kết hợp tín hiệu cũ; ARQ bỏ.
- "CC vs IR khác nhau?" → CC: cùng bit, MRC, SNR cộng trước log. IR: bit dư thừa mới, MI cộng độc lập. IR ≥ CC (Jensen).

### Sâu
- "Chứng minh IR > CC?" → Jensen: log(1+(γ₁+γ₂)/Δ) ≤ log(1+γ₁/Δ)+log(1+γ₂/Δ).
- "Pipeline stall? N_min? Tại sao GEO bất khả thi?" → N_min=⌈RTT/T_slot⌉+1=543 ở GEO, giới hạn 32 → util 5.89%.
- "Tại sao Rician không Rayleigh?" → Vệ tinh có LOS rõ, K=15dB → LOS chiếm 97%.
- "K=15dB từ đâu?" → Tuninato 2025 + TR 38.811, điển hình open-sky elevation cao.
- "LDPC gap 1.5dB?" → Mã thực cách Shannon 1.5dB (Richardson & Urbanke).
- "Monte Carlo cần bao nhiêu trial cho BLER 10⁻³?" → N≈1/(p·ε²); 20000 cho ε≈22%, đủ cho đường BLER, kém ở vùng <10⁻⁵.
- "Xác minh kết quả thế nào?" → CDF Rician (ncx2 scipy) cho TX=1, sai lệch <0.1dB; so Tuninato Fig.6.

### Phản biện
- "Mô hình i.i.d. khi nào sai?" → UE tĩnh, T_c >> T_slot → kênh tương quan → i.i.d. là cận trên lợi ích.
- "Hạn chế lớn nhất?" → Kênh 1 trạng thái (thực tế Markov good/bad), bỏ overhead lớp cao, flat fading.
- "FPT triển khai thực được ngay không?" → Không trực tiếp; cần link budget thực, SDR test, scheduler đầy đủ. Nhưng cho guideline: LEO→IR-HARQ, GEO→disable+RLC.

---

## B2. 🌊 Định tuyến mạng cảm biến dưới nước (UWSN)

### Cơ bản
- "Tại sao không dùng WiFi/4G dưới nước?" → RF bị nước biển hấp thụ (~200 dB/km). Dùng **sóng âm** (1500 m/s) → latency cao, BW thấp (kHz).
- "Khác mạng cảm biến trên cạn?" → Kênh acoustic, node trôi theo dòng (3D động), pin khó thay, BW hẹp, propagation delay lớn.
- "Ứng dụng?" → Giám sát biển, cảnh báo sóng thần, thăm dò dầu khí, quân sự, thủy sản.

### Kỹ thuật
- "VBF, DBR, EEDBR khác nhau?" → VBF: định tuyến theo ống vector nguồn-đích. DBR: ưu tiên node gần mặt nước (theo độ sâu). EEDBR: DBR + trọng số năng lượng.
- "Void hole problem?" → Vùng không có node forward → drop gói. Giải: geographic routing + fallback, anypath, AUV relay di động.
- "Tại sao geographic routing chứ không AODV/OSPF?" → Topology đổi liên tục → bảng định tuyến overhead quá lớn với BW hẹp; geographic không cần bảng.
- "Metric đánh giá?" → PDR, end-to-end delay, energy/bit, network lifetime.
- "Energy harvesting?" → Sóng (piezo), dòng chảy (turbine), gradient nhiệt → ảnh hưởng chiến lược cân bằng tải năng lượng.

### Phản biện
- "Mô phỏng bằng gì?" → AQUA-Sim (NS2), NS3, MATLAB. Mobility: Gauss-Markov, random walk 3D.
- "Sai số mô phỏng vs thực tế?" → Acoustic channel thực phức tạp (multipath, Doppler, noise tàu) → Bellhop/Urick model có sai số lớn.

---

## B3. 🤖 AI nhận diện mặt đồng hồ số

### Cơ bản
- "Input/output là gì?" → Input: ảnh đồng hồ số. Output: giá trị hiển thị. Pipeline: detect → segment → recognize.
- "Tại sao khó hơn MNIST?" → Biến dạng góc, phản chiếu ánh sáng, màu LED đa dạng, font 7-segment, background nhiễu.
- "Dùng model gì? Tại sao?" → YOLO detect + CNN/ResNet recognize, hoặc OCR (CRNN/EasyOCR). Trade-off accuracy/latency/size.

### Kỹ thuật
- "Dataset? Augmentation?" → Tự chụp + tổng hợp. Aug: rotation, brightness, contrast, noise, perspective warp.
- "Transfer learning từ đâu? Tại sao không from scratch?" → ImageNet pretrained; dataset nhỏ + tiết kiệm tài nguyên. Freeze backbone → train head → unfreeze dần.
- "Metric? Tại sao Accuracy không đủ?" → Precision/Recall/F1/mAP. Class imbalance → accuracy đánh lừa.
- "Real-time? Latency?" → Nêu inference time trên hardware. Optimize: quantization INT8, pruning, ONNX, TensorRT.
- "Tại sao không Tesseract trực tiếp?" → Tesseract cho chữ in, không tối ưu 7-segment LED → cần fine-tune/pipeline custom.

### Thực tế hóa
- "Deploy nhà máy cần gì?" → Edge (Jetson/RPi), pipeline ổn định, logging, alert khi sai, calibration ánh sáng.
- "Khi nào fail?" → Tối/sáng quá, mờ/ướt, góc cực đoan, dấu thập phân, số bị che.

---

## B4. 📡 DT-ISAC

### Cơ bản
- "DT là gì? ISAC là gì? Tại sao kết hợp?" → DT: bản sao số real-time cập nhật từ sensor. ISAC: sóng vừa truyền data vừa cảm biến (như radar). Closed-loop: ISAC sense → cập nhật DT → DT tối ưu ISAC.
- "ISAC khác radar + comm riêng?" → Riêng tốn 2× băng tần, can nhiễu. ISAC một waveform/phần cứng → hiệu quả phổ, nhưng trade-off sensing vs throughput.
- "DT trong viễn thông ứng dụng?" → Predictive beamforming, RRM, anomaly detection, network planning.

### Kỹ thuật
- "Waveform ISAC trade-off?" → Sensing muốn autocorrelation tốt (OFDM/FMCW); comm muốn SE cao. OFDM là ứng viên tốt.
- "Beamforming vừa comm vừa sense?" → Dual-function: precoding đảm bảo SINR UE + định hướng sense. Dual beam hoặc shared beam.
- "Latency vòng lặp DT-ISAC?" → sensing + DT update + optimize + feedback. Mobility tracking <10ms, optimization <1s.
- "DT mô hình bằng gì?" → Physics-based (ray tracing) / data-driven (NN) / hybrid. Trade-off chính xác vs tốc độ vs out-of-distribution.
- "Metric đánh giá?" → Comm: SE, SINR. Sensing: RMSE vị trí/vận tốc, detection prob, false alarm, resolution. DT: divergence DT vs physical.

### Phản biện
- "ISAC thực sự tiết kiệm băng tần hay marketing?" → CRB cho sensing tối ưu ≠ waveform comm tối ưu → có Pareto frontier. Nhưng so 2 hệ riêng (2× BW) thì ISAC hiệu quả hơn.
- "5G NR phù hợp ISAC không?" → OFDM ok, nhưng pilot fixed không tối ưu sense, CP giới hạn range resolution, đồng bộ timing. Release 18 đang nghiên cứu NR sensing.

---

# PHẦN C — CÂU HỎI CHUNG (mọi dự án)

- "Giải thích dự án trong 2 phút." → Chuẩn bị elevator pitch: bài toán → approach → **con số kết quả** → ý nghĩa.
- "Từ 0–10, bạn hiểu sâu dự án này bao nhiêu?" → Đừng nói 10. Nói 7–8 + giải thích phần chưa nắm.
- "Nếu làm lại, bạn làm gì khác?"
- "Paper quan trọng nhất bạn đọc?"
- "Có publish không? Plan submit paper?"
- "Thêm 3 tháng thì mở rộng gì?"
- "Đóng góp cụ thể của bạn trong nhóm?"

---

# PHẦN D — MẸO CHUẨN BỊ CHO FPT

1. **Nhớ con số cụ thể** — đây là điểm khác biệt với SV nói định tính:
   - NTN: 8.3 dB gain (IR TX=4), util 5.89% (GEO), SE ×16.7 (RLC vs HARQ), N_min=543, energy ×10⁹ (SNR thấp).
2. **Luôn có lý do kỹ thuật** cho mỗi lựa chọn — không bao giờ "vì thầy bảo" / "vì đơn giản".
3. **Tự nêu hạn chế có kiểm soát** — chứng tỏ tư duy phê phán, tốt hơn bị hỏi mà ngắc ngứ.
4. **Vẽ được sơ đồ** — chuẩn bị tay vẽ nhanh: kiến trúc HARQ pipeline, chòm sao QPSK/QAM, đường BER waterfall, hình học góc ngẩng/slant range.
5. **Liên hệ với FPT** — 5G (FPT Telecom), AI (FPT AI), edge/IoT (FPT Software) — cho thấy bạn biết họ làm gì.
6. **Trung thực khi không biết** — "Em chưa nghiên cứu sâu phần đó, nhưng em nghĩ hướng tiếp cận là..." tốt hơn bịa.

---

> **Ưu tiên ôn:** Phần A (nền tảng) → B1 (NTN, dễ bị khoan sâu nhất) → các phần còn lại. Câu A1.1 (BER/BLER), A1.3 (Eb/N0), A3.2 (phân cực tròn), A4.1 (góc ngẩng), A5.2 (SCS↔N_min) là các câu "gốc rễ" hay xuất hiện nhất.
