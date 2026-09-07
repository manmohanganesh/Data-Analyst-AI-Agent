from sql_validator import validate_sql


queries = [
    "SELECT * FROM orders",
    "select * from customers",
    "DROP TABLE orders",
    "DELETE FROM customers",
    "SELECT * FROM orders; DROP TABLE orders;"
]


for query in queries:

    result = validate_sql(query)

    print("\nQUERY:")
    print(query)

    print("RESULT:")
    print(result)