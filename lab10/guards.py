"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Cổng vòng 1 kiểm tra chính sách, lệnh hoàn tiền và tác động lên hãng vận chuyển.
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("Không tìm thấy chính sách có hiệu lực")
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    tool = action["tool"]
    if tool == "notify_carrier":
        fields = {"order_id", "parcel_id", "district", "delay_days"}
        blocked = set(ctx.gates.get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
        payload = {key: value for key, value in action["payload"].items() if key in fields - blocked}
        return Verdict.modify("Chỉ gửi dữ kiện giao hàng cần thiết", payload=payload)

    if tool not in {"issue_refund", "file_carrier_fault"}:
        return Verdict.allow()

    if any(event["type"] == "llm_fallback" and event.get("mode") == "fail_open" for event in ctx.events):
        return Verdict.escalate("LLM chưa kiểm tra được chính sách")

    order = ctx.tools.lookup_order(action["order_id"])
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)

    if tool == "issue_refund":
        entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        amount = action["amount_vnd"]
        if amount != entitled or action["payer"] != "LOGIX":
            return Verdict.escalate("Khoản hoàn không khớp tracking và chính sách")
        previous = ctx.tools.ledger_rows(order_id=order["order_id"])
        if sum(row["amount_vnd"] for row in previous) + amount > entitled:
            return Verdict.deny("Khoản hoàn đã được ghi hoặc vượt quyền lợi còn lại")
        approval_id = action.get("approval_id")
        if approval_id or amount > policy["auto_limit_vnd"]:
            approvals = ctx.tools.lookup_approvals(
                approval_id=approval_id, order_id=order["order_id"], customer_id=order["customer_id"],
                status="valid",
            )
            approver = ctx.gates.get("operations", {}).get("approver_id")
            if not any(
                approval["expires_at"] >= ctx.as_of and approval["max_vnd"] >= amount
                and (not approver or approval["approver_id"] == approver)
                for approval in approvals
            ):
                return Verdict.escalate("Thiếu phê duyệt hợp lệ cho khoản hoàn")
        else:
            finance_cap = ctx.tools.ops_limits().get("daily_auto_refund_budget_vnd")
            if finance_cap is not None and ctx.tools.auto_refund_today_vnd() + amount > finance_cap:
                return Verdict.escalate("Vượt ngân sách hoàn tự động của Finance cho ngày hiện tại")
        return Verdict.allow()

    if not H.carrier_at_fault(policy, parcel, delay):
        return Verdict.deny("Tracking không đủ căn cứ ghi lỗi hãng")
    if action["parcel_id"] != parcel["parcel_id"] or action["delay_days"] != delay:
        return Verdict.modify(
            "Ghi lỗi theo kiện và độ trễ trong tracking",
            parcel_id=parcel["parcel_id"],
            carrier_id=parcel["carrier_id"],
            driver_id=parcel.get("driver_id"),
            delay_days=delay,
        )
    return Verdict.allow()
