from app.services.sql_generator import generate_sql


question = "Which city has the most customers?"

sql = generate_sql(question)

print("Generated SQL:")
print(sql)