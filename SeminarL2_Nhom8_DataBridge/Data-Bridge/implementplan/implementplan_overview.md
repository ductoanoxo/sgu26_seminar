# Tổng hợp các phần cần lên Implementation Plan

> Phân tích dựa trên: [PRD.md](file:///home/traductoan/Seminar_Final/docs/PRD.md) · [ROADMAP.md](file:///home/traductoan/Seminar_Final/docs/ROADMAP.md) · [user_story.md](file:///home/traductoan/Seminar_Final/docs/user_story.md) và code hiện tại.

---

## 📊 Tổng quan Trạng thái Hiện tại

| Thành phần | Trạng thái | Ghi chú |
|:---|:---|:---|
| API Gateway (Kafka orchestration) | ✅ Đã có | ask, explain, manual query, history, dashboard CRUD |
| NL2SQL Service (3-Agent pipeline) | ✅ Đã có | Architect → SQL Generator → Validator |
| Query Service (SQL execution) | ✅ Đã có | validate_sql, execute, health_check |
| Frontend (Next.js SPA) | ✅ Đã có | Hero search, SQL preview/edit, chart, dashboard panel |
| Dashboard Backend (Supabase) | ✅ Đã có | CRUD + refresh widgets + schema SQL |
| Kafka message bus | ✅ Đã có | KRaft mode, docker-compose |
| Docker (dev mode) | ✅ Đã có | Hot reload, multi-stage build |
| Tests | ⚠️ Sơ bộ | Chỉ có test cơ bản cho mỗi service |

---

## 🔴 Ưu tiên Cao (Nên làm Implementation Plan ngay)

### 1. 🛡️ Security Hardening & Non-root Docker

| | |
|:---|:---|
| **PRD** | S1 (Read-only Proxy), S2 (Hard Limit), S3 (Non-root) |
| **Trạng thái** | `validate_sql` đã có ở Query Service nhưng **chưa kiểm chứng** chặt chẽ (injection, multi-statement). Dockerfile chưa confirm chạy `appuser`. |
| **Cần làm** | |

- [ ] Audit `validate_sql` — cover hết SQL injection patterns, multi-statement, DDL/DML keywords
- [ ] Kiểm tra Dockerfile cả 3 service + frontend → đảm bảo `USER appuser` (non-root)
- [ ] Chạy **Trivy Scan** trên tất cả images (Skill: [trivy/SKILL.md](file:///home/traductoan/Seminar_Final/.agents/skills/security/trivy/SKILL.md))
- [ ] Verify Hard Limit (`LIMIT` auto-append) ở Query Service
- [ ] Sanitize error messages — không lộ stack trace/DB info ra frontend

> [!IMPORTANT]
> PRD yêu cầu **"không có code nào lên Production nếu chưa pass Trivy Scan"**. Đây là blocker cho mọi release.

---

### 2. 🧪 Kiểm thử Toàn diện (QA Automation)

| | |
|:---|:---|
| **PRD** | Section 5.3 — QA Standard |
| **Trạng thái** | Mỗi service chỉ có **1 file test** cơ bản (`test_gateway.py`, `test_nl2sql_service.py`, `test_query_service.py`) |
| **Cần làm** | |

- [ ] **API Integration Tests** — Pytest + Httpx cho tất cả endpoints (Skill: [api-integration/SKILL.md](file:///home/traductoan/Seminar_Final/.agents/skills/testing/api-integration/SKILL.md))
- [ ] **Performance Tests** — k6 load test cho `/ask`, `/query/manual`, dashboard refresh (Skill: [k6-performance/SKILL.md](file:///home/traductoan/Seminar_Final/.agents/skills/testing/k6-performance/SKILL.md))
- [ ] **Test Cases Generation** — Sinh test case tự động (Skill: [test-case-generation/SKILL.md](file:///home/traductoan/Seminar_Final/.agents/skills/testing/test-case-generation/SKILL.md))
- [ ] **Test Report** — Tổng hợp báo cáo kiểm thử (Skill: [test-reporting/SKILL.md](file:///home/traductoan/Seminar_Final/.agents/skills/testing/test-reporting/SKILL.md))
- [ ] Unit tests cho `validate_sql` (injection cases, edge cases)

> [!WARNING]
> Bạn đã có sẵn **5 Skills testing** trong `.agents/skills/testing/`. Nên tận dụng tối đa để tạo workflow test tự động hoàn chỉnh.

---

### 3. 🖥️ Frontend — SQL Editor & Playground (P1 theo ROADMAP)

| | |
|:---|:---|
| **ROADMAP** | Section 2.1 — SQL Editor & Playground |
| **Trạng thái** | `SqlPreview` hiện tại hỗ trợ edit + run thủ công + so sánh kết quả. **Thiếu**: Syntax highlighting chuyên dụng, format SQL, lịch sử manual vs AI. |
| **Cần làm** | |

- [ ] Nâng cấp `SqlPreview` → dùng thư viện code editor (Monaco/CodeMirror) với SQL syntax highlighting
- [ ] Nút Format SQL (beautify)
- [ ] Hiển thị warning "Read-only Database" rõ ràng
- [ ] Lưu lịch sử phân biệt `source=ai|manual` (Backend đã hỗ trợ, Frontend chưa hiển thị)
- [ ] UI hiển thị giới hạn (Timeout, Row Limit) cho user biết

---

## 🟡 Ưu tiên Trung bình (Nên plan trước khi phát triển)

### 4. 📊 Dashboard & Widget Nâng cao (P2 theo ROADMAP)

| | |
|:---|:---|
| **ROADMAP** | Section 2.2 — Dashboard & Widget Tương tác |
| **Trạng thái** | Backend CRUD đã có (create, list, get, update, refresh). Frontend `DashboardPanel` hỗ trợ reorder, remove, refresh. **Thiếu**: Drag & drop, filter động, widget editor, refresh định kỳ. |
| **Cần làm** | |

- [ ] Drag & drop widget (dùng thư viện như `dnd-kit` hoặc `react-beautiful-dnd`)
- [ ] Widget editor UI — chọn trường dữ liệu, đổi chart type từ modal
- [ ] Bộ lọc động (Filter) — lọc theo thời gian/dimension mà không viết lại SQL
- [ ] Auto-refresh định kỳ (interval configurable)
- [ ] Cache kết quả theo `query_fingerprint` ở Backend
- [ ] Export CSV/Excel từ widget

---

### 5. 🔗 Kết nối Dữ liệu Động (Connect Modal / Data Import)

| | |
|:---|:---|
| **PRD** | F1 — Quản lý Kết nối Data |
| **Trạng thái** | `DataImport.tsx` đã có (10KB) nhưng cần verify: Connection String input, CSV/JSON upload, schema extraction hoạt động end-to-end chưa? |
| **Cần làm** | |

- [ ] Verify luồng nhập Connection String → Backend đọc schema → AI học metadata
- [ ] Verify upload CSV/JSON → Backend parse → tạo bảng tạm/virtual
- [ ] Mã hóa Connection String/Password ở Backend (PRD yêu cầu)
- [ ] Schema Masking — Admin chọn bảng/cột nào được phép (F2)
- [ ] Thiết lập Timeout và Max Rows Limit từ UI (F3)

---

### 6. 📝 Lịch sử & Chia sẻ Truy vấn

| | |
|:---|:---|
| **PRD** | F7 — Lịch sử Truy vấn |
| **Trạng thái** | Backend lưu `query_history.json` (file-based), có endpoint `GET /history`. Frontend **chưa có UI** hiển thị lịch sử. |
| **Cần làm** | |

- [ ] Frontend: Trang/panel Lịch sử truy vấn — hiển thị câu hỏi cũ, SQL, kết quả
- [ ] Click để tái chạy truy vấn từ lịch sử
- [ ] Tính năng copy/share kết quả
- [ ] Migrate lịch sử từ file JSON → Supabase (production-ready)

---

### 7. 🔐 Quản lý Người dùng & Phân quyền (Auth & RBAC)

| | |
|:---|:---|
| **ROADMAP** | Section 4.1 — Supabase Hardening & Audit |
| **Trạng thái** | Mọi truy vấn hiện tại đều là ẩn danh. Chưa có sự phân biệt giữa Admin và User. |
| **Cần làm** | |

- [ ] Tích hợp Supabase Auth (Email/Password & Google OAuth)
- [ ] Thiết lập Row Level Security (RLS) để user chỉ thấy lịch sử truy vấn của chính mình
- [ ] Phân quyền Admin: Người duy nhất được phép cấu hình Connection String và Schema Masking
- [ ] Ghi Log (Audit Trail): Lưu vết ai đã chạy câu lệnh SQL nào vào lúc nào

---

### 8. 💰 Kiểm soát Chi phí & Caching (Cost Control)

| | |
|:---|:---|
| **ROADMAP** | Section 6 — Cost & Monitoring |
| **Trạng thái** | Chưa có cơ chế chặn spam câu hỏi. Gọi API LLM trực tiếp mọi lúc. |
| **Cần làm** | |

- [ ] **Semantic Caching:** Lưu kết quả câu hỏi vào Redis/Supabase. Nếu câu hỏi tương tự xuất hiện, trả về kết quả ngay mà không gọi LLM.
- [ ] **Rate Limiting:** Giới hạn mỗi user chỉ được hỏi tối đa N câu/ngày (VD: 50 câu).
- [ ] **Token Tracking:** Thống kê chi phí sử dụng AI theo từng người dùng hoặc phòng ban.
- [ ] Query Timeout: Tự động ngắt các truy vấn SQL chạy quá 30 giây để tránh treo DB.

---

### 9. 🧠 Tầng ngữ nghĩa (Business Semantic Layer)

| | |
|:---|:---|
| **ROADMAP** | Section 3.3 — Semantic Layer & Knowledge Graph |
| **Trạng thái** | AI chỉ làm việc với Schema kỹ thuật, chưa hiểu logic kinh doanh. |
| **Cần làm** | |

- [ ] Xây dựng giao diện "Từ điển thuật ngữ" (Glossary) cho Admin.
- [ ] Lưu trữ Business Logic (VD: Lợi nhuận = Doanh thu - Chi phí) vào Vector DB để AI tra cứu.
- [ ] Cấu hình "Câu hỏi mẫu" (Few-shot samples) để AI học cách viết SQL cho các yêu cầu khó.

---

## 🟢 Ưu tiên Thấp (Plan khi hoàn thành các phần trên)

### 10. 🧠 AI Nâng cao (P3 theo ROADMAP)

| | |
|:---|:---|
| **ROADMAP** | Section 3 — Advanced AI Capabilities |
| **Trạng thái** | Chưa triển khai |
| **Cần làm** | |

- [ ] **AI Insights** — Sau khi có data, gửi summary stats lại LLM để tạo nhận xét tự động (Section 3.1)
- [ ] **Multi-turn Conversation** — Lưu conversation context, cho phép hỏi tiếp nối (Section 3.2)
- [ ] **Semantic Layer** — Từ điển thuật ngữ doanh nghiệp + pgvector RAG (Section 3.3)

---

### 11. 🏗️ Hạ tầng & Observability

| | |
|:---|:---|
| **ROADMAP** | Section 4 — Infra & Security |
| **Trạng thái** | Docker Compose dev có, Kafka có. Observability (Grafana/Prometheus/Alloy) đã triển khai ở Docker Swarm riêng (theo conversation history). |
| **Cần làm** | |

- [ ] Tích hợp OpenTelemetry tracing vào 3 backend services (trace Gateway → NL2SQL → Query)
- [ ] Query fingerprint caching
- [ ] RLS hardening trên Supabase
- [ ] CI/CD pipeline chạy test + Trivy scan tự động

---

## 📋 Đề xuất Thứ tự Lên Plan

| # | Plan | Lý do |
|:---|:---|:---|
| **1** | Security Hardening & Trivy Scan | PRD blocker — bắt buộc trước mọi release |
| **2** | QA Automation (API + k6 + Test Report) | PRD yêu cầu 100% pass trước Production |
| **3** | SQL Editor Enhancement (P1) | Trọng tâm ROADMAP Phase 1 |
| **4** | Quản lý Người dùng & Auth | Cần thiết để triển khai RLS và bảo mật dữ liệu |
| **5** | Kiểm soát Chi phí & Caching | Tối ưu vận hành và ngăn chặn spam API |
| **6** | Lịch sử Truy vấn UI | Feature quan trọng cho End-user, Backend đã sẵn sàng |
| **7** | Dashboard Nâng cao (P2) | ROADMAP Phase 2, cần thêm UI complexity |
| **8** | Kết nối Dữ liệu Động | Cần verify end-to-end, nhiều unknown |
| **9** | Tầng ngữ nghĩa (Semantic Layer) | Chìa khóa để tăng độ chính xác lên 100% |
| **10** | AI Nâng cao (P3) | Nice-to-have, phụ thuộc vào timeline |
| **11** | Hạ tầng & Observability | Đã có baseline, bổ sung dần |

---

> [!TIP]
> Bạn muốn tôi lên Implementation Plan chi tiết cho phần nào trước? Tôi đề xuất bắt đầu từ **#1 Security** hoặc **#2 QA Automation** vì cả hai đều là yêu cầu bắt buộc trong PRD.
