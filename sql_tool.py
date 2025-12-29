import sqlite3
from google.adk.tools import FunctionTool

def run_sql(query: str) -> dict:
    """
    Execute a SQLite SELECT query on the Phoenix database.
    """
    if not query.strip().lower().startswith("select"):
        return {"error": "Only SELECT queries are allowed"}

    conn = sqlite3.connect("phoenix.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return {
            "columns": columns,
            "rows": rows
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

# ✅ ADK tool wrapper (THIS is the key)
run_sql_tool = FunctionTool(run_sql)
