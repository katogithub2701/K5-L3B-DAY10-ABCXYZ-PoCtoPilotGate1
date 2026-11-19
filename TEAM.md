# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): ABCXYZ
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-ABCXYZ-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S4

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Hoàng Đức An | 2A202603800 | Kỹ sư cổng | x |
|   2 | Đào Văn Hiệp | 2A202603813 | Sản phẩm và kinh doanh | |
|   3 | Nguyễn Như Duy An | 2A202603783 | Vận hành và pháp lý | |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Các mục dưới đây ghi phần việc, bằng chứng và exit ticket của từng vai. Nội dung được soạn với hỗ trợ của AI và dựa trên bài làm trong repo. Mỗi thành viên rà lại phần của mình trước khi nộp.

## NguyenNhuDuyAn-2A202603783

### Phần việc phụ trách

Vai **Vận hành và pháp lý** (Người 3); phụ trách `TEAM.md`, câu 1.2 & 1.4 và mục A5 (`templates/form-a-criteria.md`), câu 2.4 (`B4`, `B5`), câu 2.10 (`config/operating_gates.json` mục `operations` & `legal`, `B7.5`–`B7.6`), Khối 3 (`C3`, `C4`, `C5` câu 3.3, `C7`, `C9`–`C11`), và gom kiểm bài nộp (`submission/submission.json`, `lab10.check_submission`).

### Đóng góp cụ thể

- Vòng 1 ghi góc nhìn kế toán đối soát và trưởng ca trong Phiếu A, lập HAZOP và checklist 9 nhóm việc. Cấu hình người trực, người duyệt, cổng pháp lý và viết Runbook 1–3.
- Vòng 2 đối chiếu hàng chờ S4, bổ sung ngưỡng gọi người dự phòng khi chờ trên 40 phút và ngưỡng cảnh báo Finance từ 80% trần ngày. Cập nhật fault tree, risk register, checklist và Runbook 4–5, gồm quy trình đối soát và thông báo cho hãng bị ảnh hưởng.
- Hoàn thiện `submission.json` theo Phiếu C và gom báo cáo ba mốc. Lệnh kiểm tra bài nộp báo **ĐỦ THÀNH PHẦN**.

### Bằng chứng

