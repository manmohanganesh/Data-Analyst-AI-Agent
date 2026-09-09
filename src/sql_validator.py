import re


def validate_sql(query):
    query = query.strip()

    if ";" in query[:-1]:
        return {
            "valid":False,
            "error":"Multiple SQL statement are not allowed."
        }
    if not re.match(r"^SELECT\b",query,re.IGNORECASE):
        return{
            "valid":False,
            "error": "Only SELECT statements are allowed."
        }

    return{
        'valid':True,
        "error": None
    }