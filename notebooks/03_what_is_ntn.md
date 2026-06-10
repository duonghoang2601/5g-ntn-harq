# 03 — Mạng Không Mặt Đất (NTN): Cấu trúc, Quỹ đạo và Vai trò trong 5G

> **Mục tiêu:** Hiểu NTN là gì, tại sao 3GPP đưa NTN vào chuẩn 5G NR, và các kịch bản triển khai nào liên quan đến dự án này.

---

## 1. NTN là gì?

**NTN (Non-Terrestrial Network)** là mạng truy cập vô tuyến sử dụng nền tảng trên không gian hoặc trên không để phục vụ UE (User Equipment) trên mặt đất. Khác với mạng mặt đất (gNB cố định, khoảng cách <10 km), NTN có nền tảng bay ở độ cao hàng trăm đến hàng chục nghìn km.

Theo định nghĩa trong [TR 38.811, Mục 3.1]:
- **Vệ tinh (Satellite):** phương tiện trên không gian mang payload bent pipe hoặc regenerative.
- **Phương tiện trên không (Aerial):** UAS/HAPS ở độ cao 8–50 km, mang payload viễn thông bent pipe hoặc regenerative.

NTN bổ sung cho mạng mặt đất bằng cách cung cấp **phủ sóng 3D** — kết hợp vệ tinh, HAPS và mạng mặt đất [seminar Giordani 2025].

---

## 2. Các loại quỹ đạo vệ tinh

| Quỹ đạo | Độ cao | Đặc điểm |
|---|---|---|
| LEO (Low Earth Orbit) | 200–2.000 km | RTT thấp, phủ sóng di chuyển nhanh, cần chòm sao lớn |
| MEO (Medium Earth Orbit) | 2.000–35.786 km | Cân bằng giữa RTT và phủ sóng |
| GEO (Geostationary Orbit) | 35.786 km | RTT cao, đứng yên tương đối với mặt đất, phủ sóng rộng |
| HAPS | 8–50 km | Quasi-stationary, phục vụ vùng cục bộ |

Trong nghiên cứu 3GPP cho NTN, các quỹ đạo cụ thể được nghiên cứu là: **GEO tại 35.786 km**, **LEO tại 600 km và 1.200 km**, **MEO tại 10.000 km** [TR 38.811, Bảng 5.3.4.1-1, Bảng 5.3.2.1-1].

---

## 3. Hai loại kiến trúc payload

### 3.1. Bent Pipe (Transparent Payload)

Vệ tinh hoạt động như một **bộ chuyển tiếp RF thuần túy** — khuếch đại và chuyển đổi tần số tín hiệu mà không xử lý. gNB được đặt trên mặt đất (gateway).

Ưu điểm: vệ tinh đơn giản, chi phí thấp.
Nhược điểm: RTT bao gồm cả đường feeder link (gateway ↔ vệ tinh ↔ UE) → RTT lớn hơn regenerative [TR 38.811, Mục 4.7].

### 3.2. Regenerative Payload (gNB on Board)

Vệ tinh tích hợp toàn bộ hoặc một phần gNB — xử lý tín hiệu trực tiếp trên vệ tinh. RTT chỉ gồm đường user link (vệ tinh ↔ UE) → RTT nhỏ hơn [TR 38.811, Mục 4.7].

**Trong dự án này:** theo [Tuninato 2025, Mục IV.A], phân tích $N_{\min}$ được thực hiện cho **regenerative payload** — đây là trường hợp có RTT nhỏ nhất và thuận lợi nhất cho HARQ.

---

## 4. Các kịch bản triển khai 3GPP (D1–D5)

3GPP định nghĩa 5 kịch bản triển khai NTN trong [TR 38.811, Bảng 5.2-1]:

| Kịch bản | Quỹ đạo / Độ cao | Tần số | Beam pattern |
|---|---|---|---|
| D1 | GEO 35.786 km | Ka band (~20/30 GHz) | Earth fixed |
| D2 | GEO 35.786 km | S band (~2 GHz) | Earth fixed |
| D3 | LEO xuống 600 km | S band (~2 GHz) | Moving beams |
| D4 | LEO xuống 600 km | Ka band (~20/30 GHz) | Earth fixed |
| D5 | HAPS 8–50 km | dưới và trên 6 GHz | Earth fixed |

**Dự án này tập trung vào D3 (LEO S-band)** làm kịch bản chính và mở rộng so sánh sang D1 (GEO) và MEO.

---

## 5. Tại sao 3GPP đưa NTN vào chuẩn 5G?

Theo [TR 38.811, Mục 4.2], các use case chính của NTN trong 5G bao gồm:
- **Phủ sóng liên tục (continuous coverage):** vùng nông thôn, biển, hàng không — nơi mạng mặt đất không kinh tế.
- **Dự phòng mạng (network resilience):** khi thảm họa làm hỏng hạ tầng mặt đất.
- **IoT quy mô lớn:** thiết bị cảm biến phân tán toàn cầu không cần trạm gốc cố định.
- **Cầu nối số (digital divide):** mang Internet đến các vùng chưa được phục vụ.

NTN không thay thế mà **bổ sung** cho mạng mặt đất — mô hình hybrid terrestrial/non-terrestrial là định hướng của 5G Advanced và 6G [seminar Giordani 2025].

---

## 6. Những thách thức đặc thù của NTN so với mạng mặt đất

| Thách thức | Nguyên nhân | Ảnh hưởng đến HARQ |
|---|---|---|
| RTT lớn | Khoảng cách vệ tinh–UE | Pipeline stall → cần nhiều HARQ process |
| Doppler lớn | Vệ tinh LEO di chuyển ~7,5 km/s | ICI giữa subcarrier, ảnh hưởng channel estimation |
| Suy hao đường truyền lớn | Khoảng cách → $d^2$ trong Friis | SNR thấp → HARQ phải phát lại nhiều hơn |
| Kênh thay đổi chậm (GEO) hoặc nhanh (LEO) | Quỹ đạo, tốc độ vệ tinh | Ảnh hưởng coherence time giữa các retransmission |

Bảng độ trễ lan truyền thực tế theo [TR 38.811, Bảng 5.3.4.1-1 và 5.3.2.1-1]:

| Quỹ đạo | Payload | One-way delay | RTT |
|---|---|---|---|
| LEO 600 km | Bent Pipe | ~14.2 ms | ~28.4 ms |
| LEO 600 km | Regenerative | ~6.4 ms | ~12.9 ms |
| MEO 10.000 km | Regenerative | ~46.7 ms | ~93.5 ms |
| GEO 35.786 km | Bent Pipe | ~272.4 ms | ~544.8 ms |
| GEO 35.786 km | Regenerative | ~135.3 ms | ~270.6 ms |

---

## Tóm tắt

```
NTN = vệ tinh/HAPS thay thế/bổ sung gNB mặt đất
  → LEO: RTT thấp (~13–50 ms), HARQ có thể hoạt động với N lớn hơn
  → MEO: RTT trung bình (~100–190 ms), HARQ cần rất nhiều process
  → GEO: RTT rất lớn (~270–545 ms), HARQ gần như không khả thi
Kiến trúc: bent pipe (gNB dưới đất) vs regenerative (gNB trên vệ tinh)
  → regenerative có RTT nhỏ hơn → thuận lợi hơn cho HARQ
```

---

**File tiếp theo:** `04_ntn_breaks_harq.md` — RTT explosion và bài toán pipeline stall trong NTN
