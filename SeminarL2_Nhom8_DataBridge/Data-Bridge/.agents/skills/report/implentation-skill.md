# Skill: Module Implementation Plan & Progress Report Generation (Indigo Style)

Kỹ năng này hướng dẫn AI Agent tạo ra các bản kế hoạch triển khai (Implementation Plan) và báo cáo tiến độ (Progress Report) cho **TẤT CẢ CÁC MODULE** (Frontend, Backend, Database, Infrastructure, QA Automation, v.v.) của dự án Agent_SQL, sử dụng phong cách thiết kế **Indigo Premium**.

## 1. Đặc điểm nhận diện phong cách
- **Màu chủ đạo (Primary)**: `#6366f1` (Indigo).
- **Màu nền**: `#f5f3ff` (Tím nhạt).
- **Prompt Box**: Nền đen xanh (`#0f172a`), font Courier New, viền trái Indigo.
- **Tiêu đề (H2)**: Có gạch đứng Indigo bên trái (`border-left: 4px solid var(--primary)`).

---

## 2. Mã nguồn Template HTML chuẩn

AI Agent phải sử dụng mã nguồn này khi tạo file HTML cho kế hoạch triển khai và báo cáo:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Implementation Plan: [Module Name]</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --bg: #f5f3ff;
            --card-bg: #ffffff;
            --text-main: #1e1b4b;
            --text-muted: #475569;
            --danger: #ef4444;
            --success: #10b981;
            --accent: #f8fafc;
        }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg); color: var(--text-main); line-height: 1.6; margin: 0; padding: 0; }
        .container { max-width: 900px; margin: 40px auto; padding: 40px; background: var(--card-bg); border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); }
        header { border-bottom: 2px solid #eef2ff; margin-bottom: 30px; padding-bottom: 20px; }
        h1 { font-size: 2.5rem; font-weight: 700; color: var(--primary); margin: 0 0 10px 0; }
        .meta { display: flex; gap: 20px; font-size: 0.9rem; color: var(--text-muted); }
        .badge { padding: 4px 12px; border-radius: 9999px; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; }
        .badge-purple { background: #e0e7ff; color: var(--primary); }
        h2 { font-size: 1.5rem; margin-top: 40px; border-left: 4px solid var(--primary); padding-left: 15px; color: var(--text-main); }
        .step { margin-bottom: 30px; padding: 24px; background: #fafafa; border-radius: 12px; border: 1px solid #e2e8f0; }
        .prompt-box { background: #0f172a; color: #f1f5f9; padding: 20px; border-radius: 8px; font-family: 'Courier New', Courier, monospace; position: relative; margin-top: 15px; border-left: 4px solid var(--primary); }
        .prompt-box::before { content: "PROMPT GỬI AI AGENT"; position: absolute; top: -10px; right: 15px; background: var(--primary); color: white; padding: 2px 10px; font-size: 0.7rem; border-radius: 4px; font-family: 'Inter', sans-serif; font-weight: 700; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th { background: var(--primary); color: white; padding: 12px; text-align: left; }
        td { padding: 12px; border-bottom: 1px solid #eee; }
        .checklist { list-style: none; padding: 0; }
        .checklist li { display: flex; align-items: center; gap: 12px; padding: 10px; background: #fff; border: 1px solid #f1f5f9; margin-bottom: 8px; border-radius: 8px; }
        .checkbox { width: 18px; height: 18px; border: 2px solid var(--primary); border-radius: 4px; flex-shrink: 0; }
        footer { text-align: center; margin-top: 60px; color: var(--text-muted); font-size: 0.85rem; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Content -->
    </div>
</body>
</html>
```

---

## 3. Quy tắc viết Prompt cho AI Agent

Khi tạo Implementation Plan cho bất kỳ module nào (QA, Infra, Frontend, Backend), AI Agent cần:
- Cụ thể hóa tác vụ, mô tả rõ đầu vào và kết quả mong đợi.
- Sử dụng Code Blocks với tag `text` cho các AI Prompts.
- Tham chiếu đến các skill cụ thể nếu cần (ví dụ: skill test, skill docker, skill frontend).
- **QUAN TRỌNG:** Luôn tham chiếu file `docs/implementplan_overview.md` để lấy bối cảnh, độ ưu tiên và yêu cầu gốc của từng module trước khi tạo báo cáo hoặc kế hoạch.

### 3.1. Mẫu định dạng Markdown (Implementation Plan)

```markdown
# Implementation Plan: [Tên Module]

## 1. Overview (Tổng quan)
[Phân tích dựa trên docs/implementplan_overview.md: Module này giải quyết vấn đề gì? Tại sao nó quan trọng? Công nghệ chính là gì?]

---

## 2. Các bước triển khai chi tiết
### Bước [X]: [Tên giai đoạn mang tính chiến lược]
**Mục tiêu:** [Kết quả cuối cùng của giai đoạn này là gì?]
- **Tác vụ 1:** [Hành động cụ thể: Viết code/Cấu hình/Sửa file] - [Mục tiêu kỹ thuật].
- **Tác vụ 2:** [Hành động cụ thể] - [Kiểm soát chất lượng/Verify].

> **Prompt gửi AI Agent:**
> ```text
> "Dựa trên cấu trúc thư viện [Path], hãy thực hiện [Action]. Đảm bảo tuân thủ [Tiêu chuẩn: Clean Code/Security/Indigo Style]. Kết quả: [File/Component]."
> ```
```

### 3.2. Logic sinh Tác vụ linh hoạt (Module-Specific Logic)

AI Agent phải tùy biến danh sách tác vụ dựa trên đặc thù của từng nhóm module sau đây:

| Loại Module | Trọng tâm Tác vụ (Task Focus) | Ví dụ Tác vụ Linh hoạt |
| :--- | :--- | :--- |
| **UI / Frontend** | Component, State, UX/UI, Responsive | Thiết lập Monaco Editor, Custom CSS theme, Xử lý SQL formatting logic. |
| **Security / DevSecOps** | Scanning, Permissions, Hardening | Cấu hình Non-root user, Viết RLS Policy, Quét lỗ hổng bằng Trivy. |
| **Data / Backend** | Schema, Query, Caching, API | Masking Schema nhạy cảm, Thiết lập Redis cache, Tối ưu hóa SQL Query. |
| **Infra / Observability** | Config, Docker, Logs, CI/CD | Cài đặt OpenTelemetry Collector, Viết Docker Compose, Setup GitHub Actions. |
| **QA / Testing** | Automation, Scenarios, Performance | Viết Pytest cho API /auth, Setup k6 load test, Auto-generate Test Report. |

---

---

## 4. Danh sách các Module tham chiếu (Từ `docs/implementplan_overview.md`)

Khi tạo Report hoặc Plan, AI Agent **phải đối chiếu** với một trong 11 module sau đã được định nghĩa trong Roadmap của dự án:

**🔴 Ưu tiên Cao (Critical):**
1. Security Hardening & Non-root Docker (Trivy scan, `validate_sql`, appuser).
2. Kiểm thử Toàn diện - QA Automation (API, k6, Pytest, test reports).
3. Frontend — SQL Editor & Playground (Monaco editor, formatting, limits).

**🟡 Ưu tiên Trung bình (Core Features):**
4. Dashboard & Widget Nâng cao (Drag & drop, auto-refresh, filter).
5. Kết nối Dữ liệu Động (Data Import, Connection string, Schema masking).
6. Lịch sử & Chia sẻ Truy vấn (UI history, Supabase migrate).
7. Quản lý Người dùng & Phân quyền (Supabase Auth, RLS, Audit).
8. Kiểm soát Chi phí & Caching (Semantic cache, Rate limiting).
9. Tầng ngữ nghĩa - Business Semantic Layer (Glossary, Vector DB).

**🟢 Ưu tiên Thấp (Enhancements):**
10. AI Nâng cao (AI Insights, Multi-turn context).
11. Hạ tầng & Observability (OpenTelemetry, Alloy, CI/CD).

---

## 5. Khi nào sử dụng Skill này?
Sử dụng cho các tác vụ liên quan đến:
- Lên kế hoạch (Implementation Plan) cho bất kỳ module nào trong danh sách trên.
- Chuẩn hóa cấu trúc tài liệu thiết kế.
- **Tạo báo cáo tiến độ (Progress Report)** tổng hợp để theo dõi tình trạng dự án theo đúng roadmap.

---

## 6. Template Báo cáo tiến độ (Progress & Results Report)

Khi được yêu cầu tạo báo cáo tiến độ/nghiệm thu cho **bất kỳ module nào**, AI Agent phải sử dụng cấu trúc sau để đảm bảo đầy đủ thông tin về **Tiến trình (Progress)**, các hạng mục đã xong, đang làm và các chỉ số đo lường (nếu có):

### 6.1. Prompt gợi ý để AI tạo Báo cáo Tiến độ
> **PROMPT GỬI AI AGENT:**
> ```text
> "Dựa trên file `docs/implementplan_overview.md`, Implementation Plan hiện tại của module [Tên Module] và tiến độ thực tế trong workspace, hãy tạo một Progress Report theo phong cách Indigo Premium. Cập nhật phần Tiến trình tổng quan (tính phần trăm), bảng chỉ số đánh giá (nếu có), liệt kê rõ các hạng mục đã xong/đang làm và các blocker. Xuất ra cả file .md và .html."
> ```

### 6.2. Cấu trúc Markdown Báo cáo
```markdown
# Progress Report: [Tên Module]
**Ngày cập nhật:** [Ngày/Tháng/Năm]
**Trạng thái tổng thể:** [Hoàn thành | Đang triển khai | Chậm tiến độ | Blocked]

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** [X]
- **Đã hoàn thành:** [Y]
- **Tiến độ (Completion):** [XX]%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria - Nếu có)
*(Bảng này sử dụng để đo lường các module như QA Automation, Performance, Infra)*
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **API Coverage/Uptime** | > 95% | [XX]% | [✅/❌] |
| **Latency/Performance** | < 1.5s | [X.Xs] | [✅/❌] |
| **Success Rate** | 100% | [XX]% | [✅/❌] |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- [x] **[Tên tác vụ]**: [Mô tả ngắn gọn kết quả đạt được].
- [x] **[Tên tác vụ]**: [Mô tả ngắn gọn kết quả đạt được].

## 🚧 Đang triển khai (In Progress)
- [ ] **[Tên tác vụ]**: [Trạng thái hiện tại] - Dự kiến xong [Ngày].
- [ ] **[Tên tác vụ]**: Đang chờ [Phụ thuộc - vd: Chờ review API].

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **[Vấn đề]**: [Mô tả chi tiết và đề xuất giải pháp].

## 📅 Kế hoạch tiếp theo (Next Steps)
1. [Bước tiếp theo 1]
2. [Bước tiếp theo 2]
```
