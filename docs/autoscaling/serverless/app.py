from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Response(BaseModel):
    message: str = "Ping!"


@app.get("/ping", response_model=Response)
def ping():
    return Response()
