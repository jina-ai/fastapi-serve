import os
import time

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Response(BaseModel):
    cpu_time: float
    result: int
    hostname: str = Field(default_factory=lambda: os.environ.get("HOSTNAME", "unknown"))


def _heavy_compute(count):
    sum = 0
    for i in range(count):
        sum += i
    return sum


@app.get("/load/{count}", response_model=Response)
def load_test(count: int = 1_000_000):
    _t1 = time.time()
    _sum = _heavy_compute(count)
    _t2 = time.time()
    _cpu_time = _t2 - _t1
    print(f"CPU time: {_cpu_time}")
    return Response(cpu_time=_cpu_time, result=_sum)
