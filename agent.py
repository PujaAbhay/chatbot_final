from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from sql_agent import sql_agent

root_agent = Agent(
    model=LiteLlm(model="groq/openai/gpt-oss-120b"),
    name='root_agent',
    description='Routes queries to specialized agents',
    instruction="""You route user queries and present results.

Sub-agent:
- sql_agent: queries phoenix.db using run_sql

Routing:
- Database questions (counts, lists, schema, traces, spans, projects) → delegate to sql_agent
- General chat (greetings) → answer directly
- Never guess database answers or describe hypothetical SQL

After sql_agent responds:
- Present results to user

On errors:
- Ask sql_agent to retry with corrected SQL
""",
sub_agents=[sql_agent]
)
