from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from database import init_db
from routes_items import router as items_router
from routes_reference import (
    router_departments,
    router_categories,
    router_item_types,
    router_sizes,
    router_colors,
    router_tags,
    router_conditions,
    router_item_statuses,
    router_locations
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    This runs when the application starts and when it shuts down.
    """
    # Startup: Initialize the database
    print("🚀 Starting up...")
    init_db()
    print("✅ Database initialized!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Academy St. Thrift Inventory API",
    description="Complete inventory management system for a thrift store",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/", tags=["health"])
def read_root():
    """
    Health check endpoint.
    Returns basic API information.
    """
    return {
        "message": "Academy St. Thrift Inventory API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Detailed health check endpoint.
    """
    return {
        "status": "healthy",
        "database": "connected"
    }


# Mount static files for images
if os.path.exists("images"):
    app.mount("/images", StaticFiles(directory="images"), name="images")
    print("📸 Static images directory mounted at /images")

# Include routers
app.include_router(items_router)
app.include_router(router_departments)
app.include_router(router_categories)
app.include_router(router_item_types)
app.include_router(router_sizes)
app.include_router(router_colors)
app.include_router(router_tags)
app.include_router(router_conditions)
app.include_router(router_item_statuses)
app.include_router(router_locations)


# Optional: Add global exception handler
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Handle database integrity errors (e.g., foreign key violations, unique constraints).
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database integrity error. This might be due to a duplicate value or invalid foreign key.",
            "error": str(exc.orig) if hasattr(exc, 'orig') else str(exc)
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Handle request validation errors with more detailed messages.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # In production, use: uvicorn main:app --host 0.0.0.0 --port 8000
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )
