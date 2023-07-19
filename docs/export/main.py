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
