"""NL2SQL Service — FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from core.kafka_worker import start_worker, stop_worker
from routers.nl2sql_router import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_worker(settings.KAFKA_BOOTSTRAP_SERVERS)
    yield
    await stop_worker()


app = FastAPI(
    title="NL2SQL Service",
    description="Multi-Agent NL2SQL pipeline — converts natural language to SQL",
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

app.include_router(router, tags=["NL2SQL"])


@app.get("/")
async def root():
    return {"service": "nl2sql-service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.SERVICE_HOST, port=settings.SERVICE_PORT, reload=settings.DEBUG)
