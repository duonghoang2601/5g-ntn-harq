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
---
Errors:
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git status 
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   report/skill.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        report/images/

no changes added to commit (use "git add" and/or "git commit -a")
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git add . 
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git commit -m "doc: add new requirement on contents to fix in report." 
[main 25a7eaf] doc: add new requirement on contents to fix in report.
 4 files changed, 46 insertions(+)
 create mode 100644 report/images/fig1.png
 create mode 100644 report/images/fig2.png
 create mode 100644 report/images/fig3.png
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git push -u origin main 
remote: Permission to duonghoang2601/5g-ntn-harq.git denied to gamvu1122.
fatal: unable to access 'https://github.com/duonghoang2601/5g-ntn-harq.git/': The requested URL returned error: 403
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git checkout -b doc/fix-requirement 
Switched to a new branch 'doc/fix-requirement'
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git status
On branch doc/fix-requirement
nothing to commit, working tree clean
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git add .
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git commit -m "doc: add requirement" 
On branch doc/fix-requirement
nothing to commit, working tree clean
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git push -u origin doc/fix-requirement 
remote: Permission to duonghoang2601/5g-ntn-harq.git denied to gamvu1122.
fatal: unable to access 'https://github.com/duonghoang2601/5g-ntn-harq.git/': The requested URL returned error: 403
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git push -u origin doc/fix-requirement 
remote: Permission to duonghoang2601/5g-ntn-harq.git denied to gamvu1122.
fatal: unable to access 'https://github.com/duonghoang2601/5g-ntn-harq.git/': The requested URL returned error: 403
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git checkout main 
Switched to branch 'main'
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git push -u origin main                
remote: Permission to duonghoang2601/5g-ntn-harq.git denied to gamvu1122.
fatal: unable to access 'https://github.com/duonghoang2601/5g-ntn-harq.git/': The requested URL returned error: 403
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git remote set-url origin https://github.com/duonghoang2601/5g-ntn-harq.git
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git push -u origin main                                                    
remote: Permission to duonghoang2601/5g-ntn-harq.git denied to gamvu1122.
fatal: unable to access 'https://github.com/duonghoang2601/5g-ntn-harq.git/': The requested URL returned error: 403
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git push -u origin main 
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 12 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 440.95 KiB | 20.04 MiB/s, done.
Total 8 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/duonghoang2601/5g-ntn-harq.git
   6c93333..25a7eaf  main -> main
branch 'main' set up to track 'origin/main'.
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> 
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> git pull origin main 
remote: Enumerating objects: 40, done.
remote: Counting objects: 100% (40/40), done.
remote: Compressing objects: 100% (10/10), done.
remote: Total 23 (delta 13), reused 23 (delta 13), pack-reused 0 (from 0)
Unpacking objects: 100% (23/23), 1.42 MiB | 1.10 MiB/s, done.
From https://github.com/duonghoang2601/5g-ntn-harq
 * branch            main       -> FETCH_HEAD
   25a7eaf..05f83c2  main       -> origin/main
