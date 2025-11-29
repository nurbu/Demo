from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Generator
import os

from models import Base

# Database URL - SQLite
# You can override this with an environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")

# Create engine
# connect_args={"check_same_thread": False} is needed only for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False  # Set to True for SQL query logging during development
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Enable foreign key constraints for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable foreign key constraints in SQLite"""
    if DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Use this in FastAPI route dependencies.
    
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    Call this function when starting your application.
    
    Example in main.py:
        from database import init_db
        
        @app.on_event("startup")
        def on_startup():
            init_db()
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def drop_db() -> None:
    """
    Drop all tables from the database.
    ⚠️ WARNING: This will delete all data!
    Use only in development/testing.
    """
    Base.metadata.drop_all(bind=engine)
    print("🗑️  All database tables dropped!")


def reset_db() -> None:
    """
    Reset the database by dropping and recreating all tables.
    ⚠️ WARNING: This will delete all data!
    Use only in development/testing.
    """
    drop_db()
    init_db()
    print("♻️  Database reset complete!")


# Optional: Database session context manager
class DatabaseSession:
    """
    Context manager for database sessions.
    Alternative to using get_db() dependency.
    
    Example:
        with DatabaseSession() as db:
            items = db.query(Item).all()
    """
    def __init__(self):
        self.db = SessionLocal()
    
    def __enter__(self) -> Session:
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
        self.db.close()


if __name__ == "__main__":
    """
    Run this file directly to initialize the database:
    python database.py
    """
    print("🚀 Initializing database...")
    init_db()
    print("✨ Done!")
