# fastapi_server/main.py
from fastapi import FastAPI
from data_generator import generate_user, generate_product, generate_order, generate_clickstream

app = FastAPI()

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    return generate_user(user_id)

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    return generate_product(product_id)

@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    return generate_order(order_id)

@app.get("/api/clickstream/{event_id}")
def get_clickstream(event_id: int):
    return generate_clickstream(event_id)
