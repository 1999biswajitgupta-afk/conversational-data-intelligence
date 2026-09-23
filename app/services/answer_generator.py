from app.llm.client import LLMClient


def generate_answer(question: str, sql_result) -> str:
    llm = LLMClient()

    prompt = f"""
You are a data analyst assistant.

Answer the user's question using only the database result provided below.

User question:
{question}

Database result:
{sql_result}

Give a concise, clear answer.
Do not mention SQL or the internal system.
Do not invent information that is not present in the result.
"""

    return llm.generate(prompt)