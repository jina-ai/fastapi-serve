from fastapi import Depends, FastAPI

from fastapi_serve import JinaAPIKeyHeader, JinaAuthDependency

app = FastAPI()
auth = JinaAuthDependency()


@app.get("/secure", dependencies=[Depends(auth), Depends(JinaAPIKeyHeader)])
def secure():
    return {"info": "user_specific_info"}


@app.get("/insecure")
def insecure():
    return {"info": "general_info"}