Updating 25a7eaf..05f83c2
Fast-forward
 main.pdf                                 | 4480 ++++++++++++++++
 report/chapters/ch1_intro.tex            |   20 +-
 report/chapters/ch2_theory.tex           |   72 +-
 report/chapters/ch3_method.tex           |   40 +-
 report/chapters/ch4_results.tex          |  273 +-
 report/chapters/ch5_conclusion.tex       |   26 +-
 report/frontmatter/abbreviations.tex     |    2 +-
 report/frontmatter/abstract.tex          |    6 +-
 report/frontmatter/preface.tex           |    2 +-
 report/main.pdf                          | 8526 ++++++++++++------------------
 report/main.tex                          |    2 +-
 results/figures/sim01_bler_ir_leo.pdf    |  Bin 0 -> 27490 bytes
 results/figures/sim01_bler_ir_leo.png    |  Bin 0 -> 184330 bytes
 results/figures/sim03_nmin_leo.pdf       |  Bin 0 -> 22382 bytes
 results/figures/sim03_nmin_leo.png       |  Bin 0 -> 139113 bytes
 results/figures/sim05_energy_per_bit.pdf |  Bin 29725 -> 25817 bytes
 results/figures/sim05_energy_per_bit.png |  Bin 138930 -> 51509 bytes
 17 files changed, 8036 insertions(+), 5413 deletions(-)
 create mode 100644 main.pdf
 create mode 100644 results/figures/sim01_bler_ir_leo.pdf
 create mode 100644 results/figures/sim01_bler_ir_leo.png
 create mode 100644 results/figures/sim03_nmin_leo.pdf
 create mode 100644 results/figures/sim03_nmin_leo.png
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> pip install -r requirements.txt 
Requirement already satisfied: numpy>=1.24 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from -r requirements.txt (line 1)) (1.26.4)
Requirement already satisfied: scipy>=1.10 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from -r requirements.txt (line 2)) (1.17.1)
Requirement already satisfied: matplotlib>=3.7 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from -r requirements.txt (line 3)) (3.10.8)
Collecting tqdm>=4.65 (from -r requirements.txt (line 4))
  Downloading tqdm-4.68.3-py3-none-any.whl.metadata (57 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.4/57.4 kB 432.3 kB/s eta 0:00:00
Requirement already satisfied: contourpy>=1.0.1 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from matplotlib>=3.7->-r requirements.txt (line 3)) (1.3.3)
Requirement already satisfied: cycler>=0.10 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from matplotlib>=3.7->-r requirements.txt (line 3)) (0.12.1)
Requirement already satisfied: fonttools>=4.22.0 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from matplotlib>=3.7->-r requirements.txt (line 3)) (4.61.1)
Requirement already satisfied: kiwisolver>=1.3.1 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from matplotlib>=3.7->-r requirements.txt (line 3)) (1.4.9)
Requirement already satisfied: packaging>=20.0 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from matplotlib>=3.7->-r requirements.txt (line 3)) (25.0)
Requirement already satisfied: pillow>=8 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from matplotlib>=3.7->-r requirements.txt (line 3)) (12.1.0)
Requirement already satisfied: pyparsing>=3 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from matplotlib>=3.7->-r requirements.txt (line 3)) (3.3.1)
Requirement already satisfied: python-dateutil>=2.7 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from matplotlib>=3.7->-r requirements.txt (line 3)) (2.9.0.post0)
Collecting colorama (from tqdm>=4.65->-r requirements.txt (line 4))
  Using cached colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
