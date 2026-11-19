# Tài liệu Lab 9 dùng chung cho Gate 1

Chọn cặp tài liệu LogiX-VN refund agent ở cùng commit `60cbad7f253bb2754094b38c76af9a92a8fce8a7`. Cả hai dẫn đến baseline `E-swarm-20261118-6a48`, bộ eval v1 gồm 14 ca × 5 seed trên MockLLM.

- [PRD v1.1](https://github.com/daohiep2903/K5-L3B-DAY09-DaoVanHiep-2A202603813-EvaluationandFailureAnalysis/blob/60cbad7f253bb2754094b38c76af9a92a8fce8a7/docs/PRD_v1.1.md) mô tả phạm vi pilot hoàn tiền đơn lẻ do giao trễ, ngưỡng chất lượng và cổng release.
- [Eval card](https://github.com/daohiep2903/K5-L3B-DAY09-DaoVanHiep-2A202603813-EvaluationandFailureAnalysis/blob/60cbad7f253bb2754094b38c76af9a92a8fce8a7/docs/eval_card.md) ghi nguồn dữ liệu, cấu hình đo, kết quả baseline và hồi quy. Kết quả này là bằng chứng của Lab 9. Lab 10 sẽ đo riêng trên bộ nền 22 ticket × 5 seed.

## Ghi chú khi đọc dữ liệu Lab 10

[`data/world.json`](../data/world.json) là dữ liệu giả tại ngày 2026-11-16, gồm 25 đơn hàng, 5 kho, 5 hãng vận chuyển, các bản chính sách, hồ sơ phê duyệt và dữ liệu sổ hoàn tiền ban đầu.

- `REFUND-v3` đang có hiệu lực tại ngày mô phỏng, với hạn mức tự động 200.000đ. `REFUND-v4` có hiệu lực từ 2026-12-01 và hạ hạn mức này xuống 100.000đ.
- Ngoài hạn mức từng khoản theo chính sách, `ops_limits` đặt trần hoàn tự động 300.000đ mỗi khách mỗi ngày, ngân sách hoàn tự động 2.000.000đ mỗi ngày và tối đa 2 lượt ghi lỗi tự động mỗi hãng mỗi ngày.
- Ca chuyển người duyệt có SLA tiếp nhận 60 phút. Ca mặc định có một người duyệt với năng suất 6 ca/giờ. Chi phí làm tay là 10.000đ/ticket và trần chi phí LLM là 1.500đ/ticket.
