-- Dữ liệu gốc từ CSV, API, DB... được load vào đây trước khi chuẩn hóa

CREATE TABLE IF NOT EXISTS raw_products (
    product_id INT PRIMARY KEY,
    title TEXT,
    price NUMERIC,
    description TEXT,
    category TEXT,
    image TEXT,
    rating_rate NUMERIC,
    rating_count INT
);

CREATE TABLE IF NOT EXISTS raw_users (
    user_id INT PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_campaigns (
    campaign_id INT PRIMARY KEY,
    campaign_name TEXT,
    channel TEXT,
    start_date DATE,
    end_date DATE,
    budget NUMERIC
);
CREATE TABLE IF NOT EXISTS raw_orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    product_id INT,
    order_date TIMESTAMP,
    quantity INT,
    total_amount NUMERIC,
    FOREIGN KEY (user_id) REFERENCES raw_users(user_id),
    FOREIGN KEY (product_id) REFERENCES raw_products(product_id)
);

CREATE TABLE IF NOT EXISTS raw_clickstreams (
    id SERIAL PRIMARY KEY,
    event_time TIMESTAMP,
    user_id INT,
    session_id TEXT,
    page_url TEXT,
    device_type TEXT,
    FOREIGN KEY (user_id) REFERENCES raw_users(user_id)
);
