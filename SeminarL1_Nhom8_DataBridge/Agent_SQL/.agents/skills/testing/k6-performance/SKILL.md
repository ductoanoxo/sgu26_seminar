---
name: k6 Performance Testing
description: Hướng dẫn chạy Load Test và đo lường hiệu năng bằng công cụ k6.
---

# K6 Performance Testing

Skill này dùng để chuẩn bị, thiết kế kịch bản và chạy Load Test bằng **k6** nhằm đánh giá hiệu năng (tốc độ, độ ổn định, khả năng chịu tải) của các API.

## 1. Cài đặt k6
Nếu k6 chưa được cài đặt, bạn có thể chạy bằng Docker để tiện lợi:
```bash
docker pull grafana/k6
```
Hoặc cài đặt k6 trực tiếp trên máy host theo [tài liệu chính thức của k6](https://k6.io/docs/get-started/installation/).

## 2. Các Chiến Lược Kiểm Thử (Testing Strategies)
Trong k6, bạn có thể thiết lập cấu hình `options` để chạy các loại test khác nhau tùy vào mục đích:

- **Smoke Testing (Kiểm thử sơ bộ):** Được thực hiện với tải rất thấp để xác minh kịch bản test (script) hoạt động đúng và hệ thống phản hồi cơ bản trước khi chạy các bài test lớn.
- **Load Testing (Kiểm thử tải):** Đánh giá hiệu năng hệ thống dưới mức tải dự kiến thông thường hoặc cao điểm trong thời gian ngắn, nhằm kiểm tra thời gian phản hồi (response time).
- **Stress Testing (Kiểm thử căng thẳng):** Kiểm tra giới hạn chịu tải tối đa của hệ thống bằng cách tăng dần số lượng người dùng ảo (VUs) cho đến khi hệ thống suy giảm hiệu năng hoặc sập.

## 3. Viết Script K6
Các kịch bản test (script) thường được viết bằng JavaScript. Tạo thư mục `tests/performance/` và lưu các script `.js` tại đây.

Ví dụ file `load_test.js`:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Tăng dần lên 20 user trong 30 giây
    { duration: '1m', target: 20 },  // Duy trì 20 user trong 1 phút
    { duration: '30s', target: 0 },  // Giảm dần về 0 user trong 30 giây
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% request phải phản hồi dưới 500ms
    http_req_failed: ['rate<0.01'],   // Tỉ lệ lỗi phải dưới 1%
  },
};

export default function () {
  const url = 'http://localhost:8000/api/v1/health'; // URL của API cần test
  
  const res = http.get(url);
  
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  
  sleep(1); // Nghỉ 1 giây giữa các request
}
```

## 4. Chạy K6 Script & Lưu Output
**QUAN TRỌNG:** Tương tự như các quy trình test khác, K6 **phải lưu kết quả vào thư mục chuẩn** để các skill khác (như Test Reporting) có thể đọc dữ liệu. Sử dụng cờ `--summary-export` để k6 xuất toàn bộ kết quả ra file JSON.

Chạy trực tiếp bằng command `k6`:
```bash
mkdir -p .agents/agents/k6-performance/output/
k6 run tests/performance/load_test.js --summary-export .agents/agents/k6-performance/output/k6_summary.json
```

Chạy bằng Docker (cần mount volume để lưu được file ra máy host):
```bash
docker run --rm -v $(pwd):/app -w /app grafana/k6 run tests/performance/load_test.js --summary-export .agents/agents/k6-performance/output/k6_summary.json
```

## 5. Phân tích kết quả
K6 sẽ xuất ra file JSON (như đã cấu hình ở trên). AI Agent (bạn) có nhiệm vụ đọc file `.agents/agents/k6-performance/output/k6_summary.json` và trích xuất các số liệu quan trọng sau để chuyển cho skill **Test Report Writing**:
- **http_req_duration**: Thời gian phản hồi (avg, min, med, max, p(90), p(95)).
- **http_req_failed**: Tỉ lệ phần trăm request bị lỗi.
- **vus** và **vus_max**: Số lượng Virtual Users (người dùng ảo) tham gia vào phiên test.
- **http_reqs**: Tổng thông lượng và số lượng requests.

## 6. Best Practices
- **Tách biệt môi trường**: Chỉ chạy k6 vào môi trường staging hoặc môi trường test riêng biệt, tuyệt đối KHÔNG chạy trên production nếu chưa có kế hoạch và thông báo cụ thể.
- **Rate limit**: Nếu server có chặn theo rate limit, script của bạn có thể bị block rất nhanh. Cần cấu hình disable rate limit ở môi trường test (hoặc mock) nếu mục tiêu là đo lường tải tối đa của hệ thống.