Requirement already satisfied: six>=1.5 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from python-dateutil>=2.7->matplotlib>=3.7->-r requirements.txt (line 3)) (1.17.0)
Downloading tqdm-4.68.3-py3-none-any.whl (78 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78.3/78.3 kB 1.1 MB/s eta 0:00:00
Using cached colorama-0.4.6-py2.py3-none-any.whl (25 kB)
Installing collected packages: colorama, tqdm
Successfully installed colorama-0.4.6 tqdm-4.68.3

[notice] A new release of pip is available: 24.0 -> 26.1.2
[notice] To update, run: python.exe -m pip install --upgrade pip
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> python run_all.py
==============================================================
  5G NTN HARQ — Simulation Suite
  Running: [1, 2, 3, 4, 5]
==============================================================

##############################################################
#  Simulation 1: BLER vs Es/N0
##############################################################

============================================================
  Sim 1 — MCS A — QPSK r=1/2
============================================================
  [1/3] No HARQ baseline …
  [2/3] CC-HARQ …
  [3/3] IR-HARQ …
  Saved → C:\Users\ASUS\Documents\GitHub\5g-ntn-harq\results\figures\sim01_bler_vs_snr_mcs_a.pdf
  CC TX=1: BLER=1e-02 at Es/N0=0.7 dB
  CC TX=2: BLER=1e-02 at Es/N0=-3.3 dB
  CC TX=3: BLER=1e-02 at Es/N0=-5.5 dB
  CC TX=4: BLER=1e-02 at Es/N0=-7.0 dB
  IR TX=1: BLER=1e-02 at Es/N0=0.8 dB
  IR TX=2: BLER=1e-02 at Es/N0=-3.7 dB
  IR TX=3: BLER=1e-02 at Es/N0=-6.0 dB
  IR TX=4: BLER=1e-02 at Es/N0=-7.5 dB
  Data saved → results/data/sim01_mcs_a.npz

============================================================
  Sim 1 — MCS B — 256QAM r=8/9
============================================================
  [1/3] No HARQ baseline …
  [2/3] CC-HARQ …
  [3/3] IR-HARQ …
  Saved → C:\Users\ASUS\Documents\GitHub\5g-ntn-harq\results\figures\sim01_bler_vs_snr_mcs_b.pdf
  CC TX=1: BLER=1e-02 at Es/N0=3.9 dB
  CC TX=2: BLER=1e-02 at Es/N0=-0.1 dB
  CC TX=3: BLER=1e-02 at Es/N0=-2.3 dB
  CC TX=4: BLER=1e-02 at Es/N0=-3.7 dB
  IR TX=1: BLER=1e-02 at Es/N0=3.9 dB
  IR TX=2: BLER=1e-02 at Es/N0=-0.8 dB
  IR TX=3: BLER=1e-02 at Es/N0=-3.2 dB
  IR TX=4: BLER=1e-02 at Es/N0=-4.9 dB
  Data saved → results/data/sim01_mcs_b.npz

Sim 1 complete.

  ✔  Simulation 1 finished in 8.2 s

##############################################################
#  Simulation 2: SE Goodput vs RTT
##############################################################

  ✘  Simulation 2 FAILED:
Traceback (most recent call last):
  File "C:\Users\ASUS\Documents\GitHub\5g-ntn-harq\run_all.py", line 41, in run_sim
    mod = importlib.import_module(module)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ASUS\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 936, in exec_module
  File "<frozen importlib._bootstrap_external>", line 1074, in get_code
  File "<frozen importlib._bootstrap_external>", line 1004, in source_to_code
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "C:\Users\ASUS\Documents\GitHub\5g-ntn-harq\src\sim\sim_02_throughput_vs_rtt.py", line 72
    ax.text(rtt+3, y_stagger[i], f"{orbit.replace('_','\\n')}\n$N_{{min}}$={nm}",
                                                                                ^
SyntaxError: f-string expression part cannot include a backslash

##############################################################
#  Simulation 3: N_min Optimisation
##############################################################

============================================================
  Sim 3 — N_min Optimisation
============================================================

  N_min table (regenerative payload):
  Orbit           SCS 15 kHz  SCS 30 kHz  SCS 60 kHz SCS 120 kHz
  --------------------------------------------------------------
  LEO_600               14          27          53✗        105✗ 
  LEO_1200              26          50✗         99✗        196✗ 
  MEO_10000             95✗        188✗        375✗        749✗ 
  GEO_35786            272✗        543✗       1084✗       2166✗ 
  ✗ = exceeds max 32 processes [TS 38.214, Section 5.1]
  Saved → C:\Users\ASUS\Documents\GitHub\5g-ntn-harq\results\figures\sim03_nmin_chart.pdf
  Saved → C:\Users\ASUS\Documents\GitHub\5g-ntn-harq\results\figures\sim03_se_vs_nproc.pdf
  Data saved → results/data/sim03_nmin.npz
  Sim 3 complete.

  ✔  Simulation 3 finished in 1.0 s

##############################################################
#  Simulation 4: GEO HARQ-Disable Trade-off
##############################################################

============================================================
  Sim 4 — GEO HARQ-Disable Trade-off
============================================================
  GEO RTT = 270.6 ms (regenerative, 10° elevation)
  [TR 38.811, Table 5.3.2.1-1]
  N_min at SCS 30 kHz = 542 → stall inevitable with N=32

  Saved → C:\Users\ASUS\Documents\GitHub\5g-ntn-harq\results\figures\sim04_geo_disable.pdf

  At Es/N0 = 10.0 dB:
    HARQ (N=32):    BLER=0.00e+00  SE=0.0295  Latency=271 ms  (util=0.059)
    RLC ARQ:        BLER=0.00e+00  SE=0.5000  Latency=542 ms
  Data saved → results/data/sim04_geo_disable.npz
  Sim 4 complete.

  ✔  Simulation 4 finished in 1.2 s

##############################################################
#  Simulation 5: Energy Efficiency per Bit
##############################################################

============================================================
  Sim 5 — Energy Efficiency per Bit
============================================================
  [A] No HARQ / CC-HARQ / IR-HARQ — LEO 600 km …
  Saved → C:\Users\ASUS\Documents\GitHub\5g-ntn-harq\results\figures\sim05_energy_per_bit.pdf
  [B] IR-HARQ across orbits …
  Saved → C:\Users\ASUS\Documents\GitHub\5g-ntn-harq\results\figures\sim05_energy_per_bit_orbits.pdf

  Energy comparison at Es/N0 = 5.0 dB:
    No HARQ     : E_bit=5.000e-04 J/bit  avg_ntx=1.00  BLER=0.00e+00
    CC-HARQ     : E_bit=5.000e-04 J/bit  avg_ntx=1.00  BLER=0.00e+00
    IR-HARQ     : E_bit=5.000e-04 J/bit  avg_ntx=1.00  BLER=0.00e+00
  Data saved → results/data/sim05_energy.npz
  Sim 5 complete.

  ✔  Simulation 5 finished in 2.9 s

==============================================================
  Summary  (13.3 s total)
==============================================================
  Sim 1: BLER vs Es/N0                           ✔ OK
  Sim 2: SE Goodput vs RTT                       ✘ FAILED
  Sim 3: N_min Optimisation                      ✔ OK
  Sim 4: GEO HARQ-Disable Trade-off              ✔ OK
  Sim 5: Energy Efficiency per Bit               ✔ OK

  1 simulation(s) failed. Check output above.
PS C:\Users\ASUS\Documents\GitHub\5g-ntn-harq> 
