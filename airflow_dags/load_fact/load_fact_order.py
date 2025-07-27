import psycopg2


def load_fact_orders():
    conn = psycopg2.connect(
        host='postgres',
        database='dwh',
        user='user',
        password='password'
    )
    cur = conn.cursor()

    # Chỉ insert các order hợp lệ, ánh xạ đúng các trường và kiểu dữ liệu
    cur.execute("""
        INSERT INTO fact_order (
            order_id,
            user_id,
            product_id,
            order_date,
            quantity,
            total_amount
        )
        SELECT
            o.order_id,
            o.user_id,
            o.product_id,
            o.order_date::DATE,
            o.quantity,
            o.total_amount
        FROM raw_orders o
        INNER JOIN dim_user u ON o.user_id = u.user_id
        INNER JOIN dim_product p ON o.product_id = p.product_id
        INNER JOIN dim_date d ON d.date_key = o.order_date::DATE
        ON CONFLICT (order_id) DO NOTHING
    """)

    conn.commit()
    cur.close()
    conn.close()
