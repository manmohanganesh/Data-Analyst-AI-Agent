from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = BASE_DIR/"data"/"raw"

DATABASE_PATH = (BASE_DIR/"data"/"database"/"olist.db")
DATASETS = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "category_translation":"product_category_name_translation.csv"
}

def create_database():
    print("\n Creating SQLite database..\n")
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    engine = create_engine(f"sqlite:///{DATABASE_PATH}")

    for table_name,file_name in DATASETS.items():
        file_path = RAW_DATA_PATH / file_name
        print(
            f"Loading {file_name}"
            f"-> Table: {table_name}"
        )

        df = pd.read_csv(file_path)
        df.to_sql(
            name= table_name,
            con= engine,
            if_exists="replace",
            index=False
        )

        print(f"Loaded {len(df):,}rows")

    print("\n"+"="*50)
    print("DATABASE CREATED SUCCESSFULLY")
    print("="*50)
    print(f"\n Database location:\n{DATABASE_PATH}")

if __name__=="__main__":
    create_database()