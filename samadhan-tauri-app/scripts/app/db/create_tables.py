from sqlalchemy import create_engine, text
from app.core.config import settings
from app.models.user import Base

def init_db():
    # Create database if it doesn't exist
    engine = create_engine(
        f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}"
    )
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME}"))
        conn.execute(text(f"USE {settings.DB_NAME}"))
        conn.commit()

    # Create tables
    engine = create_engine(
        f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
    )
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully!") 