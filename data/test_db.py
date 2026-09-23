from app.services.sql_generator import generate_sql
from app.services.sql_validator import validate_sql
from app.database.query_executor import execute_query


question = "Which city has the most customers?"

sql = generate_sql(question)

print("Generated SQL:")
print(sql)

validated_sql = validate_sql(sql)

results = execute_query(sql)

print("Results:")
print(results)