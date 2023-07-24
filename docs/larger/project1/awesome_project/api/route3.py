from awesome_project.services.service2 import Service2
from fastapi import APIRouter

router = APIRouter()


@router.get("/route3/")
def read_route3():
    result = Service2.perform_operation({"input": "some data"})
    return {"message": f"Hello from Route 3! Result from Service: {result}"}
