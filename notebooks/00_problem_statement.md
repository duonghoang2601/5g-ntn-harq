# 00 — Bài toán gốc: Tại sao cần cơ chế đảm bảo độ tin cậy trong truyền thông không dây?

> **Mục tiêu:** Xây dựng trực giác từ đầu — kênh vô tuyến là gì, tại sao bit bị lỗi, tại sao lỗi là vấn đề nghiêm trọng, và tại sao vấn đề đó trở nên cực kỳ khó giải quyết trong mạng vệ tinh (NTN).

---

## 1. Kênh truyền vô tuyến — Môi trường không thể kiểm soát

Trong truyền thông có dây (cáp quang, cáp đồng), tín hiệu đi qua một môi trường vật lý được kiểm soát. Tỷ lệ lỗi bit (BER — Bit Error Rate) thường dưới $10^{-12}$.

Trong truyền thông vô tuyến, tín hiệu phải đi qua không khí — một môi trường không ai kiểm soát được, bị ảnh hưởng bởi ba hiện tượng chính:

### 1.1. Suy hao đường truyền (Path Loss)

Năng lượng tín hiệu suy giảm theo bình phương khoảng cách (phương trình Friis):

$$P_r = P_t \cdot G_t \cdot G_r \cdot \left(\frac{\lambda}{4\pi d}\right)^2$$

Trong đó $P_r$, $P_t$ là công suất thu/phát, $G_t$, $G_r$ là độ lợi anten, $\lambda$ bước sóng, $d$ khoảng cách.

> *Lưu ý trích dẫn: phương trình Friis là công thức giáo khoa chuẩn, chưa có trong bộ ref/ hiện tại. Cần bổ sung tài liệu giáo trình truyền thông vô tuyến.*

Trong 3GPP NTN, tổng suy hao đường truyền được phân rã thành nhiều thành phần [TR 38.811, Eq. 6.6-1]:

$$PL = PL_b + A_{gas} + A_{scint} + A_{e}$$

trong đó $PL_b$ là suy hao cơ bản, $A_{gas}$ là hấp thụ khí quyển, $A_{scint}$ là nhấp nhánh điện ly/đối lưu, $A_e$ là suy hao xâm nhập vào tòa nhà [TR 38.811, Mục 6.6.2].

**Ý nghĩa thực tế:** Vệ tinh LEO ở 600 km, GEO ở 35.786 km — khoảng cách tăng ~60 lần dẫn đến suy hao tăng thêm ~35 dB.

### 1.2. Fading đa đường (Multipath Fading)

Tín hiệu phản xạ, nhiễu xạ qua nhiều vật thể và đến máy thu theo nhiều đường với pha khác nhau — các phiên bản tín hiệu cộng hưởng hoặc triệt tiêu nhau, gây dao động biên độ ngẫu nhiên (fading).

Đối với kênh vệ tinh có thành phần đường thẳng tầm nhìn (LOS), mô hình Rician mô tả phân phối biên độ tín hiệu. Hệ số K đặc trưng cho tỷ lệ công suất LOS so với công suất tán xạ:

$$K = \frac{P_{\text{LOS}}}{P_{\text{tán xạ}}}$$

Hệ số $K$ càng cao → kênh càng ổn định. Trong mô phỏng của dự án này, chúng tôi sử dụng $K = 15$ dB và $K = 20$ dB — đây là các giá trị được lựa chọn trong nghiên cứu cơ sở [Tuninato 2025, Mục IV] để đánh giá hiệu năng HARQ trên kênh vệ tinh LEO 600 km.

Về phía chuẩn 3GPP, TR 38.811 định nghĩa mô hình kênh vệ tinh NTN theo dạng TDL (Tapped Delay Line). Với mô hình NTN-TDL-C, tap đầu tiên theo phân phối Rician với $K_1 = 10.224$ dB; với NTN-TDL-D, $K_1 = 11.707$ dB [TR 38.811, Bảng 6.9.2-3 và 6.9.2-4].

