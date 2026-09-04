from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect, text

BASE_DIR=Path(__file__).resolve().parent.parent

DATABASE_PATH = (BASE_DIR/'data'/'database'/'olist.db')

class DatabaseManager:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        self.engine = create_engine(f"sqlite:///{self.database_path}")

    def get_table_names(self):
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    def get_table_schema(self,table_name):
        inspector =inspect(self.engine)
        columns= inspector.get_columns(table_name)
        schema=[]

        for column in columns:
            schema.append({
                "column_name" : column["name"],
                "data_type" :str(column['type'])
            })
        return schema

    def get_database_schema(self):
        database_schema={}
        table_names=self.get_table_names()

        for table_name in table_names:
            database_schema[table_name] = (
                self.get_table_schema(table_name)
            )
        return database_schema

    def execute_query(self,query):
        with self.engine.connect() as connection:
            dataframe = pd.read_sql_query(
                text(query),
                connection
            )
        return dataframe