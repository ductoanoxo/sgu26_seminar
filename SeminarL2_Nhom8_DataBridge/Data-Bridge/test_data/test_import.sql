-- ============================================================
-- TEST IMPORT FILE - Agent SQL
-- Compatible: PostgreSQL / MySQL / SQLite
-- Tables: customers, products, orders, order_items
-- ============================================================

-- ============================================================
-- TABLE 1: customers
-- ============================================================
CREATE TABLE customers (
    id INTEGER,
    full_name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(20),
    city VARCHAR(100),
    country VARCHAR(50),
    age INTEGER,
    total_spent DOUBLE PRECISION,
    is_active INTEGER,
    registered_date VARCHAR(20)
);

INSERT INTO customers (id, full_name, email, phone, city, country, age, total_spent, is_active, registered_date) VALUES
(1, 'Nguyen Van An', 'an.nguyen@email.com', '0912345678', 'Ha Noi', 'Vietnam', 28, 1250.50, 1, '2023-01-15'),
(2, 'Tran Thi Bich', 'bich.tran@email.com', '0987654321', 'Ho Chi Minh', 'Vietnam', 34, 3780.00, 1, '2022-11-03'),
(3, 'Le Van Cuong', 'cuong.le@email.com', '0905111222', 'Da Nang', 'Vietnam', 25, 540.75, 1, '2023-06-20'),
(4, 'Pham Thi Dung', 'dung.pham@email.com', '0934222333', 'Can Tho', 'Vietnam', 42, 2100.00, 0, '2022-03-08'),
(5, 'Hoang Van Em', 'em.hoang@email.com', '0978333444', 'Hai Phong', 'Vietnam', 31, 890.25, 1, '2023-09-12'),
(6, 'Vu Thi Phuong', 'phuong.vu@email.com', '0961444555', 'Hue', 'Vietnam', 27, 4500.00, 1, '2021-07-30'),
(7, 'Bui Van Giang', 'giang.bui@email.com', '0949555666', 'Vung Tau', 'Vietnam', 38, 320.10, 1, '2024-01-05'),
(8, 'Do Thi Ha', 'ha.do@email.com', '0932666777', 'Nha Trang', 'Vietnam', 29, 1670.80, 0, '2023-04-18'),
(9, 'Dinh Van Ky', 'ky.dinh@email.com', '0915777888', 'Quy Nhon', 'Vietnam', 45, 760.00, 1, '2022-08-25'),
(10, 'Ly Thi Lan', 'lan.ly@email.com', '0903888999', 'Ha Noi', 'Vietnam', 33, 5230.50, 1, '2021-12-14'),
(11, 'Ngo Van Minh', 'minh.ngo@email.com', '0976999000', 'Ho Chi Minh', 'Vietnam', 26, 980.00, 1, '2023-02-28'),
(12, 'Cao Thi Ngoc', 'ngoc.cao@email.com', '0959000111', 'Da Nang', 'Vietnam', 37, 1420.60, 1, '2022-05-17'),
(13, 'Thai Van Oanh', 'oanh.thai@email.com', '0942111222', 'Bien Hoa', 'Vietnam', 30, 230.00, 0, '2024-03-09'),
(14, 'Truong Thi Phuoc', 'phuoc.truong@email.com', '0925222333', 'Thu Duc', 'Vietnam', 22, 3100.40, 1, '2023-11-22'),
(15, 'Dang Van Quy', 'quy.dang@email.com', '0908333444', 'Bien Hoa', 'Vietnam', 50, 6750.00, 1, '2020-06-01');

-- ============================================================
-- TABLE 2: products
-- ============================================================
CREATE TABLE products (
    product_id INTEGER,
    product_name VARCHAR(200),
    category VARCHAR(100),
    brand VARCHAR(100),
    price DOUBLE PRECISION,
    cost DOUBLE PRECISION,
    stock_quantity INTEGER,
    rating DOUBLE PRECISION,
    description VARCHAR(500)
);

