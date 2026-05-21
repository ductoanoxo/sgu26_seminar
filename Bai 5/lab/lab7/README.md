# API Tính Manhattan Distance

Một microservice tính khoảng cách Manhattan giữa hai DataFrame được truyền vào dưới dạng JSON.

Lưu ý tương thích: dự án hỗ trợ Python 3.10+ và tự chọn phiên bản `pandas` phù hợp theo phiên bản Python.


## Chạy ứng dụng
Trong terminal, di chuyển vào thư mục `ch7` và chạy lệnh sau:

```bash
pip install -r requirements.txt
```

Sau đó chạy ứng dụng:

```bash
python app.py
```

Lệnh này sẽ khởi động Flask server tại http://localhost:5000

### Ví dụ request
Bạn có thể kiểm tra API bằng `curl` hoặc bất kỳ HTTP client nào. Ví dụ với `curl`:

```bash
curl -X POST http://127.0.0.1:5000/manhattan \
  -H "Content-Type: application/json" \
  -d '{"df1": [[1, 2], [3, 4]], "df2": [[2, 0], [1, 3]]}'
```

### Ví dụ response

>{
  "distance": 6.0
}

## Xử lý lỗi

API hiện đã có kiểm tra dữ liệu đầu vào và trả lỗi rõ ràng ở mã `400` cho các trường hợp phổ biến:

- Thiếu body JSON hoặc JSON không hợp lệ
- Thiếu khóa `df1` hoặc `df2`
- `df1`/`df2` không phải mảng JSON
- Hai DataFrame khác kích thước
- Dữ liệu không phải kiểu số

Ví dụ phản hồi lỗi:

```json
{
  "error": "JSON body must contain 'df1' and 'df2'."
}
```

## Logging

Ứng dụng đã bật logging ở mức `INFO` và ghi lại:

- Kích thước dữ liệu đầu vào (`df1.shape`, `df2.shape`)
- Kết quả khoảng cách Manhattan sau khi tính xong
- Cảnh báo khi validation thất bại
- Stack trace cho lỗi không mong đợi

Bạn có thể xem log trực tiếp trên terminal khi chạy `python app.py`.

## Chạy test

Chạy toàn bộ test bằng `unittest`:

```bash
py -3 -m unittest discover -s tests -p "test_*.py" -v
```

Bao gồm:

- Test hàm `get_manhattan_distance`
- Test API `/manhattan` (tự động skip nếu môi trường chưa cài `flask`)

## Chạy với Docker

Để chạy ứng dụng trong Docker container, thực hiện các bước sau.

Build Docker image:

```bash
docker build -t manhattan-distance-api .
```

Chạy Docker container:

```bash
docker run -p 5000:5000 manhattan-distance-api
```

Sau đó bạn có thể truy cập API tại http://127.0.0.1:5000

# Công việc cần bổ sung
- [x] Thêm test cases
- [x] Thêm logging
- [x] Thêm xử lý lỗi
- [x] Thêm tài liệu hướng dẫn