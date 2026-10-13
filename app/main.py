from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings

from app.api.analysis_routes import router as analysis_router
from app.api.file_routes import router as file_router
from app.api.chat_routes import router as chat_router


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

     allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.include_router(
    analysis_router
)

app.include_router(
    file_router
)

app.include_router(
    chat_router
)


@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "service": settings.app_name
    }