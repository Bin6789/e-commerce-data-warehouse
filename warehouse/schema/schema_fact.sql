-- Bảng fact phục vụ phân tích chính

CREATE TABLE IF NOT EXISTS fact_order (
    order_id INT PRIMARY KEY,
    user_id INT REFERENCES dim_user(user_id),
    product_id INT REFERENCES dim_product(product_id),
    order_date DATE REFERENCES dim_date(date_key),
    quantity INT,
    total_amount NUMERIC
);

CREATE TABLE IF NOT EXISTS fact_campaign_result (
    id SERIAL PRIMARY KEY,
    campaign_id INT REFERENCES dim_campaign(campaign_id),
    date_key DATE REFERENCES dim_date(date_key),
    impressions INT,
    clicks INT,
    conversions INT
);

CREATE TABLE IF NOT EXISTS fact_clickstream (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES dim_user(user_id),
    product_id INT REFERENCES dim_product(product_id),
    date_key DATE REFERENCES dim_date(date_key),
    click_time TIMESTAMP
);
