# Skill: Tóm tắt workflow chức năng

## Mục tiêu
Tạo bản tóm tắt chuyên nghiệp cho một chức năng (feature/module), giải thích rõ cách hoạt động, các luồng chính/phụ, dữ liệu đi vào và kết quả trả ra. Bản tóm tắt được lưu dưới dạng file Markdown để dùng làm tài liệu nội bộ.

## Khi nào dùng
- Cần tài liệu nhanh về workflow của một chức năng để onboarding hoặc review.
- Muốn tổng hợp luồng xử lý từ code, tài liệu, hoặc mô tả nghiệp vụ.
- Cần chuẩn hóa thông tin để làm tài liệu tham khảo sau này.

## Đầu vào mong muốn
- Mô tả chức năng hoặc câu hỏi cụ thể.
- Danh sách file/code liên quan (nếu có).
- Phạm vi mong muốn: chỉ luồng chính hay cả luồng lỗi/edge cases.
- Yêu cầu định dạng hoặc độ chi tiết (ngắn gọn, vừa, chi tiết).

## Đầu ra
Một file Markdown, lưu tại thư mục tương ứng trong workspace hiện tại:
`<WORKSPACE>/.agents/skills/Summary/content`

## Quy trình thực hiện
1. Thu thập thông tin: đọc README, code, API docs, hoặc mô tả người dùng.
2. Xác định phạm vi: chức năng, entry points, dependencies.
3. Phân tích luồng chính, luồng phụ, và các tình huống lỗi.
4. Trích xuất các thành phần dữ liệu: input, output, schema, config.
5. Viết bản tóm tắt theo mẫu chung, rõ ràng, trùng lặp ít.
6. Nếu còn thiếu thông tin quan trọng, ghi rõ phần cần xác minh.

## Quy tắc nội dung
- Không đoán thông tin không có căn cứ.
- Nếu thiếu dữ liệu, ghi rõ: "Cần xác minh".
- Sử dụng ngôn ngữ chuyên nghiệp, ngắn gọn, dễ đọc.
- Ưu tiên liệt kê theo bước và bullet points.

## Mẫu tiêu đề file
- Dùng kebab-case, không dấu, ngắn gọn.
- Ví dụ: `workflow-ask-api-gateway.md`, `workflow-nl2sql-pipeline.md`.

## Template gợi ý
```md
# Tên chức năng

## Tổng quan
- Mục đích:
- Phạm vi:
- Entry points:

## Luồng chính
1. ...
2. ...

## Luồng phụ và lỗi thường gặp
- ...

## Dữ liệu vào/ra
- Input:
- Output:
- Schema/Model liên quan:

## Các thành phần liên quan
- Service/Module:
- API/Route:
- Config/Env:

## Ghi chú cần xác minh
- ...
```

## Ghi chú
Đây là thư mục lưu trữ nội dung tóm tắt do người dùng yêu cầu. Mỗi file chỉ nên bao gồm 1 chức năng cụ thể để dễ tra cứu và cập nhật.
