# Notebook 11 — Kết luận và Hướng phát triển

---

## 1. Tóm tắt kết quả

Đề tài đánh giá hiệu quả HARQ trong mạng 5G NTN thông qua mô phỏng Monte Carlo trên 5 chiều: (i) BLER vs SNR, (ii) SE Goodput vs RTT, (iii) yêu cầu tiến trình N_min, (iv) so sánh HARQ/RLC ARQ tại GEO, (v) hiệu quả năng lượng.

### Kết luận 1: HARQ mang lại lợi ích link đáng kể ở LEO

Tại LEO 600 km (K = 15 dB, MCS A QPSK r = 1/2), IR-HARQ với 4 lần phát cải thiện Es/N₀ yêu cầu **8.3 dB** so với không có HARQ (từ 0.8 dB xuống −7.5 dB tại BLER = 10⁻³). CC-HARQ đạt lợi ích thấp hơn 0.5 dB do bất đẳng thức Jensen bất lợi cho MRC so với tích lũy MI (Tuninato 2025, Mục V.C). Lợi ích này nhất quán với kết quả Hình 6 của Tuninato 2025 (~8 dB cho IR TX=4).

### Kết luận 2: Pipeline stall là rào cản kiến trúc cho quỹ đạo cao

Giới hạn N ≤ 32 tiến trình HARQ (TS 38.214 Mục 5.1) chỉ đủ để tránh pipeline stall tại:
- LEO 600 km với SCS ≤ 30 kHz (N_min = 14–27)  
- LEO 1200 km với SCS = 15 kHz (N_min = 26)

Ở MEO và GEO, N_min vượt 32 tại **mọi** cấu hình SCS được nghiên cứu. Ví dụ điển hình: GEO SCS 30 kHz cần N_min = 543, gấp 17× giới hạn 3GPP (Tuninato 2025, Mục IV.A; TR 38.821 Mục 6.4).

### Kết luận 3: Tại GEO, vô hiệu hóa HARQ và dùng RLC ARQ là lựa chọn vượt trội

SE Goodput tăng **16.7×** (từ 0.030 lên 0.500 bit/s/Hz) khi chuyển từ HARQ-IR (N=32) sang RLC ARQ tại GEO Es/N₀ = 5 dB. Độ trễ end-to-end gần tương đương (~540 vs ~620 ms) do cả hai đều bị chi phối bởi RTT truyền sóng GEO = 270.57 ms (TR 38.811, Bảng 5.3.4.1-1). Kết quả này là bằng chứng định lượng cho khuyến nghị của TR 38.821 Mục 6.4.2.

### Kết luận 4: HARQ cải thiện hiệu quả năng lượng đột phá ở SNR thấp

Tại Es/N₀ = −5 dB, năng lượng/bit giảm ~10⁹× khi có HARQ (so với No HARQ). Ở SNR cao (> 5 dB) cả ba sơ đồ hội tụ về cùng E_bit ≈ P_tx × T_slot / k ≈ 3 × 10⁻³ J/bit (avg_ntx → 1, BLER → 0). Lợi ích năng lượng của HARQ đặc biệt quan trọng với đầu cuối IoT vệ tinh hoặc thiết bị di động NTN có công suất giới hạn.

---

## 2. Đóng góp gốc của đề tài

So với Tuninato 2025, đề tài này bổ sung:

1. **Phân tích N_min toàn diện theo 4 quỹ đạo × 4 cấu hình SCS** với bảng khả thi rõ ràng (Sim 03), thay vì chỉ phân tích GEO đơn lẻ.
2. **Chỉ tiêu năng lượng/bit** (Sim 05) — không có trong Tuninato 2025 — cho thấy tác động của pipeline stall lên hiệu quả năng lượng theo quỹ đạo: GEO tiêu tốn ~17× năng lượng/bit so với LEO_600 ở cùng SNR do util = 5.89%.
3. **Xác minh lý thuyết độc lập** bằng CDF Rician (ncx2) cho tất cả kết quả BLER, đảm bảo mô hình không bị hard-fit theo số liệu bài báo.

