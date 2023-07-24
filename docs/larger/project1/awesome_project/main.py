from awesome_project.api import route1, route2, route3
from fastapi import FastAPI

app = FastAPI()

app.include_router(route1.router)
app.include_router(route2.router)
app.include_router(route3.router)
