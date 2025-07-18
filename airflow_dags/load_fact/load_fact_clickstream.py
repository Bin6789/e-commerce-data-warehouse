
import pandas as pd
import re
import psycopg2

def load_fact_clickstream():
    conn = psycopg2.connect(
        host='postgres',
        database='dwh',
        user='user',
        password='password'
    )
    cur = conn.cursor()

    # Lấy dữ liệu từ dim_clickstream
    df = pd.read_sql("SELECT * FROM dim_clickstream", conn)

    # Chuyển đổi event_time và tạo date_key
    df['click_time'] = pd.to_datetime(df['event_time'])
    df['date_key'] = df['click_time'].dt.date

    # Ánh xạ product_id từ page_url
    def extract_product_id(url):
        match = re.search(r'/product/(\d+)', url)
        return int(match.group(1)) if match else None

    df['product_id'] = df['page_url'].apply(extract_product_id).fillna(0).astype(int)

    # Chuẩn bị dữ liệu cho fact_clickstream (loại bỏ id vì là SERIAL)
    values = [
        (row['user_id'], row['product_id'], row['date_key'], row['click_time'])
        for _, row in df.iterrows()
    ]

    # Chèn hàng loạt
    if values:
        cur.executemany("""
            INSERT INTO fact_clickstream (user_id, product_id, date_key, click_time)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, values)

    conn.commit()
    cur.close()
    conn.close()