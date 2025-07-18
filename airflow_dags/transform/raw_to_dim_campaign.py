import psycopg2

def transform_campaigns():
    conn = psycopg2.connect(
        host="postgres",
        database="dwh",
        user="user",
        password="password"
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO dim_campaign (campaign_id, campaign_name, channel, start_date, end_date, budget)
        SELECT DISTINCT campaign_id, campaign_name, channel, start_date, end_date, budget
        FROM raw_campaigns
        ON CONFLICT (campaign_id) DO NOTHING;
    """)
    conn.commit()
    cur.close()
    conn.close()
