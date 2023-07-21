### ☸️ Export your FastAPI App for self-hosting with `fastapi-serve`

The convenience of cloud deployments is fantastic, but sometimes you just need to run things locally. Whether you're operating within strict security constraints, developing offline, or just prefer managing your own infrastructure, `fastapi-serve` makes it easy to get your FastAPI app running on your own terms.

In this example, we'll export a FastAPI application as Docker Compose and Kubernetes deployment files, enabling you to run your API on any infrastructure that supports Docker or Kubernetes.


### 🏗️ FastAPI App: Image resizing microservice

This example features a simple FastAPI application that resizes images. The API exposes three endpoints:

- `/resize_image/` accepts an image file and resizes it to a specified maximum size.
- `/list/` lists all the resized images that are currently stored on the server.
- `/cleanup/` deletes all the resized images from the server.

```python
# main.py
import os
from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from PIL import Image

app = FastAPI()

@app.post("/resize_image/")
async def resize_image(file: UploadFile = File(...), max_size: int = 500):
    try:
        image = Image.open(BytesIO(await file.read()))
        image.thumbnail((max_size, max_size))
        new_image_path = f"resized_{file.filename}"
        image.save(new_image_path)
        return FileResponse(new_image_path, filename=new_image_path)
    except:
        raise HTTPException(status_code=400, detail="Failed to process image")

@app.get("/list/")
async def list():
    resized_images = []
    for f in os.listdir():
        if f.startswith("resized_"):
            resized_images.append(f)
    return {"resized_images": resized_images}

@app.delete("/cleanup/")
async def cleanup():
    for f in os.listdir():
        if f.startswith("resized_"):
            os.remove(f)
    return {"status": "All resized images have been deleted"}
```

This directory contains the following files:

```
.
├── main.py             # The FastAPI app    
├── README.md           # This README file
└── requirements.txt    # The requirements file including Pillow
```


### 🐳 Docker Compose

To export your application as a Docker Compose deployment, run the following command:


```bash
fastapi-serve export main:app --kind docker-compose
```

```text
INFO   Flow@187971 Docker compose file has been created under ./docker-compose.yml. You can use it by running `docker-compose -f ./docker-compose.yml up`
```

This will create a `docker-compose.yml` file in your current directory. You can use this file to run your FastAPI app locally with Docker Compose:

```bash
docker-compose -f docker-compose.yml --project-directory . up --build -d --remove-orphans
```

### 💻 Testing

Once your app is running, you can test it out by sending a request to the `/resize_image/` endpoint:

```bash
curl -X 'POST' \
  'http://localhost:8080/resize_image/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/image.jpg;type=image/jpeg'
```

To check that the image was resized, you can send a request to the `/list/` endpoint:

```bash
curl -X 'GET' 'http://localhost:8080/list/'
```

```json
{
  "resized_images": [
    "resized_image.png"
  ]
}
```

Note how `fastapi-serve` handles the dependencies, builds and pushes the docker image to the registry, and creates the deployment files for you with no additional configuration.


### ☸️ Kubernetes

`fastapi-serve` can also export Kubernetes YAML files. Run:

```bash
fastapi-serve export main:app --kind kubernetes
```

The YAMLs are generated in the current directory under `gateway/gateway.yml`. They can be used to create Kubernetes resources. You can then apply these resources to your local or managed Kubernetes cluster.


### 🎯 Wrapping up

The power of `fastapi-serve` extends beyond the cloud, with built-in support for exporting your FastAPI applications for self-hosting. We handle the setup and dependency management, so you can focus on developing your FastAPI application without worrying about the infrastructure.
