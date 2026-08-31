import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from src.api.routes import router

app = FastAPI(title="ClassSync AI - Allocation Engine API", version="1.0.0")

app.include_router(router)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "api", "static")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/index.css")
def read_css():
    return FileResponse(os.path.join(STATIC_DIR, "index.css"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("src.main:app", host="127.0.0.1", port=port, reload=True)

