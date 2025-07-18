import psycopg2
from datetime import datetime, timedelta

def generate_dim_date(start_date="2022-01-01", end_date="2026-12-31"):
    conn = psycopg2.connect(
        host="postgres",
        database="dwh",
        user="user",
        password="password"
    )
    cur = conn.cursor()

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=1)

    while start <= end:
        cur.execute("""
            INSERT INTO dim_date (date_key, day, month, year, week, quarter)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (date_key) DO NOTHING;
        """, (
            start.date(),
            start.day,
            start.month,
            start.year,
            start.isocalendar()[1],
            (start.month - 1) // 3 + 1
        ))
        start += delta

    conn.commit()
    cur.close()
    conn.close()
