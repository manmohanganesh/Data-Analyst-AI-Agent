from src.database import DatabaseManager
from src.llm import LLMManager
from src.sql_validator import validate_sql
from src.visualization import (
    generate_chart,
    inspect_dataframe,
    parse_chart_recommendation,
    validate_chart_config,
)


def main():

    # ==========================================
    # INITIALIZE DATABASE
    # ==========================================

    db = DatabaseManager()

    # Fetch complete database schema
    formatted_schema = db.format_schema_for_llm()


    # ==========================================
    # INITIALIZE LLM
    # ==========================================

    llm = LLMManager()


    # ==========================================
    # USER QUESTION
    # ==========================================

    user_question = "Which product categories generate the highest revenue?"


    # ==========================================
    # GENERATE INITIAL SQL
    # ==========================================

    generated_sql = llm.generate_sql(
        user_question=user_question,
        database_schema=formatted_schema
    )


    # ==========================================
    # INITIALIZE RETRY STATE
    # ==========================================

    max_attempts = 3
    attempt = 1
    current_sql = generated_sql


    # ==========================================
    # SQL EXECUTION + CORRECTION LOOP
    # ==========================================

    while attempt <= max_attempts:

        print("\n" + "=" * 60)
        print(f"ATTEMPT {attempt}")
        print("=" * 60)

        print("\nSQL QUERY:\n")
        print(current_sql)


        # ==========================================
        # VALIDATE SQL BEFORE EXECUTION
        # ==========================================

        validation_result = validate_sql(current_sql)


        if validation_result["valid"]:

            # Execute only validated SQL
            result = db.execute_query(current_sql)

        else:

            # Create a standardized failure result
            result = {
                "success": False,
                "data": None,
                "error": validation_result["error"]
            }


        # ==========================================
        # CHECK EXECUTION RESULT
        # ==========================================

        if result["success"]:

            dataframe = result["data"]

            print("\nQuery successful!")
            print(dataframe)

            # Inspect dataframe
            dataframe_info = inspect_dataframe(dataframe)

            print("\nDataFrame information:")
            print(dataframe_info)

            # Ask LLM for chart recommendation
            chart_recommendation = llm.recommend_chart(
                user_question,
                dataframe_info
            )

            print("\nChart recommendation:")
            print(chart_recommendation)

            # Parse LLM response
            parsed_recommendation = parse_chart_recommendation(
                chart_recommendation
            )

            if not parsed_recommendation["success"]:

                print(
                    "\nInvalid chart recommendation:"
                )
                print(parsed_recommendation["error"])

                break

            # Validate chart configuration
            chart_validation = validate_chart_config(
                parsed_recommendation["config"],
                dataframe
            )

            if not chart_validation["valid"]:

                print(
                    "\nInvalid chart configuration:"
                )
                print(chart_validation["error"])

                break

            # Generate chart
            chart_path = generate_chart(
                dataframe,
                parsed_recommendation["config"]
            )

            print("\nChart generated:")
            print(chart_path)

            break


        # ==========================================
        # HANDLE FAILURE
        # ==========================================

        else:

            print("\nQUERY FAILED!\n")
            print("ERROR:")
            print(result["error"])


            # ==========================================
            # CORRECT SQL IF ATTEMPTS REMAIN
            # ==========================================

            if attempt < max_attempts:

                corrected_sql = llm.correct_sql(
                    user_question=user_question,
                    database_schema=formatted_schema,
                    previous_sql=current_sql,
                    database_error=result["error"]
                )

                # Update workflow state
                current_sql = corrected_sql

                # Move to next attempt
                attempt += 1


            else:

                print("\nMaximum correction attempts reached.")
                break

if __name__ == "__main__":
    main()