---
name: API Integration Testing
description: Hướng dẫn viết Integration Test sử dụng Pytest và Httpx cho các dịch vụ (như FastAPI).
---

# API Integration Testing (Pytest + Httpx)

Skill này cung cấp các hướng dẫn và best practice để viết Integration Test cho các dịch vụ API trong hệ thống, sử dụng `pytest` kết hợp với `httpx` (async HTTP client).

## 1. Cấu trúc thư mục Test
Các bài test nên được đặt trong thư mục `tests/integration/` của mỗi service:
```text
tests/
  ├── conftest.py          # Chứa các fixture cấu hình chung (database, async client)
  └── integration/
      └── test_api.py      # Các test case gọi trực tiếp đến API
```

## 2. Cấu hình Pytest & Httpx (conftest.py)
Để test FastAPI, nên sử dụng `AsyncClient` của `httpx` để gọi trực tiếp ứng dụng mà không cần chạy server.
```python
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
```
*Lưu ý: Thêm `pytest-asyncio` vào file cấu hình (ví dụ `pytest.ini` hoặc `pyproject.toml`) để hỗ trợ test bất đồng bộ.*

## 3. Thực thi Test Case Từ Dữ Liệu Sinh Tự Động & Ghi Output
Thay vì viết test case thủ công từng cái một, **bạn phải lấy danh sách test case** đã được sinh ra bởi skill `Automated Test Case Generation` (được lưu tại `.agents/agents/test-case-generation/output/test_cases.json` hoặc file tương tự).

Ví dụ quy trình tự động đọc file JSON và chạy data-driven test:
```python
import pytest
import json

# Đọc test cases từ output của skill test-case-generation
TEST_CASES_PATH = ".agents/agents/test-case-generation/output/test_cases.json"
try:
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
except FileNotFoundError:
    test_cases = []

@pytest.mark.parametrize("tc", test_cases)
@pytest.mark.asyncio
async def test_api_dynamic(async_client, tc):
    # tc chứa: tc_id, description, input, expected_status
    response = await async_client.post("/api/v1/endpoint", json=tc["input"])
    assert response.status_code == tc["expected_status"]
```

## 4. Mocking các dịch vụ bên ngoài
Trong Integration Test, nếu API gọi tới các external service (ví dụ LLM, OpenRouter, Database khác), hãy sử dụng `pytest-mock` hoặc Dependency Injection (`app.dependency_overrides` trong FastAPI) để mock chúng.

```python
from main import app, get_db_session

async def override_get_db_session():
    # Return a mock or test database session
    pass

app.dependency_overrides[get_db_session] = override_get_db_session
```

## 5. Chạy Test & Lưu Kết Quả (Output)
Chạy toàn bộ test integration bằng lệnh:
```bash
pytest tests/integration/ -v > .agents/agents/api-integration/output/pytest_results.txt
```

**QUAN TRỌNG:** Sau khi quá trình kiểm thử chạy xong, bạn (AI Agent) **phải thu thập kết quả** (Pass/Fail của từng test case, lỗi trả về nếu có) và ghi lại thành báo cáo dưới dạng Markdown tại `.agents/agents/api-integration/output/api_test_results.md`. 
Skill **Test Report Writing** sẽ lấy dữ liệu từ file output này để tổng hợp báo cáo cuối cùng.
