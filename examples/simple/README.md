## Deploy a simple FastAPI app to the cloud

This example shows how to deploy a simple FastAPI app to the cloud using `fastapi-serve`. This directory contains the following files:

.
├── app.py              # The FastAPI app    
├── README.md           # This README file
└── requirements.txt    # The requirements file for the FastAPI app

The FastAPI app to be deployed is defined in `app.py` as `app`. To deploy this, simply run:

```bash
fastapi-serve deploy jcloud app:app
```

Note - first `app` comes from the name of the app in `app.py`, and the second `app` comes from the name of the FastAPI app.

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

You can now access your app at the URL given in the `Endpoint` field and the Swagger UI at the URL given in the `Swagger UI` field :tada:

To deploy the app with a custom name, you can pass the `--name` flag:

```bash
fastapi-serve deploy jcloud app:app --name myapi
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

To check the status of a deployed app, run:

```bash
fastapi-serve status myapi-9b12c3d030
```

To remove a deployed app, run:

```bash
fastapi-serve remove myapi-9b12c3d030
```
