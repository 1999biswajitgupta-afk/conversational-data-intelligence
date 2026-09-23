from fastapi import FastAPI

from app.models.query import QueryRequest
from app.services.data_agent import ask_data_agent


app = FastAPI()


@app.post("/api/v1/query")
def query_data(request: QueryRequest):
    return ask_data_agent(request.question)