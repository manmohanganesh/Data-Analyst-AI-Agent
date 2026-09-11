from src.graph import graph
from src.database import DatabaseManager


def main():

    # --------------------------------------------------
    # Initialize database
    # --------------------------------------------------

    db = DatabaseManager()

    schema = db.format_schema_for_llm()


    # --------------------------------------------------
    # Initial graph state
    # --------------------------------------------------

    initial_state = {

        "user_question":
            "Which product categories generate the highest revenue?",

        "database_schema":
            schema,

        "current_sql": "",
        "attempt": 0,

        "sql_valid": False,
        "validation_error": "",

        "query_result": None,
        "database_error": "",

        "dataframe_info": {},

        "chart_config": {},
        "chart_path": "",

        "final_error": ""
    }


    # --------------------------------------------------
    # Run LangGraph
    # --------------------------------------------------

    result = graph.invoke(initial_state)


    # --------------------------------------------------
    # Display results
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("LANGGRAPH EXECUTION COMPLETE")
    print("=" * 60)


    print("\nUser Question:")
    print(result["user_question"])


    print("\nAttempts:")
    print(result["attempt"])


    print("\nGenerated SQL:")
    print("-" * 60)
    print(result["current_sql"])


    print("\nSQL Valid:")
    print(result["sql_valid"])


    if result["validation_error"]:
        print("\nValidation Error:")
        print(result["validation_error"])


    # --------------------------------------------------
    # Database result
    # --------------------------------------------------

    if result["query_result"] is not None:

        print("\nQuery Result:")
        print("-" * 60)
        print(result["query_result"])


    if result["database_error"]:

        print("\nDatabase Error:")
        print("-" * 60)
        print(result["database_error"])


    # --------------------------------------------------
    # DataFrame information
    # --------------------------------------------------

    if result["dataframe_info"]:

        print("\nDataFrame Information:")
        print("-" * 60)

        print(
            "Columns:",
            result["dataframe_info"]["columns"]
        )

        print(
            "Row Count:",
            result["dataframe_info"]["row_count"]
        )


    # --------------------------------------------------
    # Chart
    # --------------------------------------------------

    if result["chart_config"]:

        print("\nChart Configuration:")
        print("-" * 60)
        print(result["chart_config"])


    if result["chart_path"]:

        print("\nChart Generated:")
        print(result["chart_path"])


    # --------------------------------------------------
    # Final error
    # --------------------------------------------------

    if result["final_error"]:

        print("\nFinal Error:")
        print("-" * 60)
        print(result["final_error"])


    print("\n" + "=" * 60)
    print("END")
    print("=" * 60)


if __name__ == "__main__":
    main()