from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import get_db
from .routers.users import router as users_router

app = FastAPI(
    title="Docker User Management API",
    description="A learning project demonstrating FastAPI + PostgreSQL with Docker Compose.",
    version="1.0.0",
)
app.include_router(users_router)

@app.get("/", tags=["System"])
def root():
    return {"message": "Docker User Management API is running", "docs": "/docs"}

@app.get("/health", tags=["System"])
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")
