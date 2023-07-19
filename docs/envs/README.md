### 🌍 Leverage Environment Variables for FastAPI Application Configuration

When developing FastAPI applications, being able to flexibly control different parts of your app using environment variables can provide powerful customization and control. It can enable you to modify your application behavior without changing your code. You can store anything from feature toggles, service URLs, to database credentials as environment variables.

In this example, we'll demonstrate how to leverage environment variables to control feature toggles.

### Using Environment Variables for Feature Toggles

We've created an application that has a simple messaging feature under development. The availability of this new feature is controlled by an environment variable NEW_MESSAGING_ENABLED.

```python
# app.py
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
```

```bash
# .env
NEW_MESSAGING_ENABLED=false
```

Let's deploy this application with the new messaging feature disabled.

```bash
fastapi-serve deploy jcloud app:app --env .env
```

```text
╭─────────────────────────┬──────────────────────────────────────────────────────────────────────────╮
│ App ID                  │                            fastapi-c18fb24e03                            │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ Phase                   │                                 Serving                                  │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ Endpoint                │                 https://fastapi-c18fb24e03.wolf.jina.ai                  │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ App logs                │                          https://cloud.jina.ai/                          │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ Base credits (per hour) │                     10.104 (Read about pricing here)                     │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ Swagger UI              │               https://fastapi-c18fb24e03.wolf.jina.ai/docs               │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
│ OpenAPI JSON            │           https://fastapi-c18fb24e03.wolf.jina.ai/openapi.json           │
╰─────────────────────────┴──────────────────────────────────────────────────────────────────────────╯
```

### 💻 Testing

Let's test the application by sending a request to the `/new_message` endpoint.

```bash
curl -sX GET "https://fastapi-c18fb24e03.jina.ai/new_message" | jq
```

```json
{
    "detail": "Feature not found"
}
```

Let's enable the new messaging feature by updating the environment variable and the app.

```bash
# .env
NEW_MESSAGING_ENABLED=true
```

```bash
fastapi-serve update jcloud app:app --env .env --app-id fastapi-2a94b25a5f
```

Once the update is complete, let's test the application again.

```bash
curl -X GET "https://fastapi-2a94b25a5f.jina.ai/new_message"
```

```json
{
    "status": "New messaging feature is running!"
}
```

> **Note**: It might take some time for the update to be reflected in the application. 

### 🎯 Wrapping Up

The example demonstrated how effectively `fastapi-serve` supports environment variables to manage FastAPI applications. With a simple environment file, we altered the app's behavior, revealing the potential to control almost any feature of your application. This highlights `fastapi-serve` as a powerful and convenient tool for deploying and managing FastAPI apps.
