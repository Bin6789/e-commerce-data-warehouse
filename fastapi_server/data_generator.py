# fastapi_server/data_generator.py
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_user(user_id):
    return {
        "user_id": user_id,
        "name": fake.name(),
        "email": fake.email(),
        "created_at": fake.date_time_this_decade().isoformat()
    }

def generate_product(product_id):
    return {
        "product_id": product_id,
        "title": fake.word().capitalize(),
        "price": round(random.uniform(5, 500), 2),
        "description": fake.text(),
        "category": random.choice(["electronics", "clothing", "home", "toys"]),
        "image": fake.image_url(),
        "rating_rate": round(random.uniform(1, 5), 1),
        "rating_count": random.randint(1, 1000)
    }

def generate_order(order_id):
    return {
        "order_id": order_id,
        "user_id": random.randint(1, 1000),
        "product_id": random.randint(1, 1000),
        "order_date": fake.date_this_year().isoformat(),
        "quantity": random.randint(1, 5),
        "total_amount": round(random.uniform(20, 1000), 2)
    }

def generate_clickstream(event_id):
    return {
        "event_time": fake.iso8601(),
        "user_id": random.randint(1, 500),
        "session_id": fake.uuid4(),
        "page_url": fake.uri_path(),
        "device_type": random.choice(["mobile", "desktop", "tablet"])
    }
