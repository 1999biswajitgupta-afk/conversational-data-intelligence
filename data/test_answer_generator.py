from app.services.answer_generator import generate_answer


question = "Which city has the most customers?"

database_result = [("sao paulo", 15540)]

answer = generate_answer(question, database_result)

print("Answer:")
print(answer)