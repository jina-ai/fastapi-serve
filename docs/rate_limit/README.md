## 🗝️ Using Secrets during Deployment

You can use secrets during app deployment by passing a secrets file to the `--secrets` flag. The secrets file should be a `.env` file containing the secrets. For example, if you have a `.env` file with the following contents:

```text
REDIS_HOST=redis-12345.upstash.io
REDIS_PORT=12345
REDIS_PASSWORD=12345
```

You can deploy the app with the secrets file as follows:

```bash
fastapi-serve deploy jcloud app:app --secrets .env
```

Let's look at an example of how to use an external redis instance for rate limiting endpoints.

### 🚦 Deploy a FastAPI app with redis based rate-limiting

This directory contains the following files:

```
.
├── app.py              # The FastAPI app
├── jcloud.yml          # JCloud deployment config file with 2 replicas
├── README.md           # This README file
├── requirements.txt    # The requirements file for the FastAPI app
└── secrets.env         # The secrets file containing the redis credentials
```

> **Note**
> `secret.env` in this directory is a dummy file. You should replace it with your own secrets after creating a redis instance. (For example with [Upstash](https://upstash.com/)).


```python
# app.py
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
```

In the above example, we are using the `fastapi-limiter` library to rate limit the `/endpoint` endpoint to allow only 2 requests every 5 seconds. The library uses redis to store the rate limit counters. We are using the `redis` library to connect to the redis instance. The redis credentials are read from the environment variables.


### 🚀 Deploying to Jina Cloud

```bash
fastapi-serve deploy jcloud app:app --secrets secrets.env
```

```text
╭─────────────────────────┬────────────────────────────────────────────────────────────────────────╮
│ App ID                  │                           fastapi-3a47863f19                           │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ Phase                   │                                Serving                                 │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ Endpoint                │                https://fastapi-3a47863f19.wolf.jina.ai                 │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ App logs                │                         https://cloud.jina.ai/                         │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ Base credits (per hour) │                      20.04 (Read about pricing here)                   │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ Swagger UI              │              https://fastapi-3a47863f19.wolf.jina.ai/docs              │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ OpenAPI JSON            │          https://fastapi-3a47863f19.wolf.jina.ai/openapi.json          │
╰─────────────────────────┴────────────────────────────────────────────────────────────────────────╯
```

### 💻 Testing

To test the rate-limiting, we can send a GET request to the endpoint:

```bash
curl -X GET "https://fastapi-3a47863f19.wolf.jina.ai/endpoint"
```

```json
{
  "msg": "Hello World"
}
```

The endpoint allows 2 requests every 5 seconds. If you send more than 2 requests within 5 seconds, you will get the following response:

```json
{
  "detail": "Too many requests"
}
```
