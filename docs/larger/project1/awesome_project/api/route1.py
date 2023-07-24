from awesome_project.dependencies.dependency1 import use_dependency1
from awesome_project.models.model1 import Model1
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/route1/", response_model=Model1)
def read_route1(dep: dict = Depends(use_dependency1)):
    return Model1(
        name="Route1", description=f"Hello from Route 1 with dependency: {dep}!"
    )
