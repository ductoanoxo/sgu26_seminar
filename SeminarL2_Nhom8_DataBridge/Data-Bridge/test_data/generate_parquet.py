"""
Run this script to generate sales_2024.parquet
Requirements: pip install pyarrow pandas
"""

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import date, timedelta
import random

random.seed(42)

cities    = ["Ho Chi Minh", "Hanoi", "Da Nang", "Can Tho", "Hue"]
channels  = ["Online", "In-Store", "Mobile App", "Phone"]
products  = [
    ("Laptop Dell XPS 15", "Electronics", 35000000),
    ("iPhone 15 Pro",       "Electronics", 28000000),
    ("Mechanical Keyboard", "Accessories",  2500000),
    ("Sony Headphones",     "Electronics",  8500000),
    ("Logitech Mouse",      "Accessories",  2800000),
    ("iPad Pro",            "Electronics", 26000000),
    ("USB-C Hub",           "Accessories",  1500000),
    ("Standing Desk",       "Furniture",    9000000),
    ("Gaming Chair",        "Furniture",    7500000),
    ("AirPods Pro",         "Electronics",  6500000),
]

rows = []
start = date(2024, 1, 1)

for i in range(1, 201):
    prod_name, category, base_price = random.choice(products)
    qty      = random.randint(1, 5)
    discount = random.choice([0, 0, 0, 5, 10, 15])
    price    = int(base_price * (1 - discount / 100))
    total    = price * qty
    sale_date = start + timedelta(days=random.randint(0, 364))

    rows.append({
        "sale_id":      i,
        "sale_date":    sale_date.isoformat(),
        "product_name": prod_name,
        "category":     category,
        "quantity":     qty,
        "unit_price":   price,
        "discount_pct": discount,
        "total_amount": total,
        "city":         random.choice(cities),
        "channel":      random.choice(channels),
        "customer_id":  random.randint(1001, 1500),
    })

df = pd.DataFrame(rows)
table = pa.Table.from_pandas(df)
pq.write_table(table, "sales_2024.parquet")

print(f"Created sales_2024.parquet  ({len(df)} rows)")
print(df.head(5).to_string(index=False))
