### 🕸️ Managing Larger Applications with Complex Directory Structure

Real-life FastAPI applications are not just a single `main.py` file. They often have a complex directory structure with separate files for models, routes, dependencies, and services. The goal of this project is to show an example of such a larger, structured FastAPI application and how it can be deployed using `fastapi-serve`.

### 📚 What we're doing here

We're building a structured FastAPI application with a more complex directory structure. Here's how the directory is structured:


```text
.
├── awesome_project
│   ├── api
│   │   ├── __init__.py
│   │   ├── route1.py
│   │   ├── route2.py
│   │   └── route3.py
│   ├── dependencies
│   │   ├── dependency1.py
│   │   ├── dependency2.py
│   │   └── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── model1.py
│   │   └── model2.py
│   └── services
│       ├── __init__.py
│       ├── service1.py
│       └── service2.py
└── README.md

```

### 🚀 Deploying to Jina AI Cloud

The `awesome_project.main:app` part of the below `fastapi-serve deploy` command is a string notation used in Python to denote a specific object within a module. Here's how to interpret it:

- `awesome_project.main`: This is the Python import path, pointing to the location of the Python file that contains your FastAPI application instance.
- `app`: This is the actual FastAPI application object defined in your Python script. It's the instance of FastAPI that you've created, onto which you've loaded all your routes and middleware.


```bash
fastapi-serve deploy jcloud awesome_project.main:app
```

```text
╭─────────────────────────┬────────────────────────────────────────────────────────────────────────────╮
│ App ID                  │                             fastapi-a808d44495                             │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────────┤
│ Phase                   │                                  Serving                                   │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────────┤
│ Endpoint                │                  https://fastapi-a808d44495.wolf.jina.ai                   │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────────┤
│ App logs                │                           https://cloud.jina.ai/                           │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────────┤
│ Base credits (per hour) │                      10.104 (Read about pricing here)                      │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────────┤
│ Swagger UI              │                https://fastapi-a808d44495.wolf.jina.ai/docs                │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────────┤
│ OpenAPI JSON            │            https://fastapi-a808d44495.wolf.jina.ai/openapi.json            │
╰─────────────────────────┴────────────────────────────────────────────────────────────────────────────╯
```

### 💻 Testing

Let's use curl to test all 3 routes and validate that we get the expected responses.

```bash
curl -X 'GET' 'https://fastapi-a808d44495.wolf.jina.ai/route1/?arg1=some_value'
```

```json
{
  "name": "Route1",
  "description": "Hello from Route 1 with dependency: {'arg1': 'some_value'}!"
}
```

```bash
curl -X 'POST' 'https://fastapi-a808d44495.wolf.jina.ai/route2/?arg2=other_value' \
  -d '{
  "id": 123,
  "value": "some_value"
}'
```

```json
{
  "id": 123,
  "value": "some_value",
  "extra": {
    "dep": {
      "arg2": "other_value"
    }
  }
}
```


```bash
curl -X 'GET' 'https://fastapi-a808d44495.wolf.jina.ai/route3/'
```

```json
{
  "message": "Hello from Route 3! Result from Service: {'result': 'Processed some data in Service2'}"
}
```


### 🎯 Wrapping up

This FastAPI project serves as an example of how a complex FastAPI application can be structured and deployed to the cloud using fastapi-serve. Stay tuned, as we'll be adding more structured FastAPI projects here!
