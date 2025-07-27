import requests
import pandas as pd
from sqlalchemy import create_engine

API_URL = "http://fastapi:8000/api/orders/"
DB_URI = "postgresql://user:password@postgres:5432/dwh"

def load_orders_from_api():
    orders = []
    for order_id in range(1, 1001):
        res = requests.get(f"{API_URL}{order_id}")
        if res.status_code == 200:
            orders.append(res.json())

    df = pd.DataFrame(orders)
    engine = create_engine(DB_URI)
    df.to_sql("raw_orders", con=engine, if_exists="append", index=False)
