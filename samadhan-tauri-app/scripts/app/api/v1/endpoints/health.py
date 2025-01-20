from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()

@router.get("/")
def health_check(db: Session = Depends(get_db)) -> Any:
    """
    Health check endpoint that verifies database connectivity
    """
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0"
    } 