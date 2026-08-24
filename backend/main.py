from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine

app = FastAPI(
    title="MemoraAI API",
    description="AI-Powered Personal Knowledge Intelligence Platform",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "MemoraAI Backend is running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MemoraAI Backend"
    }


@app.get("/api/database-test")
def database_test():

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        return {
            "database": "connected",
            "result": result.scalar()
        }