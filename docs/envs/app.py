import os

from fastapi import FastAPI, HTTPException

app = FastAPI()

NEW_MESSAGING_ENABLED = os.getenv("NEW_MESSAGING_ENABLED", "false").lower() == "true"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/new_message")
def new_message():
    if not NEW_MESSAGING_ENABLED:
        raise HTTPException(status_code=404, detail="Feature not found")
    return {"status": "New messaging feature is running!"}
