## 🔄 Upgrade Your FastAPI Applications with Zero Downtime

The `fastapi-serve` library is a versatile tool that not only helps you deploy FastAPI applications to the cloud but also ensures zero downtime during application upgrades. This tutorial walks you through the process of testing zero downtime upgrades for your FastAPI applications.

### 📁 Directory structure

Here's the directory structure of the FastAPI app:

```
.
├── main.py            # The FastAPI app
├── README.md          # This README file
├── requirements.txt   # The requirements file for the FastAPI app
└── zero_downtime.py   # Python script to check service availability and version updates
```

This template application provides a simple `/health` endpoint and an `/endpoint` that responds with a `Hello: World` JSON object. We'll first deploy the application, then run a script that continually checks these endpoints. We'll then update the application, redeploy it, and verify that the version of the app was updated without any downtime.


```python
# main.py
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
```

### 🐳 Deploy the FastAPI app

Let's start with deploying the app.

```bash
fastapi-serve deploy jcloud main:app
```

```text
╭─────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ App ID                  │                         fastapi-3a8d2d474f                         │
├─────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Phase                   │                              Serving                               │
├─────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Endpoint                │              https://fastapi-3a8d2d474f.wolf.jina.ai               │
├─────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ App logs                │                       https://cloud.jina.ai/                       │
├─────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Base credits (per hour) │                  10.104 (Read about pricing here)                  │
├─────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Swagger UI              │            https://fastapi-3a8d2d474f.wolf.jina.ai/docs            │
├─────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ OpenAPI JSON            │        https://fastapi-3a8d2d474f.wolf.jina.ai/openapi.json        │
╰─────────────────────────┴────────────────────────────────────────────────────────────────────╯
```


### 💻 Check service availability and version

The `zero_downtime.py` script continuously checks the `/health` endpoint and reports the status and version of the service. Run the script in your terminal:

```bash
python zero_downtime.py https://fastapi-3a8d2d474f.wolf.jina.ai
```

```text
Service status: ok, Version: 0.0.1, Revision: gateway-00001
Service status: ok, Version: 0.0.1, Revision: gateway-00001
Service status: ok, Version: 0.0.1, Revision: gateway-00001
```

As you can see, the service is up and running, and the version is `0.0.1`.


### 🔄 Upgrade the FastAPI app

Let's modify the FastAPI app. We'll change the version number `__version__` and the response of the `/endpoint` endpoint to `Hello: Universe`.

```python
# main.py
import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

__version__ = "0.0.2"

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
    return {"Hello": "Universe"}
```

Then, redeploy your app with the new changes. Don't forget to use the same app ID as before.

```bash
fastapi-serve deploy jcloud main:app --app-id fastapi-3a8d2d474f
```

### 💻 Check service availability and version Again

While the update is going on, let's start another terminal and run the `zero_downtime.py` script again:

```bash
python zero_downtime.py https://fastapi-3a8d2d474f.wolf.jina.ai
```

```text
...
Service status: ok, Version: 0.0.1, Revision: gateway-00001
Service status: ok, Version: 0.0.1, Revision: gateway-00001
Service status: ok, Version: 0.0.1, Revision: gateway-00001
Version updated from 0.0.1 to 0.0.2
Service status: ok, Version: 0.0.2, Revision: gateway-00002
Service status: ok, Version: 0.0.2, Revision: gateway-00002
Service status: ok, Version: 0.0.2, Revision: gateway-00002
...
```

Eventually, you'll see that the version has been updated to `0.0.2` without any downtime. The `zero_downtime.py` script also reports the revision number, which is incremented every time the app is updated.
check

### 🎯 Wrapping up

With `fastapi-serve`, you gain the ability to perform zero-downtime upgrades, eliminating service disruptions and enhancing your application's reliability by providing your users with constant access even during updates. Users don't need to deal with application downtime or manually check for updates. 
