import requests
import pandas as pd
from sqlalchemy import create_engine

API_URL = "http://fastapi:8000/api/clickstream/"
DB_URI = "postgresql://user:password@postgres:5432/dwh"

def load_clickstream_from_api():
    clickstream = []
    for event_id in range(1, 1001):
        res = requests.get(f"{API_URL}{event_id}")
        if res.status_code == 200:
            clickstream.append(res.json())

    df = pd.DataFrame(clickstream)
    df['event_time'] = pd.to_datetime(df['event_time'])
    engine = create_engine(DB_URI)
    df.to_sql("raw_clickstreams", con=engine, if_exists="append", index=False)
