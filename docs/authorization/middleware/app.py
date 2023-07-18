from fastapi import Depends, FastAPI

from fastapi_serve import JinaAPIKeyHeader, JinaAuthMiddleware

app = FastAPI()
app.add_middleware(
    JinaAuthMiddleware,
    exclude_paths=JinaAuthMiddleware.SKIPPED_PATHS + ["/insecure"],
)


@app.get("/secure", dependencies=[Depends(JinaAPIKeyHeader)])
def secure():
    return {"info": "user_specific_info"}


@app.get("/insecure")
def insecure():
    return {"info": "general_info"}