- Commit `0767d88` cho phần vận hành vòng 1 và `ba373dc` cho vòng 2. [Phiếu B, mục Giờ cao điểm](templates/form-b-evaluation-gates.md#b7) · [Phiếu C, checklist và runbook](templates/form-c-incident.md#c11)
- Grade `R-S4-grade-20261119-172236-9b7b78` ghi thời gian chờ dài nhất 46 phút, chưa có ca vượt SLA 60 phút. [Báo cáo grade S4](submission/runs/grade-report.md)

### Exit ticket

- **Điều học được** — Không có ca vượt SLA vẫn có thể cần can thiệp. Mốc 46 phút đã qua ngưỡng cảnh báo 40 phút, nên trưởng ca cần gọi người dự phòng trước khi có ca quá hạn.
- **Điều còn chưa chắc** — Khi lượng ticket dồn vào giờ sale, người dự phòng thực tế mất bao lâu để nhận việc và luồng thủ công còn bao nhiêu công suất?

## DaoVanHiep-2A202603813

### Phần việc phụ trách

Sản phẩm và kinh doanh. Phụ trách mục tiêu hệ thống và tiêu chí chấp nhận (câu 1.1, 1.6), bản đồ dữ liệu và drift (câu 2.3), cổng kinh doanh (câu 2.9 và phần `business` của câu 3.5), specification của thẻ (câu 3.2) và ghi quyết định v1/v2 sau khi nhóm chốt.

### Đóng góp cụ thể

- Chọn PRD v1.1 và eval card từ Lab 9 làm tài liệu chung, rồi viết mục tiêu hệ thống cho trợ lý hoàn tiền ở Phiếu A.
- Soạn bộ tiêu chí chấp nhận gồm ngưỡng chất lượng, an toàn, chi phí và ROI cùng quy tắc cho bốn quyết định Gate 1. Tiêu chí đã ký tại commit `e13f2da`.
- Lập bản đồ nguồn dữ liệu của trợ lý và mô tả tình huống drift khi chuyển từ `REFUND-v3` sang `REFUND-v4`.
- Đặt cổng kinh doanh vòng 1 gồm trần hoàn tự động 1.800.000đ/ngày, ngân sách LLM 1.500đ/ticket, phạm vi hai kho `HN`, `HCM` và ROI tối thiểu 15%. Ghi quyết định v1 dựa trên kết quả `prepared`.
- Vòng 2 viết specification yêu cầu kiểm cả trần pilot và ngân sách Finance của ngày trước lệnh hoàn tự động. So sánh phương án tăng người cả ca và thu hẹp phạm vi, rồi ghi v2 **Cải tiến thêm** để kiểm chứng phương án dự phòng theo giờ.

### Bằng chứng

- Commit `08c67be` cho Phiếu A và tài liệu Lab 9, `e13f2da` cho tiêu chí đã ký.
- [Phiếu A mục A4](templates/form-a-criteria.md#a4) và [cấu hình tiêu chí](config/acceptance_criteria.json) cho câu 1.6.
- [Phiếu B mục B3](templates/form-b-evaluation-gates.md#b3) cho câu 2.3; mục B7.4 trong cùng phiếu và [cấu hình cổng](config/operating_gates.json) cho câu 2.9.
- [Phiếu C](templates/form-c-incident.md) mục C5 và C12 ghi specification, đánh đổi chi phí khi tăng người và quyết định v2 **Cải tiến thêm**. Trợ lý AI hỗ trợ phân tích và soạn bản ghi.

### Exit ticket

- **Điều học được** — Chi phí trực duyệt có thể đổi quyết định pilot. Trong S4, tăng từ một lên hai người cả ca giảm chờ tối đa từ 46 xuống 6 phút, nhưng đẩy chi phí lên 8.787đ/ticket và ROI xuống 14%.
- **Điều còn chưa chắc** — Với hai kho `HN` và `HCM`, gọi thêm người theo giờ có giữ thời gian chờ dưới SLA mà vẫn đạt ngưỡng 8.000đ/ticket và ROI tối thiểu 15% khi sale thật hay không?

## HoangDucAn-2A202603800

### Phần việc phụ trách

Kỹ sư cổng (Người 1). Phụ trách A2 câu 1.3, B0–B2, B7.1–B7.3, kiểm thử và chốt vòng 1. Ở vòng 2, nhận thẻ, chạy grade trước khi sửa, phân tích trace C2, triển khai cổng và monitor C7–C8, rồi kiểm hồi quy.

### Đóng góp cụ thể

- Vòng 1 ghim chính sách còn hiệu lực, đối chiếu quyền lợi theo tracking trước khi hoàn và lọc dữ liệu gửi hãng. Kiểm ba ca `--adhoc` và hồi quy toàn bộ bộ nền đạt 110/110 lượt.
- Vòng 2 dùng trace S4 để xác định lỗi 429 dẫn tới fail-open và phân biệt lỗi ghi với lỗi quá tải hàng chờ. Bổ sung kiểm ngân sách Finance theo ngày trước lệnh ghi, thêm monitor `review_wait_max_min` và chạy lại grade.

### Bằng chứng

Các lần chạy `R-base-before-20261119-170927-62632e`, `R-base-after-20261119-171128-d18acb`, `R-base-prepared-20261119-171142-d18acb`. Bản chốt vòng 1 có hash đầu `2d290e3c`.

- Commit `6b7d517` lưu CP3, `ba373dc` lưu bản sửa S4. Grade trước sửa `R-S4-grade-20261119-172049-d18acb`, grade cuối `R-S4-grade-20261119-172236-9b7b78` đạt **PASS-VISIBLE**. [Phiếu C, cổng và monitor](templates/form-c-incident.md#c7) · [Báo cáo grade S4](submission/runs/grade-report.md)

### Exit ticket

- **Điều học được** — Khi LLM lỗi 429, chuyển người duyệt trước lệnh ghi bảo vệ sổ cái và hãng vận chuyển. Cần đo thêm hàng chờ vì các ca chuyển duyệt vẫn cần người xử lý.
- **Điều còn chưa chắc** — Khi nhiều yêu cầu hoàn tự động chạy đồng thời, phép kiểm số đã hoàn và việc ghi sổ có cần thực hiện cùng một giao dịch để bảo đảm giữ đúng trần ngày không?
