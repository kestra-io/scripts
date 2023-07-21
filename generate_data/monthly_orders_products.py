from datetime import datetime
import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# product-price mapping
product_price = {i: random.randint(10, 500) for i in range(1, 21)}


def create_monthly_data(month, year=2023):
    num_days = 30 if month != 2 else 28  # handle February
    num_orders = random.randint(100, 1000)

    order_ids = range(1, num_orders + 1)
    customer_names = [fake.name() for _ in range(num_orders)]
    customer_emails = [fake.email() for _ in range(num_orders)]
    product_ids = np.random.choice(list(product_price.keys()), size=num_orders)
    prices = [product_price[pid] for pid in product_ids]
    quantities = np.random.randint(1, 10, size=num_orders)
    totals = np.multiply(prices, quantities)

    # Generate random dates for given month and year
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, num_days)
    order_dates = [
        start_date + (end_date - start_date) * random.random()
        for _ in range(num_orders)
    ]

    df = pd.DataFrame(
        {
            "order_id": order_ids,
            "order_date": order_dates,
            "customer_name": customer_names,
            "customer_email": customer_emails,
            "product_id": product_ids,
            "price": prices,
            "quantity": quantities,
            "total": totals,
        }
    )

    df.to_csv(f"datasets/monthly_orders/{year}_{str(month).zfill(2)}.csv", index=False)


# product categories and brands (for the sake of demo, we assume there are 5 types of each)
product_cats = ["Electronics", "Books", "Clothing", "Household", "Outdoor"]
brands = [fake.domain_word() for i in range(20)]

# Create a data frame that contains product related info
product_data = pd.DataFrame(
    {
        "product_id": list(product_price.keys()),
        "product_name": [fake.bs() for i in list(product_price.keys())],
        "product_category": np.random.choice(product_cats, len(product_price)),
        "brand": np.random.choice(brands, len(product_price)),
    }
)

product_data.to_csv("datasets/products.csv", index=False)

for month in range(1, 13):
    create_monthly_data(month)
