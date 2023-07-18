import os

from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis.asyncio import Redis

app = FastAPI()


@app.on_event("startup")
async def startup():
    host = os.getenv("REDIS_HOST", "localhost")
    port = os.getenv("REDIS_PORT", 6379)
    password = os.getenv("REDIS_PASSWORD", None)
    redis = Redis(
        host=host, port=port, password=password, decode_responses=True, ssl=True
    )
    await FastAPILimiter.init(redis)


@app.get("/endpoint", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def endpoint():
    return {"msg": "Hello World"}