INSERT INTO products (product_id, product_name, category, brand, price, cost, stock_quantity, rating, description) VALUES
(1, 'iPhone 15 Pro Max', 'Smartphone', 'Apple', 29990000, 22000000, 50, 4.8, 'Smartphone cao cap voi chip A17 Pro'),
(2, 'Samsung Galaxy S24 Ultra', 'Smartphone', 'Samsung', 27990000, 20000000, 35, 4.7, 'Smartphone Android hang dau 2024'),
(3, 'MacBook Air M3', 'Laptop', 'Apple', 32990000, 25000000, 20, 4.9, 'Laptop sieu mong nhe voi chip M3'),
(4, 'Dell XPS 15', 'Laptop', 'Dell', 35990000, 28000000, 15, 4.6, 'Laptop cao cap man hinh OLED'),
(5, 'Sony WH-1000XM5', 'Headphone', 'Sony', 8990000, 5000000, 80, 4.8, 'Tai nghe chong on hang dau'),
(6, 'iPad Pro 12.9 inch', 'Tablet', 'Apple', 28990000, 21000000, 25, 4.7, 'May tinh bang manh nhat cua Apple'),
(7, 'Logitech MX Master 3', 'Accessory', 'Logitech', 2990000, 1500000, 120, 4.6, 'Chuot khong day chuyen nghiep'),
(8, 'LG UltraWide 34 inch', 'Monitor', 'LG', 12990000, 9000000, 30, 4.5, 'Man hinh ultrawide cho dan van phong'),
(9, 'ASUS ROG Zephyrus G14', 'Laptop', 'ASUS', 38990000, 30000000, 10, 4.7, 'Laptop gaming hieu nang cao'),
(10, 'AirPods Pro 2', 'Earphone', 'Apple', 6990000, 4000000, 100, 4.6, 'Tai nghe true wireless ANC'),
(11, 'Xiaomi Redmi Note 13', 'Smartphone', 'Xiaomi', 5990000, 3500000, 200, 4.3, 'Smartphone gia tot tam trung'),
(12, 'Keychron K2 Pro', 'Keyboard', 'Keychron', 2490000, 1200000, 60, 4.5, 'Ban phim co khong day hot swap'),
(13, 'WD My Passport 2TB', 'Storage', 'Western Digital', 1990000, 1100000, 90, 4.4, 'O cung di dong 2TB USB-C'),
(14, 'Anker USB-C Hub 7-in-1', 'Accessory', 'Anker', 890000, 400000, 150, 4.3, 'Hub USB-C da nang 7 cong'),
(15, 'Canon EOS R50', 'Camera', 'Canon', 22990000, 17000000, 12, 4.6, 'May anh mirrorless cho nguoi moi bat dau'),
(16, 'GoPro Hero 12', 'Camera', 'GoPro', 10990000, 7500000, 25, 4.5, 'Camera hanh trinh chong nuoc 4K'),
(17, 'Razer DeathAdder V3', 'Accessory', 'Razer', 1990000, 900000, 75, 4.4, 'Chuot gaming ergonomic cho game thu'),
(18, 'Samsung T7 SSD 1TB', 'Storage', 'Samsung', 2290000, 1300000, 110, 4.7, 'O cung SSD di dong toc do cao'),
(19, 'Jabra Evolve2 85', 'Headphone', 'Jabra', 11990000, 8000000, 20, 4.5, 'Tai nghe khong day cho chuyen gia'),
(20, 'Belkin MagSafe Charger', 'Accessory', 'Belkin', 1290000, 600000, 200, 4.2, 'Sac khong day MagSafe 15W');

-- ============================================================
-- TABLE 3: orders
-- ============================================================
CREATE TABLE orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date VARCHAR(20),
    status VARCHAR(30),
    payment_method VARCHAR(50),
    total_amount DOUBLE PRECISION,
    discount_amount DOUBLE PRECISION,
    shipping_fee DOUBLE PRECISION,
    notes VARCHAR(300)
);

