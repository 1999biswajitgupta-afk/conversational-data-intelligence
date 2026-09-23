from app.services.sql_generator import generate_sql
from app.services.sql_validator import validate_sql
from app.database.query_executor import execute_query
from app.services.answer_generator import generate_answer


def ask_data_agent(question: str) -> dict:
    sql = generate_sql(question)

    validated_sql = validate_sql(sql)

    results = execute_query(validated_sql)

    answer = generate_answer(question, results)

    return {
        "question": question,
        "sql": validated_sql,
        "data": results,
        "answer": answer,
    }