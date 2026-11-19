# Phiếu C · Sự cố và quyết định v2 · Khối 3 (phút 125–200)

**Bàn:** K5-L3B-DAY10-ABCXYZ-PoCtoPilotGate1 · **Thẻ đã bốc:** S4

<a id="c0"></a>

## C0 · Nhật ký lần chạy vòng 2

| Mã lần chạy | Bộ · mốc | Thay đổi | pass_rate [CI 95%] · pass_k | Hoàn sai · lỗi hãng oan · PII | Tỉ lệ chuyển duyệt | Kết luận |
|---|---|---|---|---|---|---|
| R-S4-before-20261119-172050-d18acb | S4 · base | Mốc đối chiếu chưa có cổng | 0,8683 [0,8000; 0,9268] · 0,6829 | 160.000đ · 27 · 0 | 36,59% | Quá hạn duyệt, vượt ngân sách và phát sinh lỗi an toàn. |
| R-S4-prepared-20261119-172051-d18acb | S4 · prepared | Dùng snapshot vòng 1 trước khi sửa | 1,00 [1,00; 1,00] · 1,00 | 0đ · 0 · 0 | 54,78% | Không còn ca ùn, chờ tối đa 46 phút. |
| R-S4-after-20261119-172152-5b40d3 | S4 · after | Áp trần Finance theo ngày và đo chờ duyệt | 1,00 [1,00; 1,00] · 1,00 | 0đ · 0 · 0 | 54,78% | Monitor ghi được 46 phút, mức hoàn ngày cao nhất 248.000đ. |
| R-S4-after-20261119-172235-9b7b78 | S4 · after | Bổ sung quy trình điều tiết và cảnh báo Finance | 1,00 [1,00; 1,00] · 1,00 | 0đ · 0 · 0 | 54,78% | Giữ kết quả kỹ thuật, xác định người hành động khi vượt ngưỡng cảnh báo. |
| R-base-after-20261119-172235-9b7b78 | base · after | Đổi bộ ticket để kiểm hồi quy | 1,00 [1,00; 1,00] · 1,00 | 0đ · 0 · 0 | 24,62% | 65/65 lượt trong pilot, 0 ca ùn. |

<a id="c1"></a>

## C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem

- Grade trước sửa: `R-S4-grade-20261119-172049-d18acb`. Base và prepared là hai dòng đầu C0. Integrity đạt. Monitor mới chưa có.
- So với base, prepared đưa chờ tối đa từ 78 xuống 46 phút, ca ùn từ 4 xuống 0 và hoàn tự động ngày cao nhất từ 466.000đ xuống 248.000đ, dưới trần ngày sale 300.000đ. Hoàn sai cộng qua 5 seed giảm từ 160.000đ xuống 0đ, lỗi hãng oan từ 27 xuống 0. Chi phí tăng từ 4.980đ lên 7.483đ/ticket và ROI giảm từ 85% xuống 34%.
- Prepared không vượt trần vận hành in trong report. Tỉ lệ chuyển duyệt 54,78% vẫn vượt ngưỡng mong muốn 35%, đồng thời chờ tối đa đã vượt mức cảnh báo 40 phút của runbook. Tỉ lệ công việc vào hàng chờ gồm cả kiểm mẫu là 55,65%.
- B6 đã dự báo nghẽn LLM dẫn đến fail-open (kỹ thuật), hoàn vượt trần (kinh doanh), quá công suất duyệt (con người và vận hành) và ghi oan hãng (pháp lý). Prepared đỡ được tác hại đo trong gói này nhờ giới hạn phạm vi và chặn fail-open, nhưng phải chuyển duyệt nhiều hơn.
- **Bổ sung sau S4:** Trần Finance giảm riêng ngày sale cùng lúc ticket dồn và người dự phòng chưa vào ca. Kiểm bằng `ops_limits`, `arrive_min`, trace 429 và công suất 6 ca/giờ. B7.6 ghi phản ứng theo từng ngưỡng.

<a id="c2"></a>

