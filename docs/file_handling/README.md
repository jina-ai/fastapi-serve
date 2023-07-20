## 📁 Manage your Files with Jina Blob Storage

Jina Blob Storage, through the `JinaBlobStorage` class, provides a simple yet powerful solution for managing file storage in your FastAPI applications. With built-in features for uploading, downloading, retrieving info, listing, and deleting files, it streamlines the process of managing user files, saving you the complexity of handling storage yourself.

### 🧠 Langchain RetrievalQA Example on PDF Documents

In this example, we will demonstrate how to use Jina Blob Storage in a FastAPI application. We will build a service that allows users to upload a PDF document to one endpoint and then answer questions about the document on another endpoint.

The two key endpoints are `/upload` and `/answer`. The upload endpoint takes a file and a flag indicating whether the file should be public or not, then stores it to Jina Blob Storage and returns a unique URI for the uploaded file. The `/answer` endpoint takes this URI and a user question as input, retrieves the file from Jina Blob Storage and answers the user's question based on the content of the uploaded document.


> **Note**
> This example requires the `OPENAI_API_KEY` secret to enable interaction with OpenAI APIs. You should replace the contents of `secrets.env` with your own token.


### 🚀 Deploying to Jina AI Cloud

```bash
fastapi-serve deploy jcloud main:app --secret secrets.env
```

```text
╭─────────────────────────┬───────────────────────────────────────────────────────────╮
│ App ID                  │                    fastapi-a66d3fe145                     │
├─────────────────────────┼───────────────────────────────────────────────────────────┤
│ Phase                   │                          Serving                          │
├─────────────────────────┼───────────────────────────────────────────────────────────┤
│ Endpoint                │          https://fastapi-a66d3fe145.wolf.jina.ai          │
├─────────────────────────┼───────────────────────────────────────────────────────────┤
│ App logs                │                  https://cloud.jina.ai/                   │
├─────────────────────────┼───────────────────────────────────────────────────────────┤
│ Base credits (per hour) │             10.104 (Read about pricing here)              │
├─────────────────────────┼───────────────────────────────────────────────────────────┤
│ Swagger UI              │       https://fastapi-a66d3fe145.wolf.jina.ai/docs        │
├─────────────────────────┼───────────────────────────────────────────────────────────┤
│ OpenAPI JSON            │   https://fastapi-a66d3fe145.wolf.jina.ai/openapi.json    │
╰─────────────────────────┴───────────────────────────────────────────────────────────╯
```

### 💻 Testing

Let's use curl to test the endpoints. First, we upload a PDF document to the blob storage. The response contains the URI of the uploaded file.

```bash
curl -X POST "https://fastapi-a66d3fe145.wolf.jina.ai/upload" \
    -H "accept: application/json" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@path_to_your_file.pdf;type=application/pdf" \
    -F "public=false"
```

```json
{
  "uri": "jinaai://64b56d4b933a75a3ee88feee"
}
```

Next, we use the URI to answer a question about the document. The response contains the answer to the question.

```bash
curl -X GET \
    "https://fastapi-a66d3fe145.wolf.jina.ai/answer?uri=jinaai://64b56d4b933a75a3ee88feee&question=your_question"
```

```json
{
  "answer": "your_answer"
}
```


### 🗂️ Jina Blob Storage Features

With Jina Blob Storage, you get the following features:

- **Upload**: Upload a file to the blob storage and get a unique URI to access it.
- **Download**: Download a file from the blob storage using its URI.
- **Get Info**: Get metadata about a file using its URI.
- **List**: Get a list of all files in the blob storage.
- **Delete**: Delete a file from the blob storage using its URI.

You can check the code for the `JinaBlobStorage` class in the file `storage.py`. 

https://github.com/jina-ai/fastapi-serve/blob/d6ebaea5f5e46b284451e651b32d988f70be6643/fastapi_serve/utils/blob/storage.py#L15

If you have any questions, feedback, or ideas, don't hesitate to create an issue. We'd love to hear from you!
