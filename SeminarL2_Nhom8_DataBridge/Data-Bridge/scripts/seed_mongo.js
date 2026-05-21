db = db.getSiblingDB('shopdb');

db.orders.drop();
db.orders.insertMany([
  { order_id: 1, customer: "Nguyen Van A",  product: "Laptop Dell",        category: "Electronics", quantity: 1, price: 15000000, order_date: "2024-01-15", city: "Ho Chi Minh" },
  { order_id: 2, customer: "Tran Thi B",   product: "iPhone 15",          category: "Electronics", quantity: 2, price: 25000000, order_date: "2024-01-16", city: "Hanoi" },
  { order_id: 3, customer: "Le Van C",     product: "Nike Shoes",         category: "Fashion",     quantity: 3, price:  1500000, order_date: "2024-01-17", city: "Da Nang" },
  { order_id: 4, customer: "Pham Thi D",   product: "Samsung TV",         category: "Electronics", quantity: 1, price:  8000000, order_date: "2024-01-18", city: "Ho Chi Minh" },
  { order_id: 5, customer: "Hoang Van E",  product: "Adidas Jacket",      category: "Fashion",     quantity: 2, price:  2000000, order_date: "2024-01-19", city: "Hanoi" },
  { order_id: 6, customer: "Nguyen Thi F", product: "MacBook Pro",        category: "Electronics", quantity: 1, price: 35000000, order_date: "2024-01-20", city: "Ho Chi Minh" },
  { order_id: 7, customer: "Tran Van G",   product: "Running Shoes",      category: "Fashion",     quantity: 1, price:  1200000, order_date: "2024-01-21", city: "Can Tho" },
  { order_id: 8, customer: "Le Thi H",     product: "iPad Air",           category: "Electronics", quantity: 3, price: 18000000, order_date: "2024-01-22", city: "Hanoi" },
  { order_id: 9, customer: "Pham Van I",   product: "Polo Shirt",         category: "Fashion",     quantity: 5, price:   500000, order_date: "2024-01-23", city: "Da Nang" },
  { order_id:10, customer: "Vu Thi J",     product: "Sony Headphones",    category: "Electronics", quantity: 2, price:  3000000, order_date: "2024-01-24", city: "Ho Chi Minh" },
  { order_id:11, customer: "Do Van K",     product: "Wireless Mouse",     category: "Electronics", quantity: 4, price:   800000, order_date: "2024-02-01", city: "Hanoi" },
  { order_id:12, customer: "Bui Thi L",    product: "Levi Jeans",         category: "Fashion",     quantity: 2, price:  1800000, order_date: "2024-02-03", city: "Ho Chi Minh" },
  { order_id:13, customer: "Cao Van M",    product: "Mechanical Keyboard",category: "Electronics", quantity: 1, price:  2500000, order_date: "2024-02-05", city: "Da Nang" },
  { order_id:14, customer: "Ly Thi N",     product: "Zara Dress",         category: "Fashion",     quantity: 3, price:  1200000, order_date: "2024-02-07", city: "Hanoi" },
  { order_id:15, customer: "Dang Van O",   product: "Monitor 4K",         category: "Electronics", quantity: 1, price: 12000000, order_date: "2024-02-10", city: "Ho Chi Minh" },
]);

db.products.drop();
db.products.insertMany([
  { product_id: 1, name: "Laptop Dell",         category: "Electronics", unit_price: 15000000, stock: 50 },
  { product_id: 2, name: "iPhone 15",           category: "Electronics", unit_price: 25000000, stock: 30 },
  { product_id: 3, name: "Nike Shoes",          category: "Fashion",     unit_price:  1500000, stock: 200 },
  { product_id: 4, name: "Samsung TV",          category: "Electronics", unit_price:  8000000, stock: 25 },
  { product_id: 5, name: "Adidas Jacket",       category: "Fashion",     unit_price:  2000000, stock: 150 },
  { product_id: 6, name: "MacBook Pro",         category: "Electronics", unit_price: 35000000, stock: 20 },
  { product_id: 7, name: "Running Shoes",       category: "Fashion",     unit_price:  1200000, stock: 180 },
  { product_id: 8, name: "iPad Air",            category: "Electronics", unit_price: 18000000, stock: 40 },
  { product_id: 9, name: "Polo Shirt",          category: "Fashion",     unit_price:   500000, stock: 500 },
  { product_id:10, name: "Sony Headphones",     category: "Electronics", unit_price:  3000000, stock: 100 },
]);

db.customers.drop();
db.customers.insertMany([
  { customer_id: 1, full_name: "Nguyen Van A",  email: "vana@email.com", phone: "0901111111", city: "Ho Chi Minh", joined_date: "2023-06-01" },
  { customer_id: 2, full_name: "Tran Thi B",   email: "thib@email.com", phone: "0902222222", city: "Hanoi",       joined_date: "2023-07-15" },
  { customer_id: 3, full_name: "Le Van C",     email: "vanc@email.com", phone: "0903333333", city: "Da Nang",     joined_date: "2023-08-20" },
  { customer_id: 4, full_name: "Pham Thi D",   email: "thid@email.com", phone: "0904444444", city: "Ho Chi Minh", joined_date: "2023-09-01" },
  { customer_id: 5, full_name: "Hoang Van E",  email: "vane@email.com", phone: "0905555555", city: "Hanoi",       joined_date: "2023-10-10" },
  { customer_id: 6, full_name: "Nguyen Thi F", email: "thif@email.com", phone: "0906666666", city: "Ho Chi Minh", joined_date: "2023-11-05" },
  { customer_id: 7, full_name: "Tran Van G",   email: "vang@email.com", phone: "0907777777", city: "Can Tho",     joined_date: "2023-12-01" },
  { customer_id: 8, full_name: "Le Thi H",     email: "thih@email.com", phone: "0908888888", city: "Hanoi",       joined_date: "2024-01-10" },
]);

print('MongoDB seed complete: orders=' + db.orders.countDocuments() + ', products=' + db.products.countDocuments() + ', customers=' + db.customers.countDocuments());