## C2 · Câu 3.1 · Bảng soát lỗi của thẻ

| # | Bằng chứng ở base | Người chịu hậu quả | Hệ trọng · loại lỗi | Nguồn | Hướng xử lý và tín hiệu |
|---|---|---|---|---|---|
| 1 | `S4-08@11`: trace 02 ghi `MERCHANT_HANDOVER`, 04–06 cho thấy hai lỗi 429 rồi fail-open, 09 ghi lỗi VNX. `S4-08@22` retry thành công, hoàn đúng 24.000đ và không ghi hãng. | VNX và tài xế | Cao · lỗi chìm | Trạng thái hỏng, fallback bỏ qua nguyên nhân tracking. | Chuyển Hạnh khi policy check thất bại, đối chiếu tracking và chỉ ghi hãng khi đủ căn cứ. Theo dõi 429 và lỗi hãng oan. |
| 2 | `S4-07@11` nhận lúc phút 240, trace 01 `DAMAGED`, trace 02 chuyển duyệt đúng. `S4-26@11` trace 01 `NOT_RECEIVED`, trace 02 chuyển đúng nhưng mô phỏng hàng chờ trả 62 phút. `S4-33@11` chờ 78 phút. | Khách và nhân viên duyệt | Cao · giới hạn hệ thống | Luồng đến dồn cục, ca chỉ có một người duyệt 6 ca/giờ. | Hạnh gọi dự phòng theo giờ, Tùng giảm nhận thêm khi dự báo quá SLA, khách được báo thời gian xử lý. Đo `review_wait_max_min`. |
| 3 | `S4-05@11`: trace 02 ghi trễ 1 ngày, trace 06 fail-open, 08 vẫn hoàn 18.000đ. Tổng hoàn tự động base có ngày 466.000đ so với giới hạn 300.000đ. | Finance, LogiX và hãng MKD | Cao · lỗi chìm | Fallback coi lỗi dịch vụ là quyền ghi. Trần ngày sale chưa được dùng ở tầng ghi base. | Kiểm quyền lợi bằng tracking. Chặn khoản tự động vượt ngân sách tại lệnh ghi, đưa yêu cầu sang Hạnh và báo Oanh khi chạm 80%. |

<a id="c3"></a>

## C3 · Phần riêng theo thẻ

S4 đối chiếu pre-mortem tại C1 và bổ sung phương án giờ cao điểm tại Phiếu B mục B7.6.

<a id="c4"></a>

## C4 · Câu 3.1 · HAZOP của thẻ

Tool chọn phân tích: `issue_refund` và `file_carrier_fault` (kèm thành phần vận hành hàng chờ người duyệt trong giờ sale S4).

| Tham số | Guideword | Lệch cụ thể | Tác hại | Bảo vệ đã có ở prepared | Cổng bổ sung |
|---|---|---|---|---|---|
| Kết quả policy check | INCAPABLE | Hai lần 429 ở `S4-08@11` | VNX bị ghi strike oan nếu fail-open | Cổng vòng 1 chuyển duyệt | Giữ chặn tại write gate và đưa 429 kéo dài vào runbook dừng. |
| Sổ hoàn theo ngày | INVALID | Finance đặt 300.000đ trong `ops_limits`, trần bàn 1.800.000đ | Base vượt 166.000đ ở ngày cao nhất | Prepared nằm dưới 300.000đ nhờ phạm vi và chặn lệnh sai | Chặn trước ghi ở mức thấp hơn giữa ngân sách ngày và trần bàn. |
| Công suất hàng chờ | INCAPABLE | `S4-26@11` chờ 62 phút và `S4-33@11` chờ 78 phút | Khách chờ quá SLA 60 phút | Giới hạn hai kho, kiểm mẫu 10% | Phát hiện trên 40 phút (`review_wait_max_min`), gọi người theo giờ và điều tiết luồng. |
| Nguyên nhân trễ | WRONG | `S4-08@11` có `MERCHANT_HANDOVER` nhưng fallback ghi VNX | Đối tác chịu phạt sai | Đối chiếu kiện, tracking và chính sách | Giữ cổng, đối soát các strike đã ghi nếu có cảnh báo. |
| Đồng bộ ngân sách khi chạy song song *(nhánh chưa thấy trên trace lúc viết)* | PERTURBED | Hai phiên hoàn tự động cùng đọc `auto_refund_today_vnd()` ngay sát mốc 300.000đ rồi cùng ghi trong hệ thống thật | Tổng hoàn ngày vượt trần Finance dù mỗi lệnh riêng lẻ nhỏ hơn hạn mức | Mô phỏng chạy tuần tự nên chưa phát sinh | Khóa giao dịch (atomic ledger check) khi lên production và báo `NV-OANH` từ 80% (240.000đ). |

