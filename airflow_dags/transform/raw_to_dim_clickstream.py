import psycopg2

def transform_clickstream():
        conn = psycopg2.connect(
            host="postgres",
            database="dwh",
            user="user",
            password="password"
        )
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO dim_clickstream (event_time, user_id, session_id, page_url, device_type)
            SELECT 
                CAST(event_time AS TIMESTAMP),
                user_id,
                session_id,
                page_url,
                device_type
            FROM raw_clickstreams;
        """)
        conn.commit()
        cur.close()
        conn.close()