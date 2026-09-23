from app.services.data_agent import ask_data_agent


question = "Which city has the most customers?"

answer = ask_data_agent(question)

print("Final answer:")
print(answer)