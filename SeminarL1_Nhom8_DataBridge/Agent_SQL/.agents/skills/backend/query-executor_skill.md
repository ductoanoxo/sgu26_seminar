---
name: query-executor_skill
description: "Quy trình thực thi SQL an toàn thông qua lớp bảo mật (Security Layer) và quản lý kết nối (Database Manager) sử dụng psycopg2."
metadata:
  author: antigravity
  version: "0.2.0"
---

# SQL Query Executor & Security

## Core Principles

**1. Multi-Layer Validation (Lớp bảo mật đa tầng)**
Trước khi thực thi, câu lệnh SQL phải đi qua `validate_sql` để kiểm tra:
- **Keyword Check**: Từ chối các từ khóa nguy hiểm (`INSERT`, `UPDATE`, `DROP`, `ALTER`, ...).
- **Pattern Check**: Phát hiện các mẫu tấn công như `;` (Multiple statements), `--` hoặc `/*` (Comments).
- **Sanitization**: Xóa bỏ các ký tự thừa và chuẩn hóa câu lệnh.

**2. Read-Only Enforcement (Cưỡng chế chỉ đọc)**
Kết nối cơ sở dữ liệu được thiết lập ở chế độ `readonly=True`. Đây là lớp phòng thủ cuối cùng ngay cả khi lớp validation bị vượt qua.

**3. Type-Safe Serialization**
Dữ liệu trả về từ PostgreSQL (như `Decimal`, `DateTime`) phải được chuyển đổi sang định dạng JSON-serializable (String/ISO Format) để Frontend có thể hiển thị.

## Execution Workflow

### 1. Security Layer (core/security.py)
Dự án sử dụng Regex để lọc các từ khóa cấm:
- `FORBIDDEN_KEYWORDS`: Danh sách các lệnh làm thay đổi dữ liệu.
- `DANGEROUS_PATTERNS`: Các kỹ thuật bypass hoặc phá hoại hệ thống.
- **String Literal Protection**: Hàm `_remove_string_literals` giúp tránh nhận diện nhầm từ khóa bên trong chuỗi text của người dùng.

### 2. Database Layer (core/database.py)
- Sử dụng thư viện `psycopg2` với `RealDictCursor` để kết quả trả về là một danh sách các Dictionary.
- Quản lý kết nối bằng `contextmanager` để đảm bảo luôn đóng connection (close) kể cả khi có lỗi xảy ra.

### 3. Response Structure
Kết quả trả về luôn có cấu trúc cố định:
```json
{
    "success": true,
    "columns": ["id", "name", "email"],
    "rows": [...],
    "row_count": 10,
    "error": null
}
```

## Security Checklist (Dành cho Developer)

- [x] **ReadOnly Session**: Đã gọi `conn.set_session(readonly=True)` chưa?
- [x] **Multiple Statements**: Đã chặn dấu chấm phẩy `;` chưa?
- [x] **Comments**: Đã chặn `--` và `/*` để tránh SQL Injection chưa?
- [x] **Timeouts**: Đã thiết lập timeout cho câu lệnh (nếu cần) để tránh treo connection?

## Error Handling
Lỗi từ Database phải được bắt lại, log chi tiết ở Backend nhưng chỉ trả về thông báo an toàn/dễ hiểu cho Frontend để tránh lộ thông tin hệ thống (Information Leakage).
