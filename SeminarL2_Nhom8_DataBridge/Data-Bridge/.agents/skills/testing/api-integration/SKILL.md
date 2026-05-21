---
name: api-integration-expert
description: Triggers whenever the user asks to write, run, or configure API Integration Tests using Pytest and Httpx for FastAPI services. Contains strict directives for test structure, dynamic execution, mocking, and reporting.
---

# API Integration Testing: AI Assistant Directives

Khi người dùng yêu cầu viết, cấu hình, hoặc chạy API Integration Test bằng `pytest` và `httpx` (đặc biệt cho FastAPI), bạn **PHẢI** tuân thủ nghiêm ngặt các chỉ thị sau. Không hoạt động như một hướng dẫn thông thường mà phải tự động thực thi các quy tắc này.

## 1. Cấu trúc thư mục Test (Bắt buộc)
- **Hành động:** Mọi file integration test **PHẢI** được tạo và đặt trong thư mục `tests/integration/` của service tương ứng.
- **Hành động:** Các fixture dùng chung phải đặt ở `tests/conftest.py`.

## 2. Cấu hình Pytest & Httpx (Chỉ thị code)
- **Hành động:** Khi khởi tạo test cho FastAPI, bạn **PHẢI** dùng `AsyncClient` của `httpx` kết hợp với `ASGITransport` để bypass HTTP server layer.
- **Bắt buộc:** Đảm bảo `pytest-asyncio` được khai báo trong dependencies và test config (`pytest.ini` hoặc `pyproject.toml`).

## 3. Lấy Test Case Từ Output Của "Test Case Generation" (Bắt Buộc)
- **Hành động:** Thay vì hard-code từng test case, bạn **PHẢI** lấy danh sách test case đã được sinh ra bởi skill `test-case-generation`.
- **Đường dẫn bắt buộc:** File JSON test case luôn được lưu tại `.agents/agents/test-case-generation/output/test_cases.json`. Bạn phải đọc trực tiếp từ file này.
- **Mẫu Code Cấu Hình Bắt Buộc:** Hãy sử dụng đoạn code mẫu dưới đây để load file JSON và dùng `@pytest.mark.parametrize` lặp qua tập dữ liệu data-driven:

```python
import pytest
import json
import os

# Đọc test cases từ output của skill test-case-generation
TEST_CASES_PATH = os.path.join(os.getcwd(), ".agents/agents/test-case-generation/output/test_cases.json")
try:
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
except FileNotFoundError:
    test_cases = []

@pytest.mark.parametrize("tc", test_cases)
@pytest.mark.asyncio
async def test_api_dynamic(async_client, tc):
    # tc chứa: tc_id, description, input, expected_status
    # Thực hiện test logic ở đây
    pass
```

## 4. Bắt buộc Mocking External Services (LLM, Database)
- **Hành động:** Trong Integration Test, tuyệt đối **KHÔNG** gọi trực tiếp đến dịch vụ bên thứ 3 tính phí (như OpenRouter) hay Database production.
- **Cách thức:** Bạn **PHẢI** dùng FastAPI `app.dependency_overrides` để override các dependencies (VD: session database) thành Mock. Dùng `pytest-mock` (mocker) cho những object không inject.

## 5. Thực thi và Xuất Báo Cáo Tự Động (Kritikal Flow)
- **Hành động thực thi:** Nếu được yêu cầu chạy test test, dùng lệnh `pytest tests/integration/ -v > .agents/agents/api-integration/output/pytest_results.txt`.
- **Nhiệm vụ Agent (Bắt buộc):** Chạy xong, bạng **PHẢI** tự động đọc output sinh ra để tổng kết tỷ lệ Pass/Fail, phân tích log lỗi, và ghi ra **Markdown Report** tại `.agents/agents/api-integration/output/api_test_results.md`.
- File report này là đầu vào tối quan trọng cho kỹ năng `Test Report Writing`, nên không được phép bỏ qua bước này.
