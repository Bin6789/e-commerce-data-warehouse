import psycopg2
import pandas as pd
import re

def load_fact_clickstream():
    conn = psycopg2.connect(
        host='postgres',
        database='dwh',
        user='user',
        password='password'
    )
    cur = conn.cursor()

    # Lấy dữ liệu từ dim_clickstream (dữ liệu đã chuẩn hóa)
    df = pd.read_sql("SELECT * FROM dim_clickstream", conn)

    # Lấy các giá trị hợp lệ từ các bảng dim
    cur.execute("SELECT user_id FROM dim_user")
    valid_user_ids = {row[0] for row in cur.fetchall()}
    cur.execute("SELECT product_id FROM dim_product")
    valid_product_ids = {row[0] for row in cur.fetchall()}
    cur.execute("SELECT date_key FROM dim_date")
    valid_date_keys = {row[0] for row in cur.fetchall()}

    # Chuẩn hóa thời gian và ánh xạ product_id từ page_url
    df['click_time'] = pd.to_datetime(df['event_time'])
    df['date_key'] = df['click_time'].dt.date

    def extract_product_id(url):
        match = re.search(r'/product/(\d+)', url)
        return int(match.group(1)) if match else None

    df['product_id'] = df['page_url'].apply(extract_product_id)

    # Lọc các bản ghi hợp lệ theo dimension
    valid_df = df[
        df['user_id'].isin(valid_user_ids) &
        df['product_id'].isin(valid_product_ids) &
        df['date_key'].isin(valid_date_keys)
    ].copy()

    # Lọc trùng lặp trên các trường fact
    valid_df = valid_df.drop_duplicates(subset=['user_id', 'product_id', 'date_key', 'click_time'])

    values = [
        (row['user_id'], row['product_id'], row['date_key'], row['click_time'])
        for _, row in valid_df.iterrows()
    ]

    # Insert vào bảng fact_clickstream
    if values:
        cur.executemany("""
            INSERT INTO fact_clickstream (user_id, product_id, date_key, click_time)
            VALUES (%s, %s, %s, %s)
        """, values)

    conn.commit()
    cur.close()
    conn.close()