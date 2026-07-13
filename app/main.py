from fastapi import FastAPI

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