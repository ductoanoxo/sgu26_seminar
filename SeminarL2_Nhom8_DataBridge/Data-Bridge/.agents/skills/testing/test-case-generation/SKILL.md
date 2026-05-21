---
name: Automated Test Case Generation
description: Hướng dẫn tự động sinh kịch bản kiểm thử (Test Case) và Test Script cho API/Unit bằng AI (LLM) hoặc công cụ chuyên dụng.
---

# Tự động sinh Test Case cho API

Skill này hướng dẫn quy trình tự động sinh ra các kịch bản kiểm thử (Test Cases) API có độ bao phủ cao (Happy paths, Edge cases, Negative cases) bằng AI Agent/LLM. Workflow này gắn liền trực tiếp với quy trình **API Integration Testing**, giúp chuyển đổi mạch lạc từ Đặc tả API (Swagger/Mã nguồn) -> Bảng Test Case -> Code Test Tự động (Pytest + Httpx).

## 1. Phương pháp sinh API Test Case bằng AI (LLM)

Để AI sinh ra Test Case API chính xác và bám sát dự án, yếu tố quan trọng nhất là cung cấp **Ngữ cảnh (Context)** đầy đủ.

### Bước 1: Chuẩn bị Ngữ cảnh đầu vào
Tập hợp một hoặc nhiều tài liệu sau làm đầu vào:
- **Tài liệu API (OpenAPI / Swagger)**: Cung cấp endpoint, request body schema, params, và response schema.
- **Mã nguồn (Source Code)**: File Router/Controller, Model (Pydantic/Mongoose), hoặc service logic.
- **User Stories / Yêu cầu nghiệp vụ**: Đoạn mô tả các quy tắc nghiệp vụ (Ví dụ: "Password phải có chữ và số, tối thiểu 8 ký tự").

### Bước 2: Thiết kế Prompt (Prompting)
Đóng vai AI như một chuyên gia kiểm thử. Sử dụng cấu trúc lệnh rõ ràng:
> *"Với tư cách là một QA Engineer, hãy phân tích đoạn mã nguồn/API Spec dưới đây và sinh ra danh sách Test Case đầy đủ cho API `POST /api/v1/users`. 
> Yêu cầu:
> 1. Bao phủ các luồng: Happy Path, Boundary/Edge Cases (dữ liệu rỗng, sai format), và Negative Cases (Lỗi xác thực, sai logic).
> 2. Trình bày dưới dạng Bảng Markdown gồm các cột: TC ID, Mô tả (Description), Dữ liệu đầu vào (Input), Kết quả mong đợi (Expected Result)."*

### Bước 3: Định dạng và Lưu Đầu Ra (Output)
Bạn có thể yêu cầu sinh dưới dạng Bảng (chuẩn QA) hoặc JSON để thuận tiện cho việc chạy test tự động.
**ĐẶC BIỆT QUAN TRỌNG:** Phải lưu các Test Cases đã được sinh ra vào thư mục chuẩn của skill, ví dụ: `.agents/agents/test-case-generation/output/test_cases.json` hoặc `.agents/agents/test-case-generation/output/test_cases.md`.

**Mẫu Bảng Test Case truyền thống (nếu lưu dạng Markdown):**
| TC ID | Description | Input | Expected Result |
|-------|-------------|-------|-----------------|
| TC_01 | Đăng nhập thành công với tài khoản đúng | username="admin", pass="123456" | HTTP 200, trả về token |
| TC_02 | Bỏ trống mật khẩu | username="admin", pass="" | HTTP 422, message: "Field required" |

**Mẫu JSON (Đề xuất để truyền sang API Integration):**
```json
[
  {
    "tc_id": "TC_01",
    "description": "Đăng nhập thành công",
    "input": {"username": "admin", "pass": "123456"},
    "expected_status": 200
  }
]
```

**Mẫu BDD (Behavior-Driven Development) cho Automation:**
```gherkin
Feature: Quản lý người dùng
  Scenario: Tạo user với email không hợp lệ
    Given tôi có quyền Admin
    When tôi gọi API tạo user với email "abc@.com"
    Then hệ thống phải trả về lỗi HTTP 422 Unprocessable Entity
```

## 2. Gắn kết với API Integration Test (Sinh Code Tự Động)

Khi đã có bảng Test Case API, bước tiếp theo là lập trình mã kiểm thử tự động (Test Scripts) dựa trên bộ kỹ năng **API Integration Testing** (sử dụng `pytest` và `httpx`). Bạn hoàn toàn có thể tiếp tục yêu cầu AI sinh code test từ file Test Case vừa tạo.

**Quy trình:**
1. Cung cấp file Markdown chứa Test Cases (ví dụ `test_cases.md`).
2. Yêu cầu AI viết script chạy API test: 
   > *"Dựa trên file `test_cases.md` và tuân thủ các chuẩn trong tài liệu `api-integration/SKILL.md`, hãy viết file test integration bằng Python. Sử dụng `pytest.mark.asyncio`, thư viện `httpx` và fixture `async_client` từ `conftest.py`. Đảm bảo assert đúng status code và mock các phụ thuộc bên ngoài nếu cần thiết."*
3. Cập nhật file `.py` và tiến hành chạy test (`pytest tests/integration/ -v`).

## 3. Property-Based Testing (Tự động sinh dữ liệu test)

Ngoài việc dùng AI, nếu dự án dùng Python, bạn có thể áp dụng **Property-Based Testing** với thư viện `Hypothesis`. Phương pháp này tự động sinh ra hàng ngàn giá trị đầu vào ngẫu nhiên để tìm các lỗi tiềm ẩn (Edge Cases).

```python
from hypothesis import given, strategies as st
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Tự động sinh hàng trăm chuỗi text ngẫu nhiên cho tham số q
@given(q=st.text(max_size=50))
def test_search_endpoint_fuzzy(q):
    # Mục tiêu là kiểm tra xem API có bị crash (HTTP 500) khi gặp ký tự lạ không
    response = client.get(f"/api/v1/search?q={q}")
    
    # API có thể trả về lỗi 422 (validation) hoặc 200 (ok), nhưng không được lỗi 500
    assert response.status_code in [200, 404, 422]
```

## 4. Best Practices (Thực hành tốt)
- **Review kỹ dữ liệu ảo do AI sinh ra**: AI có thể bị "hallucinate" ra các trường dữ liệu (fields) không có trong schema thực tế. Luôn đối chiếu lại với file Model.
- **Chia nhỏ (Chunking)**: Không yêu cầu sinh test case cho toàn bộ ứng dụng cùng lúc. Hãy làm từng module hoặc từng API cụ thể để đảm bảo chất lượng sâu nhất.
- **Tận dụng Data Boundary**: Nhắc nhở AI tập trung vào các giá trị biên (số âm, 0, chuỗi siêu dài, ký tự đặc biệt, SQL Injection payload cơ bản).
