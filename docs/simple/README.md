## 🌩️ Deploy a Simple FastAPI App to the Cloud

This document explains how to deploy a simple FastAPI app to the cloud using `fastapi-serve`. 

### 📁 Directory structure

```
.
├── main.py             # The FastAPI app    
├── README.md           # This README file
└── requirements.txt    # The requirements file for the FastAPI app
```

The FastAPI app to be deployed is defined in `main.py` as `app`. 


### 👀 Deploying locally

To deploy the app locally, run:

```bash
fastapi-serve deploy local main:app
```

```text
───────────────── 🎉 Flow is ready to serve! ─────────────────
╭────────────── 🔗 Endpoint ───────────────╮
│  ⛓      Protocol                   HTTP  │
│  🏠        Local           0.0.0.0:8080  │
│  🔒      Private    192.168.29.185:8080  │
│  🌍       Public      49.37.163.80:8080  │
╰──────────────────────────────────────────╯
╭─────────── 💎 HTTP extension ────────────╮
│  💬     Swagger UI    0.0.0.0:8080/docs  │
│  📚          Redoc   0.0.0.0:8080/redoc  │
╰──────────────────────────────────────────╯
```

> **Note** - We use Uvicorn to deploy the app locally. You can use the Uvicorn CLI for local deployment instead if you prefer.


### 🚀 Deploying to Jina AI Cloud

```bash
fastapi-serve deploy jcloud main:app
```

> **Note** - The `main:app` argument indicates that you want to deploy the FastAPI app named `app` found in `main.py`.

```text
╭─────────────────────────┬───────────────────────────────────────────────────────────────────────────╮
│ App ID                  │                            fastapi-37a32285c3                             │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ Phase                   │                                  Serving                                  │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ Endpoint                │                  https://fastapi-37a32285c3.wolf.jina.ai                  │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ App logs                │                          https://cloud.jina.ai/                           │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ Base credits (per hour) │                     10.104 (Read about pricing here)                      │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ Swagger UI              │               https://fastapi-37a32285c3.wolf.jina.ai/docs                │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ OpenAPI JSON            │           https://fastapi-37a32285c3.wolf.jina.ai/openapi.json            │
╰─────────────────────────┴───────────────────────────────────────────────────────────────────────────╯
```

You can now access your app at the URL in the `Endpoint` field and the Swagger UI at the URL in the `Swagger UI` field :tada:


### 📛 Custom deployment names

To deploy the app with a custom name, you can use the `--name` flag:

```bash
fastapi-serve deploy jcloud main:app --name myapi
```

```text
╭─────────────────────────┬───────────────────────────────────────────────────────────────────────────╮
│ App ID                  │                             myapi-9b12c3d030                              │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ Phase                   │                                  Serving                                  │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ Endpoint                │                   https://myapi-9b12c3d030.wolf.jina.ai                   │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ App logs                │                          https://cloud.jina.ai/                           │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ Base credits (per hour) │                     10.104 (Read about pricing here)                      │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ Swagger UI              │                https://myapi-9b12c3d030.wolf.jina.ai/docs                 │
├─────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ OpenAPI JSON            │            https://myapi-9b12c3d030.wolf.jina.ai/openapi.json             │
╰─────────────────────────┴───────────────────────────────────────────────────────────────────────────╯
```

### 🔍 List all Deployed Apps

To list all your deployed apps, run:

```bash
fastapi-serve list
```

```text
╭────────────────────┬─────────┬────────────────────────────────────────┬─────────────────────────────╮
│ AppID              │ Phase   │ Endpoint                               │ Created                     │
├────────────────────┼─────────┼────────────────────────────────────────┼─────────────────────────────┤
│ myapi-9b12c3d030   │ Serving │ https://myapi-9b12c3d030.wolf.jina.ai  │ 13-Jul-2023 15:30 GMT +0530 │
│ fastapi-37a32285c3 │ Serving │ https://fastapi-37a32285c3.wolf.jina.… │ 13-Jul-2023 15:23 GMT +0530 │
╰────────────────────┴─────────┴────────────────────────────────────────┴─────────────────────────────╯
```

### 📊 Check app status


To check the status of a deployed app, run:

```bash
fastapi-serve status myapi-9b12c3d030
```

### ❌ Remove a deployed app

To remove a deployed app, run:

```bash
fastapi-serve remove myapi-9b12c3d030
```

With `fastapi-serve`, deploying your FastAPI applications has never been easier!
