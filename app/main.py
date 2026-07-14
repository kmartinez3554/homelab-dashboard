from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.database import engine
from app.database import Base
import app.models

from app.routers import network

from app.monitoring import get_system_info

app = FastAPI(
    title = "Home Lab DashBoard",
    description = "A dashboard for monitoring my home lab infrastructure.",
    version = "1.0"
)

Base.metadata.create_all(bind = engine)

templates = Jinja2Templates(directory="app/templates")

app.mount(
    "/static",
    StaticFiles(directory = "app/static"),
    name = "static"
)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "request": request
        }
    )

@app.get("/health")
def health_check():
    return{
        "status": "online"
    }

@app.get("/system")
def system_info():
    return get_system_info()

app.include_router(network.router)