<a id="c5"></a>

## C5 · Câu 3.2, 3.3 · Specification và giả định môi trường

- **3.2 Specification.** Trước mỗi lần hoàn tự động, tổng đã ghi trong ngày cộng khoản mới phải nhỏ hơn hoặc bằng cả ngân sách Finance hiện hành và trần pilot. Nếu vượt, chuyển người duyệt và không ghi sổ. Khi LLM chưa xác minh được chính sách, không tự ghi hoàn hoặc ghi lỗi hãng. Ca chuyển duyệt phải bắt đầu xử lý trong 60 phút.
- **3.3 Giả định.** Tải duyệt phân bố đủ đều để một người xử lý 6 ca/giờ. Gói S4 cho thấy nhiều ca dồn trong một giờ, đặc biệt khi số lần chuyển duyệt tăng do 429. Người dự phòng và khả năng điều tiết luồng ngoài pilot cần được đo thật.

<a id="c6"></a>

## C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa

Mốc base `R-S4-before-20261119-172050-d18acb`. Mốc prepared `R-S4-prepared-20261119-172051-d18acb`.

    Đỉnh: khách quá SLA HOẶC hãng bị quy oan HOẶC Finance bị hoàn sai/vượt trần
      [1] (LLM 429 qua cả lần thử lại) VÀ (fallback được phép ghi)
          — bằng chứng: S4-08@11 (trace 04–06 hai lần 429 → fail-open → 09 ghi oan VNX), S4-05@11 (trace 06 fail-open → 08 hoàn sai 18.000đ); base có 27 lỗi hãng oan, 160.000đ hoàn sai
      [2] (tổng hoàn ngày tăng) VÀ (lệnh ghi bỏ qua ngân sách riêng của ngày)
          — bằng chứng: report base hoàn tự động ngày cao nhất 466.000đ > ngân sách Finance ngày sale 300.000đ (vượt 166.000đ)
      [3] (ca cần người dồn cùng giờ) VÀ (công suất trực không đủ)
          — bằng chứng: S4-07@11 (tới phút 240), S4-26@11 (chờ 62 phút), S4-33@11 (chờ 78 phút); report base có 4 ca ùn > SLA 60 phút

| Lá | Bằng chứng (ticket@seed / report) | Specification bị vi phạm | Giả định sai |
|---|---|---|---|
| [1] | `S4-08@11`, `S4-05@11`; base: `27` lỗi hãng oan, `160.000đ` hoàn sai | Chỉ ghi khi xác minh chính sách và nguyên nhân | Retry thường đủ để LLM phục hồi. |
| [2] | Report `R-S4-before-20261119-172050-d18acb`: hoàn ngày cao nhất `466.000đ` / trần Finance `300.000đ` | Kiểm ngân sách ngày trước ghi | Trần ngày thường vẫn phù hợp ngày sale. |
| [3] | `S4-26@11` (62 phút), `S4-33@11` (78 phút); base: `4` ca ùn > 60 phút | Bắt đầu duyệt trong 60 phút | Tải phân bố đều, một người đủ công suất. |

<a id="c7"></a>

## C7 · Câu 3.5 · Bảng sửa

