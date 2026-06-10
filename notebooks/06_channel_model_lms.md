# 06 — Mô hình Kênh LMS: Phân phối Loo, K-factor và Hiện thực hóa

> **Mục tiêu:** Hiểu mô hình kênh Land Mobile Satellite (LMS) theo chuẩn TR 38.811, tại sao chọn K = 15/20 dB, và cách hiện thực trong code mô phỏng.

---

## 1. Tại sao cần mô hình kênh đặc thù cho NTN?

Mô hình kênh mặt đất (TR 38.901) không đủ cho NTN vì:
- Góc ngẩng (elevation angle) lớn → ít multipath hơn, thành phần LOS mạnh hơn.
- Không có scattering địa phương quanh vệ tinh.
- Môi trường truyền sóng (ionosphere, troposphere) khác hoàn toàn.

3GPP định nghĩa mô hình kênh NTN riêng trong TR 38.811 Chương 6 — áp dụng cho đường truyền vệ tinh/HAPS ↔ UE.

---

## 2. Mô hình hai trạng thái ITU (LMS Model)

### 2.1. Tổng quan

Mô hình LMS (Land Mobile Satellite) trong [TR 38.811, Mục 6.7.1] dựa trên mô hình hai trạng thái ITU. Kênh ở mỗi thời điểm thuộc một trong hai trạng thái:

- **Trạng thái GOOD (G):** LOS rõ ràng hoặc bóng nhẹ — kênh ổn định.
- **Trạng thái BAD (B):** Bóng nặng (shadowing mạnh) — kênh suy giảm mạnh.

Thời gian ở mỗi trạng thái tuân theo mô hình semi-Markov. Trong mỗi trạng thái, fading được mô tả bằng **phân phối Loo** — tổng của thành phần đường thẳng (log-normal) và thành phần tán xạ (Rayleigh) [TR 38.811, Mục 6.7.1].

### 2.2. Phân phối Loo

Trong mỗi trạng thái, tín hiệu nhận được là tổng của:
- Thành phần LOS trực tiếp: biên độ $A$ phân phối log-normal với trung bình $\mu_A$ và độ lệch chuẩn $\sigma_A$.
- Thành phần multipath tán xạ: công suất trung bình $2\sigma_m^2$ (phân phối Rayleigh).

Ba tham số đặc trưng cho trạng thái G/B [TR 38.811, Mục 6.7.1, Bảng 6.7.1-1]:
- $(\mu_A, \sigma_A)_{G,B}$: trung bình và độ lệch chuẩn của thành phần trực tiếp (dB)
- $MP_{G,B} = h_{1,G/B} \cdot MA + h_{2,G/B}$: công suất multipath (một đa thức bậc nhất của $MA$)

Trong flat fading, kênh được đặc trưng bởi một tap duy nhất theo phân phối Loo.

---

## 3. Hệ số K-factor và Mô hình Rician đơn giản hóa

### 3.1. K-factor là gì?

$$K = \frac{P_{\text{LOS}}}{P_{\text{tán xạ}}} \quad [\text{dB}]$$

Hệ số Rician K-factor đặc trưng cho tỷ lệ năng lượng thành phần LOS trên thành phần tán xạ. K cao → kênh gần như deterministic (như AWGN); K = 0 → kênh Rayleigh thuần túy.

### 3.2. K-factor trong các mô hình 3GPP NTN

Trong mô hình TDL (Tapped Delay Line) của TR 38.811 [Bảng 6.9.2-3 và 6.9.2-4]:
- **NTN-TDL-C:** tap đầu Rician với $K_1 = 10.224$ dB
- **NTN-TDL-D:** tap đầu Rician với $K_1 = 11.707$ dB

### 3.3. K-factor trong dự án này

Dự án này theo cấu hình của [Tuninato 2025, Mục IV] — sử dụng kênh LMS với:
- $K = 15$ dB: kịch bản đặc trưng (suburban/rural LOS tốt)
- $K = 20$ dB: kịch bản kênh rất tốt (near-AWGN)

Hai giá trị này không lấy trực tiếp từ bảng TDL của TR 38.811 (vốn cho $K_1 \approx 10$–12 dB) mà là lựa chọn tham số của IEEE paper để sweep điều kiện kênh. Đây là điểm cần làm rõ trong báo cáo.

---

## 4. Phân phối Rician — Công thức sử dụng trong mô phỏng

