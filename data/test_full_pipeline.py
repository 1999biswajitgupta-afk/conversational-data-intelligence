from app.services.sql_generator import generate_sql
from app.services.sql_validator import validate_sql
from app.database.query_executor import execute_query


question = "Which city has the most customers?"

print("Question:")
print(question)

sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)

validated_sql = validate_sql(sql)

print("\nSQL validated successfully.")

results = execute_query(validated_sql)

print("\nDatabase results:")
for row in results:
    print(row)