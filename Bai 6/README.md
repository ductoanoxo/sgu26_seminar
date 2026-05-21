
# 🚀 Week 6 — Production GenAI: Bridging the Gap from Prototype to Production

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=yellow)](https://www.python.org/)
[![GenAI](https://img.shields.io/badge/GenAI-OpenAI%20%7C%20Copilot-orange)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Dự án **Week6-ProductionGenAI** tập trung vào việc hiện thực hóa tiềm năng của **Generative AI** trong toàn bộ vòng đời phát triển phần mềm (SDLC). Không còn chỉ dừng lại ở việc sinh mã (code generation), chúng ta sẽ khám phá cách AI tối ưu hóa **tài liệu**, **kiểm thử**, **hiệu năng** và đặc biệt là khả năng **vận hành (Production Readiness)** của hệ thống.

---

## 🎓 Thông tin Seminar

| Hạng mục | Chi tiết |
| :--- | :--- |
| **Trường** | Đại học Sài Gòn (SGU) |
| **Môn học** | Seminar chuyên đề công nghệ phần mềm |
| **Giảng viên** | TS. Đỗ Như Tài |
| **Sinh viên** | Trương Phú Kiệt |
| **MSSV** | `3122411109` |

---

## 📂 Cấu trúc dự án (Project Architecture)

Dự án được tổ chức theo cấu trúc module hóa, phân tách rõ ràng giữa tài liệu nghiên cứu và mã nguồn thực thi:

```text
Week6-ProductionGenAI/
├── 📄 .env                    # Lưu trữ OpenAI API Key (Local only)
├── 📄 .gitignore              # Loại bỏ các file rác và bí mật (.env, __pycache__)
├── 📂 docs/                   # Tài liệu báo cáo chi tiết từng chương
│   ├── [chapter12.docx](docs/chapter12.docx)         # Documentation & Docstrings
│   ├── [Chapter13.docx](docs/Chapter13.docx)         # Unit Testing & TDD
│   ├── [Chapter14.docx](docs/Chapter14.docx)         # Performance (Memory & Runtime)
│   ├── [chapter15.docx](docs/chapter15.docx)         # Production Readiness (Decorators)
│   └── [chapter16.docx](docs/chapter16.docx)         # Future of Software Engineering
└── 📂 Lab_3122411109_TruongPhuKiet/  # Mã nguồn thực hành chi tiết
    ├── 📁 ch12/               # Tự động hóa Documentation
    ├── 📁 ch13/               # GenAI in Unit Testing
    ├── 📁 ch14/               # Performance Optimization
    └── 📁 ch15/               # Production-Ready Code & Fine-Tuning
```

---

## 🧩 Nội dung chi tiết các chương (Case Studies)

### 📘 Chương 12: Documentation Excellence ([Báo cáo](docs/chapter12.docx))
*   **Mục tiêu:** Sử dụng AI để viết tài liệu chuẩn Google Style, duy trì sự đồng bộ giữa Code và Docs.
*   **Scripts tiêu biểu:**
    *   `distances.py`: Tính toán khoảng cách tọa độ.
    *   `base_flask_distances_with_docstring.py`: Ví dụ API Flask được tài liệu hóa bài bản.
    *   `openai_docstring_review.py`: Script tự động review chất lượng tài liệu bằng AI.

### 📗 Chương 13: Advanced Unit Testing ([Báo cáo](docs/Chapter13.docx))
*   **Mục tiêu:** Chuyển dịch từ viết test thủ công sang Data-driven Testing và phát hiện Edge Cases với AI.
*   **Scripts tiêu biểu:**
    *   `test_data_driven_ngrams.py`: Kiểm thử n-grams với bộ dữ liệu đa dạng.
    *   `test_ngrams_chatgpt.py`: Các bộ test case sinh ra từ prompt engineering.

### 📙 Chương 14: Performance Engineering ([Báo cáo](docs/Chapter14.docx))
*   **Mục tiêu:** Profiling chuyên sâu để phát hiện "bottlenecks" về thời gian chạy và bộ nhớ.
*   **Scripts tiêu biểu:**
    *   `profile_runtime.py`: Đo lường latency của thuật toán Fibonacci.
    *   `profile_space.py`: Phân tích lượng RAM tiêu thụ khi xử lý dữ liệu lớn.
    *   `top_video.py`: Ứng dụng AI tối ưu hóa logic lọc dữ liệu.

### 📕 Chương 15: Production Readiness ([Báo cáo](docs/chapter15.docx))
*   **Mục tiêu:** Áp dụng **Decorators** để tách biệt logic nghiệp vụ và logic vận hành (Logging, Monitoring).
*   **Kỹ thuật trọng tâm:**
    *   **Inverse CoT (Chain of Thought):** Định nghĩa tên decorator rồi để AI hoàn thiện logic.
    *   **Fine-tuning:** Đồng nhất phong cách viết code theo chuẩn doanh nghiệp.
*   **Scripts tiêu biểu:**
    *   `decorators_openai.py`: Tích hợp AI vào runtime để giám sát lỗi.
    *   `fine_tuning_extended.jsonl`: Dữ liệu huấn luyện mô hình AI riêng.

### 🔘 Chương 16: Future of Software Engineering ([Báo cáo](docs/chapter16.docx))
*   **Mục tiêu:** Tầm nhìn về "Vibe Coding", Democratization và vai trò mới của kỹ sư phần mềm.
*   **Nội dung:** Phân tích tác động kinh tế và sự dịch chuyển từ "người viết code" sang "người điều phối hệ thống".


---

## 🛠️ Hướng dẫn cài đặt (Installation)

### 1. Khởi tạo môi trường
Bạn nên sử dụng môi trường ảo để tránh xung đột thư viện:

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt trên Windows
.\.venv\Scripts\Activate.ps1

# Kích hoạt trên Linux/macOS
source .venv/bin/activate
```

### 2. Cài đặt Dependencies
Cài đặt các thư viện lõi cho việc thực thi và profiling:

```bash
pip install numpy flask openai pytest memory-profiler python-dotenv
```

---

## 🔐 Cấu hình OpenAI API
Dự án sử dụng OpenAI để tự động hóa các tác vụ thông minh.

1.  Sao chép file mẫu: `cp .env.example .env` (nếu có) hoặc tạo mới file `.env`.
2.  Thêm Key của bạn:
    ```env
    OPENAI_API_KEY=sk-your-secret-api-key-here
    ```

---

## ▶️ Chạy chương trình & Kiểm thử

### Kiểm tra hiệu năng (Profiling)
```bash
# Chạy bộ đo hiệu năng bộ nhớ
python Lab_3122411109_TruongPhuKiet/ch14/profile_space.py
```

### Chạy hệ thống kiểm thử tự động
```bash
# Tự động phát hiện và chạy tất cả unit tests
pytest Lab_3122411109_TruongPhuKiet/ch13/
```

---

## 🎯 Tổng kết giá trị mang lại

| Giai đoạn | Vai trò của GenAI | Công cụ áp dụng |
| :--- | :--- | :--- |
| **Doc** | Tự động sinh, kiểm tra ngữ nghĩa | Prompt Engineering |
| **Test** | Sinh Edge cases, Data-driven | Copilot / GPT-4 |
| **Perf** | Dự đoán độ phức tạp, gợi ý tối ưu | Profiling Tools + AI |
| **Prod** | Tách trách nhiệm (Separation of Concerns) | Python Decorators |

> **🌟 Lời nhắn:** GenAI không thay thế kỹ sư, nó trang bị cho họ "siêu năng lực" để xử lý các công việc lặp lại, từ đó tập trung vào tư duy kiến trúc và giải quyết các bài toán kinh doanh thực tế.

---

## 📚 Tài liệu tham khảo
1.  [Supercharged Coding with GenAI (2025)](https://www.packtpub.com/)
2.  [OpenAI API Documentation](https://platform.openai.com/docs)
3.  [Python Decorators - Real Python](https://realpython.com/primer-on-python-decorators/)

---
*© 2026 Trương Phú Kiệt - SGU Seminar*
