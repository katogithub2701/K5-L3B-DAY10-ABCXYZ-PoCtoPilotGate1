# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): ABCXYZ
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-ABCXYZ-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

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

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenNhuDuyAn-2A202603783

### Phần việc phụ trách

Vai **Vận hành và pháp lý** (Người 3); phụ trách `TEAM.md`, câu 1.2 & 1.4 và mục A5 (`templates/form-a-criteria.md`), câu 2.4 (`B4`, `B5`), câu 2.10 (`config/operating_gates.json` mục `operations` & `legal`, `B7.5`–`B7.6`), Khối 3 (`C3`, `C4`, `C5` câu 3.3, `C7`, `C9`–`C11`), và gom kiểm bài nộp (`submission/submission.json`, `lab10.check_submission`).

### Đóng góp cụ thể

Khởi tạo thông tin nhóm và bảng thành viên `TEAM.md`; cập nhật mục A5 Phiếu A; lập HAZOP vòng 1 (B4) và Checklist 9 nhóm việc lần 1 (B5); cấu hình cổng `operations` và `legal` trong `config/operating_gates.json`; viết Runbook 1–3 & Giờ cao điểm (`B7.5`–`B7.6`); khởi tạo `team` và `members` trong `submission/submission.json` *(sẽ cập nhật thêm Khối 3 và gom bài nộp cuối buổi; có sử dụng trợ lý AI để rà soát mã nguồn/quy định và hỗ trợ soạn thảo tài liệu)*.

### Bằng chứng

[Sẽ cập nhật mã commit, mã lần chạy và dòng phiếu cuối buổi]

### Exit ticket

[Sẽ hoàn thiện sau phần demo cuối buổi]

## DaoVanHiep-2A202603813

### Phần việc phụ trách

Sản phẩm và kinh doanh. Phụ trách mục tiêu hệ thống và tiêu chí chấp nhận (câu 1.1, 1.6), bản đồ dữ liệu và drift (câu 2.3), cổng kinh doanh (câu 2.9 và phần `business` của câu 3.5), specification của thẻ (câu 3.2) và ghi quyết định v1/v2 sau khi nhóm chốt.

### Đóng góp cụ thể

- Chọn PRD v1.1 và eval card từ Lab 9 làm tài liệu chung, rồi viết mục tiêu hệ thống cho trợ lý hoàn tiền ở Phiếu A.
- Soạn bộ tiêu chí chấp nhận gồm ngưỡng chất lượng, an toàn, chi phí và ROI cùng quy tắc cho bốn quyết định Gate 1. Bộ tiêu chí đang chờ nhóm ký.
- Lập bản đồ nguồn dữ liệu của trợ lý và mô tả tình huống drift khi chuyển từ `REFUND-v3` sang `REFUND-v4`.
- Đặt cổng kinh doanh vòng 1 gồm trần hoàn tự động 1.800.000đ/ngày, ngân sách LLM 1.500đ/ticket, phạm vi bốn kho `HN`, `HCM`, `DN`, `CT` và ROI tối thiểu 11%.

### Bằng chứng

- Commit `9a9be90` cho câu 1.1 và `4e2dc07` cho tài liệu tham chiếu Lab 9.
- [Phiếu A mục A4](templates/form-a-criteria.md#a4) và [cấu hình tiêu chí](config/acceptance_criteria.json) cho câu 1.6.
- [Phiếu B mục B3](templates/form-b-evaluation-gates.md#b3) cho câu 2.3; mục B7.4 trong cùng phiếu và [cấu hình cổng](config/operating_gates.json) cho câu 2.9.

### Exit ticket

- Điều học được — Ngân sách LLM mỗi ticket chỉ là một phần chi phí vận hành. Khi xét ROI còn phải tính công xử lý các ca chuyển người duyệt.
- Điều còn chưa chắc — Với phạm vi bốn kho đã chọn, số ca chuyển người duyệt vào giờ cao điểm có vượt công suất và làm trượt ngưỡng ROI 15% hay không?

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
