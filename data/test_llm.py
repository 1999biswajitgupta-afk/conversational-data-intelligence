from app.llm.client import LLMClient

llm = LLMClient()

response = llm.generate("Explain what is databse in one scentence")

print(response)