from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager
import os

from database import init_db
from routes_items import router as items_router
from routes_reference import (
    router_departments, router_categories, router_item_types,
    router_sizes, router_colors, router_tags, router_conditions,
    router_item_statuses, router_locations
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Thrift Store Inventory API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


if os.path.exists("images"):
    app.mount("/images", StaticFiles(directory="images"), name="images")
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


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database integrity error - duplicate value or invalid foreign key",
            "error": str(exc.orig) if hasattr(exc, 'orig') else str(exc)
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": exc.errors()}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
