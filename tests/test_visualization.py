import pandas as pd

from src.visualization import (
    generate_chart,
    parse_chart_recommendation,
    validate_chart_config,
)

dataframe = pd.DataFrame(
    {
        "product_category": [
            "health_beauty",
            "watches_gifts",
            "bed_bath_table"
        ],
        "total_revenue": [
            1258681.34,
            1205005.68,
            1036988.68
        ]
    }
)


recommendation = """
{
    "chart_type": "bar",
    "x_column": "product_category",
    "y_column": "total_revenue",
    "title": "Top Product Categories by Revenue"
}
"""


result = parse_chart_recommendation(recommendation)

print("Parsed recommendation:")
print(result)


validation = validate_chart_config(
    result["config"],
    dataframe
)

print("\nValidation:")
print(validation)

chart_path = generate_chart(
    dataframe,
    result["config"]
)

print("\nChart generated:")
print(chart_path)