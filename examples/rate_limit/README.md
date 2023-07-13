## Deploy a FastAPI app with redis based rate limiting to the cloud

This example shows how to deploy a FastAPI app with redis based rate limiting to the cloud using `fastapi-serve`. This directory contains the following files:

```
.
├── app.py              # The FastAPI app
├── jcloud.yml          # JCloud deployment config file with 2 replicas
├── README.md           # This README file
├── requirements.txt    # The requirements file for the FastAPI app
└── secrets.env         # The secrets file containing the redis credentials
```

> `secret.env` in this directory is a dummy file. You should replace it with your own secrets after creating a redis instance. For example with [Upstash](https://upstash.com/).

The FastAPI app to be deployed is defined in `app.py` as `app`. To deploy the app with the secrets file, simply run:

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

To test the rate-limiting, you can use the following command:

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
