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
