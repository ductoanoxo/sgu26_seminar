---
name: nl2sql_skill
description: "Cách viết Prompt và vận hành Multi-Agent Pipeline cho bài toán NL2SQL. Dựa trên kiến trúc 3 Agent: Architect, Generator, và Validator."
metadata:
  author: antigravity
  version: "0.2.0"
---

# Multi-Agent NL2SQL Pipeline

## Core Principles

Dự án sử dụng kiến trúc **Multi-Agent** để tăng độ chính xác và bảo mật. Quy trình gồm 3 giai đoạn chính:

**1. Architect Agent (Phân tích Ý định)**
- Phân tích câu hỏi tự nhiên để xác định `intent`.
- Chọn các bảng (`selected_tables`) thực sự cần thiết từ Schema.
- Lập kế hoạch truy vấn (`query_plan`) bao gồm Join logic và Aggregation.

**2. SQL Generator Agent (Lập mã SQL)**
- Dựa trên phân tích của Architect để tạo câu lệnh PostgreSQL.
- Sử dụng Alias bảng (u, o, p) để câu lệnh ngắn gọn.
- Luôn kèm theo giải thích (`explanation`) bằng ngôn ngữ tự nhiên.

**3. Validator Agent (Kiểm định & Sửa lỗi)**
- Kiểm tra tính đúng đắn (`correctness`) so với yêu cầu người dùng.
- Kiểm tra an toàn (`safety`): Chỉ cho phép SELECT, không có SQL Injection.
- Tự động sửa lỗi (`corrected_sql`) nếu phát hiện sai sót nhỏ.

## Database Schema Context

Khi viết Prompt hoặc hướng dẫn, luôn dựa trên Schema thực tế của dự án:
- **users**: id, name, email, city, country.
- **products**: id, name, category, price, stock_quantity.
- **orders**: id, user_id, order_date, status, total_amount.
- **order_items**: id, order_id, product_id, quantity, unit_price.

## Prompt Design Rules

### JSON Response Format
Tất cả các Agent phải trả về kết quả ở định dạng JSON thuần để Pipeline có thể xử lý tự động:

**Architect Output:**
```json
{
    "intent": "...",
    "selected_tables": ["users", "orders"],
    "join_needed": true,
    "query_plan": "..."
}
```

**Generator Output:**
```json
{
    "sql_query": "SELECT ...",
    "explanation": "..."
}
```

## Security & Safety Rules

1. **SELECT-Only**: Tuyệt đối không tạo các lệnh `INSERT`, `UPDATE`, `DELETE`, `DROP`.
2. **Limit Enforcement**: Mặc định thêm `LIMIT 100` nếu người dùng không yêu cầu số lượng cụ thể.
3. **No Semicolons**: Tránh sử dụng dấu chấm phẩy `;` để ngăn chặn Multiple Statements.
4. **Join Quality**: Phải sử dụng `INNER JOIN` hoặc `LEFT JOIN` với mệnh đề `ON` rõ ràng, tránh Cross Join.
