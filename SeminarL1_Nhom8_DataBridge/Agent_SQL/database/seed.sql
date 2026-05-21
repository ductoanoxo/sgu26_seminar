-- ============================================
-- NL2SQL Sample Database - Seed Script
-- Target: Supabase (PostgreSQL)
-- ============================================

-- Drop tables if they exist (for re-seeding)
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================
-- TABLE: users
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- TABLE: products
-- ============================================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- TABLE: orders
-- ============================================
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    order_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10, 2)
);

-- ============================================
-- TABLE: order_items
-- ============================================
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL
);

-- ============================================
-- INDEXES
-- ============================================
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_products_category ON products(category);

-- ============================================
-- SEED DATA: users
-- ============================================
INSERT INTO users (name, email, city, country) VALUES
('Alice Johnson', 'alice@example.com', 'New York', 'USA'),
('Bob Smith', 'bob@example.com', 'London', 'UK'),
('Charlie Brown', 'charlie@example.com', 'Tokyo', 'Japan'),
('Diana Prince', 'diana@example.com', 'Paris', 'France'),
('Eve Davis', 'eve@example.com', 'Sydney', 'Australia'),
('Frank Miller', 'frank@example.com', 'Berlin', 'Germany'),
('Grace Lee', 'grace@example.com', 'Seoul', 'South Korea'),
('Henry Wilson', 'henry@example.com', 'Toronto', 'Canada'),
('Ivy Chen', 'ivy@example.com', 'Singapore', 'Singapore'),
('Jack Taylor', 'jack@example.com', 'São Paulo', 'Brazil'),
('Karen White', 'karen@example.com', 'Mumbai', 'India'),
('Leo Martinez', 'leo@example.com', 'Mexico City', 'Mexico'),
('Mia Anderson', 'mia@example.com', 'Stockholm', 'Sweden'),
('Nathan Thomas', 'nathan@example.com', 'Amsterdam', 'Netherlands'),
('Olivia Jackson', 'olivia@example.com', 'Dubai', 'UAE');

-- ============================================
-- SEED DATA: products
-- ============================================
INSERT INTO products (name, category, price, stock_quantity) VALUES
('Wireless Headphones', 'Electronics', 79.99, 150),
('Running Shoes', 'Sports', 129.99, 80),
('Coffee Maker', 'Home & Kitchen', 49.99, 200),
('Laptop Stand', 'Electronics', 34.99, 300),
('Yoga Mat', 'Sports', 24.99, 500),
('Water Bottle', 'Sports', 14.99, 1000),
('Desk Lamp', 'Home & Kitchen', 39.99, 250),
('Bluetooth Speaker', 'Electronics', 59.99, 120),
('Notebook Set', 'Stationery', 12.99, 800),
('Backpack', 'Accessories', 69.99, 180),
('Mechanical Keyboard', 'Electronics', 149.99, 90),
('Standing Desk Mat', 'Home & Kitchen', 44.99, 160),
('Fitness Tracker', 'Electronics', 99.99, 220),
('Camping Tent', 'Sports', 199.99, 45),
('Ceramic Mug Set', 'Home & Kitchen', 29.99, 400),
('USB-C Hub', 'Electronics', 54.99, 350),
('Resistance Bands', 'Sports', 19.99, 600),
('Scented Candle', 'Home & Kitchen', 16.99, 450),
('Travel Pillow', 'Accessories', 22.99, 300),
('Portable Charger', 'Electronics', 39.99, 280);