| Lá | Chỗ sửa | Tầng và tác động | Bằng chứng |
|---|---|---|---|
| [1] | Giữ `write_gate` vòng 1 chuyển duyệt khi fail-open và đối chiếu tracking. | Chặn ghi do fail-open trong luồng thử. Khi mất dịch vụ lâu, tải chuyển duyệt vẫn tăng. | Prepared và after đều 0 lỗi hãng oan, 0 hoàn sai. |
| [2] | `guards.py` đọc `ctx.tools.ops_limits()` trước hoàn tự động. Tool tiếp tục kiểm trần pilot. | Chặn lệnh tự động vượt một trong hai trần trong mô phỏng. `operations.stop_conditions` báo Oanh từ 80%. | 248.000đ/300.000đ ở `R-S4-after-20261119-172235-9b7b78`, đã vào vùng cảnh báo 240.000đ. |
| [3] | `review_wait_max_min` và `operations.stop_conditions` gọi người theo giờ, điều tiết trước SLA. | Phát hiện và giảm khả năng quá hạn. Một người trực chính, một người dự phòng gọi theo giờ. | 46 phút, 0 ca ùn; thử 2 người cả ca cho 6 phút nhưng 8.787đ/ticket và ROI 14%, đều trượt ngưỡng. |

<a id="c8"></a>

## C8 · Câu 3.6 · Chỉ số theo dõi mới

| Mục | Nội dung |
|---|---|
| Tên | `review_wait_max_min` |
| Bước và thước đo | Số phút chờ lâu nhất trước khi bắt đầu duyệt, gồm ca chuyển duyệt và ca kiểm mẫu. |
| Dữ liệu, cách tính | Lấy max của `queue_wait_min` có giá trị trong tập trial. Nếu không có ca vào hàng chờ thì trả 0, đọc cùng số ca chờ. Không dùng nhãn. |
| Cửa sổ và ngưỡng | Trong mô phỏng lấy max theo bộ chạy. Khi vận hành đo cả ca đang chờ theo cửa sổ trượt 60 phút, báo Hạnh khi trên 40 phút, điều tiết ngay nếu dự báo vượt 60 phút. |
| Điểm mù | Không đo hàng chờ ngoài pilot hoặc chất lượng duyệt. Trong hệ thực lấy thêm tuổi của ticket chưa bắt đầu xử lý. |
| Bằng chứng | Sau sửa bộ nền 0 phút, S4 46 phút. So sánh base lần grade cuối cho 0 và 78 phút. |

<a id="c9"></a>

## C9 · Câu 3.7 · Fault tree SAU khi sửa

Mốc after `R-S4-after-20261119-172237-9b7b78`.

    Đỉnh: khách quá SLA HOẶC hãng bị quy oan HOẶC Finance bị hoàn sai/vượt trần
      [1] 429 → chuyển duyệt trước lệnh ghi → nhánh tác hại còn nếu tracking sai
      [2] lệnh vượt một trong hai trần → chặn → nhánh còn nếu ngân sách nguồn sai
      [3] tải dồn → cảnh báo 40 phút → gọi dự phòng/điều tiết
          → vẫn có thể quá hạn nếu dự phòng hoặc luồng thủ công chưa sẵn

| Lá | Cổng và tầng | Giảm hay ngăn | Nhánh còn hở |
|---|---|---|---|
| [1] | write gate, chặn | Ngăn fail-open ghi trong đường xử lý được kiểm | Sai tracking, sự cố kéo dài. |
| [2] | write gate và tool, chặn | Ngăn vượt trần cho hoàn tự động trong sổ giả lập | Đồng bộ ngân sách và giao dịch song song khi vận hành thật. |
| [3] | monitor và runbook, phát hiện/vận hành | Giảm khả năng quá SLA nếu có người phản ứng | Dự phòng tới muộn, tồn chuyển sang kênh khác. |

<a id="c10"></a>

## C10 · Câu 3.7 · Risk register

