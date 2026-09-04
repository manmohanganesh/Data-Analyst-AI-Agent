from src.database import DatabaseManager


def main():
    db = DatabaseManager()
    print("\n"+"="*60)
    print("Available Tables")
    print("="*60)

    tables = db.get_table_names()
    print(tables)

    orders_schema=db.get_table_schema('orders')
    for column in orders_schema:
        print(column)

    database_schema = db.get_database_schema()
    for table_name,columns in database_schema.items():
        print(f"\n TABLE {table_name}")
        for column in columns:
            print (column)

    query = """
        SELECT
            customer_state,
            COUNT(*) AS total_customers
        FROM customers
        GROUP BY customer_state
        ORDER BY total_customers DESC
        LIMIT 10
    """
    result = db.execute_query(query)
    print(result)

if __name__=="__main__":
    main()