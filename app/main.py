from fastapi import FastAPI
from app.config.database import create_db_and_tables
from app.api.routes.videos import router as videos_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(videos_router, prefix="/api/v1/videos")


@app.get("/")
def root():
    return {"message": "Welcome To ScrubCast API"}
