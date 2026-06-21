## Các lỗi soi được:
- THêm cho tôi thầy Hải là PGS. TS. Nguyễn Hoàng Hải, thầy Thạch là PGS. TS. Lâm Hồng Thạch 
- Đánh số các chương, cụ thể là sub số. bạn đang để nó tăng qua từng chuong, ví dụ, 2.8 sang luôn 3.9, phải là 3.1 , kể cả lúc sang chương 4 nữa
- Mô hình Jake's chuỗi thời gian là cái quái gì, phải là mô hình chuỗi thời gian Jake chứ 
- Viết lại tiêu đè các hình mà thêm ":" vàp, ví dụ: "Bảng 4/1: ........"
- Tiết kiệm năng lượng 9 bậc độ lớn nghe nó cứ ngu ngu ấy nhỉ.

## Các câu hỏi cần thêm vào lưu ý sợ bị hỏi và bảo vệ
- Mô phỏng bằng phương pháp Monte Carlo là mô phỏng gì? Tại sao lại dùng phương pháp này để mô phỏng HARQ?
- Mô hình ngưỡng thông tin tương hỗ là gì? Tại sao lại dùng mô hình này để mô phỏng HARQ?
- pipeline stall là gì? Tại sao lại xuất hiện pipeline stall trong MEO và GEO? 
- Goodput là gì? Dùng để đánh giá cái gì 
- Cần bạn nêu rõ các thuật ngữ kỹ thuật và định nghĩa của chúng trong phần tóm tắt.
- Tại sao lại có cả UE trong này ?
- Tôi cần nói rõ hơn về cái kết hợp Chase Combining và Incremental Redundancy trong HARQ.
- payloa tái sinh là gì 
- Hướng dẫn cách đọc các biểu đồ có trong phần 4 để có thể tự tin chỉ và thyết trình 
- 



--- 
New point: 
\subsection{Tổng quan về Mạng phi mặt đất (5G-NTN)}
\subsubsection{Khái niệm mạng 5G-NTN}
Mạng phi mặt đất 5G-NTN là công nghệ giao tiếp trực tiếp giữa thiết bị đầu cuối 5G và vệ tinh (terminal-satellite), dựa trên công nghệ giao diện vô tuyến mới (NR) do tổ chức 3GPP phát triển trong phiên bản Release 17 (R17).
\begin{figure}[h]
    \centering
    \includegraphics[width=0.9\linewidth]{Images/fig1.png}
    \caption{Sự kết nối 5G-NTN}
    \label{fig1}
\end{figure}
Là một phần bổ sung cho mạng di động mặt đất truyền thống, NTN cho phép xây dựng mạng lưới tích hợp Không gian - Trên không - Mặt đất (SAGIN) vượt trội hơn cơ sở hạ tầng mặt đất về băng thông, độ trễ, độ tin cậy, v.v. Nó cung cấp dịch vụ mạng liền mạch cho người dùng toàn cầu nhờ phạm vi phủ sóng lớn hơn và khả năng phục hồi cao, đáp ứng các yêu cầu mạng trong tương lai về truyền thông và kết nối mạng ở mọi thời điểm, mọi miền và mọi không gian.\cite{3gpp_ntn_2026}

\subsubsection{Kiến trúc 5G-NTN} 
NTN chủ yếu hỗ trợ hai kiến trúc được triển khai: Kiến trúc Transparent/Bent Pipe trong các phiên bản 3GPP 17 và 18 và Regenerative Payloads trong phiên bản 3GPP 19. Transparent/Bent Pipe bao gồm tất cả các thành phần cơ sở hạ tầng di động, Trạm gốc gNode (gNB) và mạng lõi 5G (5GCN), được đặt trên mặt đất, trong khi tải trọng vệ tinh cung cấp khả năng truyền tải trong suốt dạng sóng NR đến thiết bị di động. 

\begin{figure}[h]
    \centering
    \includegraphics[width=0.9\linewidth]{Images/fig2.png}
    \caption{Kiến trúc Transparent(3GPP Releases 17 and 18)}
    \label{fig2}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{Images/fig3.png}
    \caption{Kiến trúc Regenerative gNB on Board (3GPP Release 19)}
    \label{fig3}