Mô hình kênh LMS (Land Mobile Satellite) dùng trong dự án sẽ được phân tích chi tiết trong `06_channel_model_lms.md`.

### 1.3. Nhiễu nhiệt (Thermal Noise)

Mọi hệ thống điện tử đều sinh ra nhiễu nhiệt với mật độ phổ công suất:

$$N_0 = k_B \cdot T \quad [\text{W/Hz}]$$

Trong đó $k_B = 1.38 \times 10^{-23}$ J/K là hằng số Boltzmann, $T$ là nhiệt độ hệ thống. Đây là giới hạn vật lý không thể tránh, quyết định SNR tối đa đạt được.

> *Lưu ý trích dẫn: công thức nhiễu nhiệt là vật lý cơ bản, chưa có trong bộ ref/ hiện tại. Có thể trích dẫn từ giáo trình truyền thông nếu giảng viên yêu cầu.*

---

## 2. Từ SNR đến BLER — Tiêu chuẩn đánh giá trong 5G NR

**SNR** tổng hợp chất lượng kênh. Với modulation BPSK qua kênh AWGN:

$$\text{BER} = Q\left(\sqrt{2 \cdot \text{SNR}}\right)$$

> *Lưu ý trích dẫn: công thức BER-BPSK là giáo khoa chuẩn, chưa có trong bộ ref/ hiện tại. Với kênh Rician fading, công thức phức tạp hơn và sẽ được trình bày chính xác trong `06_channel_model_lms.md`.*

Trong 5G NR, đơn vị đánh giá độ tin cậy là **BLER (Block Error Rate)**, định nghĩa bằng tỷ lệ số transport block (TB) bị lỗi trên tổng số TB được gửi [Tuninato 2025, Mục III]:

$$\text{BLER} = \frac{N_{\text{TB, bị lỗi}}}{N_{\text{TB, tổng}}}$$

Trong các mô phỏng của dự án này (theo cơ sở [Tuninato 2025]), **target BLER = $10^{-3}$** — tức là mục tiêu để hệ thống chọn MCS phù hợp qua link adaptation.

---

## 3. Hậu quả của lỗi bit

- **Dữ liệu người dùng:** Lỗi 1 bit trong file nhị phân thực thi hoặc gói lệnh điều khiển có thể gây hỏng hoàn toàn chức năng.
- **Giao thức mạng:** TCP tin tưởng lớp dưới đã đảm bảo độ tin cậy. Nếu không, TCP phải tự phục hồi lỗi với RTT lớn hơn rất nhiều — cực kỳ kém hiệu quả.
- **Ứng dụng thời gian thực (IoT, điều khiển UAV, v.v.):** Lỗi không thể chờ phục hồi ở tầng cao.

---

## 4. Ba hướng giải quyết và hạn chế của từng hướng

### Hướng 1: Tăng công suất phát
Tăng $P_t$ → tăng SNR → giảm BER. Nhưng công suất là tài nguyên hữu hạn — thiết bị di động bị giới hạn bởi pin, vệ tinh bị giới hạn bởi tấm pin mặt trời. Tăng công suất tuyến tính chỉ cải thiện SNR theo thang dB (logarithm).

### Hướng 2: FEC — Mã hóa sửa lỗi thuần túy (Forward Error Correction)
Thêm bit dư thừa vào dữ liệu để máy thu tự sửa lỗi mà không cần phát lại. **Vấn đề:** overhead cố định bất kể kênh tốt hay xấu; khả năng sửa lỗi có giới hạn; không thích nghi được với điều kiện kênh thay đổi.

### Hướng 3: ARQ — Yêu cầu phát lại thuần túy (Automatic Repeat reQuest)
Máy thu kiểm tra lỗi bằng CRC. Nếu phát hiện lỗi → gửi NACK → máy phát truyền lại. **Vấn đề:** bản phát lại trước bị vứt bỏ hoàn toàn — lãng phí năng lượng đã nhận; mỗi lần lỗi mất một vòng RTT.

---

