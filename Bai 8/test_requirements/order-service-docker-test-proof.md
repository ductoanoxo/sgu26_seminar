# Minh Chứng Kiểm Thử Docker Của Order Service

- Thời gian kiểm thử: `2026-05-02 00:32 +07:00`
- Stack sử dụng: `microservices_api_demo/microservices_api_demo/docker-compose.yml`
- Container được kiểm thử: `order-service`
- Endpoint được gọi trực tiếp: `http://127.0.0.1:8082/api/order`

## Các điều chỉnh cần thực hiện trước khi kiểm thử

1. Build lại `order-service` từ file JAR mới đóng gói để container Docker chạy đúng phần mã đã được cập nhật.
2. Bổ sung biến môi trường `APP_INVENTORY_SERVICE_BASE_URL=http://inventory-service:8083/v1/api/inventory` trong `docker-compose.yml` gốc để `order-service` gọi thẳng `inventory-service` trong mạng Docker, không phụ thuộc vào trạng thái đăng ký Eureka trong lúc kiểm thử.
3. Điều chỉnh schema đang chạy của `order_db` bằng cách bỏ ràng buộc `NOT NULL` trên cột cũ `order_line_items.order_number`, vì cột này là phần dư từ mapping cũ và đã chặn thao tác lưu dữ liệu của phiên bản code mới.

## Kiểm thử nhánh thành công

### Dữ liệu tồn kho dùng để kiểm thử

- Đã chèn một bản ghi test vào PostgreSQL của Docker:
  - `sku_code = docker_test_sku_20260502`
  - `quantity = 5`

### Request gửi tới hệ thống

```http
POST /api/order
Content-Type: application/json

{
  "orderLineItemsDtoList": [
    {
      "skuCode": "docker_test_sku_20260502",
      "price": 1200,
      "quantity": 2
    }
  ]
}
```

### Kết quả trả về

```text
HTTP 201
Order Placed
```

### Xác minh sau khi gọi API

Tồn kho sau request:

```json
{"skuCode":"docker_test_sku_20260502","quantity":3,"inStock":true}
```

Dữ liệu đơn hàng đã được lưu trong PostgreSQL của Docker:

```text
order_table
 id |             order_number
----+--------------------------------------
  2 | d004a345-6ea6-4fff-bb31-18f315a2983d

order_line_items
 id |         sku_code         | quantity | order_id | order_number
----+--------------------------+----------+----------+--------------
  2 | docker_test_sku_20260502 |        2 |        2 |
```

Log xác nhận từ container:

```text
Order placed successfully
```

## Kiểm thử nhánh thất bại

### Request gửi tới hệ thống

```http
POST /api/order
Content-Type: application/json

{
  "orderLineItemsDtoList": [
    {
      "skuCode": "missing_docker_sku",
      "price": 1200,
      "quantity": 1
    }
  ]
}
```

### Kết quả trả về

```text
HTTP 400
Failed to Place Order
```

Log xác nhận từ container:

```text
Order placement failed
```