-- ============================================
-- SEED DATA: orders (spanning Jan 2024 – Aug 2024)
-- ============================================
INSERT INTO orders (user_id, order_date, status, total_amount) VALUES
(1,  '2024-01-05 10:30:00+00', 'completed', 159.98),
(2,  '2024-01-12 14:15:00+00', 'completed', 79.99),
(3,  '2024-01-20 09:00:00+00', 'completed', 129.99),
(1,  '2024-02-03 16:45:00+00', 'completed', 84.98),
(4,  '2024-02-14 11:30:00+00', 'completed', 49.99),
(5,  '2024-02-28 08:20:00+00', 'completed', 164.98),
(6,  '2024-03-05 13:00:00+00', 'completed', 34.99),
(7,  '2024-03-15 15:30:00+00', 'completed', 94.98),
(8,  '2024-03-22 10:00:00+00', 'completed', 69.99),
(9,  '2024-04-01 12:45:00+00', 'completed', 139.98),
(10, '2024-04-10 09:30:00+00', 'completed', 79.99),
(2,  '2024-04-20 14:00:00+00', 'completed', 59.99),
(3,  '2024-05-02 11:15:00+00', 'shipped', 189.97),
(4,  '2024-05-15 16:30:00+00', 'completed', 24.99),
(5,  '2024-05-28 08:45:00+00', 'shipped', 109.98),
(11, '2024-06-03 10:00:00+00', 'completed', 249.98),
(12, '2024-06-12 13:30:00+00', 'completed', 54.99),
(13, '2024-06-25 09:15:00+00', 'shipped', 179.97),
(14, '2024-07-04 11:00:00+00', 'completed', 134.98),
(15, '2024-07-18 15:45:00+00', 'completed', 89.98),
(1,  '2024-07-28 08:30:00+00', 'pending', 199.99),
(6,  '2024-08-05 12:00:00+00', 'completed', 44.99),
(7,  '2024-08-12 14:30:00+00', 'shipped', 159.98),
(8,  '2024-08-20 10:15:00+00', 'pending', 74.98),
(9,  '2024-08-28 16:00:00+00', 'pending', 119.97);

-- ============================================
-- SEED DATA: order_items
-- ============================================
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
-- Order 1: Alice - Headphones + Water Bottle
(1, 1, 1, 79.99),
(1, 6, 1, 14.99),
-- Order 2: Bob - Headphones
(2, 1, 1, 79.99),
-- Order 3: Charlie - Running Shoes
(3, 2, 1, 129.99),
-- Order 4: Alice - Coffee Maker + Laptop Stand
(4, 3, 1, 49.99),
(4, 4, 1, 34.99),
-- Order 5: Diana - Coffee Maker
(5, 3, 1, 49.99),
-- Order 6: Eve - Running Shoes + Yoga Mat
(6, 2, 1, 129.99),
(6, 5, 1, 24.99),
-- Order 7: Frank - Laptop Stand
(7, 4, 1, 34.99),
-- Order 8: Grace - Headphones + Water Bottle
(8, 1, 1, 79.99),
(8, 6, 1, 14.99),
-- Order 9: Henry - Backpack
(9, 10, 1, 69.99),
-- Order 10: Ivy - Bluetooth Speaker + Headphones
(10, 8, 1, 59.99),
(10, 1, 1, 79.99),
-- Order 11: Jack - Headphones
(11, 1, 1, 79.99),
-- Order 12: Bob - Bluetooth Speaker
(12, 8, 1, 59.99),
-- Order 13: Charlie - Headphones + Running Shoes
(13, 1, 1, 79.99),
(13, 2, 1, 129.99),
-- Order 14: Diana - Yoga Mat
(14, 5, 1, 24.99),
-- Order 15: Eve - Fitness Tracker
(15, 13, 1, 99.99),
-- Order 16: Karen - Mechanical Keyboard + Fitness Tracker
(16, 11, 1, 149.99),
(16, 13, 1, 99.99),
-- Order 17: Leo - USB-C Hub
(17, 16, 1, 54.99),
-- Order 18: Mia - Running Shoes + Coffee Maker
(18, 2, 1, 129.99),
(18, 3, 1, 49.99),
-- Order 19: Nathan - Backpack + Laptop Stand + Desk Lamp
(19, 10, 1, 69.99),
(19, 4, 1, 34.99),
-- Order 20: Olivia - Bluetooth Speaker + Ceramic Mug Set
(20, 8, 1, 59.99),
(20, 15, 1, 29.99),
-- Order 21: Alice - Camping Tent
(21, 14, 1, 199.99),
-- Order 22: Frank - Standing Desk Mat
(22, 12, 1, 44.99),
-- Order 23: Grace - Mechanical Keyboard
(23, 11, 1, 149.99),
-- Order 24: Henry - Notebook Set + Bluetooth Speaker
(24, 9, 1, 12.99),
(24, 8, 1, 59.99),
-- Order 25: Ivy - Portable Charger + Headphones + Resistance Bands
(25, 20, 1, 39.99),
(25, 1, 1, 79.99);