## 5. HARQ — Giải pháp lai ghép (Hybrid ARQ)

**HARQ = FEC + ARQ**: thay vì vứt bỏ gói tin lỗi, máy thu **lưu lại** tín hiệu đã nhận và **kết hợp** với lần phát lại tiếp theo.

Nguyên lý cốt lõi: **"năng lượng đã nhận = thông tin"** — dù gói tin chưa giải mã được, mỗi lần phát lại cộng thêm thông tin, tích lũy đến khi đủ để giải mã thành công. Chi tiết trong `01_arq_to_harq.md` và `02_harq_cc_vs_ir.md`.

Trong 5G NR, HARQ là cơ chế bắt buộc ở lớp MAC. Đây là lý do 5G có thể hoạt động đáng tin cậy ngay cả khi SNR thấp.

---

## 6. Tại sao NTN làm phức tạp mọi thứ?

HARQ giải quyết vấn đề độ tin cậy trong mạng mặt đất. Nhưng trong **mạng không mặt đất (NTN)**, HARQ gặp vấn đề chưa từng có: **RTT cực lớn**.

Bảng dưới tổng hợp độ trễ lan truyền theo quỹ đạo từ TR 38.811:

| Quỹ đạo | Độ cao | RTT — Bent Pipe | RTT — Regenerative | Nguồn |
|---|---|---|---|---|
| LEO | 600 km | ~28.4 ms | ~12.9 ms | [TR 38.811, Bảng 5.3.4.1-1] |
| LEO | 1.500 km | ~51.7 ms | ~24.3 ms | [TR 38.811, Bảng 5.3.4.1-1] |
| MEO | 10.000 km | ~190.4 ms | ~93.5 ms | [TR 38.811, Bảng 5.3.4.1-1] |
| GEO | 35.786 km | ~544.8 ms | ~270.6 ms | [TR 38.811, Bảng 5.3.2.1-1] |

*(RTT tính bằng 2× one-way delay, góc ngẩng 10° cho UE, 5° cho gateway, không tính thời gian xử lý)*

Số lượng **HARQ process** cần thiết để tránh pipeline stall tăng tuyến tính với RTT. Công thức tối thiểu [Tuninato 2025, Mục IV.A]:

$$N_{\min} = \left\lceil \frac{2T_p}{T_{\text{slot}}} \right\rceil + 1$$

Đây là **vấn đề cốt lõi** mà dự án này nghiên cứu. Chi tiết trong `04_ntn_breaks_harq.md`.

---

## 7. Năm câu hỏi nghiên cứu của dự án

1. **HARQ mang lại bao nhiêu lợi ích?** So sánh BLER vs SNR: không HARQ / CC-HARQ / IR-HARQ trên kênh vệ tinh.
2. **RTT lớn ảnh hưởng thế nào đến throughput?** Throughput thay đổi ra sao khi RTT tăng từ LEO đến GEO?
3. **Cần bao nhiêu HARQ process?** Số lượng tối thiểu $N_{\min}$ để tránh pipeline stall với từng loại quỹ đạo.
4. **Có nên tắt HARQ trên GEO không?** 3GPP Rel-17 cho phép tắt HARQ feedback — lợi và mất gì?
5. **Hiệu quả năng lượng ra sao?** Năng lượng tiêu thụ trên mỗi bit thành công thay đổi thế nào theo số lần phát lại và loại HARQ.

---

## Tóm tắt

```
Kênh vô tuyến → fading + nhiễu → lỗi bit → cần cơ chế phục hồi
     ↓
FEC: overhead cố định, không thích nghi
ARQ: vứt bỏ năng lượng đã nhận, phụ thuộc RTT
HARQ: tích lũy năng lượng từ nhiều lần phát → hiệu quả hơn cả hai
     ↓
NTN: RTT lớn → cần nhiều HARQ process hơn → vấn đề pipeline stall
```

---

**File tiếp theo:** `01_arq_to_harq.md` — Lịch sử và kiến trúc: từ Stop-and-Wait ARQ đến HARQ hiện đại
