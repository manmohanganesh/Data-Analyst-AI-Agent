from ollama import chat


class LLMManager:
    def __init__(self,model='qwen2.5:7b'):
        self.model=model

    def generate_sql(self,user_question,database_schema):
        prompt=f"""
                You are an expert SQL analyst.

                Your task is to generate a valid SQLite SQL query based on:

                1. The user's question
                2. The provided database schema

                DATABASE SCHEMA:
                {database_schema}

                USER QUESTION:
                {user_question}

                RULES:

                - Generate only a valid SQL query.
                - Use only tables and columns provided in the schema.
                - Only generate SELECT statements.
                - Do not modify the database.
                - Do not include explanations.
                - Do not use Markdown code blocks.

                SQL QUERY:
                """
        response = chat(
            model=self.model,
            messages=[
                {
                    'role':'user',
                    'content':prompt
                }
            ],
            options={
                'temperature':0
            }
        )
        return response.message.content.strip()

    def correct_sql(self,
                    user_question,
                    database_schema,
                    previous_sql,
                    database_error):
        prompt = f"""
        You are an expert SQLite SQL analyst.

        The SQL query you previously generated failed during execution.

        Your task is to correct the SQL query.

        USER QUESTION:
        {user_question}

        DATABASE SCHEMA:
        {database_schema}

        PREVIOUS SQL QUERY:
        {previous_sql}

        DATABASE ERROR:
        {database_error}

        RULES:

        - Carefully analyze the database error.
        - Use only tables and columns that exist in the provided schema.
        - Generate only a valid SQLite SELECT query.
        - Do not modify the database.
        - Do not include explanations.
        - Do not use Markdown code blocks.
        - Return only the corrected SQL query.

        CORRECTED SQL:
        """

        response = chat(
            model=self.model,
            messages=[
                {
                    'role':'user',
                    'content':prompt
                }
            ],
            options={
                'temperature':0
            }
        )       
        return response.message.content.strip()
    
    def recommend_chart(self,user_question,dataframe_info):
        prompt = f"""
        You are an expert data visualization analyst.

        Your task is to recommend the most appropriate chart
        for the user's question based on the provided dataframe.

        USER QUESTION:
        {user_question}

        DATAFRAME INFORMATION:
        {dataframe_info}

        RULES:

        - Choose only one chart type.
        - Allowed chart types are:
          bar, line, scatter, pie
        - Use the actual column names provided in the dataframe.
        - Do not invent column names.
        - Select columns that exist in the dataframe.
        - For categorical comparisons, prefer bar charts.
        - For trends over time, prefer line charts.
        - For relationships between two numerical variables,
          prefer scatter plots.
        - Use pie charts only when showing meaningful
          parts of a whole.
        - Return only valid JSON.
        - Do not use Markdown code blocks.
        - Do not include explanations.

        JSON FORMAT:

        {{
            "chart_type": "bar",
            "x_column": "column_name",
            "y_column": "column_name",
            "title": "Chart title"
        }}
        """
        response = chat(
            model=self.model,
            messages=[
                {
                    'role':'user',
                    'content':prompt
                }
            ],
            options={
                'temperature':0
            }
        )
        return response.message.content.strip()