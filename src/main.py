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

@app.get("/health")
def read_health():
    return {"status": "healthy", "tenant": os.environ.get("TENANT_NAME", "default")}

@app.on_event("startup")
def startup_event():
    if not os.environ.get("PYTEST_CURRENT_TEST"):
        tenant_name = os.environ.get("TENANT_NAME", "default")
        port = int(os.environ.get("PORT", 8000))
        if tenant_name in ("default", "platform", "") and port == 8000:
            from src.api.routes import auto_start_tenants
            auto_start_tenants()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    reload = os.environ.get("APP_ENV", "development").lower() == "development"
    uvicorn.run("src.main:app", host=host, port=port, reload=reload)


