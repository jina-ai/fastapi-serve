import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

__version__ = "0.0.1"

app = FastAPI()


class Health(BaseModel):
    status: str
    version: str = __version__
    revision: str = Field(default_factory=lambda: os.environ.get("K_REVISION", "0.0.0"))


@app.get("/health")
def health():
    return Health(status="ok")


@app.get("/endpoint")
def endpoint():
    return {"Hello": "World"}
