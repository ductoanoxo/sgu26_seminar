# Implementation Plan: AI Nâng cao (Advanced AI Capabilities)

## 1. Overview (Tổng quan)
Module AI Nâng cao tập trung vào việc gia tăng giá trị cho hệ thống thông qua các khả năng phân tích dữ liệu chuyên sâu (AI Insights), duy trì ngữ cảnh hội thoại (Multi-turn) và chuẩn hóa ngôn ngữ doanh nghiệp (Semantic Layer). Đây là các tính năng thuộc giai đoạn mở rộng (P3) nhằm tối ưu trải nghiệm người dùng cuối.

---

## 2. Các bước triển khai chi tiết

### Bước 1: AI Insights - Phân tích dữ liệu tự động
**Mục tiêu:** Tự động tạo ra các nhận xét, xu hướng từ kết quả truy vấn SQL.
- **Tác vụ 1:** Thiết kế prompt để tóm tắt kết quả bảng/biểu đồ.
- **Tác vụ 2:** Tích hợp logic gửi sample data (summary stats) lên LLM sau khi thực thi SQL thành công.

> **Prompt gửi AI Agent:**
> ```text
> "Hãy thiết kế một service xử lý AI Insights. Sau khi Query Service trả về kết quả, hãy lấy 5-10 dòng dữ liệu mẫu hoặc thống kê mô tả (min, max, avg) và gửi cho Gemini LLM với prompt: 'Dựa trên dữ liệu sau, hãy đưa ra 3 nhận xét quan trọng nhất'. Đầu ra: Một trường 'insights' trong response API của Gateway."
> ```

### Bước 2: Multi-turn Conversation - Hội thoại đa bước
**Mục tiêu:** Cho phép người dùng hỏi các câu hỏi tiếp nối dựa trên ngữ cảnh trước đó.
- **Tác vụ 1:** Triển khai Conversation History lưu trữ trong Redis hoặc Supabase.
- **Tác vụ 2:** Cập nhật NL2SQL service để nhận kèm `history` và rewrite query nếu cần (Coreference Resolution).

> **Prompt gửi AI Agent:**
> ```text
> "Thực hiện lưu trữ lịch sử hội thoại cho mỗi session_id. Khi người dùng hỏi câu tiếp theo (ví dụ: 'Còn của tháng trước thì sao?'), hãy gửi kèm 3-5 câu hỏi/trả lời gần nhất cho LLM để nó hiểu ngữ cảnh. Sử dụng LangChain MessageHistory hoặc tương đương."
> ```

### Bước 3: Semantic Layer - Tầng ngữ nghĩa doanh nghiệp
**Mục tiêu:** Định nghĩa thuật ngữ riêng của doanh nghiệp và sử dụng RAG để AI hiểu đúng schema.
- **Tác vụ 1:** Xây dựng Business Glossary (Từ điển thuật ngữ).
- **Tác vụ 2:** Sử dụng pgvector trên Supabase để tìm kiếm ngữ nghĩa các cột/bảng liên quan trước khi sinh SQL.

> **Prompt gửi AI Agent:**
> ```text
> "Tích hợp Semantic Layer vào pipeline NL2SQL. Trước khi sinh SQL, hãy sử dụng pgvector để tìm kiếm các thuật ngữ liên quan trong Business Glossary. Ví dụ: Nếu user hỏi 'doanh thu', hệ thống phải biết map vào cột 'total_amount' của bảng 'orders'. Đầu ra: Metadata bổ sung cho prompt sinh SQL."
> ```

---

# Progress Report: AI Nâng cao
**Ngày cập nhật:** 16/05/2026
**Trạng thái tổng thể:** Chưa triển khai

## 📈 Tiến trình tổng quan (Progress Overview)
- **Tổng số tác vụ:** 3
- **Đã hoàn thành:** 0
- **Tiến độ (Completion):** 0%

---

## 📊 Chỉ số đánh giá (Evaluation Criteria)
| Chỉ số | Mục tiêu | Kết quả hiện tại | Đạt yêu cầu? |
| :--- | :--- | :--- | :--- |
| **Insight Accuracy** | > 80% hữu ích | N/A | ⏳ |
| **Context Retention** | 100% ngữ cảnh | N/A | ⏳ |
| **Semantic Mapping** | > 90% chính xác | N/A | ⏳ |

---

## ✅ Các hạng mục đã hoàn thành (Done)
- (Chưa có hạng mục nào hoàn thành)

## 🚧 Đang triển khai (In Progress)
- [ ] **Lên kế hoạch chi tiết**: Đang chuẩn bị tài liệu kỹ thuật cho tầng Semantic.

## 🛑 Khó khăn & Khuyến nghị (Blockers & Recommendations)
- **Context Window**: Cần quản lý token của history để không làm chậm thời gian phản hồi của LLM.

## 📅 Kế hoạch tiếp theo (Next Steps)
1. Nghiên cứu giải pháp lưu trữ Vector DB trên Supabase (pgvector).
2. Viết prototype cho AI Insights với dữ liệu giả lập.
3. Thiết kế schema cho bảng `conversation_history`.
