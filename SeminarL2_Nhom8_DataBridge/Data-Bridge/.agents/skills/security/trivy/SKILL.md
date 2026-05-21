---
name: Trivy Security Scanning
description: Hướng dẫn dành cho AI Agent để sử dụng Trivy quét lỗ hổng bảo mật, cấu hình sai, lộ secret và kiểm tra bản quyền.
---

# Trivy Security Scanning Skill

Skill này định nghĩa cách **bạn (AI Agent)** thao tác với Trivy khi người dùng yêu cầu kiểm tra bảo mật dự án, phân tích lỗ hổng, hoặc tìm kiếm cấu hình sai. Thay vì hướng dẫn người dùng tự làm, bạn hãy tự động thực thi các tác vụ này.

## Nguyên tắc chung của bạn (AI Agent)
1. **Thực thi lệnh:** Luôn sử dụng tool `run_in_terminal` để chạy các câu lệnh `trivy` thay người dùng.
2. **Xử lý output dài:** Kết quả scan có thể rất dài. Khuyến khích xuất ra file JSON (`-f json -o report.json`) rồi tự đọc phân tích, hoặc dùng `--severity HIGH,CRITICAL` để giới hạn lỗi nghiêm trọng.
3. **Phân tích kết quả:** Cung cấp giải pháp cụ thể cho lỗ hổng/cấu hình sai bạn tìm được thay vì chỉ in lại terminal output.

## 1. Khi được yêu cầu quét lỗ hổng (Vulnerabilities)

Sử dụng kịch bản này khi phân tích độ an toàn của thư viện phụ thuộc (node_modules, requirements.txt...) hoặc Docker image.

```bash
# Quét toàn bộ mã nguồn hiện hành (Filesystem)
trivy fs .

# Quét một Docker Image cụ thể và chỉ hiển thị thiết lập nguy cơ cao
trivy image --severity HIGH,CRITICAL <tên-image>
```

## 2. Khi được yêu cầu quét bí mật (Secrets Leak)

Sử dụng khi cần kiểm tra xem mã nguồn có vô tình chứa Mật khẩu, API Keys, Tokens. Tự động cảnh báo người dùng điều chỉnh lại mã nguồn để tránh bị lộ thông tin nhạy cảm.

```bash
trivy fs --scanners secret .
```

## 3. Khi được yêu cầu kiểm tra cấu hình sai (Misconfigurations)

Dùng cho file Infrastructure as Code (IaC) như Dockerfile, file YAML, Terraform, CloudFormation để kiểm tra lỗi chạy bằng root, thiếu limit tài nguyên, ...

```bash
# Quét cấu hình sai trên tất cả các file IaC
trivy config .

# Quét trên một file duy nhất
trivy config Dockerfile
```

## 4. Khi rà soát giấy phép (License)

Dùng khi muốn kiểm tra xem có vi phạm giấy phép phần mềm mã nguồn mở nào bị cấm (như một số nhánh của GPL) hay không.

```bash
trivy fs --scanners license .
```

## 5. Khi người dùng cần tích hợp vào báo cáo hoặc CI

Nếu cần xuất dữ liệu để hỗ trợ người dùng phân tích chuyên sâu định dạng rõ ràng:
```bash
# Xuất dưới dạng JSON
trivy fs -f json -o trivy-report.json .

# Xuất dạng bảng cơ bản
trivy fs --format table .
```
*(Tip: Là AI, hãy đọc trực tiếp `trivy-report.json` bằng JSON parser hoặc \`jq\` để tóm tắt cho người dùng hiểu dễ hơn)*
