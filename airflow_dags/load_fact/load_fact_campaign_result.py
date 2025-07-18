import psycopg2
import random
import pandas as pd
from datetime import timedelta

def load_fact_campaign_result():
    conn = psycopg2.connect(
        host='postgres',
        database='dwh',
        user='user',
        password='password'
    )
    cur = conn.cursor()
    
    # Lấy dữ liệu từ dim_campaign
    cur.execute("SELECT campaign_id, start_date, end_date FROM dim_campaign")
    campaigns = cur.fetchall()

    values = []
    for campaign_id, start_date, end_date in campaigns:
        current = start_date
        while current <= end_date:
            date_key = current  # Sử dụng DATE trực tiếp
            impressions = random.randint(1000, 10000)
            clicks = random.randint(100, impressions)
            conversions = random.randint(10, clicks)
            values.append((campaign_id, date_key, impressions, clicks, conversions))
            current += timedelta(days=1)

    # Chèn hàng loạt
    if values:
        cur.executemany("""
            INSERT INTO fact_campaign_result (campaign_id, date_key, impressions, clicks, conversions)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, values)

    conn.commit()
    cur.close()
    conn.close()