Trong dự án này, kênh LMS được xấp xỉ bằng **kênh Rician flat fading** (một tap) với K-factor cố định — cách tiếp cận phổ biến trong link-level simulation theo [Tuninato 2025, Mục IV].

Hệ số kênh phức $h$ theo phân phối Rician:

$$h = \sqrt{\frac{K}{K+1}} e^{j\phi_0} + \sqrt{\frac{1}{K+1}} \cdot \tilde{h}$$

Trong đó:
- $\sqrt{K/(K+1)} e^{j\phi_0}$: thành phần LOS deterministic
- $\tilde{h} \sim \mathcal{CN}(0, 1)$: thành phần tán xạ Rayleigh (biến ngẫu nhiên phức Gaussian)

*(Công thức biểu diễn Rician này là chuẩn toán học, chưa có dạng tường minh trong bộ ref/ hiện tại. Concept được xác nhận trong [TR 38.811, Mục 6.7].)*

Biên độ $|h|$ tuân theo phân phối Rician với tham số $\nu = \sqrt{K/(K+1)}$ và $\sigma = 1/\sqrt{2(K+1)}$.

---

## 5. Doppler và Coherence Time

Kênh LMS trong NTN có Doppler shift do cả chuyển động vệ tinh lẫn UE. Coherence time theo mô hình Clarke [Tuninato 2025, Mục IV.B]:

$$T_c \approx \frac{0.423}{f_m}$$

Trong đó $f_m = v f_c / c$ là Doppler shift cực đại, $v$ là tốc độ đầu cuối, $f_c$ là tần số sóng mang, $c$ là tốc độ ánh sáng.

**Ý nghĩa cho HARQ:** Nếu $T_c$ lớn hơn khoảng cách giữa các lần retransmission HARQ, các lần phát đó trải qua **cùng điều kiện kênh** (correlated) → HARQ gain thấp hơn. Nếu $T_c$ nhỏ, mỗi lần phát có kênh độc lập → diversity gain tối đa.

Phân tích coherence time chi tiết theo [Tuninato 2025, Bảng 6 và 7] sẽ được thực hiện trong mô phỏng.

---

## 6. Tham số kênh trong mô phỏng

| Tham số | Giá trị | Nguồn |
|---|---|---|
| Mô hình kênh | LMS (Rician flat fading) | [Tuninato 2025, Mục IV] |
| K-factor | 15 dB và 20 dB | [Tuninato 2025, Mục IV] |
| Tốc độ đầu cuối | 0, 50, 150, 900 km/h | [Tuninato 2025, Mục IV] |
| Quỹ đạo cơ sở | LEO 600 km | [Tuninato 2025, Mục IV] |
| Mở rộng | MEO 10.000 km, GEO 35.786 km | Dự án này (đóng góp mới) |
| Tần số | Ka band (~20 GHz) cho coherence time | [Tuninato 2025, Mục IV.B] |

---

## 7. Hiện thực trong code

Module `src/channel/lms_channel.py` sẽ hiện thực:

```python
# Rician flat fading channel
def generate_rician_channel(K_dB, n_samples, speed_kmh, fc_GHz, T_slot):
    K = 10**(K_dB/10)
    # LOS component
    h_los = np.sqrt(K/(K+1))
    # Scattered component (Jake's Doppler model)
    fd = speed_kmh/3.6 * fc_GHz*1e9 / 3e8  # max Doppler freq
    h_scatter = generate_jakes_fading(n_samples, fd, T_slot) / np.sqrt(K+1)
    return h_los + h_scatter
```

Chi tiết Jake's Doppler model được tham chiếu từ [TR 38.811, Mục 6.7.1]: *"a Jake's Doppler spectrum is considered for UE mobility."*

---

## Tóm tắt

```
Kênh NTN = mô hình LMS hai trạng thái (ITU) với phân phối Loo
  → TR 38.811, Mục 6.7.1 + Bảng 6.7.1-1
Trong mô phỏng: xấp xỉ Rician flat fading với K cố định
  → K = 15 dB và 20 dB theo [Tuninato 2025]
  → Khác với TDL model của TR 38.811 (K1 ≈ 10-12 dB)
Doppler: Jake's model theo [TR 38.811, Mục 6.7.1]
  → Coherence time Tc ≈ 0.423/fm theo [Tuninato 2025, Mục IV.B]
```

---

**File tiếp theo:** `07_parameter_selection.md` — Lý giải từng tham số mô phỏng
