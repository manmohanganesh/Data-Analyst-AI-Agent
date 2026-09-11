from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from src.llm import LLMManager
from src.database import DatabaseManager
from src.sql_validator import validate_sql

from src.visualization import (
    inspect_dataframe,
    parse_chart_recommendation,
    validate_chart_config,
    generate_chart
)


# ============================================================
# STATE
# ============================================================

class AgentState(TypedDict):

    # User input
    user_question: str

    # Database information
    database_schema: str

    # SQL workflow
    current_sql: str
    attempt: int

    # SQL validation
    sql_valid: bool
    validation_error: str

    # Database execution
    query_result: object
    database_error: str

    # DataFrame information
    dataframe_info: dict

    # Visualization
    chart_config: dict
    chart_path: str

    # Final status
    final_error: str


# ============================================================
# NODES
# ============================================================

def generate_sql_node(state: AgentState):
    """
    Generate the initial SQL query from the user's question.
    """

    llm = LLMManager()

    sql = llm.generate_sql(
        user_question=state["user_question"],
        database_schema=state["database_schema"]
    )

    return {
        "current_sql": sql,
        "attempt": 1
    }


def validate_sql_node(state: AgentState):
    """
    Validate the generated SQL before executing it.
    """

    validation_result = validate_sql(
        state["current_sql"]
    )

    return {
        "sql_valid": validation_result["valid"],
        "validation_error": validation_result["error"]
    }


def execute_sql_node(state: AgentState):
    """
    Execute the SQL query against the database.
    """

    db = DatabaseManager()

    result = db.execute_query(
        state["current_sql"]
    )

    if result["success"]:

        return {
            "query_result": result["data"],
            "database_error": ""
        }

    return {
        "query_result": None,
        "database_error": result["error"]
    }


def correct_sql_node(state: AgentState):
    """
    Ask the LLM to correct SQL after a database execution error.
    """

    llm = LLMManager()

    corrected_sql = llm.correct_sql(
        user_question=state["user_question"],
        database_schema=state["database_schema"],
        previous_sql=state["current_sql"],
        database_error=state["database_error"]
    )

    return {
        "current_sql": corrected_sql,
        "attempt": state["attempt"] + 1
    }


def inspect_dataframe_node(state: AgentState):
    """
    Inspect the DataFrame so the LLM knows its structure
    before recommending a chart.
    """

    dataframe = state["query_result"]

    dataframe_info = inspect_dataframe(
        dataframe
    )

    return {
        "dataframe_info": dataframe_info
    }


def recommend_chart_node(state: AgentState):
    """
    Ask the LLM to recommend the most appropriate chart.
    """

    llm = LLMManager()

    recommendation = llm.recommend_chart(
        user_question=state["user_question"],
        dataframe_info=state["dataframe_info"]
    )

    parsed_result = parse_chart_recommendation(
        recommendation
    )

    if not parsed_result["success"]:

        return {
            "chart_config": {},
            "final_error": (
                "Failed to parse chart recommendation: "
                + parsed_result["error"]
            )
        }

    return {
        "chart_config": parsed_result["config"]
    }


def validate_chart_node(state: AgentState):
    """
    Validate that the chart configuration uses
    supported chart types and real DataFrame columns.
    """

    dataframe = state["query_result"]

    validation_result = validate_chart_config(
        state["chart_config"],
        dataframe
    )

    if not validation_result["valid"]:

        return {
            "final_error": validation_result["error"]
        }

    return {
        "final_error": ""
    }


def generate_chart_node(state: AgentState):
    """
    Generate and save the final visualization.
    """

    dataframe = state["query_result"]

    chart_path = generate_chart(
        dataframe=dataframe,
        chart_config=state["chart_config"]
    )

    return {
        "chart_path": chart_path
    }


# ============================================================
# ROUTING FUNCTIONS
# ============================================================

def route_after_validation(state: AgentState):
    """
    Decide whether SQL should be executed or rejected.
    """

    if state["sql_valid"]:
        return "execute_sql"

    return "end"


def route_after_execution(state: AgentState):
    """
    Decide whether execution succeeded or
    whether SQL needs to be corrected.
    """

    if state["query_result"] is not None:
        return "inspect_dataframe"

    if state["attempt"] < 3:
        return "correct_sql"

    return "end"


def route_after_chart_recommendation(state: AgentState):
    """
    Continue only if the chart recommendation
    was successfully parsed.
    """

    if state["final_error"] == "":
        return "validate_chart"

    return "end"


def route_after_chart_validation(state: AgentState):
    """
    Continue only if the chart configuration is valid.
    """

    if state["final_error"] == "":
        return "generate_chart"

    return "end"


# ============================================================
# BUILD GRAPH
# ============================================================

builder = StateGraph(AgentState)


# ------------------------------------------------------------
# Add nodes
# ------------------------------------------------------------

builder.add_node(
    "generate_sql",
    generate_sql_node
)

builder.add_node(
    "validate_sql",
    validate_sql_node
)

builder.add_node(
    "execute_sql",
    execute_sql_node
)

builder.add_node(
    "correct_sql",
    correct_sql_node
)

builder.add_node(
    "inspect_dataframe",
    inspect_dataframe_node
)

builder.add_node(
    "recommend_chart",
    recommend_chart_node
)

builder.add_node(
    "validate_chart",
    validate_chart_node
)

builder.add_node(
    "generate_chart",
    generate_chart_node
)


# ------------------------------------------------------------
# Initial flow
# ------------------------------------------------------------

builder.add_edge(
    START,
    "generate_sql"
)

builder.add_edge(
    "generate_sql",
    "validate_sql"
)


# ------------------------------------------------------------
# SQL validation routing
# ------------------------------------------------------------

builder.add_conditional_edges(
    "validate_sql",
    route_after_validation,
    {
        "execute_sql": "execute_sql",
        "end": END
    }
)


# ------------------------------------------------------------
# SQL execution routing
# ------------------------------------------------------------

builder.add_conditional_edges(
    "execute_sql",
    route_after_execution,
    {
        "inspect_dataframe": "inspect_dataframe",
        "correct_sql": "correct_sql",
        "end": END
    }
)


# ------------------------------------------------------------
# SQL correction loop
# ------------------------------------------------------------

builder.add_edge(
    "correct_sql",
    "validate_sql"
)


# ------------------------------------------------------------
# DataFrame → visualization
# ------------------------------------------------------------

builder.add_edge(
    "inspect_dataframe",
    "recommend_chart"
)


builder.add_conditional_edges(
    "recommend_chart",
    route_after_chart_recommendation,
    {
        "validate_chart": "validate_chart",
        "end": END
    }
)


builder.add_conditional_edges(
    "validate_chart",
    route_after_chart_validation,
    {
        "generate_chart": "generate_chart",
        "end": END
    }
)


builder.add_edge(
    "generate_chart",
    END
)


# ============================================================
# COMPILE
# ============================================================

graph = builder.compile()