\end{figure}
Trong cấu trúc mạng 5G-NTN, hai mô hình Transparent (Bent Pipe) và Regenerative (gNB on Board) đều được vận hành dựa trên sự phối hợp của ba loại liên kết vô tuyến cốt lõi bao gồm Service Link, Feeder Link và Inter-Satellite Link (ISL). Đầu tiên, Liên kết dịch vụ đóng vai trò là đường truyền trực tiếp giữa thiết bị người dùng (UE) và Vệ tinh. Trong kiến trúc Transparent , liên kết này vận chuyển thô tín hiệu vô tuyến (mở rộng giao diện NR Uu); còn ở kiến trúc  Regenerative , nó đóng vai trò kết nối trực tiếp thiết bị với trạm gNB được tích hợp ngay trên bo mạch bảo vệ. Tiếp theo, Feeder Link là cầu nối giữa Vệ tinh và Trạm mặt đất (Trạm mặt đất/Cổng). Đối với mô hình Transparent , Feeder Link là một loại trung chuyển bắt buộc để đưa tín hiệu vô tuyến của người dùng từ không gian về trạm gNB xử lý dưới mặt đất. Ngược lại, ở mô hình Regenerative, gNB đã ở trên không trung nên Feeder Link chuyển sang đóng vai trò là lõi mạng giao diện (giao diện NG) để truyền dữ liệu đã được xử lý về mạng lõi mặt đất (5G CN). Cuối cùng, ISL là liên kết liên kết giúp bảo vệ các giao tiếp trực tiếp với nhau trên không gian, hỗ trợ nguyên liệu tín hiệu định tuyến (đối với mô hình Transparent ) hoặc trao đổi tốc độ dữ liệu cao giữa các gNB trên giao diện Xn không thông tin (đối với mô hình Regenerative  ).

Điều đặc biệt trong cơ chế hoạt động của các ảnh liên kết này ảnh hưởng trực tiếp đến hệ thống. Ở mô hình Transparent , điều khiển vòng lặp lỗi Hybrid-ARQ bắt buộc phải đi qua cả Service Link và Feeder Link để được gNB mặt đất, tạo chế độ vòng (RTT) được nhân đôi và đặt ra bài toán tối ưu hóa HARQ cực kỳ phức hợp. Trong khi đó, mô hình Regenerative  cho phép xử lý HARQ ngay tại bảo vệ thông qua Liên kết dịch vụ, giúp cắt giảm một nửa hành động của tín hiệu và giảm thiểu đáng kể hạn chế cho toàn hệ thống.


## Các điểm cần sửa 
- Tôi không cần SE Goodput vì tôi chưa hiểu rõ về nó lắm, có thể bó đi được không, nếu bỏ được thì hãy xóa cả các đoạn liên quan đến SE Goodput (phần 2.3.3) 
- Do báo cáo chỉ cần làm đơn giản nên tôi nghĩ sẽ bỏ phần 3. Xác minh kết quả mô phỏng bằng phân tích lý thuyết (CDF Rician, bất đẳng thức
Jensen) và đề xuất cấu hình HARQ tối ưu cho từng quỹ đạo., bạn cũng bỏ tương ứng ở chương 4 giúp tôi nhé. 
- có 1 đoạn latex phía trên về cơ sở lý thuyết về 5G-NTN, bạn có thể thêm vào phần 2.1.1 để làm rõ hơn về kiến trúc mạng 5G-NTN, các liên kết vô tuyến cốt lõi và cơ chế hoạt động của chúng, đồng thời nhớ sửa chỉ mục của các phần sau.
- SNR tức thời: 𝛾 = |ℎ|2 ⋅ (𝐸𝑠/𝑁0). Phân phối của |ℎ|2 là chi-squared phi tâm bậc
tự do 2, nghịch đảo non-centrality 2𝐾: - đoạn này nhiều tiếng  anh nên đọc bị loãng quá, có từ tiếng việt nào mô tả nó là cáI gì được không 
- Tôi không cần làm phần MCS B trong 2.4 nên hãy bỏ đi và tương ứng bỏ trong chương 4 nhé. 
- Đơn giản hóa chủ đề của tôi lần cuối cùng: CHỈ LÀM 5G-NTN HARQ CHO IR LEO, CÒN LẠI BỎ HẾT ĐI TỪ CẢ CC VÀ GEO MEO NHÉ, CHẮC CẦN CHẠY LẠI CẢ MÔ PHỎNG. 
