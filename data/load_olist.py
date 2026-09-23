import sqlite3
import pandas as pd


DB_PATH = "data/business.db"
RAW_PATH = "data/raw"


tables = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
}


connection = sqlite3.connect(DB_PATH)

for table_name, file_name in tables.items():
    file_path = f"{RAW_PATH}/{file_name}"

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False,
    )

    print(f"Loaded {table_name}: {len(df)} rows")


connection.close()

print("Database loaded successfully.")