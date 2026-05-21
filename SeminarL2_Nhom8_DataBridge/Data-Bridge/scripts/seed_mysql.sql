CREATE TABLE IF NOT EXISTS orders (
    order_id    INT AUTO_INCREMENT PRIMARY KEY,
    customer    VARCHAR(100),
    product     VARCHAR(100),
    category    VARCHAR(50),
    quantity    INT,
    price       BIGINT,
    order_date  DATE,
    city        VARCHAR(50)
);

INSERT INTO orders (customer, product, category, quantity, price, order_date, city) VALUES
('Nguyen Van A',  'Laptop Dell',       'Electronics', 1, 15000000, '2024-01-15', 'Ho Chi Minh'),
('Tran Thi B',   'iPhone 15',         'Electronics', 2, 25000000, '2024-01-16', 'Hanoi'),
('Le Van C',     'Nike Shoes',        'Fashion',     3,  1500000, '2024-01-17', 'Da Nang'),
('Pham Thi D',   'Samsung TV',        'Electronics', 1,  8000000, '2024-01-18', 'Ho Chi Minh'),
('Hoang Van E',  'Adidas Jacket',     'Fashion',     2,  2000000, '2024-01-19', 'Hanoi'),
('Nguyen Thi F', 'MacBook Pro',       'Electronics', 1, 35000000, '2024-01-20', 'Ho Chi Minh'),
('Tran Van G',   'Running Shoes',     'Fashion',     1,  1200000, '2024-01-21', 'Can Tho'),
('Le Thi H',     'iPad Air',          'Electronics', 3, 18000000, '2024-01-22', 'Hanoi'),
('Pham Van I',   'Polo Shirt',        'Fashion',     5,   500000, '2024-01-23', 'Da Nang'),
('Vu Thi J',     'Sony Headphones',   'Electronics', 2,  3000000, '2024-01-24', 'Ho Chi Minh'),
('Do Van K',     'Wireless Mouse',    'Electronics', 4,   800000, '2024-02-01', 'Hanoi'),
('Bui Thi L',    'Levi Jeans',        'Fashion',     2,  1800000, '2024-02-03', 'Ho Chi Minh'),
('Cao Van M',    'Mechanical Keyboard','Electronics', 1,  2500000, '2024-02-05', 'Da Nang'),
('Ly Thi N',     'Zara Dress',        'Fashion',     3,  1200000, '2024-02-07', 'Hanoi'),
('Dang Van O',   'Monitor 4K',        'Electronics', 1, 12000000, '2024-02-10', 'Ho Chi Minh');

CREATE TABLE IF NOT EXISTS products (
    product_id   INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100),
    category     VARCHAR(50),
    unit_price   BIGINT,
    stock        INT
);

INSERT INTO products (name, category, unit_price, stock) VALUES
('Laptop Dell',        'Electronics', 15000000, 50),
('iPhone 15',          'Electronics', 25000000, 30),
('Nike Shoes',         'Fashion',      1500000, 200),
('Samsung TV',         'Electronics',  8000000, 25),
('Adidas Jacket',      'Fashion',      2000000, 150),
('MacBook Pro',        'Electronics', 35000000, 20),
('Running Shoes',      'Fashion',      1200000, 180),
('iPad Air',           'Electronics', 18000000, 40),
('Polo Shirt',         'Fashion',       500000, 500),
('Sony Headphones',    'Electronics',  3000000, 100);

CREATE TABLE IF NOT EXISTS customers (
    customer_id  INT AUTO_INCREMENT PRIMARY KEY,
    full_name    VARCHAR(100),
    email        VARCHAR(100),
    phone        VARCHAR(20),
    city         VARCHAR(50),
    joined_date  DATE
);

INSERT INTO customers (full_name, email, phone, city, joined_date) VALUES
('Nguyen Van A',  'vana@email.com',   '0901111111', 'Ho Chi Minh', '2023-06-01'),
('Tran Thi B',   'thib@email.com',   '0902222222', 'Hanoi',       '2023-07-15'),
('Le Van C',     'vanc@email.com',   '0903333333', 'Da Nang',     '2023-08-20'),
('Pham Thi D',   'thid@email.com',   '0904444444', 'Ho Chi Minh', '2023-09-01'),
('Hoang Van E',  'vane@email.com',   '0905555555', 'Hanoi',       '2023-10-10'),
('Nguyen Thi F', 'thif@email.com',   '0906666666', 'Ho Chi Minh', '2023-11-05'),
('Tran Van G',   'vang@email.com',   '0907777777', 'Can Tho',     '2023-12-01'),
('Le Thi H',     'thih@email.com',   '0908888888', 'Hanoi',       '2024-01-10');