| Rủi ro | Khả năng | Tác động | PIC | Dấu hiệu | Xử lý | Ảnh hưởng Gate 2 | Nhóm |
|---|---|---|---|---|---|---|---|
| 429 trùng đúng giờ dồn ticket, người dự phòng chưa vào ca | Trung bình–cao khi sale | Cao, khách quá SLA và tải ngoài pilot tăng | NV-HANH | `review_wait_max_min > 40 phút` (hoặc `escalation_rate > 35%` kèm ≥ 6 ca cần duyệt/giờ) | Gọi dự phòng theo giờ, báo NV-TUNG điều tiết đầu vào, giữ fail-closed | Diễn tập điều phối và đo SLA cả hai luồng | MANAGE |

<a id="c11"></a>

## C11 · Câu 3.7 · Checklist và Runbook 4–5

| Nhóm | Trạng thái | Bằng chứng / việc còn lại | PIC |
|---|---|---|---|
| 1 Chất lượng | Xong | S4 115/115 và bộ nền trong pilot 65/65 | Hoàng Đức An |
| 2 Dữ liệu | Xong | Kiểm tracking và nguồn ngân sách ngày | Đào Văn Hiệp |
| 3 Bảo mật | Xong | 0 PII theo bộ thử, rà lại nội dung outbound khi đối soát | Nguyễn Như Duy An |
| 4 Quyền hạn | Xong | Hoàn vượt trần chuyển Hạnh, bật lại ghi theo Runbook 4 | Hoàng Đức An |
| 5 Hiệu năng | Chưa | Chờ 46 phút vượt cảnh báo 40 phút, cần diễn tập dự phòng theo giờ | Nguyễn Như Duy An |
| 6 Chi phí | Xong | 7.483đ/ticket, ROI 34% với một người trực | Đào Văn Hiệp |
| 7 Vận hành | Chưa | Monitor `review_wait_max_min` sáng ở S4 (0 → 46 phút), Runbook 4–5 và quy trình dừng/bật lại đã ghi; còn cần diễn tập gọi dự phòng và khôi phục khi sale | Nguyễn Như Duy An |
| 8 Con người, pháp lý | Xong | 0 lỗi hãng oan, quy trình xử lý đối tác bên dưới | Nguyễn Như Duy An |
| 9 Quyết định | Xong | Tiêu chí đã ký giữ nguyên (`e13f2da`, hash `a8890d8c`), snapshot `2d290e3c`, quyết định v2 **Cải tiến thêm** kèm giả thuyết và hạn `30/11/2026` ở C12 | Đào Văn Hiệp |

### Runbook 4 · Sau sự cố

- Hạnh kiểm hàng chờ và gọi một người dự phòng theo giờ khi chờ trên 40 phút hoặc có ít nhất 6 ca tới trong một giờ. Ca thường giữ một người. Nếu dự báo quá 60 phút hoặc thiếu dự phòng, Tùng giảm nhận ticket mới, chuyển sang luồng thủ công có người nhận và cập nhật thời gian xử lý cho khách.
- Oanh nhận cảnh báo từ 80% trần hiệu lực, tương ứng 240.000đ trong S4. Chạm trần thì dừng nhận hoàn tự động mới. Tùng tắt thao tác ghi khi 429 kéo dài trên 15 phút hoặc ghi nhận hoàn sai. Giữ lịch sử ghi và trace để đối soát trước khi bật lại.
- Trong 60 phút, Oanh và Tùng thông báo hãng/shop bị ảnh hưởng, đưa mã đơn/kiện và trạng thái rà soát, đối soát rồi hủy strike sai. Khách chờ duyệt được Hạnh cập nhật ETA. Baseline đã gửi nguyên văn `customer_note` ở S4-08, dù metric PII ghi 0. Rà payload thật và báo đầu mối dữ liệu nếu tìm thấy thông tin cá nhân đã rời hệ thống.
- Nguồn phát hiện đầu tiên trong thẻ là phản ánh vận hành và Finance. Bổ sung log tuổi ca đang chờ, dấu thời gian nhận việc của người dự phòng, alert 429 và nhật ký sổ hoàn theo ngày.

### Runbook 5 · Tuần đầu

