from fastapi import FastAPI
from app.monitoring import get_system_info

app = FastAPI(
    title = "Home Lab DashBoard",
    description = "A dashboard for onitoring my home lab infrastructure.",
    version = "1.0"
)

@app.get("/")
def home():
    return{
        "message": "Welcome to the Home Lab Dashboard"
    }

@app.get("/health")
def health_check():
    return{
        "status": "online"
    }

@app.get("/system")
def system_info():
    return get_system_info()