---

## 3. Hướng phát triển

### 3.1 Ngắn hạn (cải tiến mô hình)

- **Kênh hai trạng thái LMS:** Triển khai chuỗi Markov good/bad theo TR 38.811 Mục 6.7.2 để mô hình hóa che khuất. Trạng thái "bad" với K << 15 dB sẽ tăng BLER burst và giảm hiệu quả HARQ trong điều kiện khuất tầm nhìn thực tế.
- **Tương quan thời gian:** Dùng Jake's model đúng (i.i.d. phases) để mô phỏng fading có tương quan giữa các TX. Khi T_slot << T_c (coherence time), các TX liên tiếp có |h|² tương quan cao → lợi ích phân tập giảm.
- **Mô hình LDPC thực:** Thay MI-threshold bằng giải mã LDPC số nguyên (như trong OpenAirInterface) để kiểm chứng LDPC gap thực tế.

### 3.2 Trung hạn (mở rộng nghiên cứu)

- **HARQ với N mở rộng:** 3GPP Release 17/18 đang nghiên cứu tăng giới hạn tiến trình HARQ hoặc dùng HARQ không đồng bộ (TR 38.821 Mục 6.4.3). Đánh giá lợi ích thực tế nếu N_max = 128 hoặc 512.
- **HARQ kết hợp precoding vệ tinh:** Trong LEO đa chùm (multi-beam), MIMO kết hợp với HARQ có thể tăng thêm phân tập không gian. Cần phân tích trade-off với overhead phản hồi CSI qua RTT cao.
- **Tối ưu hóa MCS thích nghi:** Kết hợp link adaptation (AMC) với HARQ trong NTN: chọn MCS phù hợp theo trạng thái kênh dự đoán (Doppler-based prediction) để giảm số lần phát lại trung bình.

### 3.3 Dài hạn (thiết kế giao thức)

- **Kiến trúc HARQ cho LEO regenerative:** Với payload tái sinh trên vệ tinh LEO, có thể triển khai xử lý HARQ trên vệ tinh thay vì ground station, giảm RTT hiệu dụng. Cần phân tích lại N_min dựa trên RTT nội bộ satellite–UE (~12 ms) thay vì RTT end-to-end.
- **Tiêu chuẩn hóa HARQ NTN:** Theo dõi quá trình chuẩn hóa 3GPP Release 19 về HARQ enhancement cho NTN (Work Item RP-231467) và đánh giá tác động lên kết quả mô phỏng này.

---

## 4. Đề xuất cấu hình thực tế

Dựa trên kết quả mô phỏng, đề xuất cấu hình HARQ tối ưu cho từng quỹ đạo:

| Quỹ đạo | Khuyến nghị | Lý do |
|---|---|---|
| LEO 600 km | IR-HARQ, max_retx=3, SCS 15–30 kHz | Pipeline không stall; IR cho lợi ích tối đa |
| LEO 1200 km | IR-HARQ, max_retx=3, SCS 15 kHz | Chỉ SCS 15 kHz khả thi; SCS cao gây stall |
| MEO 10000 km | HARQ disabled hoặc N mở rộng | N_min = 95–749 vượt xa giới hạn 32 |
| GEO 35786 km | **HARQ disabled + RLC ARQ** | SE tăng 16.7×; RLC window đủ lớn bù RTT |

---

## 5. Kết luận tổng quát

HARQ là cơ chế không thể thiếu trong 5G NTN tầm thấp (LEO) nơi nó mang lại cả lợi ích link (7.7–8.8 dB SNR) lẫn hiệu quả năng lượng (10⁹× so với No HARQ ở SNR thấp). Tuy nhiên, cơ chế này bị phá vỡ bởi ràng buộc pipeline khi áp dụng cho quỹ đạo cao (MEO, GEO) do RTT vượt xa khả năng của tiêu chuẩn hiện tại (N ≤ 32). Điều này đòi hỏi sửa đổi giao thức ở cấp độ tiêu chuẩn 3GPP — một hướng nghiên cứu đang được tích cực thảo luận trong Release 17 và về sau.
