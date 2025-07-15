-- Dimension Tables
CREATE TABLE IF NOT EXISTS dim_customer (
  customer_id INT PRIMARY KEY,
  full_name TEXT,
  email TEXT,
  address TEXT
);

CREATE TABLE IF NOT EXISTS dim_product (
  product_id INT PRIMARY KEY,
  product_name TEXT,
  category TEXT,
  price NUMERIC
);

CREATE TABLE IF NOT EXISTS dim_date (
  date_id DATE PRIMARY KEY,
  year INT,
  quarter INT,
  month INT,
  day INT
);

-- Fact Table
CREATE TABLE IF NOT EXISTS fact_order (
  order_id INT PRIMARY KEY,
  customer_id INT,
  product_id INT,
  date_id DATE,
  quantity INT,
  total_amount NUMERIC,
  FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- Bảng dim_campaign
CREATE TABLE IF NOT EXISTS dim_campaign (
    campaign_id INTEGER PRIMARY KEY,
    campaign_name VARCHAR(255),
    channel VARCHAR(100),
    start_date DATE,
    end_date DATE,
    budget NUMERIC
);

-- Bảng dim_user (dành cho extract từ staging-db sau)
CREATE TABLE IF NOT EXISTS dim_user (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP
);
