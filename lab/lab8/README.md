# Chương 8 - Prompting Patterns Cho Sinh Mã Python

Thư mục `ch8` gồm các ví dụ về cách thiết kế prompt để tạo, sửa và nâng cấp code Python bằng GenAI.

## Nội dung chính

Các file trong `code_samples/` minh họa 5 nhóm kỹ thuật:

- `template_based.txt`: Prompt theo mẫu có cấu trúc để sửa code khi có traceback.
- `few_shot_chatgpt.txt`: Few-shot prompt để biến đổi câu lệnh `print(...)` thành log message có cấu trúc.
- `style_guide.py`: Ví dụ code đích đến theo style guide (type hint, biến rõ nghĩa, return rõ ràng).
- `math_calculations.py`: Các hàm toán học có docstring, làm chuẩn đầu ra cho model.
- `openai_fibonacci.py`: Tạo prompt few-shot và gọi OpenAI API để sinh hàm mới.
- `distances.py`: Ví dụ hàm distance (có chú ý lỗi chính tả trong tên hàm để phục vụ bài tập review).
- `chain_of_thought.py`: Miêu tả luồng validate code được model sinh ra (syntax, compile, reproducibility).
- `iterative_prompt.py`: Vòng lặp refine code dựa trên traceback đến khi compile thành công.

## Hướng dẫn nhanh

Di chuyển vào thư mục chapter:

```bash
cd Supercharged-Coding-with-Gen-AI/ch8
```

Chạy các file Python không cần API key:

```bash
python code_samples/math_calculations.py
python code_samples/style_guide.py
python code_samples/distances.py
```

Lưu ý: `chain_of_thought.py` và `iterative_prompt.py` là mẫu workflow/pseudocode minh họa, không phải script sẵn sàng production.

## Chạy ví dụ OpenAI API

File `code_samples/openai_fibonacci.py` cần:

- Cài thư viện `openai`
- Đặt biến môi trường `OPENAI_API_KEY`

Ví dụ (PowerShell):

```powershell
pip install openai
$env:OPENAI_API_KEY="your_api_key_here"
python code_samples/openai_fibonacci.py
```

## Mục tiêu học tập

- Hiểu cách viết prompt có cấu trúc thay vì prompt tự do.
- Biết kết hợp few-shot + template để tăng độ ổn định đầu ra.
- Áp dụng vòng lặp sửa lỗi tự động dựa trên traceback.
- Chuẩn hóa style output để dễ review và dễ test.

## Gợi ý mở rộng

- Thêm test cho các hàm trong `math_calculations.py` và `distances.py`.
- Chuyển các mẫu prompt (`*.txt`) thành hàm Python để tái sử dụng.
- Thêm logger thay cho `print` trong các script demo.
