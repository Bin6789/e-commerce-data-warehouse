import requests
import pandas as pd
from sqlalchemy import create_engine

API_URL = "http://fastapi:8000/api/products/"
DB_URI = "postgresql://user:password@postgres:5432/dwh"

def load_products_from_api():
    products = []
    for product_id in range(1, 1001):
        res = requests.get(f"{API_URL}{product_id}")
        if res.status_code == 200:
            products.append(res.json())

    df = pd.DataFrame(products)
    engine = create_engine(DB_URI)
    df.to_sql("raw_products", con=engine, if_exists="append", index=False)