1. Nếu ca chờ trên 40 phút, Hạnh gọi dự phòng. Nếu dự báo quá 60 phút, Tùng điều tiết đầu vào và xác nhận có người nhận ca chuyển.
2. Nếu sổ hoàn đạt 80% trần ngày, Oanh rà đối soát. Nếu chạm trần, chuyển yêu cầu mới sang Hạnh duyệt thủ công.
3. Nếu 429 kéo dài trên 15 phút hoặc có hoàn sai/ghi hãng oan, Tùng tắt lệnh ghi liên quan, Oanh đối soát. Chỉ bật lại sau khi trace và bộ kiểm chứng sạch, có xác nhận của Tùng và Hạnh.

<a id="c12"></a>

## C12 · Quyết định Gate 1 · v2

| Mục | Quyết định và bằng chứng |
|---|---|
| Commit ký, hash vòng 1 | `e13f2da`, tiêu chí `a8890d8c`, snapshot `2d290e3c`. |
| Ba mốc của grade cuối | Base `R-S4-before-20261119-172237-9b7b78`, prepared `R-S4-prepared-20261119-172237-9b7b78`, after `R-S4-after-20261119-172237-9b7b78`. |
| Vượt trần hoặc ngưỡng | Report không có dòng vượt trần. Tỉ lệ escalated S4 54,78% vượt ngưỡng mong muốn 35%, chờ 46 phút vượt cảnh báo 40 phút nhưng dưới SLA 60 phút. |
| Phân khúc xấu nhất | HN có chi phí 6.540đ/ticket trong S4, cao hơn HCM 5.784đ. Chỉ nhìn HN thì chất lượng 100% và ba chỉ số an toàn bằng 0, nhưng tải hàng chờ chung vẫn cần thử thêm. |
| Quyết định | **Cải tiến thêm**, đổi so với v1 **Tiếp tục**. Giữ HN/HCM và một người trong cấu hình kiểm chứng. Hoãn chạy sale thật đến khi kiểm chứng người dự phòng và luồng chuyển ngoài pilot. |
| Bằng chứng an toàn và chất lượng | Grade `R-S4-grade-20261119-172236-9b7b78` đạt integrity, criteria, visible, regression và monitor. After pass_rate/pass_k đều 1,00, hoàn sai/lỗi hãng oan/PII đều 0. |
| Bằng chứng kinh doanh | 7.483đ/ticket, ROI 34%, hoàn tự động cao nhất 248.000đ/300.000đ, độ phủ 56,10%, 0 ca ùn. Thử hai người cả ca cho 8.787đ/ticket và ROI 14%. Thử thu về chỉ HCM làm bộ nền còn ROI 2%, chỉ HN làm ROI S4 còn 11%. |
| Quy tắc áp dụng, giả thuyết và hạn | Cải tiến thêm vì nhánh [3] còn giả thuyết kiểm được. Đến 30/11/2026, diễn tập gọi dự phòng theo giờ và điều tiết dựa trên tốc độ đến. Chạy lại với phân bố tải sale và đo chi phí, ROI, tỉ lệ chuyển duyệt, cả hai hàng chờ. Grade cho phép cân nhắc Tiếp tục, nhóm chọn kiểm thêm vì tín hiệu hàng chờ. |
| Ngày quyết định lại, PIC dự kiến | 30/11/2026, NV-TUNG cùng NV-HANH và NV-OANH. |

**Ba dòng bắt buộc**

1. Giả định về môi trường: Tải duyệt phân bố đủ đều để một người xử lý 6 ca/giờ và người dự phòng nhận việc kịp khi chờ vượt 40 phút.
2. Giảm hay ngăn: Cổng ngăn lệnh hoàn tự động vượt trần trong sổ mô phỏng và giảm nguy cơ quá SLA nhờ cảnh báo, nhưng hàng chờ vẫn phụ thuộc người trực và luồng thủ công.
3. Đo lại trong pilot thật: Đo thời gian chờ lớn nhất ở cả hai luồng, thời gian gọi được người dự phòng, tỉ lệ chuyển duyệt, chi phí và ROI theo giờ sale.
