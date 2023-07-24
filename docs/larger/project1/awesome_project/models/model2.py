from pydantic import BaseModel


class Model2(BaseModel):
    id: int
    value: str


class ExtendedModel2(Model2):
    extra: dict
