import psycopg2

def transform_users():
        conn = psycopg2.connect(
            host="postgres",
            database="dwh",
            user="user",
            password="password"
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO dim_user (user_id, name, email, created_at)
            SELECT DISTINCT user_id, name, email, CAST(created_at AS TIMESTAMP WITHOUT TIME ZONE)
            FROM raw_users
            ON CONFLICT (user_id) DO NOTHING;
        """)
        conn.commit()
        cur.close()
        conn.close()
