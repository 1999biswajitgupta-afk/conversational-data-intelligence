from app.database.schema import DATABASE_SCHEMA
from app.llm.client import LLMClient


def generate_sql(question: str) -> str:
    llm = LLMClient()

    prompt = f"""
You are a SQL generation assistant.

Generate a SQLite SQL query that correctly and completely answers the user's question.

Database schema:
{DATABASE_SCHEMA}

User question:
{question}

Requirements:
- Use only tables and columns that exist in the provided schema.
- Return all columns necessary to support a complete answer.
- If the question asks for a maximum, minimum, highest, lowest, largest, or smallest value, return both the entity and the calculated value.
- Use appropriate JOINs when information is spread across multiple tables.
- Use COUNT(DISTINCT ...) when counting unique entities such as orders or customers.
- For text comparisons, use case-insensitive matching when appropriate, such as LOWER(column) = LOWER(value).
- Match the user's wording to the correct semantic column. For example, "city" must use a city column, while "state" must use a state column.
- Do not substitute one geographic attribute for another. If the user asks about a city, do not use a state column.
- When the user asks about an order's current status or asks how many orders are delivered, use the orders.order_status column. Use order_delivered_customer_date only when the question explicitly asks about delivery dates or delivery timing.
- Do not invent columns or tables.
- Return only the SQL query.
- Do not include markdown.
- Do not explain the query.
"""

    return llm.generate(prompt)