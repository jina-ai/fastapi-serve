from awesome_project.dependencies.dependency2 import use_dependency2
from awesome_project.models.model2 import ExtendedModel2, Model2
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/route2/", response_model=ExtendedModel2)
def create_route2(item: Model2, dep: dict = Depends(use_dependency2)):
    return {**item.dict(), **{"extra": {"dep": dep}}}
