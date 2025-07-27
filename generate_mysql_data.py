import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
NUM_USERS = 1000
NUM_PRODUCTS = 200
NUM_ORDERS = 2000
NUM_VENDORS = 50
NUM_CATEGORIES = 10

output_dir = './datasets/static'
os.makedirs(output_dir, exist_ok=True)

# USERS
users = []
for i in range(1, NUM_USERS + 1):
    users.append({
        'user_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'created_at': fake.date_time_between(start_date='-3y', end_date='now')
    })
pd.DataFrame(users).to_csv(f'{output_dir}/users.csv', index=False)

# ADDRESSES
addresses = []
for i in range(1, NUM_USERS + 1):
    addresses.append({
        'address_id': i,
        'user_id': i,
        'street': fake.street_address(),
        'city': fake.city(),
        'country': fake.country(),
        'zip_code': fake.postcode()
    })
pd.DataFrame(addresses).to_csv(f'{output_dir}/addresses.csv', index=False)

# CATEGORIES
categories = [fake.word().capitalize() for _ in range(NUM_CATEGORIES)]
pd.DataFrame([{'category_id': i+1, 'name': cat} for i, cat in enumerate(categories)]).to_csv(f'{output_dir}/categories.csv', index=False)

# VENDORS
vendors = []
for i in range(1, NUM_VENDORS + 1):
    vendors.append({
        'vendor_id': i,
        'name': fake.company(),
        'contact_email': fake.company_email()
    })
pd.DataFrame(vendors).to_csv(f'{output_dir}/vendors.csv', index=False)

# PRODUCTS
products = []
for i in range(1, NUM_PRODUCTS + 1):
    products.append({
        'product_id': i,
        'name': fake.word().capitalize(),
        'description': fake.sentence(),
        'price': round(random.uniform(10, 500), 2),
        'category': random.choice(categories),
        'image': fake.image_url()
    })
pd.DataFrame(products).to_csv(f'{output_dir}/products.csv', index=False)

# ORDERS
orders = []
for i in range(1, NUM_ORDERS + 1):
    user_id = random.randint(1, NUM_USERS)
    orders.append({
        'order_id': i,
        'user_id': user_id,
        'order_date': fake.date_time_between(start_date='-2y', end_date='now'),
        'status': random.choice(['completed', 'processing', 'cancelled']),
        'total_amount': round(random.uniform(20, 1000), 2)
    })
pd.DataFrame(orders).to_csv(f'{output_dir}/orders.csv', index=False)

# ORDER_ITEMS
order_items = []
for i in range(1, NUM_ORDERS + 1):
    order_items.append({
        'order_item_id': i,
        'order_id': i,
        'product_id': random.randint(1, NUM_PRODUCTS),
        'quantity': random.randint(1, 5),
        'price': round(random.uniform(10, 500), 2)
    })
pd.DataFrame(order_items).to_csv(f'{output_dir}/order_items.csv', index=False)

# PAYMENTS
payments = []
for i in range(1, NUM_ORDERS + 1):
    payments.append({
        'payment_id': i,
        'order_id': i,
        'payment_date': fake.date_time_between(start_date='-2y', end_date='now'),
        'payment_method': random.choice(['credit_card', 'paypal', 'bank_transfer']),
        'amount': round(random.uniform(20, 1000), 2)
    })
pd.DataFrame(payments).to_csv(f'{output_dir}/payments.csv', index=False)

print(f"✅ Generated test data into {output_dir}")
