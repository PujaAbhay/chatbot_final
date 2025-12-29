from google.adk.agents import Agent
from sql_tool import run_sql_tool
from google.adk.models.lite_llm import LiteLlm

sql_agent = Agent(
    name="sql_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-120b"),
    description="Executes SQL queries on phoenix.db database",
    instruction="""Answer database questions using run_sql tool on phoenix.db.

Rules:
- Call run_sql for every database query
- Only answer using tool results from current turn
- Generate SELECT queries only (no INSERT/UPDATE/DELETE/DDL)
- Discover schema via SQL, never ask user
"""
,
    tools=[run_sql_tool]
)
