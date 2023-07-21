### 📉 Serverless (scale-to-zero) deployments based on requests-per-second

Serverless architectures play a pivotal role by allowing applications to scale automatically with fluctuating demand, while only charging for the resources actually consumed. Autoscaling your FastAPI apps based on requests per second (RPS) enables a serverless architecture, which ensures your application remains responsive at all times and reduces costs during periods of low traffic.

The `fastapi-serve` library has built-in support for auto-scaling your FastAPI apps based on RPS. You can configure the RPS threshold for scaling up and down and the maximum number of replicas by specifying them in a `jcloud.yml` file and using the `--config` flag to give it to the deployment.


```yaml
instance: C3
autoscale:
  min: 0
  max: 1
  metric: rps
  target: 1
```

The above configuration will ensure that your app scales up to 1 replica when the RPS exceeds 1, and scales down to 0 replicas when the RPS falls below 1. 

Let's look at an example of how to auto-scale a FastAPI app based on RPS.

### 📈 Deploy a FastAPI app with auto-scaling based on RPS

This directory contains the following files:

```
.
├── main.py             # The FastAPI app
├── jcloud.yml          # JCloud deployment config with the autoscaling config
└── README.md           # This README file
```

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Response(BaseModel):
    message: str = "Ping!"

@app.get("/ping", response_model=Response)
def ping():
    return Response()
```

In the above example, we have a `/ping` endpoint that responds with the message "Ping!"

### 🚀 Deploying to Jina AI Cloud

```bash
fastapi-serve deploy jcloud main:app
```

### 💻 Testing


The first request after a period of inactivity will have a longer roundtrip time due to the "cold start" delay. Let's measure the roundtrip time for the requests:


```bash
# Make the first request and measure time taken
time curl -sX GET https://fastapi-2a94b25a5f.wolf.jina.ai/ping | jq

# Wait for a while till the instance scales down to zero

# Make the second request and measure time taken
time curl -sX GET https://fastapi-2a94b25a5f.wolf.jina.ai/ping | jq
```

The `time` command measures the total time taken for the `curl` command to run, measuring the roundtrip time for the request. The first request might take a bit longer as it includes the time taken to spin up a new instance (known as a "cold start"). The second request will likely be quicker as the instance is already running.


### 🎯 Wrapping Up

With serverless autoscaling in place, your application can efficiently handle fluctuating traffic and reduce costs when not in use. You can also mix and match autoscaling strategies based on your needs. This flexibility, along with fastapi-serve's ability to deploy anywhere, provides a robust and cost-effective way to run your FastAPI applications.
