import psycopg2
import random
from datetime import timedelta, datetime

def load_fact_campaign_result():
    conn = psycopg2.connect(
        host='postgres',
        database='dwh',
        user='user',
        password='password'
    )
    cur = conn.cursor()

    cur.execute("SELECT campaign_id, start_date, end_date FROM dim_campaign")
    campaigns = cur.fetchall()

    cur.execute("SELECT date_key FROM dim_date")
    valid_dates = {row[0] for row in cur.fetchall()}

    batch_size = 1000

    for campaign_id, start_date, end_date in campaigns:
        # Chuyển về kiểu date nếu cần
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        values = []
        current = start_date
        while current <= end_date:
            if current in valid_dates:
                impressions = random.randint(1000, 10000)
                clicks = random.randint(100, impressions)
                conversions = random.randint(10, clicks)
                values.append((campaign_id, current, impressions, clicks, conversions))
                if len(values) >= batch_size:
                    cur.executemany("""
                        INSERT INTO fact_campaign_result (campaign_id, date_key, impressions, clicks, conversions)
                        VALUES (%s, %s, %s, %s, %s)
                    """, values)
                    values = []
            current += timedelta(days=1)
        # Insert các bản ghi còn lại
        if values:
            cur.executemany("""
                INSERT INTO fact_campaign_result (campaign_id, date_key, impressions, clicks, conversions)
                VALUES (%s, %s, %s, %s, %s)
            """, values)

    conn.commit()
    cur.close()
    conn.close()

