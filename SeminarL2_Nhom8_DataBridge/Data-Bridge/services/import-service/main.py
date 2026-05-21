"""Import Service — FastAPI entry point."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.import_router import router
from routers.connection_router import router as conn_router
from core.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

settings = get_settings()

app = FastAPI(
    title="Import Service",
    description="Universal data import from PostgreSQL, MySQL, MongoDB, SQLite, CSV, Excel, JSON, SQL dump",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/import", tags=["Import"])
app.include_router(conn_router, prefix="/connections", tags=["Connections"])


@app.get("/")
def root():
    return {"service": "import-service", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "import-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=settings.DEBUG,
    )