INSERT INTO orders (order_id, customer_id, order_date, status, payment_method, total_amount, discount_amount, shipping_fee, notes) VALUES
(1001, 1, '2024-01-10', 'delivered', 'credit_card', 29990000, 0, 30000, NULL),
(1002, 2, '2024-01-15', 'delivered', 'bank_transfer', 36980000, 1000000, 0, 'Giao hang truoc 5h chieu'),
(1003, 3, '2024-01-20', 'shipped', 'cod', 8990000, 500000, 30000, NULL),
(1004, 5, '2024-02-01', 'delivered', 'momo', 2990000, 0, 30000, NULL),
(1005, 6, '2024-02-05', 'delivered', 'credit_card', 45980000, 2000000, 0, 'Khach VIP - uu tien giao'),
(1006, 7, '2024-02-10', 'processing', 'bank_transfer', 6990000, 0, 30000, NULL),
(1007, 10, '2024-02-14', 'delivered', 'credit_card', 32990000, 1500000, 0, NULL),
(1008, 11, '2024-02-18', 'cancelled', 'momo', 5990000, 0, 30000, 'Khach huy don vi het hang'),
(1009, 1, '2024-02-25', 'delivered', 'credit_card', 2490000, 0, 30000, NULL),
(1010, 14, '2024-03-01', 'shipped', 'bank_transfer', 28990000, 0, 0, 'Giao hang nhanh'),
(1011, 2, '2024-03-05', 'delivered', 'credit_card', 10990000, 1000000, 30000, NULL),
(1012, 6, '2024-03-10', 'delivered', 'zalo_pay', 1990000, 0, 30000, NULL),
(1013, 15, '2024-03-15', 'delivered', 'credit_card', 62980000, 5000000, 0, 'Don hang lon - tang qua'),
(1014, 9, '2024-03-20', 'processing', 'cod', 890000, 0, 30000, NULL),
(1015, 12, '2024-03-25', 'delivered', 'bank_transfer', 22990000, 2000000, 0, NULL),
(1016, 3, '2024-04-01', 'delivered', 'momo', 1290000, 0, 30000, NULL),
(1017, 8, '2024-04-05', 'shipped', 'credit_card', 38990000, 0, 0, NULL),
(1018, 4, '2024-04-10', 'delivered', 'cod', 11990000, 0, 30000, NULL),
(1019, 10, '2024-04-15', 'delivered', 'credit_card', 6990000, 500000, 0, NULL),
(1020, 5, '2024-04-20', 'cancelled', 'bank_transfer', 2290000, 0, 30000, 'Thanh toan that bai');

-- ============================================================
-- TABLE 4: order_items
-- ============================================================
CREATE TABLE order_items (
    item_id INTEGER,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DOUBLE PRECISION,
    subtotal DOUBLE PRECISION
);

INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price, subtotal) VALUES
(1, 1001, 1, 1, 29990000, 29990000),
(2, 1002, 2, 1, 27990000, 27990000),
(3, 1002, 5, 1, 8990000, 8990000),
(4, 1003, 5, 1, 8990000, 8990000),
(5, 1004, 7, 1, 2990000, 2990000),
(6, 1005, 3, 1, 32990000, 32990000),
(7, 1005, 10, 1, 6990000, 6990000),
(8, 1005, 12, 2, 2490000, 4980000),
(9, 1006, 10, 1, 6990000, 6990000),
(10, 1007, 3, 1, 32990000, 32990000),
(11, 1009, 12, 1, 2490000, 2490000),
(12, 1010, 6, 1, 28990000, 28990000),
(13, 1011, 16, 1, 10990000, 10990000),
(14, 1012, 13, 1, 1990000, 1990000),
(15, 1013, 4, 1, 35990000, 35990000),
(16, 1013, 9, 1, 38990000, 38990000),
(17, 1014, 14, 1, 890000, 890000),
(18, 1015, 15, 1, 22990000, 22990000),
(19, 1016, 14, 1, 1290000, 1290000),
(20, 1017, 9, 1, 38990000, 38990000),
(21, 1018, 19, 1, 11990000, 11990000),
(22, 1019, 10, 1, 6990000, 6990000),
(23, 1020, 18, 1, 2290000, 2290000);
