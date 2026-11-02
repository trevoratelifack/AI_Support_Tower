from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.tickets import router as tickets_router
from app.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.get("/", include_in_schema=False)
def root():
    return {
        "app_name": settings.app_name,
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment":settings.app_env,
        "app_name":settings.app_name
    }


app.include_router(tickets_router)
