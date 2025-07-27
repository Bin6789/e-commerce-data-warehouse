import requests
import pandas as pd
from sqlalchemy import create_engine

API_URL = "http://fastapi:8000/api/users/"
DB_URI = "postgresql://user:password@postgres:5432/dwh"

def load_users_from_api():
    users = []
    for user_id in range(1, 1001):
        res = requests.get(f"{API_URL}{user_id}")
        if res.status_code == 200:
            users.append(res.json())

    df = pd.DataFrame(users)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.drop_duplicates(subset=['user_id'])
    engine = create_engine(DB_URI)
    df.to_sql("raw_users", con=engine, if_exists="append", index=False)
