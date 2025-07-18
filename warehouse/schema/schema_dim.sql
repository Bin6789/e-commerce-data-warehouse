-- Các bảng dimension dùng trong Star Schema

CREATE TABLE IF NOT EXISTS dim_product (
    product_id INT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price NUMERIC,
    rating NUMERIC,
    image TEXT
);

CREATE TABLE IF NOT EXISTS dim_user (
    user_id INT PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_campaign (
    campaign_id INT PRIMARY KEY,
    campaign_name TEXT,
    channel TEXT,
    start_date DATE,
    end_date DATE,
    budget NUMERIC
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key DATE PRIMARY KEY,
    day INT,
    month INT,
    year INT,
    week INT,
    quarter INT
);

CREATE TABLE IF NOT EXISTS dim_clickstream (
    clickstream_id SERIAL PRIMARY KEY,  -- Khóa thay thế
    event_time TIMESTAMP,
    user_id INT,
    session_id TEXT,
    page_url TEXT,
    device_type TEXT,
);


