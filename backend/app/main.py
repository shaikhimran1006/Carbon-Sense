from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, users, carbon

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CarbonSense AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(carbon.router)


@app.get("/")
def root():
    return {"message": "Welcome to CarbonSense AI API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
