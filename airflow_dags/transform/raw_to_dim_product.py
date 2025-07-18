import psycopg2

def transform_products():
        conn = psycopg2.connect(
            host="postgres",
            database="dwh",
            user="user",
            password="password"
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO dim_product (product_id, product_name, category, price, rating, image)
            SELECT DISTINCT 
                product_id,
                title AS product_name,
                category,
                price,
                COALESCE(CAST(rating_rate AS NUMERIC), 0) AS rating,  -- Handle NULL with default 0
                image
            FROM raw_products
            ON CONFLICT (product_id) DO NOTHING;
        """)
        conn.commit()
        cur.close()
        conn.close()
