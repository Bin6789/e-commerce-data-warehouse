-- Database & Use
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- USERS
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at DATETIME
);

-- ADDRESSES
CREATE TABLE IF NOT EXISTS addresses (
    address_id INT PRIMARY KEY,
    user_id INT,
    street VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    zip_code VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2),
    category VARCHAR(100),
    image VARCHAR(255)
);

-- CATEGORIES
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100)
);

-- VENDORS
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id INT PRIMARY KEY,
    name VARCHAR(100),
    contact_email VARCHAR(100)
);

-- ORDERS
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    order_date DATETIME,
    status VARCHAR(50),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ORDER_ITEMS
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- PAYMENTS
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT PRIMARY KEY,
    order_id INT,
    payment_date DATETIME,
    payment_method VARCHAR(50),
    amount DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
